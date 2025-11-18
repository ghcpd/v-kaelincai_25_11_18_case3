from __future__ import annotations

import json
import os
import random
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Dict, Any

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageOps


@dataclass
class ImageSpec:
    id: str
    description: str
    size: tuple[int, int]
    style: str
    noise: float = 0.08
    tags: tuple[str, ...] = ()
    invalid: bool = False
    palette: tuple[tuple[int, int, int], ...] | None = None


def ensure_directories(base_dir: Path) -> dict[str, Path]:
    dirs = {
        "original": base_dir / "images_original",
        "optimized": base_dir / "images_optimized",
        "comparison": base_dir / "images_comparison",
    }
    for path in dirs.values():
        path.mkdir(parents=True, exist_ok=True)
    return dirs


def _bounded_coord(low: int, high: int, limit: int) -> int:
    limit = max(limit, 0)
    low = max(0, min(low, limit))
    high = max(0, min(high, limit))
    if low > high:
        low, high = high, low
    return low if low == high else random.randint(low, high)


def _create_placeholder_image(size: tuple[int, int], text: str | None = None) -> Image.Image:
    canvas = Image.new("RGB", size, (38, 38, 42))
    if text and size[0] > 80 and size[1] > 20:
        draw = ImageDraw.Draw(canvas)
        draw.text((8, 8), text, fill=(255, 255, 255))
    return canvas


def generate_mock_image(spec: ImageSpec) -> Image.Image:
    width, height = spec.size
    palette = spec.palette or (
        (30, 40, 70),
        (255, 255, 255),
        (90, 150, 200),
    )
    base_color = palette[0]
    canvas = Image.new("RGB", (width, height), base_color)
    draw = ImageDraw.Draw(canvas)

    if spec.style == "ui":
        margin = int(width * 0.05)
        draw.rectangle([margin, margin, width - margin, height - margin], fill=palette[1])
        for idx in range(3):
            top = margin + idx * (height // 5)
            bottom = top + (height // 8)
            accent = tuple(min(255, val + idx * 30) for val in palette[2])
            draw.rounded_rectangle(
                [margin + 10, top + 10, width - margin - 10, bottom],
                radius=10,
                fill=accent,
                outline=palette[2],
            )
        draw.text((margin + 20, height - 60), "Dashboard • Q4 Metrics", fill=palette[2])
    else:
        draw.rectangle([0, 0, width, height], fill=palette[1])
        for _ in range(6):
            x0 = _bounded_coord(10, width - 60, width - 1)
            y0 = _bounded_coord(10, height - 60, height - 1)
            x1 = _bounded_coord(60, width - 10, width - 1)
            y1 = _bounded_coord(60, height - 10, height - 1)
            box = [min(x0, x1), min(y0, y1), max(x0, x1), max(y0, y1)]
            draw.ellipse(box, fill=random.choice(palette), outline=(255, 255, 255))
        for size in range(3, 6):
            draw.line(
                (random.randint(0, width), random.randint(0, height), random.randint(0, width), random.randint(0, height)),
                fill=random.choice(palette),
                width=size,
            )

    if spec.noise > 0:
        arr = np.array(canvas).astype(np.float32)
        noise = np.random.normal(scale=spec.noise * 255, size=arr.shape)
        arr += noise
        arr = np.clip(arr, 0, 255).astype(np.uint8)
        canvas = Image.fromarray(arr)

    return canvas


def enhance_image(image: Image.Image, spec: ImageSpec) -> Image.Image:
    warm_tone = Image.new("RGB", image.size, (235, 230, 255))
    blended = Image.blend(image, warm_tone, alpha=0.1)
    sharpened = blended.filter(ImageFilter.UnsharpMask(radius=2, percent=180, threshold=3))
    contrasted = ImageOps.autocontrast(sharpened, cutoff=2)
    vignette = Image.new("L", image.size, 0)
    draw = ImageDraw.Draw(vignette)
    radius = max(image.size) // 2
    draw.ellipse([
        -radius,
        -radius // 2,
        image.width + radius,
        image.height + radius,
    ], fill=200)
    vignette = vignette.filter(ImageFilter.GaussianBlur(radius / 3))
    contrasted = Image.composite(contrasted, Image.new("RGB", image.size, (15, 15, 20)), vignette)
    return contrasted


def create_comparison_image(original: Image.Image, optimized: Image.Image) -> Image.Image:
    total_width = original.width + optimized.width + 20
    max_height = max(original.height, optimized.height)
    comparison = Image.new("RGB", (total_width, max_height + 30), (245, 245, 245))
    comparison.paste(original, (0, 0))
    comparison.paste(optimized, (original.width + 20, 0))
    draw = ImageDraw.Draw(comparison)
    draw.text((10, max_height + 5), "original", fill=(60, 60, 60))
    draw.text((original.width + 30, max_height + 5), "optimized", fill=(60, 60, 60))
    return comparison


def run_project(
    project_name: str,
    specs: Iterable[ImageSpec],
    output_root: Path,
    write_metadata: bool = True,
) -> List[Dict[str, Any]]:
    base_dir = output_root / project_name
    dirs = ensure_directories(base_dir)
    metadata: List[Dict[str, Any]] = []

    for spec in specs:
        original_path = dirs["original"] / f"{spec.id}_original.png"
        optimized_path = dirs["optimized"] / f"{spec.id}_optimized.png"
        comparison_path = dirs["comparison"] / f"{spec.id}_compare.png"
        entry = {
            "id": spec.id,
            "description": spec.description,
            "tags": list(spec.tags),
            "original": os.path.relpath(original_path, Path.cwd()),
            "optimized": os.path.relpath(optimized_path, Path.cwd()),
            "comparison": os.path.relpath(comparison_path, Path.cwd()),
            "status": "pending",
            "notes": "",
        }

        try:
            if spec.invalid:
                original_path.write_text("corrupt")
                raise ValueError("simulated asset corruption")

            original_image = generate_mock_image(spec)
            original_image.save(original_path)
            optimized_image = enhance_image(original_image, spec)
            optimized_image.save(optimized_path)
            comparison_image = create_comparison_image(original_image, optimized_image)
            comparison_image.save(comparison_path)

            entry["status"] = "ok"
            entry["notes"] = "layout margins cleaned, palette harmonized, clarity boosted"
        except Exception as exc:  # pragma: no cover - best effort fallback
            entry["status"] = "failed"
            placeholder = _create_placeholder_image(spec.size, "invalid asset")
            placeholder.save(optimized_path)
            placeholder.save(comparison_path)
            entry["notes"] = f"{exc}"[:140]
        metadata.append(entry)

    if write_metadata:
        metadata_path = base_dir / "metadata.json"
        metadata_path.write_text(json.dumps(metadata, indent=2))

    return metadata


def aggregate_metrics(entries: Iterable[Dict[str, Any]]) -> Dict[str, float]:
    entries = list(entries)
    total = len(entries)
    succeeded = sum(1 for entry in entries if entry.get("status") == "ok")
    failed = total - succeeded
    edge_cases = [entry for entry in entries if "edge" in entry["tags"]]
    edge_success = sum(1 for entry in edge_cases if entry.get("status") == "ok")
    return {
        "processed": total,
        "success_rate": succeeded / total if total else 0.0,
        "failure_rate": failed / total if total else 0.0,
        "edge_case_success_rate": edge_success / len(edge_cases) if edge_cases else 0.0,
    }
