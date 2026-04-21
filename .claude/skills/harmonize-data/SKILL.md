---
name: harmonize-data
description: One-click CDE harmonization for any consortia data file. Automatically generates a mapping if one doesn't exist, then runs the pipeline to produce a clean CDE-matched table. Use when a user wants to harmonize a new data file to PanKbase CDEs.
disable-model-invocation: true
argument-hint: <path-to-excel-file> [consortium-name]
allowed-tools: Bash Read Write Glob Grep
---

# One-Click CDE Harmonization

Harmonize a consortia data file to PanKbase CDEs in one step.

## Inputs
- **Data file**: `$0` (path to the Excel file)
- **Consortium name**: `$1` (optional; infer from filename if not provided)

## Procedure

### 1. Check for existing mapping

Look in `task2_cde_pipeline/mappings/` for a mapping JSON matching the consortium name. If found, use it directly. If not found, generate one.

### 2. If no mapping exists: generate one

Follow the `/generate-mapping` procedure:
- Inspect the Excel file structure (sheets, headers, sample data, unique values)
- Load the CDE schema from `task1_cde_definitions/pankbase_donor_cdes.json`
- Match source columns to CDE fields using name similarity, data patterns, and units
- Generate value_maps for categorical fields
- Save mapping to `task2_cde_pipeline/mappings/<consortium>_mapping.json`

### 3. Run the pipeline

```bash
python3 task2_cde_pipeline/pipeline.py \
  --data "$0" \
  --mapping task2_cde_pipeline/mappings/<consortium>_mapping.json \
  --cde task1_cde_definitions/pankbase_donor_cdes.json \
  --output task2_cde_pipeline/output/<consortium>_cde_harmonized.tsv
```

### 4. Report results

Show the user:
1. Number of records harmonized
2. Field completeness summary (from validation report)
3. Any validation warnings that need attention
4. Path to the output TSV file
5. If a new mapping was generated, note which fields could not be mapped and ask for review

## Key paths (relative to project root)

- CDE schema: `task1_cde_definitions/pankbase_donor_cdes.json`
- Pipeline script: `task2_cde_pipeline/pipeline.py`
- Mappings directory: `task2_cde_pipeline/mappings/`
- Output directory: `task2_cde_pipeline/output/`
