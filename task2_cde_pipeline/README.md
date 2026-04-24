# PanKbase CDE Harmonization Pipeline

## Overview

This pipeline takes raw metadata from any research consortium (e.g., HPAP, IIDP) or assay type (donor-level spreadsheets, scRNA-seq sample metadata RDS) and transforms it into a standardized table that matches a PanKbase Common Data Element (CDE) schema. The same `pipeline.py` drives both the donor and scRNA-seq flows — the input format and target CDE schema are picked from the mapping JSON and the `--cde` argument.

## Architecture

```
Input                               Config                        Output
─────                               ──────                        ──────
Raw metadata file  ──────┐
  .xlsx (donor)          │    CDE Schema JSON ──┐
  .rds  (scRNA-seq)      ├──► pipeline.py ──────┼──► Harmonized TSV
Mapping config ──────────┘                      └──► Validation Report
(JSON file)
```

## Quick Start

### Donor metadata (HPAP example)

```bash
python pipeline.py \
    --data ../data/HPAP_Donor_Summary_197.xlsx \
    --mapping mappings/hpap_mapping.json \
    --cde ../task1_cde_definitions/pankbase_donor_cdes.json \
    --output output/hpap_cde_harmonized.tsv
```

### scRNA-seq sample metadata (PanKbase reference RDS)

```bash
python pipeline.py \
    --data ../data/metadata_for_DEG.rds \
    --mapping mappings/pankbase_scrnaseq_mapping.json \
    --cde ../task1_cde_definitions/pankbase_scrnaseq_cdes.json \
    --output output/scrnaseq_cde_harmonized.tsv
```

## Requirements

- Python 3.7+
- `openpyxl` (required for Excel input)
- `pyreadr` (required for `.rds` input only — omit if you never load RDS)

```bash
pip install -r ../requirements.txt
```

## How It Works

### 1. Load source data

The pipeline auto-selects a loader based on the mapping's `data_format` field (or, if missing, the file extension and consortium tag):

| `data_format` | Loader | Used for |
|---|---|---|
| `hpap_excel` | `openpyxl` with named-column headers | HPAP donor spreadsheets |
| `iidp_excel` | `openpyxl` with positional headers + header row offset | IIDP donor spreadsheets |
| `rds` | `pyreadr` (first / named `data.frame` in the RDS) | scRNA-seq sample metadata, any other R-side tabular export |

### 2. Apply column mappings
Each CDE field is mapped from source columns using a transform function:

| Transform | Description |
|-----------|-------------|
| `direct` | Pass through as-is |
| `constant` | Fixed value (e.g., cohort_id = "HPAP") |
| `numeric` | Convert to float, handling edge cases |
| `value_map` | Map source values to CDE permissible values |
| `binary_to_pos_neg` | Convert 0/1 to Negative/Positive |
| `parse_value_cutoff` | Extract value from "value/cutoff" format |
| `timedelta_to_hours` | Convert "X days HH:MM:SS" to decimal hours |
| `minutes_to_hours` | Convert minutes to hours |
| `parse_duration_years` | Extract years from "18 years" text |
| `derive_hba1c_status` | Classify HbA1c into Normal/Prediabetes/Diabetes |
| `derive_ethnicity_from_race` | Infer ethnicity from combined race/ethnicity fields |
| `derive_donation_type` | Derive DBD/DCD from boolean fields |
| `datetime_diff_days` | Calculate days between two datetimes |
| `presence_to_yes_no` | Convert presence of value to Yes/No |
| `lookup_sheet` | Look up data from auxiliary Excel sheets |
| `not_available` | Field not available in this source |

### 3. Validate
Each harmonized record is validated against the CDE schema:
- Required field presence
- Permissible value compliance
- Numeric range checks
- Pattern matching (e.g., RRID format)

### 4. Output
- **TSV file**: Clean, tab-separated table with one row per donor and one column per CDE field
- **Validation report**: Field completeness statistics and per-record warnings

## Adding a New Consortium

To add support for a new data source:

1. **Create a mapping JSON** in `mappings/` (use `hpap_mapping.json` as a template)
2. **Define column_mappings** for each CDE field, specifying:
   - `source_column`: Column name or index in the source data
   - `transform`: Which transform function to apply
   - `value_map`: For value_map transforms, the source-to-CDE value lookup
3. **Run the pipeline** with your new mapping
4. **Review the validation report** to identify data quality issues

### Mapping JSON structure

```json
{
  "consortium": "NEW_CONSORTIUM",
  "data_format": "hpap_excel",
  "source_sheet": "Sheet1",
  "record_id_column": "donor_id",
  "column_mappings": {
    "cde_field_name": {
      "source_column": "source_column_name",
      "transform": "transform_function",
      "value_map": { "source_val": "cde_val" },
      "default": "Unknown"
    }
  }
}
```

Recognized top-level keys:

| Key | Required | Description |
|---|---|---|
| `consortium` | yes | Short identifier shown in pipeline logs and validation reports |
| `data_format` | recommended | `hpap_excel`, `iidp_excel`, or `rds`; inferred from file extension if omitted |
| `source_sheet` | for Excel | Sheet name containing the records |
| `header_row` / `data_start_row` | for `iidp_excel` | 1-indexed row numbers for headers and first data row |
| `rds_object_name` | for `rds` | Optional — name of the R object to read if the RDS contains multiple; otherwise the first `data.frame` is used |
| `record_id_column` | recommended | Column (name or index) that uniquely identifies each record; used for lookup joins and in validation-report labels (alias: `donor_id_column`) |
| `column_mappings` | yes | Map of CDE field name → transform spec |

## Output Format

The output TSV has one row per source record and one column per CDE in the supplied `--cde` schema.

### Donor schema (`pankbase_donor_cdes.json`) — 34 columns

| Column | Category | Type |
|--------|----------|------|
| donor_rrid | Identification | Text |
| program_donor_id | Identification | Text |
| cohort_id | Identification | Value List |
| sex_at_birth | Demographics | Value List |
| age_years | Demographics | Number |
| bmi | Demographics | Number |
| ethnicity | Demographics | Value List |
| race | Demographics | Value List |
| diabetes_status | Medical | Value List |
| hba1c_percent | Medical | Number |
| hba1c_adjusted_diabetes_status | Medical | Value List |
| glucose_lowering_therapy | Medical | Text |
| other_disease_states | Medical | Text |
| family_history_diabetes | Medical | Value List |
| hospital_stay_days | Medical | Number |
| donation_type | Medical | Value List |
| cause_of_death | Medical | Value List |
| diabetes_duration_years | Medical | Number |
| c_peptide_ng_ml | Medical | Number |
| aab_gada_positive | Autoantibodies | Value List |
| aab_gada_value | Autoantibodies | Number |
| aab_iaa_positive | Autoantibodies | Value List |
| aab_iaa_value | Autoantibodies | Number |
| aab_ia2_positive | Autoantibodies | Value List |
| aab_ia2_value | Autoantibodies | Number |
| aab_znt8_positive | Autoantibodies | Value List |
| aab_znt8_value | Autoantibodies | Number |
| isolation_center | Processing | Text |
| cold_ischemia_time_hours | Processing | Number |
| warm_ischemia_time_hours | Processing | Number |
| organ_source | Processing | Text |
| pancreas_weight_g | Processing | Number |
| islet_viability_pre_percent | Processing | Number |
| islet_purity_pre_percent | Processing | Number |
| pre_shipment_culture_time_hours | Processing | Number |
| pre_shipment_islet_function_available | Processing | Value List |
| islet_viability_post_percent | Transportation | Number |
| islet_purity_post_percent | Transportation | Number |
| total_culture_time_hours | Transportation | Number |

### scRNA-seq schema (`pankbase_scrnaseq_cdes.json`) — 20 columns

| Column | Category | Type |
|--------|----------|------|
| sample_id | Sample Identification | Text |
| donor_rrid_ref | Sample Identification (FK → donor PKB_D_001) | Text |
| study_accession | Sample Identification | Text |
| library_chemistry | Library & Platform | Value List |
| library_prep_kit | Library & Platform (inferred) | Text |
| sequencing_platform | Library & Platform (inferred) | Text |
| alignment_tool | Library & Platform (inferred) | Value List |
| reference_genome | Library & Platform (inferred) | Text |
| cellranger_version | Library & Platform (inferred) | Text |
| n_cells | Cell Calling (inferred) | Number |
| mean_umi_count_per_cell | Sequencing QC | Number |
| mean_genes_per_cell | Sequencing QC | Number |
| mean_total_reads_per_cell | Sequencing QC | Number |
| mean_uniquely_mapped_reads_per_cell | Sequencing QC | Number |
| mean_secondary_alignments_per_cell | Sequencing QC | Number |
| mean_supplementary_alignments_per_cell | Sequencing QC | Number |
| mean_cellbender_cell_probability | Ambient RNA (CellBender) | Number |
| mean_post_cellbender_umis_per_cell | Ambient RNA (CellBender) | Number |
| mean_pct_cellbender_removed | Ambient RNA (CellBender) | Number |
| mean_pct_mitochondrial_reads | Mitochondrial QC | Number |

Fields marked "inferred" are not present in the reference RDS; they are expected commonly-reported scRNA-seq metadata that downstream contributors can populate.

## Joining scRNA-seq samples to donor metadata

The scRNA-seq CDE collection intentionally does NOT redefine donor-level fields (sex, age, BMI, diabetes status, autoantibodies, race/ethnicity). Instead, each scRNA-seq sample row includes `donor_rrid_ref` (CDE PKB_S_002), a foreign key to `donor_rrid` (CDE PKB_D_001) in the donor CDE collection. To build a fully-annotated per-sample table, join the two TSVs on `donor_rrid_ref == donor_rrid`:

```python
import pandas as pd
donors = pd.read_csv("output/hpap_cde_harmonized.tsv", sep="\t")
samples = pd.read_csv("output/scrnaseq_cde_harmonized.tsv", sep="\t")
merged = samples.merge(donors, left_on="donor_rrid_ref", right_on="donor_rrid", how="left")
```

## Validation Report Example

```
Field Completeness:
  donor_rrid: 195/197 (99.0%)
  sex_at_birth: 197/197 (100.0%)
  age_years: 197/197 (100.0%)
  diabetes_status: 197/197 (100.0%)
  hba1c_percent: 190/197 (96.4%)
  ...
```
