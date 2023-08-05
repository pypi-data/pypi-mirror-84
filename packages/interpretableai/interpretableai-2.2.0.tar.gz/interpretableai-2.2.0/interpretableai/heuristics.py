from .iai import _IAI, _requires_iai_version
from .iaibase import (Learner, ClassificationLearner, RegressionLearner)


class RandomForestLearner(Learner):
    """Abstract type encompassing all random forest learners."""
    pass


class RandomForestClassifier(RandomForestLearner, ClassificationLearner):
    """Learner for training random forests for classification problems.

    Julia Equivalent:
    `IAI.RandomForestClassifier <https://docs.interpretable.ai/v2.0.0/Heuristics/reference/#IAI.RandomForestClassifier>`

    Examples
    --------
    >>> RandomForestClassifier(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 2.1 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("2.1.0", "RandomForestClassifier")
        jl_obj = _IAI.RandomForestClassifier_convert(*args, **kwargs)
        super().__init__(jl_obj)


class RandomForestRegressor(RandomForestLearner, RegressionLearner):
    """Learner for training random forests for regression problems.

    Julia Equivalent:
    `IAI.RandomForestRegressor <https://docs.interpretable.ai/v2.0.0/Heuristics/reference/#IAI.RandomForestRegressor>`

    Examples
    --------
    >>> RandomForestRegressor(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 2.1 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("2.1.0", "RandomForestRegressor")
        jl_obj = _IAI.RandomForestRegressor_convert(*args, **kwargs)
        super().__init__(jl_obj)


class XGBoostLearner(Learner):
    """Abstract type encompassing all XGBoost learners."""
    pass


class XGBoostClassifier(XGBoostLearner, ClassificationLearner):
    """Learner for training XGBoost models for classification problems.

    Julia Equivalent:
    `IAI.XGBoostClassifier <https://docs.interpretable.ai/v2.0.0/Heuristics/reference/#IAI.XGBoostClassifier>`

    Examples
    --------
    >>> XGBoostClassifier(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 2.1 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("2.1.0", "XGBoostClassifier")
        jl_obj = _IAI.XGBoostClassifier_convert(*args, **kwargs)
        super().__init__(jl_obj)


class XGBoostRegressor(XGBoostLearner, RegressionLearner):
    """Learner for training XGBoost models for regression problems.

    Julia Equivalent:
    `IAI.XGBoostRegressor <https://docs.interpretable.ai/v2.0.0/Heuristics/reference/#IAI.XGBoostRegressor>`

    Examples
    --------
    >>> XGBoostRegressor(**kwargs)

    Parameters
    ----------
    Use keyword arguments to set parameters on the resulting learner. Refer to
    the Julia documentation for available parameters.

    Compatibility
    -------------
    Requires IAI version 2.1 or higher.
    """
    def __init__(self, *args, **kwargs):
        _requires_iai_version("2.1.0", "XGBoostRegressor")
        jl_obj = _IAI.XGBoostRegressor_convert(*args, **kwargs)
        super().__init__(jl_obj)

