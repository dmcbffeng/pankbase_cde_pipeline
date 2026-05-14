# PanKbase scRNA-seq Metadata: Common Data Element (CDE) Collection v0.2

## Overview

This document defines the formal Common Data Elements (CDEs) for PanKbase **single-cell / single-nucleus RNA-seq sample-level metadata**. The field list is sourced from a collaborator-curated metadata spreadsheet and covers two areas: (1) sample-level Single Cell/Nucleus Preparation (assay, library, sequencing), and (2) Processing Steps (alignment, count-matrix generation, reference build). Two identifier CDEs (`sample_id`, `donor_rrid_ref`) are included so that the schema can be used to harmonize actual records and to join back to the [PanKbase Donor Metadata CDE Collection](pankbase_donor_cdes.md); donor-level fields (demographics, medical history, autoantibodies, pancreas processing) are NOT duplicated here.

Each CDE follows the NIH CDE format (ISO/IEC 11179-aligned) with the following attributes:

- **CDE ID**: PanKbase-assigned identifier (PKB_S_xxx — `S` = scRNA-seq)
- **CDE Name**: Short, standardized variable name
- **Question Text**: The data collection prompt
- **Definition**: Precise description of what the element captures
- **Data Type**: Number, Text, Value List
- **Input Restrictions**: Constraints on the value (e.g., range, pattern)
- **Permissible Values**: Allowed values for enumerated types
- **Unit of Measure**: UCUM-standard unit where applicable
- **Terminology Binding**: Ontology/vocabulary references (EFO, OBI, LOINC)
- **PanKbase Tier**: Required / Desired
- **Origin**: `Collaborator spreadsheet` (scRNAseq_metadata.xlsx) — the canonical source for this version; or `Identifier CDE` — sample/donor identifiers added so the schema can be used in practice.

CDEs are organized by category: Sample Identification, Single Cell/Nucleus Preparation, Processing Steps.

### NIH CDE Repository Search

The NIH CDE Repository ([cde.nlm.nih.gov](https://cde.nlm.nih.gov/home)) and caDSR II were searched for existing CDEs covering single-cell assay resolution, modality, platform, library construction, sequencing run configuration, and reference-genome reporting. **No exact matches were found**: the NIH CDE collections are dominated by clinical and phenotypic elements and do not yet cover single-cell assay-level metadata. The CDEs below were therefore drafted in NIH format from the collaborator spreadsheet, with terminology bindings drawn from EFO/OBI, SRA/ENA library-selection vocabulary, and HCA / CELLxGENE conventions where appropriate.

### Linkage to Donor CDE Collection

| scRNA-seq CDE | → | Donor CDE |
|---|---|---|
| PKB_S_002 `donor_rrid_ref` | foreign_key | PKB_D_001 `donor_rrid` |

---

## 1. SAMPLE IDENTIFICATION

### CDE PKB_S_001: Sample ID

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_001 |
| **CDE Name** | sample_id |
| **Question Text** | What is the unique identifier for this single-cell / single-nucleus RNA-seq sample? |
| **Definition** | A unique identifier for one library / one experimental condition. Free-text string with no enforced format. |
| **Data Type** | Text |
| **Input Restrictions** | Non-empty string. Must be unique within a study; global uniqueness recommended. |
| **Permissible Values** | N/A (free text) |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | No exact match. Analogous to "Biospecimen Identifier" / "Library Identifier" concepts. |
| **PanKbase Tier** | Required |
| **Origin** | Identifier CDE (added to make the schema usable for actual records; not in the collaborator spreadsheet). |

---

### CDE PKB_S_002: Donor RRID (Reference)

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_002 |
| **CDE Name** | donor_rrid_ref |
| **Question Text** | What is the RRID of the donor from whom this sample was derived? |
| **Definition** | A foreign-key reference to the donor record in the [PanKbase Donor Metadata CDE Collection](pankbase_donor_cdes.md), specifically CDE **PKB_D_001 (`donor_rrid`)**. Enables joining scRNA-seq sample records to their corresponding donor demographic, medical, and processing metadata without duplicating those fields. |
| **Data Type** | Text |
| **Input Restrictions** | Accepts canonical RRID (`RRID:SAMN[0-9]+`), bare BioSample accession (`SAMN[0-9]+`), or a consortium-native donor ID (e.g., `HPAP-019`, `HP-21070-01`). |
| **Cross-Reference** | **Schema**: `pankbase_donor_cdes.json` · **CDE ID**: `PKB_D_001` · **CDE Name**: `donor_rrid` · **Relationship**: foreign_key |
| **Unit of Measure** | N/A |
| **Terminology Binding** | RRID Portal |
| **PanKbase Tier** | Required |
| **Origin** | Identifier CDE (added to enable join to donor CDE collection; not in the collaborator spreadsheet). |
| **Example Values** | `HP-21070-01`, `HPAP-019`, `RRID:SAMN18434646` |

---

## 2. SINGLE CELL / NUCLEUS PREPARATION

### CDE PKB_S_003: Assay Resolution

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_003 |
| **CDE Name** | assay_resolution |
| **Question Text** | At what resolution was the assay performed? |
| **Definition** | Whether the assay captured intact cells (e.g., scRNA-seq) or isolated nuclei (e.g., snRNA-seq). |
| **Data Type** | Value List |
| **Permissible Values** | `cell`, `nucleus`, `Unknown` |
| **Unit of Measure** | N/A |
| **Terminology Binding** | EFO (`cell` → EFO:0010550, `nucleus` → EFO:0010551) |
| **PanKbase Tier** | Required |
| **Origin** | Collaborator spreadsheet — 'Assay resolution'. |
| **Example Values** | `cell`, `nucleus` |

---

### CDE PKB_S_004: Modality

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_004 |
| **CDE Name** | modality |
| **Question Text** | Which molecular modality (or modalities) does this assay measure? |
| **Definition** | The molecular layer(s) profiled. Multiome assays (e.g., 10x Multiome ATAC + Gene Expression) should be recorded as `multiome`. |
| **Data Type** | Value List |
| **Permissible Values** | `RNA`, `transcriptome`, `ATAC`, `chromatin accessibility`, `multiome`, `Other`, `Unknown` |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Required |
| **Origin** | Collaborator spreadsheet — 'Modality'. |

---

### CDE PKB_S_005: Assay Platform

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_005 |
| **CDE Name** | assay_platform |
| **Question Text** | Which single-cell assay platform was used? |
| **Definition** | The vendor / technology family used to perform single-cell capture. |
| **Data Type** | Value List |
| **Permissible Values** | `10x`, `Fluidigm`, `SMART-Seq`, `Drop-Seq`, `Other`, `Unknown` |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Required |
| **Origin** | Collaborator spreadsheet — 'Assay platform'. |

---

### CDE PKB_S_006: Reagent Kit

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_006 |
| **CDE Name** | reagent_kit |
| **Question Text** | Which reagent / library-preparation kit was used? |
| **Definition** | Free-text identification of the kit and chemistry version where available. |
| **Data Type** | Text |
| **Permissible Values** | N/A |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Reagen kit' (typo in source; canonicalized to `reagent_kit`). |
| **Example Values** | `Chromium Next GEM Single Cell Multiome ATAC + Gene Expression`, `10X-Chromium-GEX-3p-v2`, `10X-Chromium-GEX-3p-v3` |

---

### CDE PKB_S_007: Treatment Protocol

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_007 |
| **CDE Name** | treatment_protocol |
| **Question Text** | What treatment protocol was applied to the cells/nuclei prior to capture? |
| **Definition** | Free-text description of the experimental treatment applied prior to capture (drug exposure, cytokine stimulation, etc.). May be `None` / `Untreated` when no treatment was applied. |
| **Data Type** | Text |
| **Permissible Values** | N/A |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Treatment protocol'. |
| **Example Values** | `CMRL (10% FBS, 1% Glutamax) supplemented with 0.025% DMSO, 250 nM thapsigargin, or 25 U/mL IL1β + 1000 U/mL IFNγ for 24 h at 37°C, 5% CO2.` |

---

### CDE PKB_S_008: Growth Protocol

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_008 |
| **CDE Name** | growth_protocol |
| **Question Text** | What growth / culture protocol was used for the source cells/tissue? |
| **Definition** | Free-text description of how the source biospecimen (e.g., human cadaveric pancreatic islets) was procured and maintained prior to dissociation. |
| **Data Type** | Text |
| **Permissible Values** | N/A |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Growth protocol'. |

---

### CDE PKB_S_009: Extracted Molecule

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_009 |
| **CDE Name** | extracted_molecule |
| **Question Text** | What molecule was extracted from the cells/nuclei? |
| **Definition** | The molecular species captured into the library. |
| **Data Type** | Value List |
| **Permissible Values** | `total RNA`, `polyA RNA`, `nuclear RNA`, `cytoplasmic RNA`, `genomic DNA`, `Other`, `Unknown` |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Extracted molecule'. |

---

### CDE PKB_S_010: Extraction Protocol

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_010 |
| **CDE Name** | extraction_protocol |
| **Question Text** | What protocol was used to extract and capture the cells/nuclei? |
| **Definition** | Free-text description of cell/nucleus dissociation, staining, hashing, and droplet/well loading. |
| **Data Type** | Text |
| **Permissible Values** | N/A |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Extraction protocol'. |

---

### CDE PKB_S_011: Library Construction Protocol

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_011 |
| **CDE Name** | library_construction_protocol |
| **Question Text** | What library-construction protocol (text or URL) was followed? |
| **Definition** | Free text. URLs are encouraged when a public protocol document exists. |
| **Data Type** | Text |
| **Permissible Values** | N/A |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Library construction protocol'. |
| **Example Values** | `https://hpap.pmacs.upenn.edu/explore/workflow/islet-molecular-phenotyping-studies?protocol=4` |

---

### CDE PKB_S_012: Library Selection

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_012 |
| **CDE Name** | library_selection |
| **Question Text** | Which library selection strategy was used? |
| **Definition** | The molecular selection applied during library construction (e.g., cDNA from polyA capture). Vocabulary follows SRA / ENA conventions. |
| **Data Type** | Value List |
| **Permissible Values** | `cDNA`, `PolyA`, `Random`, `Hybrid Selection`, `Inverse rRNA`, `Other`, `Unknown` |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Library selection'. |

---

### CDE PKB_S_013: Sequencing Run Type

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_013 |
| **CDE Name** | sequencing_run_type |
| **Question Text** | Was the library sequenced as paired-end or single-end? |
| **Definition** | Read-pair configuration of the sequencing run. |
| **Data Type** | Value List |
| **Permissible Values** | `paired-end`, `single-end`, `Unknown` |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Sequencing run type'. |

---

### CDE PKB_S_014: Sequencing Instrument

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_014 |
| **CDE Name** | sequencing_instrument |
| **Question Text** | Which sequencing instrument was used? |
| **Definition** | Free text, ideally manufacturer + model. |
| **Data Type** | Text |
| **Permissible Values** | N/A |
| **Unit of Measure** | N/A |
| **Terminology Binding** | EFO / OBI (sequencing instrument) |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Sequencing instrument'. |
| **Example Values** | `Illumina NovaSeq 6000`, `Illumina HiSeq 4000` |

---

### CDE PKB_S_015: Read Length Configuration

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_015 |
| **CDE Name** | read_length_configuration |
| **Question Text** | What was the planned read-length configuration of the sequencing run? |
| **Definition** | The planned / run-configured read lengths. Format `<R1>x<R2>` for paired-end, single integer for single-end. |
| **Data Type** | Text |
| **Input Restrictions** | Matches `^[0-9]+(x[0-9]+)?$` |
| **Unit of Measure** | bp |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Read length configuration'. |
| **Example Values** | `101x101`, `75` |

---

### CDE PKB_S_016: Demultiplexed Read Lengths

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_016 |
| **CDE Name** | demultiplexed_read_lengths |
| **Question Text** | What were the read lengths in the demultiplexed FASTQ files (R1/R2)? |
| **Definition** | Actual read lengths in delivered FASTQs, excluding index reads (i7/i5). Format `<R1>x<R2>`. |
| **Data Type** | Text |
| **Input Restrictions** | Matches `^[0-9]+(x[0-9]+)?$` |
| **Unit of Measure** | bp |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Demultiplexed read lengths'. |
| **Example Values** | `26x98` |

---

### CDE PKB_S_017: Number of Target Cells

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_017 |
| **CDE Name** | number_of_target_cells |
| **Question Text** | What was the targeted (loaded) cell/nucleus count for this library? |
| **Definition** | Targeted / planned cell number loaded into the assay; not the post-QC recovered count. |
| **Data Type** | Number (integer) |
| **Input Restrictions** | 0 ≤ value ≤ 1,000,000 |
| **Unit of Measure** | cells |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Number of target cells'. |
| **Example Values** | `5000` |

---

## 3. PROCESSING STEPS

### CDE PKB_S_018: Processing Workflow Overview

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_018 |
| **CDE Name** | processing_workflow_overview |
| **Question Text** | Provide a high-level description of the data-processing workflow. |
| **Definition** | Free text covering BCL→FASTQ conversion, alignment, count-matrix generation, demultiplexing, hashtag processing, etc. |
| **Data Type** | Text |
| **Permissible Values** | N/A |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Processing workflow overview'. |
| **Example Values** | `Illumina BCL → FASTQ via bcl2fastq; aligned to GRCh38.93 with Cell Ranger count; HTO libraries processed with CITE-seq-Count; demultiplexing via demuxlet + Seurat HTO enrichment.` |

---

### CDE PKB_S_019: Processing Workflow Code

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_019 |
| **CDE Name** | processing_workflow_code |
| **Question Text** | Where can the code or pipeline definition for the processing workflow be found? |
| **Definition** | Free text; URL preferred (GitHub repo, Snakemake/Nextflow definition, DOI). |
| **Data Type** | Text |
| **Permissible Values** | N/A |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Processing workflow code'. |

---

### CDE PKB_S_020: Genome Build

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_020 |
| **CDE Name** | genome_build |
| **Question Text** | Which reference genome build was used for alignment? |
| **Definition** | The human reference genome build (and annotation bundle, when known) used to align reads. |
| **Data Type** | Text |
| **Permissible Values** | N/A (free text) |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | Collaborator spreadsheet — 'Genome build'. |
| **Example Values** | `GRCh38`, `GRCh38.93`, `refdata-gex-GRCh38-2020-A` |

---

## Design Decisions

This section documents non-obvious choices made while defining these CDEs in v0.2.

1. **Field list is sourced from the collaborator spreadsheet.** All 18 substantive CDEs (PKB_S_003 through PKB_S_020) correspond 1:1 to rows in `scRNAseq_metadata.xlsx`. The v0.1 field set — derived from the per-cell QC RDS — has been retired and is not part of v0.2.
2. **Two identifier CDEs added.** The collaborator spreadsheet does not specify a sample identifier or a donor link, but a CDE schema is unusable for actual records without them. `sample_id` (PKB_S_001) and `donor_rrid_ref` (PKB_S_002, foreign key to PKB_D_001) are therefore added, marked clearly as Origin: "Identifier CDE" rather than from the spreadsheet.
3. **Cross-reference via `donor_rrid_ref`.** Rather than duplicating donor fields, a foreign-key CDE links each sample back to PKB_D_001 (`donor_rrid`). The JSON encodes this via a `cross_reference` block (`{schema, cde_id, cde_name, relationship}`) so consuming tools can programmatically resolve the join.
4. **Categories follow the spreadsheet's top-level grouping.** "Single Cell/Nucleus Preparation" (15 CDEs) and "Processing Steps" (3 CDEs) match the collaborator's `Single cell/nucleus profiling` hierarchy. A "Sample Identification" category was added for the two identifier CDEs.
5. **Required vs. Desired.** Only the two identifier CDEs and the three top-level assay descriptors (`assay_resolution`, `modality`, `assay_platform`) are **Required**; all protocol-text and run-configuration fields are **Desired** to reflect that not every contributor will have them at submission time.
6. **Value lists vs. free text.** Fields with a small enumerable vocabulary (`assay_resolution`, `modality`, `assay_platform`, `extracted_molecule`, `library_selection`, `sequencing_run_type`) are encoded as value lists with `Other` and `Unknown` escape values. Fields that are inherently descriptive (`treatment_protocol`, `growth_protocol`, `extraction_protocol`, `library_construction_protocol`, `processing_workflow_overview`, `processing_workflow_code`, `reagent_kit`, `sequencing_instrument`, `genome_build`) are kept as free text; constraining them prematurely would lose information.
7. **Spelling normalization.** The spreadsheet contains a typo ("Reagen kit"); the CDE name is canonicalized to `reagent_kit`. The original spelling is preserved in the `Origin` note for traceability.
8. **NIH CDE Repository.** Searched for existing elements covering single-cell assay metadata, library construction, sequencing run configuration, and reference-genome reporting. No direct matches — this was expected, as NIH CDEs today focus on clinical/phenotypic elements. The definitions therefore follow NIH format but are newly authored.
9. **Schema version 0.2 (not 1.0).** This is a substantive revision of v0.1; bumped to 0.2 to signal continued evolution and explicit alignment with the collaborator's curated list. A 1.0 release will wait until the field set is stable across multiple contributing datasets.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-04-23 | Initial draft. 20 CDEs = 13 observed (per-cell QC, CellBender, mitochondrial) + 1 donor cross-reference + 6 inferred common fields. Retired in v0.2 in favor of a collaborator-curated field list. |
| 0.2 | 2026-05-14 | Replaced v0.1 field set with 20 CDEs sourced from the collaborator-curated `scRNAseq_metadata.xlsx` spreadsheet (2 identifier CDEs + 15 Single Cell/Nucleus Preparation + 3 Processing Steps). Per-cell QC fields and RDS-derived inferred fields are removed. Previously-shipped per-cell QC mapping/output artifacts no longer match this schema and have been deleted; the source RDS file is retained as a historical reference. |
