#!/usr/bin/env python3
"""Convert DWG/DXF drawings to a verified PDF using local tools."""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


PAPER_SIZES = {
    "a4-landscape": (11.69, 8.27),
    "a4-portrait": (8.27, 11.69),
    "a3-landscape": (16.54, 11.69),
    "a3-portrait": (11.69, 16.54),
    "a2-landscape": (23.39, 16.54),
    "a2-portrait": (16.54, 23.39),
}


def find_oda_converter() -> Path | None:
    candidates = [
        Path(r"C:\Program Files\ODA"),
        Path(r"C:\Program Files (x86)\ODA"),
    ]
    for root in candidates:
        if root.exists():
            matches = sorted(root.rglob("ODAFileConverter.exe"), reverse=True)
            if matches:
                return matches[0]
    found = shutil.which("ODAFileConverter.exe")
    return Path(found) if found else None


def convert_dwg_to_dxf(source: Path, work_dir: Path) -> Path:
    oda = find_oda_converter()
    if not oda:
        raise RuntimeError(
            "ODA File Converter is required for DWG input. Install ODA.ODAFileConverter with winget."
        )

    input_dir = work_dir / "input"
    output_dir = work_dir / "converted"
    input_dir.mkdir(parents=True, exist_ok=True)
    output_dir.mkdir(parents=True, exist_ok=True)
    copied = input_dir / "source.dwg"
    shutil.copyfile(source, copied)

    cmd = [str(oda), str(input_dir), str(output_dir), "ACAD2018", "DXF", "0", "0"]
    result = subprocess.run(cmd, text=True, capture_output=True)
    if result.returncode != 0:
        raise RuntimeError(
            "ODA File Converter failed.\n"
            f"stdout:\n{result.stdout}\n"
            f"stderr:\n{result.stderr}"
        )

    dxf = output_dir / "source.dxf"
    if not dxf.exists() or dxf.stat().st_size == 0:
        raise RuntimeError("ODA File Converter did not produce a DXF output.")
    return dxf


def render_dxf_to_pdf(dxf: Path, output: Path, preview: Path, paper: str, dpi: int) -> dict:
    try:
        import ezdxf
        import fitz
        import matplotlib.pyplot as plt
        from ezdxf.addons.drawing import matplotlib
        from ezdxf.addons.drawing.config import BackgroundPolicy, ColorPolicy, Configuration
        from ezdxf.addons.drawing.frontend import Frontend
        from ezdxf.addons.drawing.properties import RenderContext
    except ModuleNotFoundError as exc:
        raise RuntimeError(
            "Missing Python dependency. Install with: python -m pip install ezdxf matplotlib pymupdf"
        ) from exc

    width, height = PAPER_SIZES[paper]
    doc = ezdxf.readfile(dxf)
    modelspace = doc.modelspace()

    fig = plt.figure(figsize=(width, height), dpi=dpi)
    ax = fig.add_axes([0.02, 0.02, 0.96, 0.96])
    ax.set_aspect("equal")
    ax.axis("off")

    context = RenderContext(doc)
    backend = matplotlib.MatplotlibBackend(ax)
    config = Configuration.defaults().with_changes(
        color_policy=ColorPolicy.BLACK,
        background_policy=BackgroundPolicy.WHITE,
    )
    Frontend(context, backend, config=config).draw_layout(modelspace, finalize=True)
    ax.autoscale()
    ax.margins(0.03)

    output.parent.mkdir(parents=True, exist_ok=True)
    preview.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="dwg-pdf-") as tmp:
        temp_pdf = Path(tmp) / "drawing.pdf"
        fig.savefig(temp_pdf, format="pdf", bbox_inches="tight", pad_inches=0.15, facecolor="white")
        plt.close(fig)
        shutil.copyfile(temp_pdf, output)

    pdf = fitz.open(output)
    if pdf.page_count < 1:
        raise RuntimeError("Generated PDF has no pages.")
    page = pdf[0]
    pixmap = page.get_pixmap(matrix=fitz.Matrix(0.5, 0.5), alpha=False)
    pixmap.save(preview)

    return {
        "output": str(output),
        "bytes": output.stat().st_size,
        "pages": pdf.page_count,
        "preview": str(preview),
        "paper": paper,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Convert DWG/DXF to PDF and verify the result.")
    parser.add_argument("--input", required=True, help="Input .dwg or .dxf file")
    parser.add_argument("--output", help="Output .pdf path; defaults beside the input")
    parser.add_argument("--preview", help="Preview PNG path; defaults beside the output")
    parser.add_argument("--paper", choices=sorted(PAPER_SIZES), default="a3-landscape")
    parser.add_argument("--dpi", type=int, default=300)
    args = parser.parse_args()

    source = Path(args.input).resolve()
    if not source.exists():
        raise FileNotFoundError(source)
    if source.suffix.lower() not in {".dwg", ".dxf"}:
        raise ValueError("Input must be a .dwg or .dxf file.")

    output = Path(args.output).resolve() if args.output else source.with_suffix(".pdf")
    preview = Path(args.preview).resolve() if args.preview else output.with_suffix(".preview.png")

    with tempfile.TemporaryDirectory(prefix="dwg-to-pdf-") as tmp:
        work_dir = Path(tmp)
        dxf = source if source.suffix.lower() == ".dxf" else convert_dwg_to_dxf(source, work_dir)
        result = render_dxf_to_pdf(dxf, output, preview, args.paper, args.dpi)

    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"error: {exc}", file=sys.stderr)
        raise SystemExit(1)
