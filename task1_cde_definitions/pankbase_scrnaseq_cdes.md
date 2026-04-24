# PanKbase scRNA-seq Metadata: Common Data Element (CDE) Collection v0.1

## Overview

This document defines the formal Common Data Elements (CDEs) for PanKbase **single-cell RNA-seq (scRNA-seq) sample-level experiment and QC metadata**. It is a companion to the [PanKbase Donor Metadata CDE Collection](pankbase_donor_cdes.md); donor-level fields (demographics, medical history, autoantibodies, pancreas processing, sample transportation) are NOT duplicated here. Each scRNA-seq sample record links back to its donor via `donor_rrid_ref` (see CDE PKB_S_002).

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
- **Origin**: `Observed` — present in `data/metadata_for_DEG.rds`; `Observed (donor cross-reference)`; or `Inferred` — commonly-expected scRNA-seq metadata added by collaborator convention, not present in the source RDS

CDEs are organized by category: Sample Identification, Library & Platform, Cell Calling, Sequencing QC, Ambient RNA (CellBender), Mitochondrial QC.

### NIH CDE Repository Search

The NIH CDE Repository ([cde.nlm.nih.gov](https://cde.nlm.nih.gov/home)) and caDSR II were searched for existing CDEs covering scRNA-seq sample identification, 10x Genomics library chemistry, CellBender QC metrics, and per-cell UMI/gene/mitochondrial summaries. **No exact matches were found**: the NIH CDE collections are dominated by clinical and phenotypic elements and do not yet cover single-cell assay-level QC. The CDEs below were therefore drafted from scratch in NIH format, taking inspiration from:

- The scRNA-seq metadata conventions used by the [HCA Data Portal (Human Cell Atlas)](https://data.humancellatlas.org/) and [CELLxGENE](https://cellxgene.cziscience.com/)
- The 10x Genomics CellRanger output (`metrics_summary.csv`) field definitions
- The [CellBender](https://github.com/broadinstitute/CellBender) documentation for ambient-RNA metrics
- Standard single-cell QC practice (`nCount_RNA`, `nFeature_RNA`, `percent.mt` in Seurat)

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
| **Question Text** | What is the unique identifier for this single-cell RNA-seq sample? |
| **Definition** | A unique identifier for a single-cell RNA-seq sample (one library / one condition). In PanKbase-contributed datasets, values conventionally take the form `<donor_id>__<treatment_label>` (e.g., `HP-21070-01__DHT_10nM`), but this format is not enforced — the identifier may also be a GEO sample accession, a consortium-native sample label, or an arbitrary string. |
| **Data Type** | Text |
| **Input Restrictions** | Non-empty string. Must be unique within a `study_accession`; global uniqueness is recommended. |
| **Permissible Values** | N/A (free text) |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | No exact match. Analogous to "Biospecimen Identifier" / "Library Identifier" concepts. |
| **Terminology Binding** | N/A |
| **PanKbase Tier** | Required |
| **Origin** | Observed (source column: `samples`) |
| **Example Values** | `HP-21070-01__DHT_10nM`, `HPAP-020__Untreated` |

---

### CDE PKB_S_002: Donor RRID (Reference)

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_002 |
| **CDE Name** | donor_rrid_ref |
| **Question Text** | What is the RRID of the donor from whom this sample was derived? |
| **Definition** | A foreign-key reference to the donor record in the [PanKbase Donor Metadata CDE Collection](pankbase_donor_cdes.md), specifically CDE **PKB_D_001 (`donor_rrid`)**. This element enables joining scRNA-seq sample records to their corresponding donor demographic, medical, and processing metadata without duplicating those fields in this collection. |
| **Data Type** | Text |
| **Input Restrictions** | Accepts a canonical RRID (`RRID:SAMN[0-9]+`), a bare BioSample accession (`SAMN[0-9]+`), or a consortium-native donor ID (e.g., `HPAP-019`, `HP-21070-01`) when an RRID has not been assigned. |
| **Permissible Values** | N/A |
| **Cross-Reference** | **Schema**: `pankbase_donor_cdes.json` · **CDE ID**: `PKB_D_001` · **CDE Name**: `donor_rrid` · **Relationship**: foreign_key |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | Linkage semantics; no content CDE. |
| **Terminology Binding** | RRID Portal |
| **PanKbase Tier** | Required |
| **Origin** | Observed (source column: `rrid`) |
| **Notes** | Value-domain and validation rules for the RRID string itself are governed by PKB_D_001. Downstream tooling is expected to resolve non-RRID donor IDs to RRIDs by joining to the donor CDE table. |
| **Example Values** | `HP-21070-01`, `HPAP-019`, `RRID:SAMN18434646` |

---

### CDE PKB_S_003: Study Accession

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_003 |
| **CDE Name** | study_accession |
| **Question Text** | What is the study or dataset accession that this sample belongs to? |
| **Definition** | The public-repository accession or internal identifier of the study to which this scRNA-seq sample belongs. Serves as the data-provenance pointer. |
| **Data Type** | Text |
| **Input Restrictions** | Accepts GEO (`GSE########`), ArrayExpress (`E-MTAB-####`), BioProject (`PRJNA######`), a PanKbase consortium tag (e.g., `HPAP`), or an internal study identifier. |
| **Permissible Values** | N/A (free text with pattern) |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | No exact match. Analogous to "Study Identifier" / "Accession Number" CDEs. |
| **Terminology Binding** | NCBI GEO, ArrayExpress, NCBI BioProject |
| **PanKbase Tier** | Required |
| **Origin** | Observed (source column: `study`) |
| **Example Values** | `GSE201256`, `GSE251730`, `HPAP` |

---

## 2. LIBRARY & PLATFORM

### CDE PKB_S_004: Library Chemistry

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_004 |
| **CDE Name** | library_chemistry |
| **Question Text** | Which library chemistry version was used to construct this single-cell RNA-seq library? |
| **Definition** | The chemistry version of the library-preparation kit used to generate this scRNA-seq library. For 10x Genomics workflows this refers to the Chromium chemistry version (V1, V2, V3, V3.1). Non-10x protocols are recorded as `Other`. |
| **Data Type** | Value List |
| **Permissible Values** | `V1`, `V2`, `V3`, `V3.1`, `Multiome`, `Other`, `Unknown` |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | No exact match. |
| **Terminology Binding** | EFO: `V2`→EFO:0009899, `V3`→EFO:0009922 |
| **PanKbase Tier** | Required |
| **Origin** | Observed (source column: `chemistry`) |
| **Example Values** | `V3`, `V2` |

---

### CDE PKB_S_005: Library Prep Kit

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_005 |
| **CDE Name** | library_prep_kit |
| **Question Text** | Which library preparation kit was used for this sample? |
| **Definition** | Free-text identification of the scRNA-seq library-preparation kit and catalog number where available. |
| **Data Type** | Text |
| **Permissible Values** | N/A |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | **Inferred** — not present in `data/metadata_for_DEG.rds`. Added as a commonly-expected scRNA-seq metadata element; may be removed if no source populates it. |
| **Example Values** | `10x Genomics Chromium Single Cell 3' v3` |

---

### CDE PKB_S_006: Sequencing Platform

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_006 |
| **CDE Name** | sequencing_platform |
| **Question Text** | Which sequencing platform was used to sequence this library? |
| **Definition** | The sequencing instrument used, ideally as manufacturer + model. |
| **Data Type** | Text |
| **Permissible Values** | N/A (free text) |
| **Unit of Measure** | N/A |
| **Terminology Binding** | EFO / OBI (sequencing instrument) |
| **PanKbase Tier** | Desired |
| **Origin** | **Inferred** — not present in `data/metadata_for_DEG.rds`. Added as a commonly-expected scRNA-seq metadata element. |
| **Example Values** | `Illumina NovaSeq 6000`, `Illumina HiSeq 4000` |

---

### CDE PKB_S_007: Alignment Tool

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_007 |
| **CDE Name** | alignment_tool |
| **Question Text** | Which tool was used to align and count reads for this sample? |
| **Definition** | The primary software used to align sequencing reads and produce a cell-by-gene count matrix. |
| **Data Type** | Value List |
| **Permissible Values** | `CellRanger`, `STARsolo`, `Alevin`, `Alevin-fry`, `Kallisto\|Bustools`, `Other`, `Unknown` |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | **Inferred** — not present in `data/metadata_for_DEG.rds`. Added as a commonly-expected scRNA-seq metadata element. |

---

### CDE PKB_S_008: Reference Genome

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_008 |
| **CDE Name** | reference_genome |
| **Question Text** | Which reference genome build was used for alignment? |
| **Definition** | The human reference genome build (and annotation bundle, when known) used to align reads. |
| **Data Type** | Text |
| **Permissible Values** | N/A (free text; commonly `GRCh38`, `GRCh38-2020-A`) |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | **Inferred** — not present in `data/metadata_for_DEG.rds`. Added as a commonly-expected scRNA-seq metadata element. |
| **Example Values** | `GRCh38`, `refdata-gex-GRCh38-2020-A` |

---

### CDE PKB_S_009: CellRanger Version

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_009 |
| **CDE Name** | cellranger_version |
| **Question Text** | If CellRanger was used, which version? |
| **Definition** | The CellRanger version string. Applies when `alignment_tool == CellRanger`. |
| **Data Type** | Text |
| **Input Restrictions** | Should match `MAJOR.MINOR[.PATCH]`. |
| **Permissible Values** | N/A |
| **Unit of Measure** | N/A |
| **PanKbase Tier** | Desired |
| **Origin** | **Inferred** — not present in `data/metadata_for_DEG.rds`. Added as a commonly-expected scRNA-seq metadata element. |
| **Example Values** | `7.1.0`, `6.1.2` |

---

## 3. CELL CALLING

### CDE PKB_S_010: Number of Cells

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_010 |
| **CDE Name** | n_cells |
| **Question Text** | How many cells passed QC and are included in this sample's expression matrix? |
| **Definition** | The per-sample post-QC cell count (after filtering low-quality barcodes, doublets, and/or ambient-RNA-dominated droplets, as applicable). |
| **Data Type** | Number (integer) |
| **Input Restrictions** | 0 ≤ value ≤ 1,000,000 |
| **Permissible Values** | N/A |
| **Unit of Measure** | cells |
| **PanKbase Tier** | Desired |
| **Origin** | **Inferred** — not present in `data/metadata_for_DEG.rds`. Added as a commonly-expected scRNA-seq metadata element. |

---

## 4. SEQUENCING QC

### CDE PKB_S_011: Mean UMI Count per Cell

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_011 |
| **CDE Name** | mean_umi_count_per_cell |
| **Question Text** | What is the mean UMI (nCount_RNA) count per cell for this sample? |
| **Definition** | Mean total UMI counts per cell, computed over cells passing QC. Corresponds to the `nCount_RNA` column in a Seurat object. |
| **Data Type** | Number |
| **Input Restrictions** | 0 ≤ value ≤ 1,000,000 |
| **Unit of Measure** | UMIs/cell |
| **PanKbase Tier** | Desired |
| **Origin** | Observed (source column: `mean_nCount_RNA`) |

---

### CDE PKB_S_012: Mean Genes per Cell

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_012 |
| **CDE Name** | mean_genes_per_cell |
| **Question Text** | What is the mean number of detected genes (nFeature_RNA) per cell for this sample? |
| **Definition** | Mean number of genes with >0 counts per cell. Corresponds to `nFeature_RNA` in a Seurat object. |
| **Data Type** | Number |
| **Input Restrictions** | 0 ≤ value ≤ 100,000 |
| **Unit of Measure** | genes/cell |
| **PanKbase Tier** | Desired |
| **Origin** | Observed (source column: `mean_nFeature_RNA`) |

---

### CDE PKB_S_013: Mean Total Reads per Cell

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_013 |
| **CDE Name** | mean_total_reads_per_cell |
| **Question Text** | What is the mean number of total sequencing reads per cell for this sample? |
| **Definition** | Mean number of sequencing reads (pre-filtering) per cell. |
| **Data Type** | Number |
| **Input Restrictions** | 0 ≤ value ≤ 100,000,000 |
| **Unit of Measure** | reads/cell |
| **PanKbase Tier** | Desired |
| **Origin** | Observed (source column: `mean_rna_total_reads`) |

---

### CDE PKB_S_014: Mean Uniquely Mapped Reads per Cell

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_014 |
| **CDE Name** | mean_uniquely_mapped_reads_per_cell |
| **Question Text** | What is the mean number of uniquely mapped reads per cell? |
| **Definition** | Mean number of reads per cell that align to a single location in the reference genome. |
| **Data Type** | Number |
| **Input Restrictions** | 0 ≤ value ≤ 100,000,000 |
| **Unit of Measure** | reads/cell |
| **PanKbase Tier** | Desired |
| **Origin** | Observed (source column: `mean_rna_uniquely_mapped_reads`) |

---

### CDE PKB_S_015: Mean Secondary Alignments per Cell

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_015 |
| **CDE Name** | mean_secondary_alignments_per_cell |
| **Question Text** | What is the mean number of secondary alignments per cell? |
| **Definition** | Mean per-cell count of secondary alignments (SAM flag 0x100) — alignments to multiple locations in the reference. |
| **Data Type** | Number |
| **Input Restrictions** | 0 ≤ value ≤ 100,000,000 |
| **Unit of Measure** | alignments/cell |
| **PanKbase Tier** | Desired |
| **Origin** | Observed (source column: `mean_rna_secondary_alignments`) |

---

### CDE PKB_S_016: Mean Supplementary Alignments per Cell

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_016 |
| **CDE Name** | mean_supplementary_alignments_per_cell |
| **Question Text** | What is the mean number of supplementary (chimeric) alignments per cell? |
| **Definition** | Mean per-cell count of supplementary alignments (SAM flag 0x800). For standard scRNA-seq pipelines this is typically 0. Retained for forward compatibility with chimeric-aware aligners. |
| **Data Type** | Number |
| **Input Restrictions** | 0 ≤ value ≤ 100,000,000 |
| **Unit of Measure** | alignments/cell |
| **PanKbase Tier** | Desired |
| **Origin** | Observed (source column: `mean_rna_supplementary_alignments`; value is 0 for all 227 samples in the reference RDS) |

---

## 5. AMBIENT RNA (CELLBENDER)

### CDE PKB_S_017: Mean CellBender Cell Probability

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_017 |
| **CDE Name** | mean_cellbender_cell_probability |
| **Question Text** | What is the mean CellBender cell-probability score across cells in this sample? |
| **Definition** | Mean of the per-barcode posterior probability (output of CellBender's `remove-background` workflow) that the barcode represents a true cell rather than an empty droplet / ambient RNA. QC-passing samples are typically ≈1. |
| **Data Type** | Number |
| **Input Restrictions** | 0.0 ≤ value ≤ 1.0 |
| **Unit of Measure** | dimensionless |
| **Terminology Binding** | CellBender (Broad Institute) |
| **PanKbase Tier** | Desired |
| **Origin** | Observed (source column: `mean_cell_probability`) |

---

### CDE PKB_S_018: Mean Post-CellBender UMIs per Cell

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_018 |
| **CDE Name** | mean_post_cellbender_umis_per_cell |
| **Question Text** | What is the mean post-CellBender UMI count per cell? |
| **Definition** | Mean UMI count per cell after CellBender removes ambient-RNA contamination. Should be ≤ `mean_umi_count_per_cell`. |
| **Data Type** | Number |
| **Input Restrictions** | 0 ≤ value ≤ 1,000,000 |
| **Unit of Measure** | UMIs/cell |
| **PanKbase Tier** | Desired |
| **Origin** | Observed (source column: `mean_post_cellbender_umis`) |

---

### CDE PKB_S_019: Mean % UMIs Removed by CellBender

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_019 |
| **CDE Name** | mean_pct_cellbender_removed |
| **Question Text** | What percentage of UMIs was removed on average per cell by CellBender? |
| **Definition** | Mean per-cell percentage of UMIs attributed to ambient RNA and removed by CellBender. |
| **Data Type** | Number |
| **Input Restrictions** | 0.0 ≤ value ≤ 100.0 |
| **Unit of Measure** | % |
| **PanKbase Tier** | Desired |
| **Origin** | Observed (source column: `mean_pct_cellbender_removed`) |

---

## 6. MITOCHONDRIAL QC

### CDE PKB_S_020: Mean % Mitochondrial Reads

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_S_020 |
| **CDE Name** | mean_pct_mitochondrial_reads |
| **Question Text** | What is the mean percentage of reads mapping to mitochondrial genes per cell? |
| **Definition** | Mean per-cell percentage of reads/UMIs aligning to mitochondrial genes (commonly computed from `MT-` gene-symbol patterns). Values >20% typically indicate stressed or dying cells. |
| **Data Type** | Number |
| **Input Restrictions** | 0.0 ≤ value ≤ 100.0 |
| **Unit of Measure** | % |
| **PanKbase Tier** | Desired |
| **Origin** | Observed (source column: `mean_rna_pct_mitochondrial`) |

---

## Design Decisions

This section documents non-obvious choices made while defining these CDEs.

1. **Separate collection rather than extending donor CDEs.** Per project instruction, scRNA-seq metadata lives in its own CDE collection (`pankbase_scrnaseq_cdes`) so it can evolve independently and be added/removed without affecting donor CDE consumers. Donor-scope fields in the source RDS (`sex`, `age`, `bmi`, `diabetes_status_description`, `ethnicity`, autoantibodies) are **not** redefined here — they already exist in `pankbase_donor_cdes.json`.
2. **Cross-reference via `donor_rrid_ref` (PKB_S_002).** Rather than duplicating donor fields, a foreign-key CDE links each sample back to PKB_D_001 (`donor_rrid`). The JSON encodes this via a `cross_reference` block (`{schema, cde_id, cde_name, relationship}`) so consuming tools can programmatically resolve the join.
3. **Skipped columns.** `tissue_source` and `isolation_center` (islet isolation) and `treatments` (islet treatment) were excluded per instruction. Treatment parsing is out of scope because only partial treatment metadata is available; `sample_id` is retained as an opaque string and not decomposed.
4. **Inferred vs. observed fields.** 13 CDEs correspond directly to columns in `data/metadata_for_DEG.rds` ("Observed" origin). 6 additional CDEs (`library_prep_kit`, `sequencing_platform`, `alignment_tool`, `reference_genome`, `cellranger_version`, `n_cells`) are explicitly marked **Inferred** in both the JSON `notes` and this MD — they are commonly-expected scRNA-seq metadata drawn from HCA / CELLxGENE / CellRanger / Seurat conventions but are not populated by the reference RDS. These are `Desired` tier to reflect that contributors may not always have them.
5. **`mean_rna_supplementary_alignments` retained.** Value is 0 for all 227 samples in the reference RDS; kept per project instruction for forward compatibility.
6. **Required vs. Desired.** Only the three sample-identification CDEs (`sample_id`, `donor_rrid_ref`, `study_accession`) and the library-chemistry CDE are **Required**. All QC-metric CDEs are **Desired** because different pipelines emit different summaries.
7. **Schema version 0.1.** This collection is new and expected to evolve after collaborator review (hence 0.x rather than 1.0). The donor CDE schema remains at 1.0 and is unchanged by this work.
8. **NIH CDE Repository.** Searched for existing elements covering scRNA-seq sample identification, 10x library chemistry, CellBender QC, and per-cell UMI / gene / mitochondrial summaries. No direct matches — this was expected, as NIH CDEs today focus on clinical/phenotypic elements. The definitions below therefore follow NIH format but are newly authored.

---

## Version History

| Version | Date | Changes |
|---------|------|---------|
| 0.1 | 2026-04-23 | Initial draft. 20 CDEs = 13 observed + 1 donor cross-reference + 6 inferred common fields. All inferred fields marked with "Origin: Inferred" and `Desired` tier. |
