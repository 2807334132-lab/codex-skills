---
name: dwg-to-pdf
description: Convert AutoCAD DWG or DXF drawing files into PDF files on Windows using local tools, with rendered-output verification. Use when Codex is asked to convert `.dwg` or `.dxf` files to PDF, export CAD drawings, make a printable floor plan PDF, or verify that a converted CAD PDF is not blank or badly cropped.
---

# DWG To PDF

## Overview

Use this skill to convert CAD drawings into PDF files without uploading the drawing to a web service. Prefer the bundled script because DWG conversion has several brittle details on Windows: ODA command-line argument order, CAD library dependencies, and non-ASCII output paths.

## Workflow

1. Confirm the source file exists and identify whether it is `.dwg` or `.dxf`.
2. Choose an output path. If the user did not specify one, save `<source-stem>.pdf` beside the source file.
3. Run `scripts/convert_dwg_to_pdf.py` with absolute paths:

```powershell
python scripts/convert_dwg_to_pdf.py --input "D:\path\plan.dwg" --output "D:\path\plan.pdf"
```

4. Verify the result in the script output:
   - `pages` must be at least 1.
   - `bytes` must be greater than 0.
   - `preview` should point to a rendered PNG of page 1.
5. Open the PDF for the user when they asked to "open" it or when opening is clearly useful.

## Tooling

The script supports:

- `.dwg`: convert to DXF with ODA File Converter, then render to PDF.
- `.dxf`: render directly to PDF.

If ODA File Converter is missing, install it with Windows Package Manager when allowed:

```powershell
winget install --id ODA.ODAFileConverter -e --accept-source-agreements --accept-package-agreements --disable-interactivity
```

The script requires Python packages `ezdxf`, `matplotlib`, and `pymupdf`. If they are missing and package installation is allowed, install them:

```powershell
python -m pip install ezdxf matplotlib pymupdf
```

## Quality Checks

Always check that the generated PDF renders. A non-empty PDF can still be wrong if the drawing was not visible, the page was badly cropped, or text/fonts failed.

Use the generated preview PNG for a quick visual check. If it is blank or heavily cropped:

- rerun with a larger paper size, for example `--paper a2-landscape`;
- try direct ODA viewer/manual print if the drawing uses layouts or features that `ezdxf` cannot render well;
- tell the user if the output may not preserve every CAD feature exactly.

## Notes

- Do not modify the original DWG. Work from a copied intermediate folder when converting.
- Avoid web converters unless the user explicitly approves uploading the drawing.
- When saving to Chinese or other non-ASCII paths, let the script write to an ASCII temporary PDF first and copy it to the requested output path.
- Use absolute file paths in final responses.
