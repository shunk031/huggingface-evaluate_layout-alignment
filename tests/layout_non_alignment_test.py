import os
import pathlib

import evaluate
import pytest
import torch


@pytest.fixture
def base_dir(metrics_dir: pathlib.Path) -> str:
    return metrics_dir / "layout_non_alignment"


@pytest.fixture
def metric_path(base_dir: pathlib.Path) -> str:
    return os.path.join(base_dir, "layout-non-alignment.py")


@pytest.fixture
def expected_score(is_CI: bool) -> float:
    # https://github.com/PKU-ICST-MIPL/PosterLayout-CVPR2023/blob/main/output/results.txt#L4
    return 0.0054257973599846545 if is_CI else 0.0046338920146440955


def test_metric(
    metric_path: str,
    poster_predictions: torch.Tensor,
    poster_gold_labels: torch.Tensor,
    poster_width: int,
    poster_height: int,
    expected_score: float,
):
    metric = evaluate.load(
        path=metric_path,
        canvas_width=poster_width,
        canvas_height=poster_height,
    )
    metric.add_batch(
        predictions=poster_predictions,
        gold_labels=poster_gold_labels,
    )
    score = metric.compute()
    assert score is not None and score == pytest.approx(expected_score, 1e-5)
