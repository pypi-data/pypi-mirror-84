from __future__ import annotations
from abc import ABC, abstractmethod
from hyperopt import hp, STATUS_OK
from hyperopt.pyll import scope
import numpy as np
import logging
import pandas as pd
import shap
import matplotlib.pyplot as plt
import seaborn as sns
import lightgbm as lgb
import xgboost as xgb
from crosspredict.iterator import Iterator


class CrossModelFabric(ABC):
    def __init__(self,
                 iterator: Iterator,
                 params,
                 feature_name,
                 col_target,
                 cols_cat='auto',
                 num_boost_round=99999,
                 early_stopping_rounds=50,
                 valid=True,
                 random_state=0,
                 cross_target_encoder=None
                 ):

        self.params = params
        self.feature_name = feature_name
        self.cols_cat = cols_cat
        self.num_boost_round = num_boost_round
        self.early_stopping_rounds = early_stopping_rounds
        self.valid = valid
        self.col_target = col_target
        self.random_state = random_state

        self.iterator = iterator
        self.cross_target_encoder = cross_target_encoder
        self.models = {}
        self.scores = None
        self.score_max = None
        self.num_boost_optimal = None
        self.std = None

    @abstractmethod
    def get_hyperopt_space(self, params, random_state):
        pass

    @abstractmethod
    def get_dataset(self, data, label, categorical_feature, **kwargs):
        pass

    @abstractmethod
    def train(
            self,
            params,
            train_set,
            train_name,
            valid_sets,
            valid_name,
            num_boost_round,
            evals_result,
            categorical_feature,
            early_stopping_rounds,
            verbose_eval):
        pass

    # @abstractmethod
    # def predict(self):
    #     pass

    def fit(self, df):
        log = logging.getLogger(__name__)
        scores = {}
        scores_avg = []
        log.info(self.params)

        self.iterator.fit(df=df)

        for fold, (train, val) in enumerate(self.iterator.split(df)):
            if self.cross_target_encoder is not None:
                encoded_train, encoded_test = self.cross_target_encoder.transform(
                    fold=fold, train=train, test=val)
                train = pd.concat([train, encoded_train], axis=1)
                val = pd.concat([val, encoded_test], axis=1)

            X_train, X_val = train[self.feature_name], val[self.feature_name]
            y_train, y_val = train[self.col_target], val[self.col_target]

            dtrain = self.get_dataset(
                data=X_train.astype(float),
                label=y_train,
                categorical_feature=self.cols_cat)
            dvalid = self.get_dataset(data=X_val.astype(float), label=y_val,
                                      categorical_feature=self.cols_cat)

            if fold % self.iterator.n_splits == 0:
                log.info(f'REPEAT FOLDS {fold//self.iterator.n_splits} START')

            # Обучение
            evals_result = {}
            if self.valid:
                model = self.train(
                    params=self.params,
                    train_set=dtrain,
                    train_name='train',
                    valid_set=dvalid,
                    valid_name='eval',
                    num_boost_round=self.num_boost_round,
                    evals_result=evals_result,
                    categorical_feature=self.cols_cat,
                    early_stopping_rounds=self.early_stopping_rounds,
                    verbose_eval=False)
            else:
                model = self.train(params=self.params,
                                   train_set=dtrain,
                                   num_boost_round=self.num_boost_round,
                                   categorical_feature=self.cols_cat,
                                   verbose_eval=False)

            self.models[fold] = model
            if self.valid:
                # Построение прогнозов при разном виде взаимодействия
                scores[fold] = evals_result['eval']['auc']
                best_auc = np.max(evals_result['eval']['auc'])
                scores_avg.append(best_auc)

                log.info(f'\tCROSSVALIDATION FOLD {fold%self.iterator.n_splits} ENDS with best ROCAUC = {best_auc}')

        if self.valid:
            self.scores = pd.DataFrame(
                dict([(k, pd.Series(v)) for k, v in scores.items()]))
            mask = self.scores.isnull().sum(axis=1) == 0
            self.num_boost_optimal = np.argmax(
                self.scores[mask].mean(axis=1).values)
            self.score_max = self.scores[mask].mean(
                axis=1)[self.num_boost_optimal]
            # self.score_max = np.mean(scores_avg)
            self.std = self.scores[mask].std(axis=1)[self.num_boost_optimal]
            # self.std = np.std(scores_avg)

            result = {'loss': -self.score_max,
                      'status': STATUS_OK,
                      'std': self.std,
                      'score_max': self.score_max,
                      'scores_all': scores_avg,
                      'num_boost': int(self.num_boost_optimal),
                      }
            log.info(result)
            return result
        return self

    def transform(self, df):
        x = df[self.feature_name]
        y = df[self.col_target]
        predict = pd.Series(data=np.zeros(shape=(df.shape[0],1)),index=df.index)

        for fold, (train, val) in enumerate(self.iterator.split(df)):
            if self.cross_target_encoder is not None:
                encoded_train, encoded_test = self.cross_target_encoder.transform(
                    fold=fold, train=train, test=val)
                train = pd.concat([train, encoded_train], axis=1)
                val = pd.concat([val, encoded_test], axis=1)

            X_train, X_val = train[self.feature_name], val[self.feature_name]
            y_train, y_val = train[self.col_target], val[self.col_target]

            # Подготовка данных в нужном формате
            model = self.models[fold]
            predict.loc[X_val.index] += \
                model.predict(X_val[model.feature_name()].astype(float),
                              num_iteration=self.num_boost_optimal) / self.iterator.n_repeats

        return predict

    def predict(self, test):
        models_len = len(self.models.keys())
        if self.cross_target_encoder is not None:
            encoded_test = self.cross_target_encoder.predict(test)
            test = pd.concat([test, encoded_test], axis=1)

        predict = pd.Series(data=np.zeros(shape=(test.shape[0],1)),index=test.index)

        for fold in self.models.keys():
            model = self.models[fold]
            predict += model.predict(test[model.feature_name()].astype(
                float), num_iteration=self.num_boost_optimal) / models_len

        return predict

    def shap(self, df: pd.DataFrame):
        fig = plt.figure(figsize=(10, 10))
        log = logging.getLogger(__name__)
        shap_df_fin = pd.DataFrame(columns=['feature'])

        x = df[self.feature_name]
        y = df[self.col_target]

        for fold, (train, val) in enumerate(self.iterator.split(df)):
            if self.cross_target_encoder is not None:
                encoded_train, encoded_test = self.cross_target_encoder.transform(
                    fold=fold, train=train, test=val)
                train = pd.concat([train, encoded_train], axis=1)
                val = pd.concat([val, encoded_test], axis=1)

            X_train, X_val = train[self.feature_name], val[self.feature_name]
            y_train, y_val = train[self.col_target], val[self.col_target]

            model = self.models[fold]
            explainer = shap.TreeExplainer(model)
            df_sample = X_val[model.feature_name()].sample(
                n=500, random_state=0, replace=True).astype(float)
            shap_values = explainer.shap_values(df_sample)[1]
            shap_df = pd.DataFrame(zip(model.feature_name(), np.mean(
                np.abs(shap_values), axis=0)), columns=['feature', 'shap_' + str(fold)])
            shap_df_fin = pd.merge(shap_df_fin, shap_df,
                                   how='outer', on='feature')

        shap_feature_stats = shap_df_fin.set_index('feature').agg(
            ['mean', 'std'], axis=1).sort_values('mean', ascending=False)
        cols_best = shap_feature_stats[:30].index

        best_features = shap_df_fin.loc[shap_df_fin['feature'].isin(cols_best)]
        best_features_melt = pd.melt(
            best_features, id_vars=['feature'], value_vars=[
                feature for feature in best_features.columns.values.tolist() if feature not in ['feature']])

        sns.barplot(x='value', y='feature', data=best_features_melt,
                    estimator=np.mean, order=cols_best)
        return fig, shap_feature_stats.reset_index()

    def shap_summary_plot(self, test: pd.DataFrame):
        fig = plt.figure()
        log = logging.getLogger(__name__)
        shap_df_fin = pd.DataFrame(columns=['feature'])
        if self.cross_target_encoder is not None:
            encoded_test = self.cross_target_encoder.predict(test=test)
            test = pd.concat([test, encoded_test], axis=1)

        # Подготовка данных в нужном формате
        model = self.models[0]
        explainer = shap.TreeExplainer(model)
        df_sample = test[model.feature_name()].sample(
            n=500, random_state=0, replace=True).astype(float)
        shap_values = explainer.shap_values(df_sample)[1]
        shap_df = pd.DataFrame(zip(model.feature_name(), np.mean(
            np.abs(shap_values), axis=0)), columns=['feature', 'shap_'])
        shap_df_fin = pd.merge(shap_df_fin, shap_df, how='outer', on='feature')

        shap.summary_plot(shap_values, df_sample, show=False, )
        return fig


class CrossLightgbmModel(CrossModelFabric):
    def get_hyperopt_space(self, params={}, random_state=None):
        if random_state is None:
            random_state = self.random_state
        result = {
            'num_leaves': scope.int(hp.quniform('num_leaves', 100, 500, 1)),
            'max_depth': scope.int(hp.quniform('max_depth', 10, 70, 1)),
            'min_data_in_leaf': scope.int(hp.quniform('min_data_in_leaf', 10, 150, 1)),
            'feature_fraction': hp.uniform('feature_fraction', 0.75, 1.0),
            'bagging_fraction': hp.uniform('bagging_fraction', 0.75, 1.0),
            'min_sum_hessian_in_leaf': hp.loguniform('min_sum_hessian_in_leaf', 0, 2.3),
            'lambda_l1': hp.uniform('lambda_l1', 1e-4, 2),
            'lambda_l2': hp.uniform('lambda_l2', 1e-4, 2),
            'seed': random_state,
            'feature_fraction_seed': random_state,
            'bagging_seed': random_state,
            'drop_seed': random_state,
            'data_random_seed': random_state,
            'verbose': -1,
            'bagging_freq': 5,
            'max_bin': 255,
            'learning_rate': 0.03,
            'boosting_type': 'gbdt',
            'objective': 'binary',
            'metric': 'auc',
        }
        if params != {}:
            result.update(params)
        return result

    def get_dataset(self, data, label, categorical_feature, **kwargs):
        return lgb.Dataset(
            data=data,
            label=label,
            categorical_feature=categorical_feature,
            **kwargs)

    def train(
            self,
            params,
            train_set,
            train_name,
            valid_set,
            valid_name,
            num_boost_round,
            evals_result,
            categorical_feature,
            early_stopping_rounds,
            verbose_eval,
            **kwargs):
        model = lgb.train(params=params,
                          train_set=train_set,
                          valid_sets=[train_set, valid_set],
                          valid_names=[train_name, valid_name],
                          num_boost_round=num_boost_round,
                          evals_result=evals_result,
                          categorical_feature=categorical_feature,
                          early_stopping_rounds=early_stopping_rounds,
                          verbose_eval=verbose_eval,
                          **kwargs)
        return model


class CrossXgboostModel(CrossModelFabric):
    def get_hyperopt_space(self, params={}, random_state=None):
        if random_state is None:
            random_state = self.random_state
        result = {
            'n_estimators': scope.int(hp.quniform('n_estimators', 100, 1000, 1)),
            'eta': hp.quniform('eta', 0.025, 0.5, 0.025),
            # A problem with max_depth casted to float instead of int with
            # the hp.quniform method.
            'max_depth': scope.int(hp.quniform('max_depth', 1, 14, 1)),
            'min_child_weight': hp.quniform('min_child_weight', 1, 6, 1),
            'subsample': hp.quniform('subsample', 0.5, 1, 0.05),
            'gamma': hp.quniform('gamma', 0.5, 1, 0.05),
            'colsample_bytree': hp.quniform('colsample_bytree', 0.5, 1, 0.05),
            'eval_metric': 'auc',
            'objective': 'binary:logistic',
            # Increase this number if you have more cores. Otherwise, remove it and it will default
            # to the maxium number.
            # 'nthread': 4,
            'booster': 'gbtree',
            'tree_method': 'exact',
            'silent': 1,
            'seed': random_state
        }
        if params != {}:
            result.update(params)
        return result

    def get_dataset(self, data, label, categorical_feature, **kwargs):
        return xgb.DMatrix(data=data, label=label, **kwargs)

    def train(
            self,
            params,
            train_set,
            train_name,
            valid_set,
            valid_name,
            num_boost_round,
            evals_result,
            categorical_feature,
            early_stopping_rounds,
            verbose_eval,
            **kwargs):
        model = xgb.train(params=params,
                          dtrain=train_set,
                          evals=[(train_set, train_name),
                                 (valid_set, valid_name)],
                          num_boost_round=num_boost_round,
                          evals_result=evals_result,
                          early_stopping_rounds=early_stopping_rounds,
                          verbose_eval=verbose_eval,
                          **kwargs)
        return model


#
#
#
# class CatboostModel(CrossModelFabric):
#     def get_hyperopt_space(self, params={}, random_state=None):
#         if random_state is None:
#             random_state = self.random_state
#         result = {
#             'num_leaves': scope.int(hp.quniform('num_leaves', 300, 500, 1)),
#             'max_depth': scope.int(hp.quniform('max_depth', 10, 70, 1)),
#             'min_data_in_leaf': scope.int(hp.quniform('min_data_in_leaf', 10, 150, 1)),
#             'feature_fraction': hp.uniform('feature_fraction', 0.75, 1.0),
#             'bagging_fraction': hp.uniform('bagging_fraction', 0.75, 1.0),
#             'min_sum_hessian_in_leaf': hp.loguniform('min_sum_hessian_in_leaf', 0, 2.3),
#             'lambda_l1': hp.uniform('lambda_l1', 1e-4, 2),
#             'lambda_l2': hp.uniform('lambda_l2', 1e-4, 2),
#             'seed': random_state,
#             'feature_fraction_seed': random_state,
#             'bagging_seed': random_state,
#             'drop_seed': random_state,
#             'data_random_seed': random_state,
#             'verbose': -1,
#             'bagging_freq': 5,
#             'max_bin': 255,
#             'learning_rate': 0.03,
#             'boosting_type': 'gbdt',
#             'objective': 'binary',
#             'metric': 'auc',
#         }
#         if params!={}:
#             result.update(params)
#         return result
#
#     def get_dataset(self, data, label, categorical_feature, **kwargs):
#         return data, label
#
#     def train(self, params, train_set, valid_sets, valid_names, num_boost_round, evals_result, categorical_feature,
#               early_stopping_rounds, verbose_eval, **kwargs):
#
#         params = {'loss_function': 'Logloss',  # objective function
#                   'eval_metric': 'AUC',  # metric
#                   'verbose': 200,  # output to stdout info about training process every 200 iterations
#                   'random_seed': SEED
#                   }
#         cbc = CatBoostClassifier(**params)
#         model = cbc.fit(X,
#                         y=None,
#                         cat_features=categorical_feature,
#                         # text_features=None,
#                         # sample_weight=None,
#                         # baseline=None,
#                         # use_best_model=None,
#                         eval_set=valid_sets,
#                         verbose=verbose_eval,
#                         # logging_level=None,
#                         # plot=False,
#                         column_description=None,
#                         verbose_eval=None,
#                         metric_period=None,
#                         silent=None,
#                         early_stopping_rounds=early_stopping_rounds,
#                         # save_snapshot=None,
#                         # snapshot_file=None,
#                         # snapshot_interval=None,
#                         # init_model=None
#                         )
#         return model
