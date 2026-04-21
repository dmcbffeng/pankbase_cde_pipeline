# PanKbase Donor Metadata: Common Data Element (CDE) Collection v1.0

## Overview

This document defines the formal Common Data Elements (CDEs) for PanKbase donor metadata. Each CDE follows the NIH CDE format (ISO/IEC 11179-aligned) with the following attributes:

- **CDE ID**: PanKbase-assigned identifier (PKB_D_xxx)
- **CDE Name**: Short, standardized variable name
- **Question Text**: The data collection prompt
- **Definition**: Precise description of what the element captures
- **Data Type**: Number, Text, Value List, Date, Boolean
- **Input Restrictions**: Constraints on the value (e.g., range, format)
- **Permissible Values**: Allowed values for enumerated types
- **Unit of Measure**: UCUM-standard unit where applicable
- **NIH CDE Reference**: Existing NIH CDE mapping (if available)
- **Terminology Binding**: Ontology/vocabulary references
- **PanKbase Tier**: Required / Desired (from PANKBASE META DATA_MB.xlsx)
- **PanKbase Standard Tier**: Tier 0-3 (from PanKbase human donor standards)

CDEs are organized by category: Donor Identification, Demographics, Medical, Autoantibodies, Pancreas Processing, and Sample Transportation.

---

## 1. DONOR IDENTIFICATION

### CDE PKB_D_001: RRID

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_001 |
| **CDE Name** | donor_rrid |
| **Question Text** | What is the Research Resource Identifier (RRID) for this donor? |
| **Definition** | A unique, persistent identifier assigned to the donor specimen through the RRID system (Research Resource Identifiers), enabling unambiguous cross-referencing across repositories and publications. Format: "RRID:SAMN" followed by a numeric string (BioSample accession). |
| **Data Type** | Text |
| **Input Restrictions** | Must match pattern `RRID:SAMN[0-9]+`. Required field; cannot be null. |
| **Permissible Values** | N/A (free text with format constraint) |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | No direct NIH CDE equivalent. Aligns with FAIR data principles for persistent identifiers. RRID is an NIH-recognized identifier system (see RIN/RRID Initiative). |
| **Terminology Binding** | RRID Portal (https://scicrunch.org/resources) |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | Tier 2 |
| **Example Values** | `RRID:SAMN08769199`, `RRID:SAMN18741978` |

---

### CDE PKB_D_002: Program Donor ID

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_002 |
| **CDE Name** | program_donor_id |
| **Question Text** | What is the program-specific donor identifier? |
| **Definition** | The unique identifier assigned to the donor by the contributing research program or consortium. Typically formatted as a program prefix followed by a numeric code (e.g., "HPAP-001", "IIDP-1234"). This serves as the primary cross-reference between PanKbase and the source consortium. |
| **Data Type** | Text |
| **Input Restrictions** | Non-empty string. Must be unique within the contributing program. |
| **Permissible Values** | N/A (free text, program-specific format) |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | Maps conceptually to "Patient/Subject Identifier" CDEs in multiple NIH collections. |
| **Terminology Binding** | N/A |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | Tier 0 |
| **Example Values** | `HPAP-001`, `HPAP-197` |

---

### CDE PKB_D_003: Cohort ID

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_003 |
| **CDE Name** | cohort_id |
| **Question Text** | What is the contributing consortium or cohort for this donor? |
| **Definition** | The name or abbreviation of the research consortium, program, or cohort from which the donor data originates. This identifies the provenance of the donor record and links to the data governance and collection protocols used. |
| **Data Type** | Value List |
| **Input Restrictions** | Must be a value from the permissible values list. |
| **Permissible Values** | `HPAP` = Human Pancreas Analysis Program; `IIDP` = Integrated Islet Distribution Program; `INSPIRE` = Innovative Stimuli to Promote Islet Research Excellence; `TIGER` = Tissue Interrogation of Gene Expression in Research; `nPOD` = Network for Pancreatic Organ Donors with Diabetes; `IsletCore` = University of Alberta IsletCore; `Other` = Other consortium (specify in notes) |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | No direct NIH CDE equivalent. Analogous to "Contributing Study/Site" metadata. |
| **Terminology Binding** | N/A |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | N/A (administrative) |
| **Example Values** | `HPAP`, `IIDP` |

---

## 2. DEMOGRAPHICS

### CDE PKB_D_004: Reported Gender

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_004 |
| **CDE Name** | sex_at_birth |
| **Question Text** | What is the donor's sex at birth? |
| **Definition** | The sex assigned to the donor at birth based on biological and physiological characteristics, including chromosomes, hormones, and reproductive anatomy. This field captures biological sex for research purposes, consistent with NIH policy on Sex as a Biological Variable (SABV, NOT-OD-15-102). Note: The source metadata uses "Reported Gender (M/F)" but PanKbase aligns with the NIH-recommended terminology "Sex at Birth." |
| **Data Type** | Value List |
| **Input Restrictions** | Single selection from permissible values. Required field. |
| **Permissible Values** | `Male` = Male sex at birth; `Female` = Female sex at birth; `Other` = Sex at birth does not fit into binary categories; `Unknown` = Sex at birth is not known or not reported |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | Maps to NIH CDE "Sex at Birth" / PanKbase Tier 1 "Sex at Birth". Aligns with OMB standards and USCDI "Sex (Assigned at Birth)" data class. NIH CDE Repository contains multiple sex/gender CDEs; the recommended approach uses "Sex at Birth" with values Male/Female/Other/Unknown. |
| **Terminology Binding** | NCI Thesaurus: C28421 (Male), C16576 (Female); SNOMED CT: 248153007 (Male), 248152002 (Female) |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | Tier 1 |
| **Example Values** | `Male`, `Female` |
| **Mapping Notes** | HPAP uses `sex` with values "Male"/"Female". IIDP uses `Sex` with values "Male"/"Female". Both map directly. |

---

### CDE PKB_D_005: Age

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_005 |
| **CDE Name** | age_years |
| **Question Text** | What is the donor's age at the time of donation? |
| **Definition** | The age of the donor at the time of organ/tissue procurement, reported in years. For donors younger than 2 years (24 months), age should be reported in months to maintain precision. Age is calculated from date of birth to date of procurement. This is a core demographic variable required for all biomedical research. |
| **Data Type** | Number |
| **Input Restrictions** | Non-negative numeric value. If donor age < 2 years, report in months with `age_unit` = "months". Otherwise, report as integer years. Range: 0-120 years. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | Years (UCUM: `a`); or Months (UCUM: `mo`) for donors < 24 months |
| **NIH CDE Reference** | Maps to NIH CDE "Age at Enrollment" / "Person Age" concepts. NIH Inclusion Across the Lifespan policy requires age at enrollment. NIH CDE Repository recommends reporting in months for young children. The PanKbase Tier 0 "Age (years)" is a strictly required field. |
| **Terminology Binding** | UCUM for units |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | Tier 0 |
| **Example Values** | `43`, `26`, `47`, `5` (months, for infant donors) |
| **Mapping Notes** | HPAP field: `age_years` (integer). IIDP field: `Age (years)` (integer string). Both report in whole years. |

---

### CDE PKB_D_006: BMI

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_006 |
| **CDE Name** | bmi |
| **Question Text** | What is the donor's body mass index (BMI)? |
| **Definition** | Body Mass Index, calculated as weight in kilograms divided by height in meters squared (kg/m^2). BMI is a widely used screening measure for body weight categories. The value should be calculated from measured height and weight at the time closest to organ procurement. |
| **Data Type** | Number |
| **Input Restrictions** | Positive decimal value. Typical range: 10.0-80.0 kg/m^2. Precision: 1 decimal place. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | kg/m^2 (UCUM: `kg/m2`) |
| **NIH CDE Reference** | Maps to NIDA CTN CDE "Body Mass Index (BMI)" and similar CDEs in multiple NIH collections. Standard biomedical variable. PanKbase Tier 1 required field. |
| **Terminology Binding** | LOINC: 39156-5 (Body mass index); UCUM for unit |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | Tier 1 |
| **Example Values** | `29.5`, `32.2`, `16.4`, `24.5` |
| **Mapping Notes** | HPAP field: `bmi` (decimal). IIDP field: `BMI` (decimal string). Direct mapping. |

---

### CDE PKB_D_007: Self-Reported Race and Ethnicity

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_007 |
| **CDE Name** | race_ethnicity |
| **Question Text** | What is the donor's self-reported race and ethnicity? |
| **Definition** | The donor's self-identified racial and ethnic background. Following NIH/OMB standards, ethnicity and race are collected as two components: (1) Ethnicity: Hispanic or Latino vs. Not Hispanic or Latino; (2) Race: one or more of the five OMB minimum categories. When source data combines race and ethnicity into a single field, best-effort parsing should be applied. PanKbase stores both components. |
| **Data Type** | Composite (two sub-elements below) |
| **Input Restrictions** | See sub-elements PKB_D_007a and PKB_D_007b. |
| **Permissible Values** | See sub-elements. |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | Maps to NIH/OMB Race and Ethnicity CDEs (NOT-OD-01-053). NIH requires self-reporting with ethnicity collected first, then race (with multi-select). NIH CDE Repository has an "Ethnicity" form (tinyId: mJQYD354Q) and race CDEs. |
| **Terminology Binding** | OMB 1997 Revised Standards; CDC Race/Ethnicity codes |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | Tier 2 |

#### CDE PKB_D_007a: Ethnicity

| Attribute | Value |
|-----------|-------|
| **CDE Name** | ethnicity |
| **Question Text** | Is the donor of Hispanic or Latino origin? |
| **Data Type** | Value List |
| **Permissible Values** | `Hispanic or Latino` = A person of Cuban, Mexican, Puerto Rican, South or Central American, or other Spanish culture or origin, regardless of race; `Not Hispanic or Latino` = Not of Hispanic or Latino origin; `Unknown` = Ethnicity not reported or not known |
| **Example Values** | `Hispanic or Latino`, `Not Hispanic or Latino` |

#### CDE PKB_D_007b: Race

| Attribute | Value |
|-----------|-------|
| **CDE Name** | race |
| **Question Text** | What is the donor's self-reported race? (Select all that apply) |
| **Data Type** | Value List (multi-select) |
| **Permissible Values** | `American Indian or Alaska Native` = A person having origins in any of the original peoples of North and South America who maintains tribal affiliation or community attachment; `Asian` = A person having origins in any of the original peoples of the Far East, Southeast Asia, or the Indian subcontinent; `Black or African American` = A person having origins in any of the Black racial groups of Africa; `Native Hawaiian or Other Pacific Islander` = A person having origins in any of the original peoples of Hawaii, Guam, Samoa, or other Pacific Islands; `White` = A person having origins in any of the original peoples of Europe, the Middle East, or North Africa; `Multiracial` = A person who identifies with two or more races; `Unknown` = Race not reported or not known |
| **Mapping Notes** | HPAP uses `race` with values: "Caucasian" -> "White", "African American" -> "Black or African American", "Hispanic" -> requires re-mapping to ethnicity="Hispanic or Latino" with race separately assessed, "Asian" -> "Asian", "American Indian or Alaska Native" -> direct, "Biracial" -> "Multiracial". IIDP separates `Race` and `Ethnicity` columns - `Race` values map similarly; "Not Documented"/"Not Available" -> "Unknown". |

---

## 3. MEDICAL

### CDE PKB_D_008: Diabetes Status

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_008 |
| **CDE Name** | diabetes_status |
| **Question Text** | What is the donor's diabetes status at time of donation? |
| **Definition** | The clinical diabetes classification of the donor at the time of organ procurement. This is a critical variable for PanKbase as the knowledgebase focuses on pancreas biology and diabetes research. The classification should reflect the most current clinical assessment. |
| **Data Type** | Value List |
| **Input Restrictions** | Single selection from permissible values. Required field. |
| **Permissible Values** | `No diabetes` = No diagnosis of diabetes mellitus (control); `Type 1 diabetes (T1D)` = Autoimmune destruction of pancreatic beta cells; `Type 2 diabetes (T2D)` = Insulin resistance and relative insulin deficiency; `Gestational diabetes` = Diabetes first diagnosed during pregnancy; `MODY` = Maturity-onset diabetes of the young (monogenic); `LADA` = Latent autoimmune diabetes in adults; `Neonatal diabetes` = Diabetes diagnosed within the first 6 months of life; `Type 3c diabetes` = Diabetes secondary to exocrine pancreatic disease; `Cystic fibrosis-related diabetes` = Diabetes in the context of cystic fibrosis; `Steroid-induced diabetes` = Diabetes resulting from corticosteroid use; `Wolfram syndrome` = Diabetes as part of Wolfram syndrome; `Other` = Other form of diabetes not listed (specify in notes); `Unknown` = Diabetes status not known or not assessed |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | No single NIH CDE covers this granularity for pancreas-specific research. PanKbase defines its own value set based on clinical classification. PanKbase standard Tier 1 field "Description of diabetes status." |
| **Terminology Binding** | MONDO:0005015 (diabetes mellitus); MONDO:0007179 (T1D); MONDO:0005148 (T2D); MONDO:0008242 (MODY); MONDO:0015028 (LADA); MONDO:0005159 (gestational diabetes); MONDO:0019207 (neonatal diabetes); MONDO:0005340 (type 3c); MONDO:0019071 (CF-related diabetes) |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | Tier 1 |
| **Example Values** | `Type 1 diabetes (T1D)`, `Type 2 diabetes (T2D)`, `No diabetes` |
| **Mapping Notes** | HPAP `clinical_diagnosis`: "T1DM"/"T1DM Recent onset"/"T1DM (recent DKA)"/"Recent T1DM Unsuspected" -> "Type 1 diabetes (T1D)"; "T2DM"/"T2DM Gastric bypass"/"T2DM (? prediabetic)"/"T2DM polycystic ovaries" -> "Type 2 diabetes (T2D)"; "T1D control"/"T2D control" -> "No diabetes"; "T1DM or MODY, undetermined" -> "Other". IIDP `Disease`: "Non-Diabetic" -> "No diabetes"; "T1D" -> "Type 1 diabetes (T1D)"; "T2D" -> "Type 2 diabetes (T2D)"; "Not Available" -> "Unknown". |

---

### CDE PKB_D_009: HbA1c

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_009 |
| **CDE Name** | hba1c_percent |
| **Question Text** | What is the donor's most recent glycated hemoglobin (HbA1c) value? |
| **Definition** | The percentage of hemoglobin that is glycated (HbA1c), reflecting average blood glucose levels over the preceding 2-3 months. This is a key biomarker for diabetes diagnosis and glycemic control. The value should represent the most recent measurement prior to organ procurement. Clinical interpretation: <5.7% = Normal; 5.7-6.4% = Prediabetes; >=6.5% = Diabetes. |
| **Data Type** | Number |
| **Input Restrictions** | Positive decimal value. Typical range: 3.0-20.0%. Precision: 1 decimal place. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | % (UCUM: `%`) |
| **NIH CDE Reference** | Maps to standard HbA1c laboratory CDEs. LOINC 4548-4 (Hemoglobin A1c/Hemoglobin.total in Blood). PanKbase standard Tier 2 field. |
| **Terminology Binding** | LOINC: 4548-4; UCUM for unit |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | Tier 2 |
| **Example Values** | `5.7`, `9.8`, `5.6`, `5.4` |
| **Mapping Notes** | HPAP field: `hba1c` (decimal). IIDP: not a standard column in HIPP report (available in separate clinical data). Direct numeric mapping. |

---

### CDE PKB_D_010: HbA1c-Adjusted Diabetes Status

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_010 |
| **CDE Name** | hba1c_adjusted_diabetes_status |
| **Question Text** | What is the donor's diabetes classification based on HbA1c levels? |
| **Definition** | A derived diabetes status classification based on the donor's HbA1c value, following American Diabetes Association (ADA) criteria. This provides a standardized, lab-based classification that may differ from the clinical diagnosis. This is computed from HbA1c: <5.7% = Normal, 5.7-6.4% = Prediabetes, >=6.5% = Diabetes. |
| **Data Type** | Value List |
| **Input Restrictions** | Single selection. Derived from HbA1c value (PKB_D_009). |
| **Permissible Values** | `Normal` = HbA1c < 5.7%; `Prediabetes` = HbA1c 5.7-6.4%; `Diabetes` = HbA1c >= 6.5%; `Unknown` = HbA1c value not available |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | PanKbase-defined. Based on ADA Standards of Medical Care in Diabetes. Maps to PanKbase standard Tier 3 "Derived diabetes status." |
| **Terminology Binding** | ADA diagnostic criteria for HbA1c thresholds |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | Tier 3 |
| **Example Values** | `Normal`, `Diabetes`, `Prediabetes` |
| **Mapping Notes** | Can be computed from PKB_D_009 (HbA1c) value. Not typically provided as a source field. |

---

### CDE PKB_D_011: Glucose-Lowering Therapy

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_011 |
| **CDE Name** | glucose_lowering_therapy |
| **Question Text** | Was the donor receiving any glucose-lowering therapy at the time of donation? If yes, specify. |
| **Definition** | Documentation of any pharmacological or non-pharmacological treatments for hyperglycemia or diabetes that the donor was receiving at the time of or shortly before organ procurement. This includes oral hypoglycemic agents, injectable therapies (insulin, GLP-1 agonists), and relevant surgical interventions (e.g., bariatric surgery). |
| **Data Type** | Text |
| **Input Restrictions** | Free text description. Use "None" if no therapy. Use "Unknown" if not assessed. |
| **Permissible Values** | N/A (free text) |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | PanKbase-defined. Aligns with PanKbase standard Tier 2 "Other Therapy." Related to medication history CDEs in clinical trial data collections. |
| **Terminology Binding** | RxNorm for medication names (recommended) |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | Tier 2 |
| **Example Values** | `Metformin - 2000mg/d`, `Insulin sliding scale`, `None`, `Unknown` |
| **Mapping Notes** | HPAP: found in `medical_history_medications` sheet, condition="Type of Diabetes", medication field. IIDP: not in standard HIPP report. |

---

### CDE PKB_D_012: Other Disease States

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_012 |
| **CDE Name** | other_disease_states |
| **Question Text** | Does the donor have any other significant disease states or medical conditions? |
| **Definition** | Documentation of clinically significant comorbid conditions beyond diabetes status. This includes but is not limited to hypertension, cardiovascular disease, autoimmune diseases, cancer, obesity-related conditions, and other chronic diseases that may influence pancreas biology or islet function. |
| **Data Type** | Text |
| **Input Restrictions** | Free text, semicolon-separated list of conditions. Use "None" if no other diseases. Use "Unknown" if not assessed. |
| **Permissible Values** | N/A (free text) |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | PanKbase-defined. Maps to general "Medical History" CDEs in multiple NIH collections. |
| **Terminology Binding** | MONDO or ICD-10-CM for disease coding (recommended) |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | N/A |
| **Example Values** | `Hypertension; Hyperlipidemia; CAD`, `None`, `Asthma` |
| **Mapping Notes** | HPAP: reconstructed from `medical_history` sheet (condition + value columns). IIDP: not in standard HIPP report. |

---

### CDE PKB_D_013: Family History of Diabetes

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_013 |
| **CDE Name** | family_history_diabetes |
| **Question Text** | Does the donor have a family history of diabetes? |
| **Definition** | Indicates whether any biological family members of the donor have been diagnosed with diabetes mellitus of any type. If yes, the relationship and type of diabetes should be specified when available. Family history of diabetes is a significant risk factor for both Type 1 and Type 2 diabetes. |
| **Data Type** | Value List |
| **Input Restrictions** | Single selection for the primary indicator. |
| **Permissible Values** | `Yes` = One or more family members diagnosed with diabetes; `No` = No known family history of diabetes; `Unknown` = Family history not known or not assessed |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | PanKbase-defined. PanKbase standard Tier 3 fields: "Family History of Diabetes" (Boolean) and "Family History of Diabetes Relationship" (Array). |
| **Terminology Binding** | N/A |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | Tier 3 |
| **Example Values** | `Yes`, `No`, `Unknown` |
| **Mapping Notes** | HPAP: from `family_medical_history` sheet, condition="Diabetes", value field. IIDP: not in standard HIPP report. |

---

### CDE PKB_D_014: Hospital Stay

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_014 |
| **CDE Name** | hospital_stay_days |
| **Question Text** | How many days was the donor hospitalized prior to organ procurement? |
| **Definition** | The total duration of the donor's hospital stay prior to organ procurement, measured in days. This reflects the period from hospital admission to the time of organ recovery. Prolonged hospital stays can affect organ quality through hemodynamic instability, medication effects, and physiological stress. |
| **Data Type** | Number |
| **Input Restrictions** | Non-negative integer. Range: 0-365 days. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | Days (UCUM: `d`) |
| **NIH CDE Reference** | PanKbase-defined. PanKbase standard Tier 2 "Hospital Stay (hours)" — note PanKbase standard uses hours; the source metadata uses days. PanKbase CDE standardizes to days for alignment with source data. |
| **Terminology Binding** | UCUM for unit |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | Tier 2 |
| **Example Values** | `9`, `8`, `3` |
| **Mapping Notes** | HPAP: not a direct field; can be derived from `admission_datetime_est` and `cross_clamp_datetime_est`. IIDP field: `Hospital Stay (days)` (integer string). Direct mapping from IIDP. |

---

### CDE PKB_D_015: Donation Type

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_015 |
| **CDE Name** | donation_type |
| **Question Text** | What was the type of organ donation? |
| **Definition** | The classification of the organ donation based on the circumstances and clinical determination of death. This directly impacts organ quality, ischemia times, and downstream tissue processing. |
| **Data Type** | Value List |
| **Input Restrictions** | Single selection from permissible values. |
| **Permissible Values** | `DBD` = Donation after Brain Death (donor declared dead by neurological criteria); `DCD` = Donation after Circulatory Death (donor declared dead by cardiopulmonary criteria); `MAID` = Medical Assistance in Dying; `NDD` = Natural Death Donation; `Living` = Living donor; `Unknown` = Donation type not documented |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | PanKbase-defined. PanKbase standard Tier 2 field "Donation Type" with values: "Donation after Circulatory Death", "Donation after Brain Death", "Natural Death Donation", "Medical Assistance in Dying". |
| **Terminology Binding** | N/A |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | Tier 2 |
| **Example Values** | `DBD`, `DCD`, `MAID` |
| **Mapping Notes** | HPAP: derived from `dbd` (Yes/blank) and `dcd` (Yes/blank) fields. If dbd=Yes -> "DBD"; if dcd=Yes -> "DCD". IIDP: not in standard HIPP report. |

---

### CDE PKB_D_016: Cause of Death

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_016 |
| **CDE Name** | cause_of_death |
| **Question Text** | What was the donor's cause of death? |
| **Definition** | The primary medical condition or event that led to the donor's death and subsequent organ procurement. This is clinically relevant as certain causes of death (e.g., anoxia, trauma, cerebrovascular events) can differentially affect organ and islet quality. |
| **Data Type** | Value List |
| **Input Restrictions** | Single selection from permissible values. Free text specification encouraged in notes. |
| **Permissible Values** | `Head Trauma` = Death resulting from traumatic brain injury; `Cerebrovascular/Stroke` = Death resulting from cerebrovascular accident (hemorrhagic or ischemic stroke); `Anoxia` = Death resulting from oxygen deprivation; `Cardiovascular` = Death resulting from cardiac or vascular causes; `DKA` = Death resulting from diabetic ketoacidosis; `Other` = Other cause of death (specify); `Unknown` = Cause of death not documented |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | PanKbase-defined. PanKbase standard Tier 2 field "Cause of Death" (free text). Related to UNOS donor CDEs. |
| **Terminology Binding** | ICD-10 for cause-of-death coding (recommended); SNOMED CT |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | Tier 2 |
| **Example Values** | `Head Trauma`, `Anoxia`, `Cerebrovascular/Stroke` |
| **Mapping Notes** | HPAP field: `cause_of_death` (text). Values require normalization: "Anoxia 2nd CVA" -> "Anoxia" or "Cerebrovascular/Stroke" (judgment); "GSW" -> "Head Trauma"; "Subarachnoid Hemorrhage" -> "Cerebrovascular/Stroke". IIDP: not in standard HIPP report. |

---

### CDE PKB_D_017: Diabetes Duration

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_017 |
| **CDE Name** | diabetes_duration_years |
| **Question Text** | How many years has the donor had diabetes? |
| **Definition** | The duration of time since the donor was first diagnosed with diabetes mellitus, reported in years. This is relevant for understanding disease progression and its effects on pancreatic tissue and islet function. A value of 0 indicates recent diagnosis (within the past year). Null/blank indicates the donor does not have diabetes or duration is unknown. |
| **Data Type** | Number |
| **Input Restrictions** | Non-negative decimal value. Range: 0-120 years. Null if not applicable (non-diabetic) or unknown. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | Years (UCUM: `a`) |
| **NIH CDE Reference** | PanKbase-defined. PanKbase standard Tier 3 field "Diabetes Duration (years)". |
| **Terminology Binding** | UCUM for unit |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | Tier 3 |
| **Example Values** | `18`, `5`, `0.5` |
| **Mapping Notes** | HPAP field: `disease_duration` (text, e.g., "18 years", "5 years"). Requires parsing to extract numeric value. IIDP: not in standard HIPP report. |

---

### CDE PKB_D_018: C-Peptide

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_018 |
| **CDE Name** | c_peptide_ng_ml |
| **Question Text** | What is the donor's C-peptide level? |
| **Definition** | The concentration of C-peptide in blood, a biomarker of endogenous insulin secretion. C-peptide is a byproduct of insulin production and is used to assess residual beta cell function. The fasting/random status of the sample should be noted when available. |
| **Data Type** | Number |
| **Input Restrictions** | Non-negative decimal value. Typical range: 0.0-20.0 ng/mL. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | ng/mL (UCUM: `ng/mL`) |
| **NIH CDE Reference** | PanKbase-defined. PanKbase standard Tier 3 field "C-Peptide (ng/ml)". LOINC: 1986-9 (C-peptide in serum/plasma). |
| **Terminology Binding** | LOINC: 1986-9; UCUM for unit |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | Tier 3 |
| **Example Values** | `0.43`, `0.51`, `9`, `6.73` |
| **Mapping Notes** | HPAP field: `c_peptide_ng_ml` (decimal). Direct mapping. IIDP: not in standard HIPP report. |

---

## 4. AUTOANTIBODIES

### CDE PKB_D_019: Autoantibody - GADA

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_019 |
| **CDE Name** | aab_gada |
| **Question Text** | What is the donor's glutamic acid decarboxylase autoantibody (GADA/GAD65) status and value? |
| **Definition** | The presence and measured level of autoantibodies against glutamic acid decarboxylase 65 (GAD65). GADA is one of the primary autoantibodies associated with Type 1 diabetes and autoimmune destruction of pancreatic beta cells. Results are reported as the measured value and a positive/negative interpretation based on the assay-specific cutoff. |
| **Data Type** | Composite (sub-elements below) |
| **NIH CDE Reference** | PanKbase-defined. PanKbase standard Tier 3 autoantibody fields. |
| **Terminology Binding** | LOINC: 56540-2 (GAD65 antibody); UCUM for unit |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | Tier 3 |

| Sub-element | Data Type | Unit | Description |
|-------------|-----------|------|-------------|
| `aab_gada_positive` | Boolean | N/A | True if GADA value exceeds assay cutoff (typically >=20 unit/mL); False otherwise |
| `aab_gada_value` | Number | unit/mL | Measured GADA concentration |
| `aab_gada_assay` | Text | N/A | Assay method used for measurement |

| **Mapping Notes** | HPAP: `aab_gada` field contains "0" or "1" (binary positive/negative); `aab_gada_level` contains the raw value (e.g., "0/20" = value/cutoff, or "119/20"). Also available in `confirmatory_results` sheet. Cutoff from `aab_lookup`: GADA-65 = 20. IIDP: not in standard HIPP report. |

---

### CDE PKB_D_020: Autoantibody - IAA

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_020 |
| **CDE Name** | aab_iaa |
| **Question Text** | What is the donor's insulin autoantibody (IAA) status and value? |
| **Definition** | The presence and measured level of autoantibodies against insulin (IAA). IAA is one of the islet autoantibodies predictive of Type 1 diabetes, particularly in young children. |
| **Data Type** | Composite |
| **NIH CDE Reference** | PanKbase-defined. |
| **Terminology Binding** | LOINC: 56541-0 (Insulin antibody); UCUM for unit |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | Tier 3 |

| Sub-element | Data Type | Unit | Description |
|-------------|-----------|------|-------------|
| `aab_iaa_positive` | Boolean | N/A | True if IAA value exceeds assay cutoff (typically >=0.01 unit/mL) |
| `aab_iaa_value` | Number | unit/mL | Measured IAA concentration |
| `aab_iaa_assay` | Text | N/A | Assay method used |

| **Mapping Notes** | HPAP: `aab_iaa` (0/1); `aab_iaa_level` (value/cutoff format, e.g., "0.003/0.01"). Cutoff from `aab_lookup`: Insulin AAB = 0.01. IIDP: not in standard HIPP report. |

---

### CDE PKB_D_021: Autoantibody - IA-2

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_021 |
| **CDE Name** | aab_ia2 |
| **Question Text** | What is the donor's islet antigen-2 autoantibody (IA-2A) status and value? |
| **Definition** | The presence and measured level of autoantibodies against islet antigen-2 (IA-2/ICA512). IA-2A is an islet autoantibody used in the prediction and diagnosis of Type 1 diabetes. |
| **Data Type** | Composite |
| **NIH CDE Reference** | PanKbase-defined. |
| **Terminology Binding** | LOINC: 56542-8 (IA-2 antibody); UCUM for unit |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | Tier 3 |

| Sub-element | Data Type | Unit | Description |
|-------------|-----------|------|-------------|
| `aab_ia2_positive` | Boolean | N/A | True if IA-2 value exceeds assay cutoff (typically >=5 unit/mL) |
| `aab_ia2_value` | Number | unit/mL | Measured IA-2 concentration |
| `aab_ia2_assay` | Text | N/A | Assay method used |

| **Mapping Notes** | HPAP: `aab_ia_2` (0/1); `aab_ia_2_level` (value/cutoff format, e.g., "0/5"). Cutoff from `aab_lookup`: IA-2 = 5. IIDP: not in standard HIPP report. |

---

### CDE PKB_D_022: Autoantibody - ZnT8

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_022 |
| **CDE Name** | aab_znt8 |
| **Question Text** | What is the donor's zinc transporter 8 autoantibody (ZnT8A) status and value? |
| **Definition** | The presence and measured level of autoantibodies against zinc transporter 8 (ZnT8). ZnT8A is the most recently identified major islet autoantibody and is associated with Type 1 diabetes. |
| **Data Type** | Composite |
| **NIH CDE Reference** | PanKbase-defined. |
| **Terminology Binding** | LOINC: 63474-1 (ZnT8 antibody); UCUM for unit |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | Tier 3 |

| Sub-element | Data Type | Unit | Description |
|-------------|-----------|------|-------------|
| `aab_znt8_positive` | Boolean | N/A | True if ZnT8 value exceeds assay cutoff (typically >=0.02 unit/mL) |
| `aab_znt8_value` | Number | unit/mL | Measured ZnT8 concentration |
| `aab_znt8_assay` | Text | N/A | Assay method used |

| **Mapping Notes** | HPAP: `aab_znt8` (0/1); `aab_znt8_level` (value/cutoff format, e.g., "0/0.02"). Cutoff from `aab_lookup`: ZnT8 = 0.02. IIDP: not in standard HIPP report. |

---

## 5. PANCREAS PROCESSING

### CDE PKB_D_023: Isolation Center

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_023 |
| **CDE Name** | isolation_center |
| **Question Text** | Which center performed the pancreas/islet isolation? |
| **Definition** | The name or identifier of the laboratory or center that performed the islet isolation procedure from the donor pancreas. This is important for quality control and for understanding inter-center variability in isolation outcomes. |
| **Data Type** | Text |
| **Input Restrictions** | Non-empty string. Standardized center names are preferred. |
| **Permissible Values** | N/A (free text, but standardized center abbreviations recommended) |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | PanKbase-defined. Maps conceptually to "Site/Center" CDEs in multi-center studies. |
| **Terminology Binding** | N/A |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | N/A |
| **Example Values** | `SC-ICRC`, `UPENN`, `nPOD` |
| **Mapping Notes** | HPAP: `allocation_via` or derived from lab information. IIDP field: `Center`. Direct mapping. |

---

### CDE PKB_D_024: Cold Ischemia Time

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_024 |
| **CDE Name** | cold_ischemia_time_hours |
| **Question Text** | What is the cold ischemia time for the donated pancreas? |
| **Definition** | The duration of cold ischemia, defined as the time from initiation of cold perfusion (aortic flush with cold preservation solution) to the start of the islet isolation procedure or tissue processing. Cold ischemia time is a critical factor affecting organ viability and islet yield/function. Reported in hours. |
| **Data Type** | Number |
| **Input Restrictions** | Non-negative decimal value. Typical range: 0.0-48.0 hours. Precision: 1-2 decimal places or HH:MM format converted to decimal hours. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | Hours (UCUM: `h`) |
| **NIH CDE Reference** | PanKbase-defined. No standard NIH CDE; widely used in organ transplant research. |
| **Terminology Binding** | UCUM for unit |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | N/A |
| **Example Values** | `2.33`, `21.57`, `10.55`, `9.18` |
| **Mapping Notes** | HPAP field: `cold_ischemia_time_DDHHMMSS` (format "0 days HH:MM:SS"). Requires conversion to decimal hours. IIDP field: `Cold Ischemia Duration (hours)` (numeric string). Direct mapping from IIDP. |

---

### CDE PKB_D_025: Warm Ischemia Duration / Down Time

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_025 |
| **CDE Name** | warm_ischemia_time_hours |
| **Question Text** | What is the warm ischemia duration (down time) for the donated pancreas? |
| **Definition** | The warm ischemia time, defined as the period during which the organ is at or near body temperature without adequate blood supply. For DCD donors, this is the time from withdrawal of life support (or circulatory arrest) to the initiation of cold perfusion. For DBD donors, this may represent the estimated down time. This is a critical quality parameter affecting tissue viability. |
| **Data Type** | Number |
| **Input Restrictions** | Non-negative decimal value. Typical range: 0.0-4.0 hours. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | Hours (UCUM: `h`) |
| **NIH CDE Reference** | PanKbase-defined. No standard NIH CDE. |
| **Terminology Binding** | UCUM for unit |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | N/A |
| **Example Values** | `0.25`, `0.5`, `1.17` |
| **Mapping Notes** | HPAP: `dcd_donor_warm_ischemia_time_DDHHMMSS` or derived from `estimated_downtime_minutes` (convert minutes to hours). IIDP: not in standard HIPP report. |

---

### CDE PKB_D_026: Organ Source

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_026 |
| **CDE Name** | organ_source |
| **Question Text** | What is the source organ procurement organization or provider? |
| **Definition** | The organ procurement organization (OPO) or other entity responsible for recovering the donor pancreas. This is relevant for tracking procurement practices and regional variations. |
| **Data Type** | Text |
| **Input Restrictions** | Non-empty string. Standardized OPO names/abbreviations preferred. |
| **Permissible Values** | N/A (free text) |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | PanKbase-defined. |
| **Terminology Binding** | UNOS OPO codes (recommended) |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | N/A |
| **Example Values** | `GLDP`, `UPENN` |
| **Mapping Notes** | HPAP field: `recovery_opo`. IIDP: not in standard HIPP report. |

---

### CDE PKB_D_027: Pancreas Weight

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_027 |
| **CDE Name** | pancreas_weight_g |
| **Question Text** | What is the weight of the donor pancreas (trimmed)? |
| **Definition** | The weight of the donor pancreas after trimming of surrounding tissue, measured in grams. This is typically the weight at the time of islet isolation processing. Pancreas weight is correlated with islet yield and is an important quality parameter. |
| **Data Type** | Number |
| **Input Restrictions** | Positive decimal value. Typical range: 30.0-250.0 g. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | Grams (UCUM: `g`) |
| **NIH CDE Reference** | PanKbase-defined. |
| **Terminology Binding** | UCUM for unit |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | N/A |
| **Example Values** | `66.83`, `53.95`, `86`, `53.73` |
| **Mapping Notes** | HPAP field: `pancreas_weight_trimmed_grams` (decimal). Direct mapping. IIDP: not in standard HIPP report. |

---

### CDE PKB_D_028: Estimated Islet Viability (Pre-Shipment)

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_028 |
| **CDE Name** | islet_viability_pre_percent |
| **Question Text** | What is the estimated islet viability before shipment? |
| **Definition** | The percentage of viable islets in the preparation, assessed by dye exclusion or similar viability assay prior to shipment from the isolation center. This is a key quality control measure for islet preparations. |
| **Data Type** | Number |
| **Input Restrictions** | Decimal value in range 0.0-100.0. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | Percent (UCUM: `%`) |
| **NIH CDE Reference** | PanKbase-defined. |
| **Terminology Binding** | UCUM for unit |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | N/A |
| **Example Values** | `63`, `88.7`, `90`, `81` |
| **Mapping Notes** | HPAP field: `islet_viability_percent`. IIDP field: `Broadcast Islet Viability (%)`. Direct mapping. |

---

### CDE PKB_D_029: Estimated Islet Purity (Pre-Shipment)

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_029 |
| **CDE Name** | islet_purity_pre_percent |
| **Question Text** | What is the estimated islet purity before shipment? |
| **Definition** | The percentage of islet tissue in the total preparation, assessed by dithizone (DTZ) staining or similar method prior to shipment. Islet purity reflects the proportion of endocrine tissue relative to exocrine and other contaminant tissue. |
| **Data Type** | Number |
| **Input Restrictions** | Decimal value in range 0.0-100.0. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | Percent (UCUM: `%`) |
| **NIH CDE Reference** | PanKbase-defined. |
| **Terminology Binding** | UCUM for unit |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | N/A |
| **Example Values** | `80`, `83`, `70`, `95` |
| **Mapping Notes** | HPAP: not a direct single field; related to `islet_quality_yield` sheet. IIDP field: `Broadcast Islet Purity (%)`. Direct mapping from IIDP. |

---

### CDE PKB_D_030: Pre-Shipment Culture Time

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_030 |
| **CDE Name** | pre_shipment_culture_time_hours |
| **Question Text** | How long were the islets cultured before shipment? |
| **Definition** | The duration of islet culture at the isolation center before shipment to the receiving laboratory, measured in hours. Culture time affects islet recovery, function, and purity. |
| **Data Type** | Number |
| **Input Restrictions** | Non-negative decimal value. Typical range: 0-168 hours. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | Hours (UCUM: `h`) |
| **NIH CDE Reference** | PanKbase-defined. |
| **Terminology Binding** | UCUM for unit |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | N/A |
| **Example Values** | `115`, `75`, `24`, `48` |
| **Mapping Notes** | HPAP: can be derived from `biopsy_islet_isolation_datetime_est` and shipment records. IIDP field: `Pre-shipment Culture Time (hours)`. Direct mapping from IIDP. |

---

### CDE PKB_D_031: Pre-Shipment Islet Function Available

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_031 |
| **CDE Name** | pre_shipment_islet_function_available |
| **Question Text** | Are pre-shipment islet function assessment results available? |
| **Definition** | Indicates whether glucose-stimulated insulin secretion (GSIS) or other functional assessments of the islet preparation were performed prior to shipment. |
| **Data Type** | Value List |
| **Input Restrictions** | Single selection. |
| **Permissible Values** | `Yes` = Pre-shipment islet function data is available; `No` = Pre-shipment islet function was not assessed or data is not available |
| **Unit of Measure** | N/A |
| **NIH CDE Reference** | PanKbase-defined. |
| **Terminology Binding** | N/A |
| **PanKbase Tier** | Desired |
| **PanKbase Standard Tier** | N/A |
| **Example Values** | `Yes`, `No` |
| **Mapping Notes** | HPAP: derived from presence/absence of `gsir_si` value. IIDP: not in standard HIPP report. |

---

## 6. SAMPLE TRANSPORTATION

### CDE PKB_D_032: Post-Shipment Islet Viability

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_032 |
| **CDE Name** | islet_viability_post_percent |
| **Question Text** | What is the islet viability after shipment? |
| **Definition** | The percentage of viable islets in the preparation, assessed upon receipt at the destination laboratory after shipment. This is a critical quality control measure for assessing transport effects on islet preparations. |
| **Data Type** | Number |
| **Input Restrictions** | Decimal value in range 0.0-100.0. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | Percent (UCUM: `%`) |
| **NIH CDE Reference** | PanKbase-defined. |
| **Terminology Binding** | UCUM for unit |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | N/A |
| **Example Values** | `85`, `92`, `78` |
| **Mapping Notes** | HPAP: `Dispersed Islet Cell Viability (%)` in IIDP data may serve as a proxy. IIDP field: `Dispersed Islet Cell Viability (%)` (post-assessment). Requires verification of timing (pre vs post shipment). |

---

### CDE PKB_D_033: Post-Shipment Islet Purity

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_033 |
| **CDE Name** | islet_purity_post_percent |
| **Question Text** | What is the islet purity after shipment? |
| **Definition** | The percentage of islet tissue in the total preparation, assessed upon receipt at the destination laboratory after shipment. Comparison with pre-shipment purity helps assess transport effects. |
| **Data Type** | Number |
| **Input Restrictions** | Decimal value in range 0.0-100.0. |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | Percent (UCUM: `%`) |
| **NIH CDE Reference** | PanKbase-defined. |
| **Terminology Binding** | UCUM for unit |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | N/A |
| **Example Values** | `75`, `88`, `65` |
| **Mapping Notes** | HPAP: not directly available as post-shipment field. IIDP field: `Islet Purity (%)` (post-assessment) may serve as proxy. Requires verification. |

---

### CDE PKB_D_034: Total Culture Time

| Attribute | Value |
|-----------|-------|
| **CDE ID** | PKB_D_034 |
| **CDE Name** | total_culture_time_hours |
| **Question Text** | What is the total culture time for the islets from isolation to use? |
| **Definition** | The total duration of islet culture from the time of isolation to the time of experimental use or cryopreservation, including both pre-shipment and post-shipment culture periods. Measured in hours. |
| **Data Type** | Number |
| **Input Restrictions** | Non-negative decimal value. Typical range: 0-336 hours (up to 14 days). |
| **Permissible Values** | N/A (numeric) |
| **Unit of Measure** | Hours (UCUM: `h`) |
| **NIH CDE Reference** | PanKbase-defined. |
| **Terminology Binding** | UCUM for unit |
| **PanKbase Tier** | Required |
| **PanKbase Standard Tier** | N/A |
| **Example Values** | `72`, `96`, `48` |
| **Mapping Notes** | HPAP: can be derived from isolation and experiment datetimes. IIDP: `Pre-shipment Culture Time (hours)` + `Islet Transit Time (hours)` may approximate total culture time. |

---

## Summary Table

| CDE ID | CDE Name | Category | Data Type | PanKbase Tier | NIH CDE Exists? |
|--------|----------|----------|-----------|---------------|-----------------|
| PKB_D_001 | donor_rrid | Donor ID | Text | Required | Partial (RRID system) |
| PKB_D_002 | program_donor_id | Donor ID | Text | Required | Partial |
| PKB_D_003 | cohort_id | Donor ID | Value List | Required | No |
| PKB_D_004 | sex_at_birth | Demographics | Value List | Required | Yes |
| PKB_D_005 | age_years | Demographics | Number | Required | Yes |
| PKB_D_006 | bmi | Demographics | Number | Required | Yes |
| PKB_D_007 | race_ethnicity | Demographics | Composite | Required | Yes (OMB) |
| PKB_D_008 | diabetes_status | Medical | Value List | Required | No (PanKbase-defined) |
| PKB_D_009 | hba1c_percent | Medical | Number | Required | Yes (LOINC) |
| PKB_D_010 | hba1c_adjusted_diabetes_status | Medical | Value List | Desired | No (derived) |
| PKB_D_011 | glucose_lowering_therapy | Medical | Text | Desired | No |
| PKB_D_012 | other_disease_states | Medical | Text | Desired | Partial |
| PKB_D_013 | family_history_diabetes | Medical | Value List | Desired | No |
| PKB_D_014 | hospital_stay_days | Medical | Number | Desired | No |
| PKB_D_015 | donation_type | Medical | Value List | Desired | No |
| PKB_D_016 | cause_of_death | Medical | Value List | Desired | No |
| PKB_D_017 | diabetes_duration_years | Medical | Number | Desired | No |
| PKB_D_018 | c_peptide_ng_ml | Medical | Number | Desired | Yes (LOINC) |
| PKB_D_019 | aab_gada | Autoantibodies | Composite | Desired | No |
| PKB_D_020 | aab_iaa | Autoantibodies | Composite | Desired | No |
| PKB_D_021 | aab_ia2 | Autoantibodies | Composite | Desired | No |
| PKB_D_022 | aab_znt8 | Autoantibodies | Composite | Desired | No |
| PKB_D_023 | isolation_center | Processing | Text | Required | No |
| PKB_D_024 | cold_ischemia_time_hours | Processing | Number | Required | No |
| PKB_D_025 | warm_ischemia_time_hours | Processing | Number | Required | No |
| PKB_D_026 | organ_source | Processing | Text | Desired | No |
| PKB_D_027 | pancreas_weight_g | Processing | Number | Desired | No |
| PKB_D_028 | islet_viability_pre_percent | Processing | Number | Desired | No |
| PKB_D_029 | islet_purity_pre_percent | Processing | Number | Desired | No |
| PKB_D_030 | pre_shipment_culture_time_hours | Processing | Number | Required | No |
| PKB_D_031 | pre_shipment_islet_function_available | Processing | Value List | Desired | No |
| PKB_D_032 | islet_viability_post_percent | Transportation | Number | Required | No |
| PKB_D_033 | islet_purity_post_percent | Transportation | Number | Required | No |
| PKB_D_034 | total_culture_time_hours | Transportation | Number | Required | No |

---

## References

1. NIH CDE Repository: https://cde.nlm.nih.gov/
2. NCI caDSR II: https://cadsr.cancer.gov/
3. PanKbase Human Donor Standards: https://data.pankbase.org/standards/human-donor/
4. NIH Policy on Race/Ethnicity (NOT-OD-01-053): https://grants.nih.gov/grants/guide/notice-files/not-od-01-053.html
5. NIH Policy on Sex as a Biological Variable (NOT-OD-15-102): https://grants.nih.gov/grants/guide/notice-files/not-od-15-102.html
6. OMB 1997 Revised Standards for Race/Ethnicity
7. UCUM (Unified Code for Units of Measure): https://ucum.org/
8. LOINC: https://loinc.org/
9. MONDO Disease Ontology: https://mondo.monarchinitiative.org/
10. NCI Thesaurus: https://ncithesaurus.nci.nih.gov/
11. RRID Portal: https://scicrunch.org/resources

## Version History

| Version | Date | Description |
|---------|------|-------------|
| 1.0 | 2026-04-21 | Initial CDE collection based on PANKBASE META DATA_MB.xlsx (Required + Desired fields) |
