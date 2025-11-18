from pathlib import Path

from ux_optimizer import ImageSpec, run_project


def get_specs() -> list[ImageSpec]:
    return [
        ImageSpec(
            id="beta_001",
            description="Low-resolution prototype mock",
            size=(200, 120),
            style="ui",
            tags=("edge", "low_res"),
        ),
        ImageSpec(
            id="beta_002",
            description="Tiny icon-sized snapshot",
            size=(32, 32),
            style="photo",
            tags=("boundary", "tiny", "edge"),
        ),
        ImageSpec(
            id="beta_003",
            description="Very large billboard-style photo",
            size=(2048, 2048),
            style="photo",
            tags=("boundary", "photo"),
        ),
        ImageSpec(
            id="beta_004",
            description="Malformed upload (corrupt file)",
            size=(640, 360),
            style="ui",
            invalid=True,
            tags=("invalid",),
        ),
        ImageSpec(
            id="beta_005",
            description="Mixed UI + photo collage",
            size=(1024, 768),
            style="photo",
            tags=("mixed", "photo", "ui"),
        ),
    ]


def run(output_root: Path | str) -> list[dict]:
    output_root = Path(output_root)
    return run_project("project_beta", get_specs(), output_root)
