---
name: generate-mapping
description: Auto-generate a CDE mapping JSON for a new data file (donor Excel or scRNA-seq RDS). Use when a user provides a new file from an unfamiliar consortium / dataset and needs a column-to-CDE mapping config. The LLM picks the right CDE schema (donor vs. scRNA-seq), inspects the source structure, matches columns, and produces a ready-to-use mapping JSON.
disable-model-invocation: true
argument-hint: <path-to-data-file> [consortium-or-dataset-name]
allowed-tools: Bash Read Write Glob Grep
---

# Generate CDE Mapping for New PanKbase Data

You are generating a column mapping configuration for PanKbase CDE harmonization.

## Inputs
- **Data file**: `$0` (path to an `.xlsx` donor spreadsheet OR an `.rds` R data.frame)
- **Consortium / dataset name**: `$1` (optional; infer from filename if not provided)

## Step-by-step procedure

### 1. Detect file type and pick the CDE schema

- `.xlsx` / `.xls` → most commonly donor-level metadata. Load with `openpyxl`. Target schema: `task1_cde_definitions/pankbase_donor_cdes.json`. Set `data_format` to `hpap_excel` (named-column headers) or `iidp_excel` (positional + header row offset).
- `.rds` → R data.frame, most commonly scRNA-seq sample metadata. Load with `pyreadr`. Target schema: `task1_cde_definitions/pankbase_scrnaseq_cdes.json`. Set `data_format` to `rds`.
- If uncertain (e.g., an Excel that looks like scRNA-seq QC), inspect the columns and ask the user which CDE schema to target.

### 2. Inspect the source data

For Excel:
```python
import openpyxl
wb = openpyxl.load_workbook(path, data_only=True)
# sheet names, headers, first 5-10 rows, unique values per column (cap at 20)
```

For RDS:
```python
import pyreadr
result = pyreadr.read_r(path)
df = next(iter(result.values()))  # or a named object
# df.columns, df.dtypes, df.head(), df[col].unique() per column
```

Report to the user: file format, number of records, number of columns, and unique-value samples for categorical columns.

### 3. Load the target CDE schema

Read the chosen schema JSON. Understand each CDE field's name, data type, permissible values, units, and any `cross_reference` blocks (e.g., `donor_rrid_ref` → donor `donor_rrid`).

### 4. Match source columns to CDE fields

For each CDE field, determine:
- **Which source column(s)** contain the relevant data (by name similarity, data patterns, units)
- **Which transform** is needed (see transform registry in `task2_cde_pipeline/pipeline.py`)
- **What value_map** is needed (for enumerated fields, map source values to CDE permissible values)

Typical matches:
- Donor: `Age (years)` → `age_years`; `Sex` → `sex_at_birth`; `BMI` → `bmi`; `RRID:SAMN...` → `donor_rrid`; `T1D`/`T2D` → `diabetes_status`
- scRNA-seq: `samples` → `sample_id`; `rrid` → `donor_rrid_ref`; `study`/`GSE...` → `study_accession`; `chemistry` (`V2`/`V3`) → `library_chemistry`; `mean_nCount_RNA` → `mean_umi_count_per_cell`; `mean_nFeature_RNA` → `mean_genes_per_cell`; `mean_rna_pct_mitochondrial` → `mean_pct_mitochondrial_reads`
- If a CDE has no matching source column, set transform to `not_available` and add a `_note` explaining why (e.g., `"Inferred CDE; not present in the source RDS."`)

### 5. Generate the mapping JSON

```json
{
  "consortium": "<NAME>",
  "data_format": "hpap_excel | iidp_excel | rds",
  "description": "<one-line description>",
  "source_sheet": "<sheet name if Excel>",
  "rds_object_name": "<R object name if RDS and multiple objects>",
  "record_id_column": "<column that identifies each record>",
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

### 6. Write the mapping file

Save to `task2_cde_pipeline/mappings/<name_lowercase>_mapping.json`. Reference existing mappings (`hpap_mapping.json` for donor Excel, `pankbase_scrnaseq_mapping.json` for RDS) as templates.

### 7. Test the mapping

```bash
python3 task2_cde_pipeline/pipeline.py \
  --data <data_file> \
  --mapping task2_cde_pipeline/mappings/<mapping>.json \
  --cde task1_cde_definitions/<pankbase_donor_cdes.json | pankbase_scrnaseq_cdes.json> \
  --output task2_cde_pipeline/output/<name>_cde_harmonized.tsv
```

### 8. Review and report

- Check the validation report for errors
- Show the field completeness summary
- Highlight source columns that could NOT be mapped to any CDE
- Highlight required CDEs that have no source data
- Ask the user to review `value_map`s for categorical fields
- For scRNA-seq: explicitly note which `donor_rrid_ref` values are bare BioSample (`SAMN...`) vs. canonical RRID vs. consortium-native (`HPAP-xxx`), since the donor-side join may need resolution

## Important guidelines

- Prefer reading existing mapping files (`hpap_mapping.json`, `pankbase_scrnaseq_mapping.json`) as examples
- Be conservative with `value_map`s: only map values you are confident about; use `"Unknown"` as default for uncertain cases
- For columns with non-standard formats, add a `_note` in the mapping explaining the issue
- Respect the project scope: for scRNA-seq files, skip donor-scope columns (sex, age, BMI, etc.) — they live in the donor CDE collection and are joined via `donor_rrid_ref`
- Handle edge cases: merged header rows, `NA` sentinels in RDS (`"NA"`, `NaN`), blank rows, inconsistent types within a column
