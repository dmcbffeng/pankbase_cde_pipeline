# PanKbase Metadata CDE Pipeline

Common Data Elements (CDEs) and a harmonization pipeline for pancreas research metadata. Part of the [PanKbase](https://pankbase.org/) Pancreas Knowledgebase project.

Currently ships two CDE collections:

1. **PanKbase Donor Metadata CDEs (v1.0)** — 34 CDEs for pancreas donor demographics, medical history, autoantibodies, isolation, and transportation.
2. **PanKbase scRNA-seq Metadata CDEs (v0.1)** — 20 CDEs for single-cell RNA-seq sample-level experiment and QC metadata (library chemistry, per-sample UMI/gene/read metrics, CellBender ambient-RNA QC, mitochondrial QC). Links back to donor CDEs via a `donor_rrid_ref` foreign-key CDE rather than duplicating donor fields.

## Features

- **54 formal CDEs** across both collections, in NIH CDE format (ISO/IEC 11179-aligned) with permissible values, UCUM units, and terminology bindings (MONDO, LOINC, NCIt, EFO)
- **Deterministic harmonization pipeline** — converts raw consortia Excel (`.xlsx`) or R (`.rds`) metadata files to clean, CDE-matched TSVs
- **Per-consortium / per-dataset mapping configs** — add new consortia or new assay types by writing a JSON mapping (no code changes)
- **Cross-collection linking** — scRNA-seq samples join to donor records via `donor_rrid_ref` (PKB_S_002 → PKB_D_001), avoiding duplicated donor fields
- **Automated validation** — field completeness report and per-record warnings for out-of-range or non-permissible values
- **Claude Code skills** — `/generate-mapping` and `/harmonize-data` slash commands for LLM-assisted one-click harmonization of new data sources

## Installation

```bash
git clone https://github.com/dmcbffeng/pankbase_cde_pipeline.git
cd pankbase_cde_pipeline
pip install -r requirements.txt
```

Requirements: Python 3.7+, `openpyxl` (required), `pyreadr` (required only for `.rds` input).

## Quick Start

### Donor metadata (HPAP example)

Harmonize the HPAP donor summary (197 donors) to the donor CDE schema:

```bash
python3 task2_cde_pipeline/pipeline.py \
    --data data/HPAP_Donor_Summary_197.xlsx \
    --mapping task2_cde_pipeline/mappings/hpap_mapping.json \
    --cde task1_cde_definitions/pankbase_donor_cdes.json \
    --output task2_cde_pipeline/output/hpap_cde_harmonized.tsv
```

Output:
```
[Pipeline] Consortium / dataset: HPAP
[Pipeline] CDE schema: PanKbase Donor Metadata CDEs
[Pipeline] Data format: hpap_excel
[Pipeline] Loaded 197 source records
[Pipeline] Harmonized 197 records
[Pipeline] Validation warnings: 1115
[Pipeline] Output written to: task2_cde_pipeline/output/hpap_cde_harmonized.tsv
```

First few rows:

| donor_rrid | program_donor_id | cohort_id | sex_at_birth | age_years | bmi | diabetes_status | hba1c_percent |
|---|---|---|---|---|---|---|---|
| RRID:SAMN18741978 | HPAP-001 | HPAP | Male | 47 | 32.2 | Type 2 diabetes (T2D) | 5.7 |
| RRID:SAMN19763626 | HPAP-002 | HPAP | Male | 26 | 16.4 | Type 1 diabetes (T1D) | 9.8 |
| RRID:SAMN18741941 | HPAP-003 | HPAP | Male | 29 | 24.5 | No diabetes | 5.6 |
| RRID:SAMN19776437 | HPAP-004 | HPAP | Female | 24 | 32.2 | No diabetes | 5.4 |

### scRNA-seq sample metadata (reference RDS)

Harmonize the reference PanKbase scRNA-seq RDS (227 samples) to the scRNA-seq CDE schema:

```bash
python3 task2_cde_pipeline/pipeline.py \
    --data data/metadata_for_DEG.rds \
    --mapping task2_cde_pipeline/mappings/pankbase_scrnaseq_mapping.json \
    --cde task1_cde_definitions/pankbase_scrnaseq_cdes.json \
    --output task2_cde_pipeline/output/scrnaseq_cde_harmonized.tsv
```

Output:
```
[Pipeline] Consortium / dataset: PanKbase-scRNAseq
[Pipeline] CDE schema: PanKbase scRNA-seq Metadata CDEs
[Pipeline] Data format: rds
[Pipeline] Loaded 227 source records
[Pipeline] Harmonized 227 records
[Pipeline] Validation warnings: 0
```

First few rows:

| sample_id | donor_rrid_ref | study_accession | library_chemistry | mean_umi_count_per_cell | mean_genes_per_cell | mean_pct_mitochondrial_reads |
|---|---|---|---|---|---|---|
| HP-21070-01__DHT_10nM | HP-21070-01 | GSE201256 | V3 | 25005.05 | 4801.12 | 4.62 |
| HP-21070-01__EtOH | HP-21070-01 | GSE201256 | V3 | 28827.58 | 5470.32 | 7.54 |

To build a fully-annotated sample table, join scRNA-seq output to the donor output on `donor_rrid_ref == donor_rrid`.

## Pipeline Workflow

```
Raw metadata file  ─────┐
  .xlsx (donor)         │
  .rds  (scRNA-seq)    │    CDE schema (JSON) ──┐
                        ├──► pipeline.py ───────┼──► Harmonized TSV
Mapping JSON ───────────┘                       └──► Validation report
(consortium / dataset-specific)
```

Steps:
1. **Load** the source file. The loader is chosen by the mapping's `data_format` (`hpap_excel`, `iidp_excel`, `rds`) or the file extension. Excel paths use `openpyxl`; `.rds` uses `pyreadr`.
2. **Map** each source column to a CDE field via the mapping JSON (transforms: `direct`, `value_map`, `numeric`, `timedelta_to_hours`, `parse_value_cutoff`, `lookup_sheet`, etc.)
3. **Validate** each record against the `--cde` schema (required fields, permissible values, ranges, patterns)
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
pankbase_cde_pipeline/
├── README.md                                      # This file
├── LICENSE                                        # MIT License
├── requirements.txt                               # Python dependencies
├── .gitignore
├── data/                                          # Example data
│   ├── HPAP_Donor_Summary_197.xlsx                # 197 HPAP donors
│   └── metadata_for_DEG.rds                       # 227 scRNA-seq samples
├── task1_cde_definitions/                         # Task 1: Formal CDE definitions
│   ├── pankbase_donor_cdes.md                     # 34 donor CDEs (human-readable)
│   ├── pankbase_donor_cdes.json                   # 34 donor CDEs (machine-readable)
│   ├── pankbase_scrnaseq_cdes.md                  # 20 scRNA-seq CDEs (human-readable)
│   └── pankbase_scrnaseq_cdes.json                # 20 scRNA-seq CDEs (machine-readable)
├── task2_cde_pipeline/                            # Task 2: Harmonization pipeline
│   ├── README.md                                  # Pipeline documentation
│   ├── pipeline.py                                # Main script (Excel + RDS)
│   ├── mappings/
│   │   ├── hpap_mapping.json                      # HPAP donor → donor CDE
│   │   └── pankbase_scrnaseq_mapping.json         # RDS → scRNA-seq CDE
│   ├── tests/
│   │   └── test_pipeline.py
│   └── output/                                    # Harmonized TSVs + validation reports
└── .claude/
    └── skills/                                    # Claude Code slash commands
        ├── generate-mapping/
        │   └── SKILL.md
        └── harmonize-data/
            └── SKILL.md
```

## CDE Categories

### Donor CDE Collection — 34 CDEs (v1.0)

| Category | Count | Key Fields |
|---|---|---|
| Donor Identification | 3 | RRID, Program Donor ID, Cohort ID |
| Demographics | 5 | Sex at Birth, Age, BMI, Ethnicity, Race |
| Medical | 10 | Diabetes Status, HbA1c, C-Peptide, Cause of Death, ... |
| Autoantibodies | 8 | GADA, IAA, IA-2, ZnT8 (positive + value) |
| Pancreas Processing | 9 | Cold/Warm Ischemia, Pancreas Weight, Islet Viability/Purity |
| Sample Transportation | 3 | Post-Shipment Viability/Purity, Total Culture Time |

Full definitions in [task1_cde_definitions/pankbase_donor_cdes.md](task1_cde_definitions/pankbase_donor_cdes.md).

### scRNA-seq CDE Collection — 20 CDEs (v0.1)

| Category | Count | Key Fields |
|---|---|---|
| Sample Identification | 3 | `sample_id`, `donor_rrid_ref` (FK → PKB_D_001), `study_accession` |
| Library & Platform | 6 | `library_chemistry`, `library_prep_kit`*, `sequencing_platform`*, `alignment_tool`*, `reference_genome`*, `cellranger_version`* |
| Cell Calling | 1 | `n_cells`* |
| Sequencing QC | 6 | mean per-cell UMI, genes, total reads, uniquely mapped, secondary / supplementary alignments |
| Ambient RNA (CellBender) | 3 | mean cell probability, post-CellBender UMIs, % UMIs removed |
| Mitochondrial QC | 1 | mean % mitochondrial reads |

`*` = inferred (not in the reference RDS; commonly-expected scRNA-seq metadata).

Full definitions in [task1_cde_definitions/pankbase_scrnaseq_cdes.md](task1_cde_definitions/pankbase_scrnaseq_cdes.md).

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

> PanKbase Metadata CDE Pipeline (2026). https://github.com/dmcbffeng/pankbase_cde_pipeline
