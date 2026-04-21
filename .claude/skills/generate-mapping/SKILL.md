---
name: generate-mapping
description: Auto-generate a CDE mapping JSON for a new consortia data file. Use when a user provides a new Excel file from an unfamiliar consortium and needs to create a column-to-CDE mapping configuration. The LLM inspects the source data structure, matches columns to PanKbase CDEs, and produces a ready-to-use mapping JSON.
disable-model-invocation: true
argument-hint: <path-to-excel-file> [consortium-name]
allowed-tools: Bash Read Write Glob Grep
---

# Generate CDE Mapping for New Consortium Data

You are generating a column mapping configuration for PanKbase CDE harmonization.

## Inputs
- **Data file**: `$0` (path to the Excel file)
- **Consortium name**: `$1` (optional; infer from filename if not provided)

## Step-by-step procedure

### 1. Inspect the source data

Use Python to load the Excel file and extract:
- All sheet names
- For each sheet: column headers (handle multi-row headers, merged cells)
- First 5-10 data rows to understand value formats and patterns
- Unique values for categorical columns (cap at 20 unique values)

```python
import openpyxl
# ... inspect the workbook
```

### 2. Load the CDE schema

Read the CDE schema from `task1_cde_definitions/pankbase_donor_cdes.json` in the project root. Understand each CDE field's name, data type, permissible values, and units.

### 3. Match source columns to CDE fields

For each CDE field, determine:
- **Which source column(s)** contain the relevant data (by name similarity, data patterns, units)
- **Which transform** is needed (see transform registry in `task2_cde_pipeline/pipeline.py`)
- **What value_map** is needed (for enumerated fields, map source values to CDE permissible values)

Use this reasoning:
- Column name matching: "Age (years)" -> age_years, "Sex" -> sex_at_birth, "BMI" -> bmi
- Data pattern matching: RRID:SAMN... -> donor_rrid, values like "T1D"/"T2D" -> diabetes_status
- Unit matching: values 0-100 with "%" in header -> percentage fields
- If a CDE has no matching source column, set transform to "not_available"

### 4. Generate the mapping JSON

Produce a JSON file following this structure (reference existing mappings in `task2_cde_pipeline/mappings/`):

```json
{
  "consortium": "<NAME>",
  "source_description": "<description>",
  "source_sheet": "<sheet_name>",
  "donor_id_column": "<column>",
  "column_mappings": {
    "cde_field_name": {
      "source_column": "<source_col>",
      "transform": "<transform_name>",
      "value_map": {},
      "default": "Unknown"
    }
  }
}
```

Available transforms: `direct`, `constant`, `numeric`, `value_map`, `binary_to_pos_neg`, `parse_value_cutoff`, `timedelta_to_hours`, `minutes_to_hours`, `parse_duration_years`, `derive_hba1c_status`, `derive_ethnicity_from_race`, `derive_donation_type`, `datetime_diff_days`, `presence_to_yes_no`, `not_available`, `lookup_sheet`.

### 5. Write the mapping file

Save to `task2_cde_pipeline/mappings/<consortium_lowercase>_mapping.json`.

### 6. Test the mapping

Run the pipeline with the new mapping to verify it works:

```bash
python3 task2_cde_pipeline/pipeline.py \
  --data <data_file> \
  --mapping task2_cde_pipeline/mappings/<mapping>.json \
  --cde task1_cde_definitions/pankbase_donor_cdes.json \
  --output task2_cde_pipeline/output/<consortium>_cde_harmonized.tsv
```

### 7. Review and report

- Check the validation report for errors
- Show the field completeness summary to the user
- Highlight any columns in the source data that could NOT be mapped to any CDE
- Highlight any required CDEs that have no source data
- Ask the user to review the value mappings for categorical fields

## Important guidelines

- Always prefer reading existing mapping files (`hpap_mapping.json`, `iidp_mapping.json`) as examples of the expected format
- Be conservative with value_maps: only map values you are confident about; use "Unknown" as default for uncertain cases
- For columns with non-standard formats, write a note explaining the issue
- If the Excel has multiple sheets, identify the main donor-level sheet (typically the one with demographic info)
- Handle edge cases: merged header rows, blank rows, inconsistent data types within columns
