# PanKbase CDE Harmonization Pipeline

## Overview

This pipeline takes raw data from any research consortium (e.g., HPAP, IIDP) and transforms it into a standardized table that matches the PanKbase Common Data Element (CDE) definitions.

## Architecture

```
Input                          Config                        Output
─────                          ──────                        ──────
Raw consortia data  ──┐
(Excel file)         │    CDE Schema JSON ──┐
                     ├──► pipeline.py ──────┼──► Harmonized TSV
Mapping config ──────┘                      └──► Validation Report
(JSON file)
```

## Quick Start

```bash
# Harmonize HPAP data
python pipeline.py \
    --data ../data/HPAP_Donor_Summary_197.xlsx \
    --mapping mappings/hpap_mapping.json \
    --cde ../task1_cde_definitions/pankbase_donor_cdes.json \
    --output output/hpap_cde_harmonized.tsv

# Harmonize IIDP data
python pipeline.py \
    --data ../data/IIDP_HIPP_Report.xlsx \
    --mapping mappings/iidp_mapping.json \
    --cde ../task1_cde_definitions/pankbase_donor_cdes.json \
    --output output/iidp_cde_harmonized.tsv
```

## Requirements

- Python 3.7+
- openpyxl (`pip install openpyxl`)

## How It Works

### 1. Load source data
The pipeline reads the raw Excel file using the consortium-specific loading strategy (named columns for HPAP, positional columns for IIDP's multi-header format).

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
  "source_sheet": "Sheet1",
  "donor_id_column": "donor_id",
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

## Output Format

The output TSV contains 34 columns matching the PanKbase Donor CDEs:

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
