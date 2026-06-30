#!/usr/bin/env python3
"""Smoke tests for scripts/pptx_inspect.py using a minimal synthetic .pptx zip."""
from __future__ import annotations

import importlib.util
import json
import tempfile
import zipfile
from pathlib import Path


def load_module(path: Path):
    spec = importlib.util.spec_from_file_location("pptx_inspect", path)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def write_minimal_pptx(path: Path) -> None:
    slide_xml = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<p:sld xmlns:p="http://schemas.openxmlformats.org/presentationml/2006/main"
       xmlns:a="http://schemas.openxmlformats.org/drawingml/2006/main">
  <p:cSld>
    <p:spTree>
      <p:sp>
        <p:nvSpPr><p:cNvPr id="2" name="Title 1"/></p:nvSpPr>
        <p:txBody><a:p><a:r><a:t>Quarterly Results</a:t></a:r></a:p></p:txBody>
      </p:sp>
      <p:pic>
        <p:nvPicPr><p:cNvPr id="3" name="Picture 1" descr="Revenue trend chart"/></p:nvPicPr>
      </p:pic>
    </p:spTree>
  </p:cSld>
</p:sld>"""
    core_xml = """<?xml version='1.0' encoding='UTF-8' standalone='yes'?>
<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties"
 xmlns:dc="http://purl.org/dc/elements/1.1/">
 <dc:title>Sample Deck</dc:title><dc:creator>Test</dc:creator>
</cp:coreProperties>"""
    with zipfile.ZipFile(path, "w") as zf:
        zf.writestr("ppt/slides/slide1.xml", slide_xml)
        zf.writestr("ppt/media/image1.png", b"not-really-png")
        zf.writestr("ppt/slideLayouts/slideLayout1.xml", "<xml/>")
        zf.writestr("ppt/slideMasters/slideMaster1.xml", "<xml/>")
        zf.writestr("docProps/core.xml", core_xml)


def test_inspection() -> None:
    script_path = Path(__file__).resolve().parents[1] / "scripts" / "pptx_inspect.py"
    module = load_module(script_path)
    with tempfile.TemporaryDirectory() as tmp:
        pptx_path = Path(tmp) / "sample.pptx"
        write_minimal_pptx(pptx_path)
        report = module.inspect_pptx(pptx_path)
        assert report["slide_count"] == 1
        assert report["media_count"] == 1
        assert report["slides"][0]["title_guess"] == "Quarterly Results"
        assert report["slides"][0]["picture_count"] == 1
        assert "Sample Deck" == report["core_properties"]["title"]
        assert "Slides with images" in " ".join(report["warnings"])
        json.dumps(report)
        markdown = module.to_markdown(report)
        assert "PPTX Inspection Report" in markdown


if __name__ == "__main__":
    test_inspection()
    print("pptx_inspect smoke test passed")
