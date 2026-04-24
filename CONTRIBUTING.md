# Contributing to the PanKbase Metadata CDE Pipeline

Thank you for your interest in contributing! This project welcomes contributions in several areas:

## 1. Adding a new consortium or dataset (donor or scRNA-seq)

If you have donor metadata or scRNA-seq sample metadata from a consortium / dataset not yet supported:

1. Place a sample data file in `data/` (`.xlsx` for donor spreadsheets, `.rds` for R-side tabular exports)
2. Create a mapping JSON in `task2_cde_pipeline/mappings/<name>_mapping.json`. Use `hpap_mapping.json` (donor/Excel) or `pankbase_scrnaseq_mapping.json` (scRNA-seq/RDS) as a template. Set `data_format` to `hpap_excel`, `iidp_excel`, or `rds`.
3. Pick the right `--cde` schema at run time:
   - `task1_cde_definitions/pankbase_donor_cdes.json` for donor-level metadata
   - `task1_cde_definitions/pankbase_scrnaseq_cdes.json` for scRNA-seq sample metadata
4. Run the pipeline and verify the validation report
5. Add a smoke test in `task2_cde_pipeline/tests/`
6. Open a pull request

Tip: If you have Claude Code, run `/generate-mapping <your-file>.(xlsx|rds) <NAME>` to get a first-draft mapping automatically.

## 2. Updating CDE definitions

When CDEs need to change (new field, revised value set, updated terminology binding):

1. Update **both** the human-readable `.md` and machine-readable `.json` files for the affected CDE collection — they must stay in sync:
   - Donor: `task1_cde_definitions/pankbase_donor_cdes.{md,json}`
   - scRNA-seq: `task1_cde_definitions/pankbase_scrnaseq_cdes.{md,json}`
2. Bump the `schema_version` in the JSON file
3. Add an entry to the "Version History" section in the markdown file
4. If you added / removed a CDE that is referenced across collections (e.g., a donor CDE that the scRNA-seq collection cross-references), update the `cross_reference` block in the dependent collection
5. Update all mapping files that are affected
6. Re-run the pipeline on all supported consortia / datasets and commit updated outputs
7. Open a pull request describing the change and its backward-compatibility implications

### When to add a new CDE

- A new metadata field is required by PanKbase collaborators
- An existing composite field needs to be decomposed (e.g., separating race and ethnicity)
- A new autoantibody or biomarker needs tracking

### When to retire a CDE

Don't delete CDEs — mark them as deprecated and keep them in the schema with a deprecation note. This preserves backward compatibility with existing mappings.

## 3. Pipeline improvements

New transforms, validation rules, or performance improvements:

1. Add the transform function to `task2_cde_pipeline/pipeline.py`
2. Register it in the `TRANSFORM_REGISTRY` dict
3. Add a test case in `task2_cde_pipeline/tests/test_pipeline.py`
4. Document the transform in `task2_cde_pipeline/README.md`

## Running tests

```bash
pip install -r requirements.txt pytest
python -m pytest task2_cde_pipeline/tests/ -v
```

## Code style

- Python 3.7+ compatible
- Runtime dependencies: standard library, `openpyxl` (Excel), `pyreadr` (RDS). Avoid adding further dependencies unless strictly necessary.
- Docstrings for all transform functions
- Prefer clarity over cleverness

## Questions?

Open an issue with the `question` label.
