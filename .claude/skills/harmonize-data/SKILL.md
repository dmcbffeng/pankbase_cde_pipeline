---
name: harmonize-data
description: One-click CDE harmonization for any PanKbase data file (donor Excel or scRNA-seq RDS). Auto-detects the file type, picks the right CDE schema (donor vs. scRNA-seq), generates a mapping if one doesn't exist, then runs the pipeline to produce a clean CDE-matched table.
disable-model-invocation: true
argument-hint: <path-to-data-file> [consortium-or-dataset-name]
allowed-tools: Bash Read Write Glob Grep
---

# One-Click CDE Harmonization

Harmonize a consortia / dataset data file to PanKbase CDEs in one step.

## Inputs
- **Data file**: `$0` (path to an `.xlsx` donor spreadsheet OR an `.rds` R data.frame)
- **Consortium / dataset name**: `$1` (optional; infer from filename if not provided)

## Procedure

### 1. Detect file type → CDE schema

- `.xlsx` / `.xls` → `task1_cde_definitions/pankbase_donor_cdes.json` (donor schema)
- `.rds` → `task1_cde_definitions/pankbase_scrnaseq_cdes.json` (scRNA-seq schema)
- If the file is an Excel but clearly holds scRNA-seq metadata (e.g., per-sample QC), ask the user which schema to target instead of guessing.

### 2. Check for an existing mapping

Look in `task2_cde_pipeline/mappings/` for a mapping JSON matching the consortium / dataset name. If found, use it directly. If not found, go to step 3.

### 3. If no mapping exists: generate one

Follow the `/generate-mapping` procedure:
- Inspect the file structure (sheets, headers, sample data, unique values; or RDS columns, dtypes, unique values)
- Load the chosen CDE schema
- Match source columns to CDE fields using name similarity, data patterns, and units
- Generate `value_map`s for categorical fields
- Save mapping to `task2_cde_pipeline/mappings/<name>_mapping.json`
- Be sure to set `data_format` explicitly (`hpap_excel`, `iidp_excel`, or `rds`)

### 4. Run the pipeline

Pick the right `--cde` based on step 1.

```bash
python3 task2_cde_pipeline/pipeline.py \
  --data "$0" \
  --mapping task2_cde_pipeline/mappings/<name>_mapping.json \
  --cde task1_cde_definitions/<pankbase_donor_cdes.json | pankbase_scrnaseq_cdes.json> \
  --output task2_cde_pipeline/output/<name>_cde_harmonized.tsv
```

### 5. Report results

Show the user:
1. Detected file format + which CDE schema was used
2. Number of records harmonized
3. Field completeness summary (from validation report)
4. Any validation warnings that need attention
5. Path to the output TSV file and validation report
6. If a new mapping was generated, note which fields could not be mapped and ask for review
7. For scRNA-seq: remind the user they can join the harmonized TSV to donor output on `donor_rrid_ref == donor_rrid`

## Key paths (relative to project root)

- Donor CDE schema: `task1_cde_definitions/pankbase_donor_cdes.json`
- scRNA-seq CDE schema: `task1_cde_definitions/pankbase_scrnaseq_cdes.json`
- Pipeline script: `task2_cde_pipeline/pipeline.py`
- Mappings directory: `task2_cde_pipeline/mappings/`
- Output directory: `task2_cde_pipeline/output/`
