import numpy as np
import pandas as pd
import pytest

from evalml import AutoMLSearch
from evalml.objectives import FraudCost


def test_fraud_objective(X_y_binary):
    X, y = X_y_binary

    objective = FraudCost(retry_percentage=.5,
                          interchange_fee=.02,
                          fraud_payout_percentage=.75,
                          amount_col=10)

    automl = AutoMLSearch(problem_type='binary', objective=objective, max_iterations=1)
    automl.search(X, y)

    pipeline = automl.best_pipeline
    pipeline.fit(X, y)
    pipeline.predict(X, objective)
    pipeline.predict_proba(X)
    pipeline.score(X, y, [objective])


def test_fraud_objective_function_amount_col(X_y_binary):
    X, y = X_y_binary

    objective = FraudCost(retry_percentage=.5,
                          interchange_fee=.02,
                          fraud_payout_percentage=.75,
                          amount_col="this column does not exist")
    y_predicted = pd.Series([.1, .5, .5])
    y_true = [True, False, True]
    with pytest.raises(ValueError, match="`this column does not exist` is not a valid column in X."):
        objective.objective_function(y_true, y_predicted, X)


def test_input_contains_nan(X_y_binary):
    fraud_cost = FraudCost(amount_col="value")
    y_predicted = np.array([np.nan, 0, 0])
    y_true = np.array([1, 2, 1])
    with pytest.raises(ValueError, match="y_predicted contains NaN or infinity"):
        fraud_cost.score(y_true, y_predicted)

    y_true = np.array([np.nan, 0, 0])
    y_predicted = np.array([1, 2, 0])
    with pytest.raises(ValueError, match="y_true contains NaN or infinity"):
        fraud_cost.score(y_true, y_predicted)


def test_input_contains_inf(capsys):
    fraud_cost = FraudCost(amount_col="value")
    y_predicted = np.array([np.inf, 0, 0])
    y_true = np.array([1, 0, 0])
    with pytest.raises(ValueError, match="y_predicted contains NaN or infinity"):
        fraud_cost.score(y_true, y_predicted)

    y_true = np.array([np.inf, 0, 0])
    y_predicted = np.array([1, 0, 0])
    with pytest.raises(ValueError, match="y_true contains NaN or infinity"):
        fraud_cost.score(y_true, y_predicted)


def test_different_input_lengths():
    fraud_cost = FraudCost(amount_col="value")
    y_predicted = np.array([0, 0])
    y_true = np.array([1])
    with pytest.raises(ValueError, match="Inputs have mismatched dimensions"):
        fraud_cost.score(y_true, y_predicted)

    y_true = np.array([0, 0])
    y_predicted = np.array([1, 2, 0])
    with pytest.raises(ValueError, match="Inputs have mismatched dimensions"):
        fraud_cost.score(y_true, y_predicted)


def test_zero_input_lengths():
    fraud_cost = FraudCost(amount_col="value")
    y_predicted = np.array([])
    y_true = np.array([])
    with pytest.raises(ValueError, match="Length of inputs is 0"):
        fraud_cost.score(y_true, y_predicted)


def test_binary_more_than_two_unique_values():
    fraud_cost = FraudCost(amount_col="value")
    y_predicted = np.array([0, 1, 2])
    y_true = np.array([1, 0, 1])
    with pytest.raises(ValueError, match="y_predicted contains more than two unique values"):
        fraud_cost.score(y_true, y_predicted)

    y_true = np.array([0, 1, 2])
    y_predicted = np.array([1, 0, 1])
    with pytest.raises(ValueError, match="y_true contains more than two unique values"):
        fraud_cost.score(y_true, y_predicted)


def test_fraud_objective_score(X_y_binary):
    X, y = X_y_binary
    fraud_cost = FraudCost(amount_col="value")

    y_predicted = pd.Series([.1, .5, .5])
    y_true = [True, False, True]
    extra_columns = pd.DataFrame({"value": [100, 5, 250]})

    out = fraud_cost.decision_function(y_predicted, 5, extra_columns)
    assert isinstance(out, pd.Series)
    assert out.tolist() == y_true
    score = fraud_cost.score(y_true, out, extra_columns)
    assert (score == 0.0)

    out = fraud_cost.decision_function(y_predicted.to_numpy(), 5, extra_columns)
    assert isinstance(out, pd.Series)
    assert out.tolist() == y_true
    score = fraud_cost.score(y_true, out, extra_columns)
    assert (score == 0.0)

    # testing with other types of inputs
    y_predicted = np.array([.1, .5, .5])
    extra_columns = {"value": [100, 5, 250]}
    out = fraud_cost.decision_function(y_predicted, 5, extra_columns)
    assert out.tolist() == y_true
    score = fraud_cost.score(y_true, out, extra_columns)
    assert (score == 0.0)

    y_predicted = pd.Series([.2, .01, .01])
    extra_columns = pd.DataFrame({"value": [100, 50, 50]})
    y_true = [False, False, True]
    expected_y_pred = [True, False, False]
    out = fraud_cost.decision_function(y_predicted, 10, extra_columns)
    assert out.tolist() == expected_y_pred
    score = fraud_cost.score(y_true, out, extra_columns)
    assert (score == 0.255)
