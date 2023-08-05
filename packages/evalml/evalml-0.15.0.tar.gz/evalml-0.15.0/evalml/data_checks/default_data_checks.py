from .class_imbalance_data_check import ClassImbalanceDataCheck
from .data_checks import DataChecks
from .highly_null_data_check import HighlyNullDataCheck
from .id_columns_data_check import IDColumnsDataCheck
from .invalid_targets_data_check import InvalidTargetDataCheck
from .no_variance_data_check import NoVarianceDataCheck
from .target_leakage_data_check import TargetLeakageDataCheck

from evalml.problem_types import ProblemTypes, handle_problem_types


class DefaultDataChecks(DataChecks):
    """A collection of basic data checks that is used by AutoML by default.
    Includes HighlyNullDataCheck, IDColumnsDataCheck, TargetLeakageDataCheck, InvalidTargetDataCheck, ClassImbalanceDataCheck,
    and NoVarianceDataCheck."""

    _DEFAULT_DATA_CHECK_CLASSES = [HighlyNullDataCheck, IDColumnsDataCheck,
                                   TargetLeakageDataCheck, InvalidTargetDataCheck, NoVarianceDataCheck]

    def __init__(self, problem_type):
        """
        A collection of basic data checks.
        Arguments:
            problem_type (str): The problem type that is being validated. Can be regression, binary, or multiclass.
        """
        if handle_problem_types(problem_type) == ProblemTypes.REGRESSION:
            super().__init__(self._DEFAULT_DATA_CHECK_CLASSES,
                             data_check_params={"InvalidTargetDataCheck": {"problem_type": problem_type}})
        else:
            super().__init__(self._DEFAULT_DATA_CHECK_CLASSES + [ClassImbalanceDataCheck],
                             data_check_params={"InvalidTargetDataCheck": {"problem_type": problem_type}})
