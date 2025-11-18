from pathlib import Path

from ux_optimizer import ImageSpec, run_project


def get_specs() -> list[ImageSpec]:
    return [
        ImageSpec(
            id="alpha_001",
            description="Cramped dashboard with inconsistent spacing",
            size=(1280, 720),
            style="ui",
            tags=("ui", "normal"),
        ),
        ImageSpec(
            id="alpha_002",
            description="Marketing banner with vibrant colors",
            size=(1200, 600),
            style="ui",
            tags=("marketing",),
        ),
        ImageSpec(
            id="alpha_003",
            description="App screenshot with low contrast text",
            size=(1080, 1920),
            style="ui",
            tags=("ui", "long"),
        ),
    ]


def run(output_root: Path | str) -> list[dict]:
    output_root = Path(output_root)
    return run_project("project_alpha", get_specs(), output_root)
