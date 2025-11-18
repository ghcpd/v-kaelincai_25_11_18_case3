"""Automated tests covering the UI/UX improvement pipeline scenarios."""
from pathlib import Path
import tempfile

import pytest

from ux_optimizer import ImageSpec, aggregate_metrics, run_project


def run_scenario(specs, tmp_path, project_name):
    return run_project(project_name, specs, tmp_path)


def assert_artifacts(tmp_path, project_name, expected_count):
    base = tmp_path / project_name
    for sub in ("images_original", "images_optimized", "images_comparison"):
        folder = base / sub
        assert folder.exists(), f"{sub} missing"
        files = list(folder.glob("*"))
        if sub == "images_original":
            assert len(files) >= expected_count
        else:
            assert len(files) >= expected_count


def build_normal_specs():
    return [
        ImageSpec("test_normal_001", "UI modal with poor spacing", (640, 480), "ui", tags=("normal",)),
        ImageSpec("test_normal_002", "Photo promo with uneven contrast", (800, 600), "photo", tags=("normal", "photo")),
    ]


def build_edge_specs():
    return [
        ImageSpec("test_edge_001", "Low-resolution icon", (120, 80), "ui", tags=("edge", "low_res")),
        ImageSpec("test_edge_002", "Noisy screenshot", (480, 320), "ui", noise=0.18, tags=("edge", "noise")),
    ]


def build_boundary_specs():
    return [
        ImageSpec("test_boundary_001", "Very tiny crop", (32, 32), "photo", tags=("boundary",)),
        ImageSpec("test_boundary_002", "Ultra-wide hero", (2000, 900), "ui", tags=("boundary", "wide")),
    ]


def build_invalid_specs():
    return [
        ImageSpec("test_invalid_001", "Corrupted upload", (640, 360), "ui", invalid=True, tags=("invalid",)),
    ]


def build_mixed_specs():
    return [
        ImageSpec("test_mixed_001", "UI + photo collage", (1024, 768), "photo", tags=("mixed", "photo", "ui")),
        ImageSpec("test_mixed_002", "Cinematic screenshot", (1280, 720), "ui", tags=("mixed",)),
    ]


def describe_metrics(entries):
    metrics = aggregate_metrics(entries)
    assert metrics["processed"] == len(entries)
    return metrics


def test_normal_flow(tmp_path):
    """Normal flow: valid UI and photo inputs should be optimized."""
    specs = build_normal_specs()
    metadata = run_scenario(specs, tmp_path, "scenario_normal")
    assert_artifacts(tmp_path, "scenario_normal", expected_count=len(specs))
    metrics = describe_metrics(metadata)
    assert metrics["success_rate"] == 1.0


def test_edge_cases(tmp_path):
    """Edge cases: low resolution and noisy screenshots maintain success."""
    specs = build_edge_specs()
    metadata = run_scenario(specs, tmp_path, "scenario_edge")
    assert_artifacts(tmp_path, "scenario_edge", expected_count=len(specs))
    metrics = describe_metrics(metadata)
    assert metrics["edge_case_success_rate"] == 1.0


def test_boundary_cases(tmp_path):
    """Boundary cases: tiny and very large assets keep structural consistency."""
    specs = build_boundary_specs()
    metadata = run_scenario(specs, tmp_path, "scenario_boundary")
    assert_artifacts(tmp_path, "scenario_boundary", expected_count=len(specs))
    metrics = describe_metrics(metadata)
    assert metrics["success_rate"] == 1.0


def test_invalid_input(tmp_path):
    """Invalid inputs should be flagged without blocking other assets."""
    specs = build_invalid_specs()
    metadata = run_scenario(specs, tmp_path, "scenario_invalid")
    assert_artifacts(tmp_path, "scenario_invalid", expected_count=len(specs))
    assert metadata[0]["status"] == "failed"
    assert "corrupt" in metadata[0]["notes"].lower()


def test_mixed_image_types(tmp_path):
    """Mixed UI and photo types harmonize under the same flow."""
    specs = build_mixed_specs()
    metadata = run_scenario(specs, tmp_path, "scenario_mixed")
    assert_artifacts(tmp_path, "scenario_mixed", expected_count=len(specs))
    metrics = describe_metrics(metadata)
    assert metrics["success_rate"] == 1.0
