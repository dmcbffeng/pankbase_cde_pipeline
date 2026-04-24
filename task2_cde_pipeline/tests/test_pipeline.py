"""Smoke tests for the PanKbase CDE harmonization pipeline."""
import json
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[2]
PIPELINE = ROOT / "task2_cde_pipeline" / "pipeline.py"
CDE = ROOT / "task1_cde_definitions" / "pankbase_donor_cdes.json"
SCRNA_CDE = ROOT / "task1_cde_definitions" / "pankbase_scrnaseq_cdes.json"
HPAP_DATA = ROOT / "data" / "HPAP_Donor_Summary_197.xlsx"
IIDP_DATA = ROOT / "data" / "IIDP_HIPP_Report.xlsx"
SCRNA_DATA = ROOT / "data" / "metadata_for_DEG.rds"
HPAP_MAP = ROOT / "task2_cde_pipeline" / "mappings" / "hpap_mapping.json"
IIDP_MAP = ROOT / "task2_cde_pipeline" / "mappings" / "iidp_mapping.json"
SCRNA_MAP = ROOT / "task2_cde_pipeline" / "mappings" / "pankbase_scrnaseq_mapping.json"


def run_pipeline(data, mapping, output, cde=None):
    result = subprocess.run(
        [
            sys.executable, str(PIPELINE),
            "--data", str(data),
            "--mapping", str(mapping),
            "--cde", str(cde or CDE),
            "--output", str(output),
        ],
        capture_output=True, text=True,
    )
    assert result.returncode == 0, f"Pipeline failed: {result.stderr}"
    return result.stdout


def test_cde_schema_loads():
    with open(CDE) as f:
        schema = json.load(f)
    assert schema["schema_version"] == "1.0"
    assert len(schema["cdes"]) >= 34, "Expected at least 34 CDEs"
    required_names = {"donor_rrid", "sex_at_birth", "age_years", "bmi", "diabetes_status"}
    names = {c["cde_name"] for c in schema["cdes"]}
    assert required_names.issubset(names)


def test_hpap_harmonization(tmp_path):
    output = tmp_path / "hpap.tsv"
    stdout = run_pipeline(HPAP_DATA, HPAP_MAP, output)
    assert output.exists()
    text = output.read_text()
    # Count header + data rows (may contain embedded newlines in free-text fields)
    assert "donor_rrid" in text.split("\n")[0]
    assert "diabetes_status" in text.split("\n")[0]
    assert "Loaded 197 source records" in stdout
    assert "Harmonized 197 records" in stdout


@pytest.mark.skipif(
    not IIDP_DATA.exists() or not IIDP_MAP.exists(),
    reason="IIDP data/mapping not present (not publicly available)",
)
def test_iidp_harmonization(tmp_path):
    output = tmp_path / "iidp.tsv"
    stdout = run_pipeline(IIDP_DATA, IIDP_MAP, output)
    assert output.exists()
    lines = output.read_text().strip().split("\n")
    assert len(lines) >= 500
    assert "Harmonized" in stdout


@pytest.mark.skipif(
    not SCRNA_DATA.exists() or not SCRNA_MAP.exists(),
    reason="scRNA-seq RDS / mapping not present",
)
def test_scrnaseq_schema_loads():
    with open(SCRNA_CDE) as f:
        schema = json.load(f)
    assert schema["schema_name"] == "PanKbase scRNA-seq Metadata CDEs"
    names = {c["cde_name"] for c in schema["cdes"]}
    assert {
        "sample_id",
        "donor_rrid_ref",
        "study_accession",
        "library_chemistry",
        "mean_umi_count_per_cell",
    }.issubset(names)
    # donor_rrid_ref carries a cross_reference block
    cross = next(c for c in schema["cdes"] if c["cde_name"] == "donor_rrid_ref")
    assert cross["cross_reference"]["cde_id"] == "PKB_D_001"


@pytest.mark.skipif(
    not SCRNA_DATA.exists() or not SCRNA_MAP.exists(),
    reason="scRNA-seq RDS / mapping not present",
)
def test_scrnaseq_harmonization(tmp_path):
    try:
        import pyreadr  # noqa: F401
    except ImportError:
        pytest.skip("pyreadr not installed")
    output = tmp_path / "scrnaseq.tsv"
    stdout = run_pipeline(SCRNA_DATA, SCRNA_MAP, output, cde=SCRNA_CDE)
    assert output.exists()
    text = output.read_text()
    header = text.split("\n")[0].split("\t")
    assert "sample_id" in header
    assert "donor_rrid_ref" in header
    assert "mean_umi_count_per_cell" in header
    assert "Loaded 227 source records" in stdout
    assert "Harmonized 227 records" in stdout


def test_value_maps_applied(tmp_path):
    output = tmp_path / "hpap.tsv"
    run_pipeline(HPAP_DATA, HPAP_MAP, output)
    content = output.read_text()
    # HPAP uses "T1DM" but the CDE value is "Type 1 diabetes (T1D)"
    assert "Type 1 diabetes (T1D)" in content
    assert "T1DM\t" not in content  # Should have been mapped
