# PanKbase Donor Metadata CDE Pipeline

Common Data Elements (CDEs) and a harmonization pipeline for pancreas donor metadata. Part of the [PanKbase](https://pankbase.org/) Pancreas Knowledgebase project.

## Features

- **34 formal CDEs** for pancreas donor metadata, covering demographics, medical history, autoantibodies, pancreas processing, and sample transportation
- **NIH CDE-format definitions** (ISO/IEC 11179-aligned) with permissible values, UCUM units, and terminology bindings (MONDO, LOINC, NCIt)
- **Deterministic harmonization pipeline** — converts raw consortia Excel files to clean, CDE-matched TSVs
- **Per-consortium mapping configs** — add new consortia by writing a JSON mapping (no code changes)
- **Automated validation** — field completeness report and per-record warnings for out-of-range or non-permissible values
- **Claude Code skills** — `/generate-mapping` and `/harmonize-data` slash commands for LLM-assisted one-click harmonization of new data sources

## Installation

```bash
git clone https://github.com/<your-org>/pankbase-cde-pipeline.git
cd pankbase-cde-pipeline
pip install openpyxl
```

Requirements: Python 3.7+, openpyxl.

## Quick Start (HPAP Example)

Harmonize the HPAP donor summary (197 donors) to PanKbase CDEs:

```bash
python3 task2_cde_pipeline/pipeline.py \
    --data data/HPAP_Donor_Summary_197.xlsx \
    --mapping task2_cde_pipeline/mappings/hpap_mapping.json \
    --cde task1_cde_definitions/pankbase_donor_cdes.json \
    --output task2_cde_pipeline/output/hpap_cde_harmonized.tsv
```

Output:
```
[Pipeline] Consortium: HPAP
[Pipeline] Loading data from: data/HPAP_Donor_Summary_197.xlsx
[Pipeline] Loaded 197 source records
[Pipeline] Harmonized 197 records
[Pipeline] Validation warnings: 1115
[Pipeline] Output written to: task2_cde_pipeline/output/hpap_cde_harmonized.tsv
[Pipeline] Validation report written to: task2_cde_pipeline/output/hpap_cde_harmonized.validation_report.txt
```

First few rows of the harmonized output:

| donor_rrid | program_donor_id | cohort_id | sex_at_birth | age_years | bmi | diabetes_status | hba1c_percent |
|---|---|---|---|---|---|---|---|
| RRID:SAMN18741978 | HPAP-001 | HPAP | Male | 47 | 32.2 | Type 2 diabetes (T2D) | 5.7 |
| RRID:SAMN19763626 | HPAP-002 | HPAP | Male | 26 | 16.4 | Type 1 diabetes (T1D) | 9.8 |
| RRID:SAMN18741941 | HPAP-003 | HPAP | Male | 29 | 24.5 | No diabetes | 5.6 |
| RRID:SAMN19776437 | HPAP-004 | HPAP | Female | 24 | 32.2 | No diabetes | 5.4 |

## Pipeline Workflow

```
Raw consortia Excel  ──┐
                       │
CDE schema (JSON) ─────┼──► pipeline.py ──► Harmonized TSV
                       │                    + validation report
Mapping JSON ──────────┘
(consortium-specific)
```

Steps:
1. **Load** the source Excel (handling named columns, positional columns, multi-row headers)
2. **Map** each source column to a CDE field via the mapping JSON (transforms: `direct`, `value_map`, `numeric`, `timedelta_to_hours`, `parse_value_cutoff`, `lookup_sheet`, etc.)
3. **Validate** each record against the CDE schema (required fields, permissible values, ranges, patterns)
4. **Emit** a CDE-matched TSV + validation report

## Adding a New Consortium

### Option A: Manual mapping (deterministic)

Create `task2_cde_pipeline/mappings/<consortium>_mapping.json` using `hpap_mapping.json` or `iidp_mapping.json` as a template. Each CDE field specifies:

```json
{
  "cde_field_name": {
    "source_column": "source_col_name",
    "transform": "value_map",
    "value_map": { "source_val": "cde_val" },
    "default": "Unknown"
  }
}
```

Then run the pipeline with your new mapping.

### Option B: LLM-assisted (Claude Code skills)

If you have Claude Code installed, one-click harmonization:

```
/harmonize-data path/to/new_data.xlsx MY_CONSORTIUM
```

Claude will inspect the Excel, match columns to CDEs, generate the mapping JSON, run the pipeline, and report results. The mapping is saved as a reviewable JSON artifact — once approved, future data from the same consortium runs deterministically without LLM involvement.

To only generate the mapping (without running):

```
/generate-mapping path/to/new_data.xlsx MY_CONSORTIUM
```

## Project Structure

```
pankbase-cde-pipeline/
├── README.md                              # This file
├── CLAUDE.md                              # Project context for Claude Code
├── LICENSE                                # MIT License
├── .gitignore
├── cde-deep-research-report.md            # Background research on CDE ecosystem
├── PANKBASE META DATA_MB.xlsx             # Collaborator-selected metadata fields
├── data/                                  # Example consortia data
│   └── HPAP_Donor_Summary_197.xlsx        # 197 HPAP donors
├── task1_cde_definitions/                 # Task 1: Formal CDE definitions
│   ├── pankbase_donor_cdes.md             # Human-readable CDE collection (34 CDEs)
│   └── pankbase_donor_cdes.json           # Machine-readable CDE schema
├── task2_cde_pipeline/                    # Task 2: Harmonization pipeline
│   ├── README.md                          # Pipeline documentation
│   ├── pipeline.py                        # Main script
│   ├── mappings/
│   │   └── hpap_mapping.json              # HPAP column-to-CDE mapping
│   └── output/                            # Harmonized TSVs + validation reports
└── .claude/
    └── skills/                            # Claude Code slash commands
        ├── generate-mapping/
        │   └── SKILL.md
        └── harmonize-data/
            └── SKILL.md
```

## CDE Categories (34 total)

| Category | Count | Key Fields |
|---|---|---|
| Donor Identification | 3 | RRID, Program Donor ID, Cohort ID |
| Demographics | 5 | Sex at Birth, Age, BMI, Ethnicity, Race |
| Medical | 10 | Diabetes Status, HbA1c, C-Peptide, Cause of Death, ... |
| Autoantibodies | 8 | GADA, IAA, IA-2, ZnT8 (positive + value) |
| Pancreas Processing | 9 | Cold/Warm Ischemia, Pancreas Weight, Islet Viability/Purity |
| Sample Transportation | 3 | Post-Shipment Viability/Purity, Total Culture Time |

Full definitions in [task1_cde_definitions/pankbase_donor_cdes.md](task1_cde_definitions/pankbase_donor_cdes.md).

## Validation Report (HPAP example)

```
Field Completeness:
  donor_rrid: 195/197 (99.0%)
  sex_at_birth: 197/197 (100.0%)
  age_years: 197/197 (100.0%)
  bmi: 197/197 (100.0%)
  diabetes_status: 197/197 (100.0%)
  hba1c_percent: 190/197 (96.4%)
  cold_ischemia_time_hours: 181/197 (91.9%)
  aab_gada_positive: 197/197 (100.0%)
  ...
```

Fields flagged as `0.0%` are not available in the source data — this is expected when a consortium does not collect that variable.

## Data Sources

- [NIH CDE Repository](https://cde.nlm.nih.gov/) — Reference for existing CDE definitions
- [NCI caDSR II](https://cadsr.cancer.gov/) — ISO/IEC 11179 metadata registry
- [PanKbase Human Donor Standards](https://data.pankbase.org/standards/human-donor/) — Reference schema
- [HPAP](https://hpap.pmacs.upenn.edu/) — Human Pancreas Analysis Program
- [IIDP](https://iidp.coh.org/) — Integrated Islet Distribution Program (mapping config available on request)

## Conventions

- CDE definitions follow NIH CDE Repository format (ISO/IEC 11179-aligned)
- Units follow UCUM standard
- Terminology bindings: MONDO (disease), LOINC (lab tests), NCIt (cancer concepts), UCUM (units)
- Version dependencies are tracked explicitly

## Contributing

1. Fork and clone
2. For new consortia: add a mapping JSON in `task2_cde_pipeline/mappings/` and place sample data in `data/`
3. For CDE changes: update both `pankbase_donor_cdes.md` and `pankbase_donor_cdes.json`, bump the schema version
4. Open a pull request

## License

MIT License — see [LICENSE](LICENSE).

## Citation

If you use this pipeline, please cite:

> PanKbase Donor Metadata CDE Pipeline (2026). https://github.com/<your-org>/pankbase-cde-pipeline
