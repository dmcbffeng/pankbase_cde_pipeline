# Contributing to PanKbase Donor Metadata CDE Pipeline

Thank you for your interest in contributing! This project welcomes contributions in three main areas:

## 1. Adding a new consortium

If you have donor metadata from a research consortium not yet supported:

1. Place a sample data file in `data/`
2. Create a mapping JSON in `task2_cde_pipeline/mappings/<consortium>_mapping.json`. Use `hpap_mapping.json` as a template.
3. Run the pipeline and verify the validation report
4. Add a smoke test in `task2_cde_pipeline/tests/`
5. Open a pull request

Tip: If you have Claude Code, run `/generate-mapping <your-file>.xlsx <CONSORTIUM_NAME>` to get a first-draft mapping automatically.

## 2. Updating CDE definitions

When CDEs need to change (new field, revised value set, updated terminology binding):

1. Update both `task1_cde_definitions/pankbase_donor_cdes.md` (human-readable) and `pankbase_donor_cdes.json` (machine-readable) — they must stay in sync
2. Bump the `schema_version` in the JSON file
3. Add an entry to the "Version History" table in the markdown file
4. Update all mapping files that are affected
5. Re-run the pipeline on all supported consortia and commit updated outputs
6. Open a pull request describing the change and its backward-compatibility implications

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
- Standard library + `openpyxl` only (no pandas, numpy, etc. to keep deployment simple)
- Docstrings for all transform functions
- Prefer clarity over cleverness

## Questions?

Open an issue with the `question` label.
