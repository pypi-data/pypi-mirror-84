from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from evalml.automl.pipeline_search_plots import SearchIterationPlot


def test_search_iteration_plot_class():
    pytest.importorskip('plotly.graph_objects', reason='Skipping plotting test because plotly not installed')

    class MockObjective:
        def __init__(self):
            self.name = 'Test Objective'
            self.greater_is_better = True

    class MockResults:
        def __init__(self):
            self.objective = MockObjective()
            self.results = {
                'pipeline_results': {
                    2: {
                        'score': 0.50
                    },
                    0: {
                        'score': 0.60
                    },
                    1: {
                        'score': 0.75
                    },
                },
                'search_order': [1, 2, 0]
            }
            self.rankings = pd.DataFrame({
                'score': [0.75, 0.60, 0.50]
            })

    mock_data = MockResults()
    plot = SearchIterationPlot(mock_data)

    # Check best score trace
    plot_data = plot.best_score_by_iter_fig.data[0]
    x = list(plot_data['x'])
    y = list(plot_data['y'])

    assert isinstance(plot, SearchIterationPlot)
    assert x == [0, 1, 2]
    assert y == [0.60, 0.75, 0.75]

    # Check current score trace
    plot_data = plot.best_score_by_iter_fig.data[1]
    x = list(plot_data['x'])
    y = list(plot_data['y'])

    assert isinstance(plot, SearchIterationPlot)
    assert x == [0, 1, 2]
    assert y == [0.60, 0.75, 0.50]


@patch('evalml.automl.pipeline_search_plots.jupyter_check')
@patch('evalml.automl.pipeline_search_plots.import_or_raise')
def test_jupyter(import_check, jupyter_check):
    mock_data = MagicMock()

    pytest.importorskip('plotly.graph_objects', reason='Skipping plotting test because plotly not installed')
    jupyter_check.return_value = True
    with pytest.warns(None) as graph_valid:
        SearchIterationPlot(mock_data)
        assert len(graph_valid) == 0
        import_check.assert_called_with('ipywidgets', warning=True)

    jupyter_check.return_value = False
    with pytest.warns(None) as graph_valid:
        SearchIterationPlot(mock_data)
        assert len(graph_valid) == 0
