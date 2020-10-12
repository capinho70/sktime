#!/usr/bin/env python3 -u
# -*- coding: utf-8 -*-
# copyright: sktime developers, BSD-3-Clause License (see LICENSE file)

__author__ = ["Markus Löning"]
__all__ = ["ESTIMATOR_TEST_PARAMS", "EXCLUDED_ESTIMATORS", "EXCLUDED_TESTS"]

import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import FunctionTransformer
from sklearn.preprocessing import StandardScaler

from sktime.base import BaseEstimator
from sktime.classification.base import BaseClassifier
from sktime.classification.compose import ColumnEnsembleClassifier
from sktime.classification.compose import TimeSeriesForestClassifier
from sktime.classification.frequency_based import RandomIntervalSpectralForest
from sktime.classification.interval_based import TimeSeriesForest
from sktime.classification.shapelet_based import ShapeletTransformClassifier
from sktime.forecasting.arima import AutoARIMA
from sktime.forecasting.base import BaseForecaster
from sktime.forecasting.compose import DirectRegressionForecaster
from sktime.forecasting.compose import DirectTimeSeriesRegressionForecaster
from sktime.forecasting.compose import EnsembleForecaster
from sktime.forecasting.compose import RecursiveRegressionForecaster
from sktime.forecasting.compose import RecursiveTimeSeriesRegressionForecaster
from sktime.forecasting.compose import StackingForecaster
from sktime.forecasting.compose import TransformedTargetForecaster
from sktime.forecasting.exp_smoothing import ExponentialSmoothing
from sktime.forecasting.model_selection import ForecastingGridSearchCV
from sktime.forecasting.model_selection import SingleWindowSplitter
from sktime.forecasting.naive import NaiveForecaster
from sktime.forecasting.theta import ThetaForecaster
from sktime.performance_metrics.forecasting import sMAPE
from sktime.regression.base import BaseRegressor
from sktime.regression.compose import TimeSeriesForestRegressor
from sktime.series_as_features.compose import FeatureUnion
from sktime.transformers.base import _BaseTransformer
from sktime.transformers.base import _SeriesAsFeaturesToSeriesAsFeaturesTransformer
from sktime.transformers.base import _SeriesAsFeaturesToTabularTransformer
from sktime.transformers.base import _SeriesToPrimitivesTransformer
from sktime.transformers.base import _SeriesToSeriesTransformer
from sktime.transformers.series_as_features.compose import ColumnTransformer
from sktime.transformers.series_as_features.compose import (
    SeriesToPrimitivesRowTransformer,
)
from sktime.transformers.series_as_features.compose import SeriesToSeriesRowTransformer
from sktime.transformers.series_as_features.dictionary_based import SFA
from sktime.transformers.series_as_features.interpolate import TSInterpolator
from sktime.transformers.series_as_features.reduce import Tabularizer
from sktime.transformers.series_as_features.shapelets import ContractedShapeletTransform
from sktime.transformers.series_as_features.shapelets import ShapeletTransform
from sktime.transformers.series_as_features.summarize import FittedParamExtractor
from sktime.transformers.series_as_features.summarize import TSFreshFeatureExtractor
from sktime.transformers.series_as_features.summarize import (
    TSFreshRelevantFeatureExtractor,
)
from sktime.transformers.single_series.adapt import SingleSeriesTransformAdaptor
from sktime.transformers.single_series.detrend import Detrender

# The following estimators currently do not pass all unit tests or fail some of them
# and are excluded until fixed.
EXCLUDED_ESTIMATORS = [
    "ElasticEnsemble",
    "KNeighborsTimeSeriesClassifier",
    "ProximityForest",
    "ProximityStump",
    "ProximityTree",
]

EXCLUDED_TESTS = {
    "ShapeletTransformClassifier": ["check_fit_idempotent"],
    "ContractedShapeletTransform": ["check_fit_idempotent"],
}

# We here configure estimators for basic unit testing, including setting of
# required hyper-parameters and setting of hyper-parameters for faster training.
SERIES_TO_SERIES_TRANSFORMER = StandardScaler()
SERIES_TO_PRIMITIVES_TRANSFORMER = FunctionTransformer(
    np.mean, kw_args={"axis": 0}, check_inverse=False
)
TRANSFORMERS = [
    (
        "transformer1",
        SeriesToSeriesRowTransformer(
            SERIES_TO_SERIES_TRANSFORMER, check_transformer=False
        ),
    ),
    (
        "transformer2",
        SeriesToSeriesRowTransformer(
            SERIES_TO_SERIES_TRANSFORMER, check_transformer=False
        ),
    ),
]
REGRESSOR = LinearRegression()
TIME_SERIES_CLASSIFIER = TimeSeriesForest(n_estimators=3)
TIME_SERIES_CLASSIFIERS = [
    ("tsf1", TIME_SERIES_CLASSIFIER),
    ("tsf2", TIME_SERIES_CLASSIFIER),
]
FORECASTER = ExponentialSmoothing()
FORECASTERS = [("ses1", FORECASTER), ("ses2", FORECASTER)]
STEPS = [
    ("transformer", Detrender(ThetaForecaster())),
    ("forecaster", NaiveForecaster()),
]
ESTIMATOR_TEST_PARAMS = {
    FeatureUnion: {"transformer_list": TRANSFORMERS},
    DirectRegressionForecaster: {"regressor": REGRESSOR},
    RecursiveRegressionForecaster: {"regressor": REGRESSOR},
    DirectTimeSeriesRegressionForecaster: {
        "regressor": make_pipeline(Tabularizer(), REGRESSOR)
    },
    RecursiveTimeSeriesRegressionForecaster: {
        "regressor": make_pipeline(Tabularizer(), REGRESSOR)
    },
    TransformedTargetForecaster: {"steps": STEPS},
    EnsembleForecaster: {"forecasters": FORECASTERS},
    StackingForecaster: {"forecasters": FORECASTERS, "final_regressor": REGRESSOR},
    Detrender: {"forecaster": FORECASTER},
    ForecastingGridSearchCV: {
        "forecaster": NaiveForecaster(strategy="mean"),
        "cv": SingleWindowSplitter(fh=1),
        "param_grid": {"window_length": [2, 5]},
        "scoring": sMAPE(),
    },
    SingleSeriesTransformAdaptor: {"transformer": StandardScaler()},
    ColumnEnsembleClassifier: {
        "estimators": [
            (name, estimator, 0) for (name, estimator) in TIME_SERIES_CLASSIFIERS
        ]
    },
    FittedParamExtractor: {
        "forecaster": FORECASTER,
        "param_names": ["smoothing_level"],
    },
    SeriesToPrimitivesRowTransformer: {
        "transformer": SERIES_TO_PRIMITIVES_TRANSFORMER,
        "check_transformer": False,
    },
    SeriesToSeriesRowTransformer: {
        "transformer": SERIES_TO_SERIES_TRANSFORMER,
        "check_transformer": False,
    },
    ColumnTransformer: {
        "transformers": [(name, estimator, [0]) for name, estimator in TRANSFORMERS]
    },
    AutoARIMA: {
        "d": 0,
        "suppress_warnings": True,
        "max_p": 2,
        "max_q": 2,
        "seasonal": False,
    },
    ShapeletTransformClassifier: {"n_estimators": 3, "time_contract_in_mins": 0.125},
    ContractedShapeletTransform: {"time_contract_in_mins": 0.125},
    ShapeletTransform: {
        "max_shapelets_to_store_per_class": 1,
        "min_shapelet_length": 3,
        "max_shapelet_length": 4,
    },
    TSFreshFeatureExtractor: {"disable_progressbar": True, "show_warnings": False},
    TSFreshRelevantFeatureExtractor: {
        "disable_progressbar": True,
        "show_warnings": False,
        "fdr_level": 0.01,
    },
    TSInterpolator: {"length": 10},
    RandomIntervalSpectralForest: {"n_estimators": 3, "acf_lag": 10, "min_interval": 5},
    SFA: {"return_pandas_data_series": True},
    TimeSeriesForest: {"n_estimators": 3},
    TimeSeriesForestClassifier: {"n_estimators": 3},
    TimeSeriesForestRegressor: {"n_estimators": 3},
}

# These methods should not change the state of the estimator, that is, they should
# not change fitted parameters or hyper-parameters. They are also the methods that
# "apply" the fitted estimator to data and useful for checking results.
NON_STATE_CHANGING_METHODS = (
    "predict",
    "predict_proba",
    "decision_function",
    "transform",
    "inverse_transform",
)

# We use estimator tags in addition to class hierarchies to further distinguish
# estimators into different categories. This is useful for defining and running
# common tests for estimators with the same tags.
VALID_ESTIMATOR_TAGS = (
    "fit-in-transform",  # fitted in transform or non-fittable
    "univariate-only",
    "transform-returns-same-time-index",
)

# The following gives a list of valid estimator base classes.
VALID_TRANSFORMER_TYPES = (
    _SeriesToPrimitivesTransformer,
    _SeriesToSeriesTransformer,
    _SeriesAsFeaturesToTabularTransformer,
    _SeriesAsFeaturesToSeriesAsFeaturesTransformer,
)
VALID_ESTIMATOR_BASE_TYPES = (
    BaseClassifier,
    BaseRegressor,
    BaseForecaster,
    _BaseTransformer,
)
VALID_ESTIMATOR_TYPES = (
    BaseEstimator,
    *VALID_ESTIMATOR_BASE_TYPES,
    *VALID_TRANSFORMER_TYPES,
)

VALID_ESTIMATOR_BASE_TYPE_LOOKUP = {
    "classifier": BaseClassifier,
    "regressor": BaseRegressor,
    "forecaster": BaseForecaster,
    "transformer": _BaseTransformer,
}
