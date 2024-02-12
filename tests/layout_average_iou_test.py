import math
import os
import pathlib
import pickle
from typing import Dict

import evaluate
import numpy as np
import pytest
import torch


@pytest.fixture
def base_dir() -> str:
    return "layout_average_iou"


@pytest.fixture
def metric_path(base_dir: str) -> str:
    return os.path.join(base_dir, "layout_average_iou.py")


@pytest.fixture
def test_fixture_dir() -> pathlib.Path:
    return pathlib.Path(__file__).parents[1] / "test_fixtures"


@pytest.fixture
def layouts(test_fixture_dir: pathlib.Path):
    layouts1_path = test_fixture_dir / "layouts_sub.pkl"
    with layouts1_path.open("rb") as rf:
        layouts1 = pickle.load(rf)
    return layouts1


@pytest.fixture
def expected_scores() -> Dict[str, float]:
    return {
        "average-iou_BLT": 0.06813084535104685,
        "average-iou_VTN": 0.19680290990805305,
    }


def test_metric(
    metric_path: str,
    layouts,
    expected_scores: Dict[str, float],
):
    metric = evaluate.load(path=metric_path)
    metric.add_batch(layouts=layouts)

    scores = metric.compute()
    assert scores is not None
    for k in expected_scores.keys():
        score = scores[k]
        expected_score = expected_scores[k]
        assert math.isclose(score, expected_score, rel_tol=1e-5)


@pytest.mark.parametrize(
    argnames="arr_func",
    argvalues=(np.array, torch.Tensor),
)
def test_array_variant(metric_path: str, layouts, arr_func):
    metric = evaluate.load(path=metric_path)

    metric.add_batch(
        layouts=[{k: arr_func(v) for k, v in layout.items()} for layout in layouts],
    )
