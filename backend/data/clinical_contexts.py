# data/clinical_contexts.py
# All 20 clinical domains with their context information

CLINICAL_CONTEXTS = {
    "cardiology": {
        "domain": "cardiology",
        "title": "Cardiology — Heart Disease Prediction",
        "problem": (
            "Heart disease is the leading cause of death worldwide. "
            "Early identification of high-risk patients allows clinicians to intervene "
            "before a cardiac event occurs. An AI model trained on patient measurements "
            "such as age, cholesterol, blood pressure, and ECG results can flag patients "
            "who need urgent review."
        ),
        "goal": "Predict whether a patient is at high risk of a cardiac event within 12 months.",
        "target_column": "heart_disease",
        "recommended_features": ["age", "cholesterol", "blood_pressure", "ecg_result", "max_heart_rate"],
        "class_labels": {"0": "No Disease", "1": "Disease Present"},
        "example_dataset": "heart_disease.csv",
    },
    "oncology": {
        "domain": "oncology",
        "title": "Oncology — Cancer Diagnosis Support",
        "problem": (
            "Early detection of cancer dramatically improves survival rates. "
            "AI models can assist pathologists by analysing tumour measurements and "
            "biopsy features to classify tumours as benign or malignant, reducing "
            "diagnostic delays."
        ),
        "goal": "Classify whether a tumour biopsy is benign or malignant.",
        "target_column": "diagnosis",
        "recommended_features": ["radius_mean", "texture_mean", "perimeter_mean", "area_mean", "smoothness_mean"],
        "class_labels": {"0": "Benign", "1": "Malignant"},
        "example_dataset": "breast_cancer.csv",
    },
    "neurology": {
        "domain": "neurology",
        "title": "Neurology — Stroke Risk Prediction",
        "problem": (
            "Stroke is a time-critical emergency. Predicting stroke risk from patient "
            "demographics and medical history enables preventive treatment. "
            "Key risk factors include hypertension, atrial fibrillation, smoking, and BMI."
        ),
        "goal": "Predict the likelihood of a patient experiencing a stroke.",
        "target_column": "stroke",
        "recommended_features": ["age", "hypertension", "heart_disease", "avg_glucose_level", "bmi", "smoking_status"],
        "class_labels": {"0": "No Stroke", "1": "Stroke"},
        "example_dataset": "stroke.csv",
    },
    "endocrinology": {
        "domain": "endocrinology",
        "title": "Endocrinology — Diabetes Prediction",
        "problem": (
            "Type 2 diabetes affects hundreds of millions globally and often goes "
            "undiagnosed. AI models can screen high-risk patients using routine "
            "blood tests and lifestyle data, enabling early dietary and pharmacological intervention."
        ),
        "goal": "Predict whether a patient will develop Type 2 diabetes.",
        "target_column": "diabetes",
        "recommended_features": ["glucose", "bmi", "insulin", "age", "blood_pressure", "skin_thickness"],
        "class_labels": {"0": "No Diabetes", "1": "Diabetes"},
        "example_dataset": "diabetes.csv",
    },
    "pulmonology": {
        "domain": "pulmonology",
        "title": "Pulmonology — COPD Readmission Risk",
        "problem": (
            "Chronic Obstructive Pulmonary Disease (COPD) causes frequent hospital "
            "readmissions. Predicting which patients are likely to be readmitted within "
            "30 days helps allocate respiratory nursing follow-up resources effectively."
        ),
        "goal": "Predict 30-day hospital readmission in COPD patients.",
        "target_column": "readmitted_30d",
        "recommended_features": ["fev1", "fvc", "exacerbations_last_year", "smoking_pack_years", "age", "oxygen_saturation"],
        "class_labels": {"0": "Not Readmitted", "1": "Readmitted"},
        "example_dataset": "copd_readmission.csv",
    },
    "nephrology": {
        "domain": "nephrology",
        "title": "Nephrology — Chronic Kidney Disease Detection",
        "problem": (
            "Chronic Kidney Disease (CKD) progresses silently until advanced stages. "
            "Routine blood and urine tests contain early markers. ML models can identify "
            "patients with CKD before GFR declines severely, allowing timely referral."
        ),
        "goal": "Detect the presence of Chronic Kidney Disease from lab results.",
        "target_column": "ckd",
        "recommended_features": ["creatinine", "albumin", "haemoglobin", "gfr", "blood_urea", "potassium"],
        "class_labels": {"0": "No CKD", "1": "CKD Present"},
        "example_dataset": "ckd.csv",
    },
    "psychiatry": {
        "domain": "psychiatry",
        "title": "Psychiatry — Depression Severity Classification",
        "problem": (
            "Depression is underdiagnosed in primary care. PHQ-9 scores combined with "
            "demographic and sleep data can be used to train models that flag patients "
            "requiring urgent mental health referral."
        ),
        "goal": "Classify depression severity (none / mild / moderate / severe) from screening data.",
        "target_column": "depression_severity",
        "recommended_features": ["phq9_score", "sleep_hours", "activity_level", "age", "previous_episode"],
        "class_labels": {"0": "None", "1": "Mild", "2": "Moderate", "3": "Severe"},
        "example_dataset": "depression.csv",
    },
    "gastroenterology": {
        "domain": "gastroenterology",
        "title": "Gastroenterology — Liver Disease Prediction",
        "problem": (
            "Liver disease is often detected late due to non-specific symptoms. "
            "Liver function tests and patient history can train models to identify "
            "at-risk patients before cirrhosis or liver failure develops."
        ),
        "goal": "Predict presence of liver disease from clinical and biochemical markers.",
        "target_column": "liver_disease",
        "recommended_features": ["bilirubin", "alkaline_phosphotase", "alamine_aminotransferase", "albumin", "age"],
        "class_labels": {"0": "Healthy", "1": "Liver Disease"},
        "example_dataset": "liver_disease.csv",
    },
    "rheumatology": {
        "domain": "rheumatology",
        "title": "Rheumatology — Rheumatoid Arthritis Flare Prediction",
        "problem": (
            "Rheumatoid Arthritis flares are unpredictable, causing joint damage if "
            "untreated. Predicting flares from CRP, ESR, and patient-reported outcomes "
            "enables proactive dose adjustment of DMARDs."
        ),
        "goal": "Predict whether an RA patient will experience a disease flare in the next 4 weeks.",
        "target_column": "flare",
        "recommended_features": ["crp", "esr", "das28_score", "tender_joint_count", "swollen_joint_count"],
        "class_labels": {"0": "No Flare", "1": "Flare"},
        "example_dataset": "ra_flare.csv",
    },
    "haematology": {
        "domain": "haematology",
        "title": "Haematology — Anaemia Classification",
        "problem": (
            "Anaemia has multiple causes requiring different treatments. ML models "
            "trained on full blood count results can distinguish iron-deficiency, "
            "B12-deficiency, and haemolytic anaemia, guiding faster treatment decisions."
        ),
        "goal": "Classify the type of anaemia from full blood count and iron studies.",
        "target_column": "anaemia_type",
        "recommended_features": ["haemoglobin", "mcv", "mchc", "ferritin", "b12", "folate"],
        "class_labels": {"0": "Normal", "1": "Iron Deficiency", "2": "B12/Folate", "3": "Other"},
        "example_dataset": "anaemia.csv",
    },
    "dermatology": {
        "domain": "dermatology",
        "title": "Dermatology — Skin Lesion Risk Classification",
        "problem": (
            "Melanoma is deadly if missed but highly treatable when caught early. "
            "Dermoscopy features — asymmetry, border, colour, diameter — can be "
            "quantified and used to train models that triage lesions for urgent biopsy."
        ),
        "goal": "Classify skin lesions as low, medium, or high malignancy risk.",
        "target_column": "risk_level",
        "recommended_features": ["asymmetry_score", "border_irregularity", "colour_variation", "diameter_mm", "evolution"],
        "class_labels": {"0": "Low Risk", "1": "Medium Risk", "2": "High Risk"},
        "example_dataset": "skin_lesion.csv",
    },
    "ophthalmology": {
        "domain": "ophthalmology",
        "title": "Ophthalmology — Diabetic Retinopathy Screening",
        "problem": (
            "Diabetic retinopathy is the leading cause of blindness in working-age adults. "
            "Regular screening identifies patients needing laser treatment before "
            "vision loss. AI grading tools can triage large screening programmes."
        ),
        "goal": "Grade diabetic retinopathy severity from retinal image features.",
        "target_column": "dr_grade",
        "recommended_features": ["microaneurysm_count", "haemorrhage_count", "hba1c", "diabetes_duration", "blood_pressure"],
        "class_labels": {"0": "No DR", "1": "Mild", "2": "Moderate", "3": "Severe", "4": "Proliferative"},
        "example_dataset": "diabetic_retinopathy.csv",
    },
    "obstetrics": {
        "domain": "obstetrics",
        "title": "Obstetrics — Preterm Birth Risk Prediction",
        "problem": (
            "Preterm birth (before 37 weeks) is a leading cause of neonatal mortality. "
            "Risk factors include cervical length, infection markers, and obstetric history. "
            "Early identification allows progesterone therapy and hospital transfer planning."
        ),
        "goal": "Predict the risk of preterm birth from maternal clinical data.",
        "target_column": "preterm_birth",
        "recommended_features": ["cervical_length_mm", "crp", "fibronectin_positive", "previous_preterm", "gestational_age_weeks"],
        "class_labels": {"0": "Term Birth", "1": "Preterm Birth"},
        "example_dataset": "preterm_birth.csv",
    },
    "paediatrics": {
        "domain": "paediatrics",
        "title": "Paediatrics — Sepsis Early Warning",
        "problem": (
            "Paediatric sepsis progresses rapidly. Vital sign trend analysis using "
            "AI can flag deteriorating children earlier than manual review of "
            "NEWS2-equivalent scores, enabling faster antibiotic administration."
        ),
        "goal": "Predict sepsis onset in paediatric patients within 6 hours using vital signs.",
        "target_column": "sepsis",
        "recommended_features": ["temperature", "heart_rate", "respiratory_rate", "wbc_count", "lactate"],
        "class_labels": {"0": "No Sepsis", "1": "Sepsis"},
        "example_dataset": "paediatric_sepsis.csv",
    },
    "emergency_medicine": {
        "domain": "emergency_medicine",
        "title": "Emergency Medicine — Triage Priority Classification",
        "problem": (
            "Emergency departments face overcrowding. Accurate triage ensures the "
            "most critically ill patients are seen first. ML models trained on "
            "presenting complaints, vitals, and history can assist triage nurses "
            "in high-pressure environments."
        ),
        "goal": "Classify patient triage priority (1=immediate to 5=non-urgent) on arrival.",
        "target_column": "triage_level",
        "recommended_features": ["systolic_bp", "heart_rate", "gcs_score", "pain_score", "oxygen_saturation"],
        "class_labels": {"1": "Immediate", "2": "Emergent", "3": "Urgent", "4": "Less Urgent", "5": "Non-Urgent"},
        "example_dataset": "triage.csv",
    },
    "orthopaedics": {
        "domain": "orthopaedics",
        "title": "Orthopaedics — Hip Fracture Mortality Risk",
        "problem": (
            "Hip fractures in elderly patients carry significant 30-day mortality risk. "
            "Pre-operative risk stratification using ASA grade, age, and comorbidities "
            "guides anaesthetic and surgical decision-making."
        ),
        "goal": "Predict 30-day post-operative mortality risk in hip fracture patients.",
        "target_column": "mortality_30d",
        "recommended_features": ["age", "asa_grade", "albumin", "sodium", "haemoglobin", "dementia"],
        "class_labels": {"0": "Survived", "1": "Deceased"},
        "example_dataset": "hip_fracture.csv",
    },
    "infectious_disease": {
        "domain": "infectious_disease",
        "title": "Infectious Disease — Antibiotic Resistance Prediction",
        "problem": (
            "Antimicrobial resistance is a global health crisis. Predicting resistance "
            "patterns from patient history and local epidemiology allows targeted "
            "antibiotic prescribing, reducing broad-spectrum use."
        ),
        "goal": "Predict antibiotic resistance likelihood from patient and microbiological data.",
        "target_column": "resistant",
        "recommended_features": ["prior_antibiotics", "hospital_acquired", "icu_stay", "previous_resistance", "organism"],
        "class_labels": {"0": "Sensitive", "1": "Resistant"},
        "example_dataset": "antibiotic_resistance.csv",
    },
    "radiology": {
        "domain": "radiology",
        "title": "Radiology — Chest X-Ray Finding Classification",
        "problem": (
            "Radiologists report hundreds of chest X-rays daily. AI-extracted features "
            "from CXR reports (or image-derived metrics) can pre-classify findings, "
            "prioritising abnormal studies for urgent radiologist review."
        ),
        "goal": "Classify chest X-ray findings as normal, pneumonia, or other pathology.",
        "target_column": "finding",
        "recommended_features": ["opacity_score", "consolidation", "pleural_effusion", "cardiomegaly", "age"],
        "class_labels": {"0": "Normal", "1": "Pneumonia", "2": "Other Pathology"},
        "example_dataset": "chest_xray.csv",
    },
    "geriatrics": {
        "domain": "geriatrics",
        "title": "Geriatrics — Falls Risk Prediction",
        "problem": (
            "Falls in elderly patients cause fractures and loss of independence. "
            "Combining gait assessments, medication counts, and cognitive scores "
            "into a predictive model helps community nurses target fall prevention visits."
        ),
        "goal": "Predict the risk of a patient falling within 3 months.",
        "target_column": "fall_risk",
        "recommended_features": ["tug_test_seconds", "medication_count", "mmse_score", "previous_falls", "age", "grip_strength"],
        "class_labels": {"0": "Low Risk", "1": "High Risk"},
        "example_dataset": "falls_risk.csv",
    },
    "general_practice": {
        "domain": "general_practice",
        "title": "General Practice — Hypertension Management",
        "problem": (
            "Uncontrolled hypertension is a major risk factor for stroke and MI. "
            "Predicting which patients will fail to achieve BP control on their current "
            "regimen allows GPs to proactively intensify treatment."
        ),
        "goal": "Predict whether a hypertensive patient will achieve blood pressure control within 6 months.",
        "target_column": "bp_controlled",
        "recommended_features": ["systolic_bp", "diastolic_bp", "age", "medication_count", "adherence_score", "bmi"],
        "class_labels": {"0": "Uncontrolled", "1": "Controlled"},
        "example_dataset": "hypertension.csv",
    },
}

DOMAIN_LIST = list(CLINICAL_CONTEXTS.keys())


# ── Clinical Sense-Check text for Step 6 ─────────────────────────────────────
# Domain-specific explanation of why the top predicted features make clinical sense.

CLINICAL_SENSE_CHECK = {
    "cardiology": (
        "LVEF (%), NT-proBNP and Troponin Levels are the top predictors here. "
        "Low Left Ventricular Ejection Fraction and high NT-proBNP/Troponin are direct "
        "biomarkers of cardiac muscle damage and pump failure."
    ),
    "radiology": (
        "Lesion Size/Volume, Margin Sharpness and Contrast Enhancement Rate lead the model. "
        "Irregular margins and rapid contrast enhancement on scans strongly correlate with "
        "malignant angiogenesis and tumour aggression."
    ),
    "nephrology": (
        "Serum Creatinine, eGFR and Proteinuria are the strongest predictors. "
        "Declining GFR and protein leakage are the primary, most reliable biochemical markers "
        "of acute kidney injury and progression to ESRD."
    ),
    "oncology": (
        "TNM Stage, Histological Grade and Metastasis Indicator dominate the model. "
        "Tumour staging and cellular grade are the most universally validated predictors of "
        "survival rates, recurrence risk, and treatment response."
    ),
    "neurology": (
        "Cognitive Score (MMSE), Brain Atrophy Volume and Amyloid/Tau Biomarkers are the top features. "
        "Structural brain changes and specific protein accumulations are the core drivers of "
        "neurodegenerative decline and dementia progression."
    ),
    "endocrinology": (
        "TSH Levels, Free T4 and Cortisol Levels lead the predictions. "
        "Severe hormone dysregulation directly impacts systemic metabolic stability, predicting "
        "crises like thyroid storms or adrenal insufficiency."
    ),
    "hepatology": (
        "AST/ALT Ratio, Serum Bilirubin and MELD Score are the strongest predictors. "
        "Liver enzyme ratios and bilirubin levels directly quantify hepatocellular injury "
        "and the liver's remaining detoxifying capacity."
    ),
    "cardiology-stroke": (
        "AFib History, CHA\u2082DS\u2082-VASc Score and Left Atrial Enlargement are the top features. "
        "Atrial Fibrillation causes blood pooling in the heart's atria, creating cardiogenic "
        "clots that travel to the brain, risking ischaemic stroke."
    ),
    "mental-health": (
        "PHQ-9 (Depression Score), Previous Crisis Episodes and Medication Adherence dominate. "
        "Severe symptom severity scores and a history of non-adherence are the strongest "
        "predictors of acute psychiatric relapse or crisis."
    ),
    "diabetes": (
        "HbA1c Levels, Fasting Blood Glucose and Neuropathy Presence are the top predictors. "
        "Long-term elevated HbA1c mechanically damages microvasculature, leading directly to "
        "irreversible complications like neuropathy and retinopathy."
    ),
    "pulmonology": (
        "FEV1/FVC Ratio, O\u2082 Saturation (SpO\u2082) and Smoking Pack-Years lead the model. "
        "Reduced expiratory volume and chronic hypoxia indicate irreversible airway obstruction, "
        "strongly predicting COPD exacerbations."
    ),
    "sepsis-icu": (
        "Serum Lactate, SOFA Score and Procalcitonin are the strongest predictors. "
        "Elevated lactate indicates severe tissue hypoperfusion, while a rising SOFA score "
        "reflects imminent multi-organ failure."
    ),
    "fetal-health": (
        "Fetal Heart Rate Baseline, Late Decelerations and Uterine Contraction Rate dominate. "
        "Prolonged decelerations in heart rate during contractions indicate fetal oxygen "
        "deprivation and acute distress requiring intervention."
    ),
    "dermatology": (
        "Lesion Asymmetry, Colour Variegation and Border Irregularity are the top features. "
        "Morphological asymmetry and uneven pigmentation (the ABCD rule) are the hallmark "
        "clinical signs of malignant melanocytes."
    ),
    "stroke": (
        "NIHSS Score at Admission, Time to Thrombolysis and Infarct Volume lead the model. "
        "Initial neurological deficit severity (NIHSS) and the time elapsed before intervention "
        "heavily dictate permanent brain damage and recovery."
    ),
    "gastroenterology": (
        "Fecal Calprotectin, CRP Levels and Haemoglobin Drops are the strongest predictors. "
        "Calprotectin is a highly specific marker for intestinal inflammation (IBD), while "
        "dropping haemoglobin indicates active gastrointestinal bleeding."
    ),
    "orthopedics": (
        "Joint Space Narrowing, Bone Mineral Density and Pain Severity Score dominate the model. "
        "Mechanical degradation of cartilage and low bone density directly predict joint failure, "
        "fracture risk, and the need for arthroplasty."
    ),
    "ophthalmology": (
        "Intraocular Pressure (IOP), Cup-to-Disc Ratio and Macular Thickness are the top features. "
        "Sustained high intraocular pressure and optic nerve cupping are the fundamental mechanical "
        "causes of irreversible visual field loss in glaucoma."
    ),
    "hematology": (
        "Blast Cell Count, Platelet Count and Haemoglobin Levels lead the predictions. "
        "The presence of immature blast cells and severe cytopenias (low platelets/Hb) indicate "
        "severe bone marrow failure or haematologic malignancy."
    ),
    "infectious-disease": (
        "Viral/Bacterial Load, WBC Count and CRP/ESR are the strongest predictors. "
        "High pathogen loads coupled with extreme immune responses (WBC and inflammatory markers) "
        "correlate directly with systemic infectious severity."
    ),
}


# ── Clinical display names for common feature column names ────────────────────
# Maps snake_case CSV column names → human-readable clinical labels.
# Fallback: replace underscores with spaces and apply title case.

FEATURE_DISPLAY_NAMES = {
    # Cardiovascular / General
    "age": "Age (years)",
    "sex": "Sex",
    "gender": "Gender",
    "blood_pressure": "Blood Pressure (mmHg)",
    "systolic_bp": "Systolic BP (mmHg)",
    "diastolic_bp": "Diastolic BP (mmHg)",
    "heart_rate": "Heart Rate (bpm)",
    "cholesterol": "Cholesterol (mg/dL)",
    "bmi": "BMI (kg/m²)",
    "smoking": "Smoking Status",
    "smoking_status": "Smoking Status",
    "smoking_pack_years": "Smoking Pack-Years",
    "diabetes": "Diabetes",
    "hypertension": "Hypertension",
    "ecg_result": "ECG Result",
    "max_heart_rate": "Max Heart Rate (bpm)",
    "heart_disease": "Heart Disease",
    # Cardiology (heart failure)
    "ejection_fraction": "Ejection Fraction (%)",
    "serum_creatinine": "Serum Creatinine (mg/dL)",
    "serum_sodium": "Serum Sodium (mEq/L)",
    "anaemia": "Anaemia",
    "creatinine_phosphokinase": "Creatinine Phosphokinase (mcg/L)",
    "platelets": "Platelets (kiloplatelets/mL)",
    # Oncology
    "radius_mean": "Radius Mean",
    "texture_mean": "Texture Mean",
    "perimeter_mean": "Perimeter Mean",
    "area_mean": "Area Mean",
    "smoothness_mean": "Smoothness Mean",
    "compactness_mean": "Compactness Mean",
    "concavity_mean": "Concavity Mean",
    "symmetry_mean": "Symmetry Mean",
    "fractal_dimension_mean": "Fractal Dimension Mean",
    "diagnosis": "Diagnosis",
    # Neurology (stroke)
    "avg_glucose_level": "Average Glucose Level (mg/dL)",
    "stroke": "Stroke",
    "ever_married": "Ever Married",
    "work_type": "Work Type",
    "residence_type": "Residence Type",
    # Endocrinology (diabetes)
    "glucose": "Glucose (mg/dL)",
    "insulin": "Insulin (μU/mL)",
    "skin_thickness": "Skin Thickness (mm)",
    "dpf": "Diabetes Pedigree Function",
    "pregnancies": "Number of Pregnancies",
    # Pulmonology (COPD)
    "fev1": "FEV1 (L)",
    "fvc": "FVC (L)",
    "exacerbations_last_year": "Exacerbations Last Year",
    "oxygen_saturation": "Oxygen Saturation (%)",
    "readmitted_30d": "Readmitted (30-day)",
    # Nephrology (CKD)
    "creatinine": "Creatinine (mg/dL)",
    "albumin": "Albumin (g/dL)",
    "haemoglobin": "Haemoglobin (g/dL)",
    "gfr": "eGFR (mL/min/1.73m²)",
    "blood_urea": "Blood Urea (mg/dL)",
    "potassium": "Potassium (mEq/L)",
    "ckd": "CKD",
    # Psychiatry
    "phq9_score": "PHQ-9 Score",
    "sleep_hours": "Sleep Duration (hours)",
    "activity_level": "Physical Activity Level",
    "previous_episode": "Previous Depressive Episode",
    "depression_severity": "Depression Severity",
    # Gastroenterology (liver)
    "bilirubin": "Total Bilirubin (mg/dL)",
    "alkaline_phosphotase": "Alkaline Phosphatase (IU/L)",
    "alamine_aminotransferase": "Alanine Aminotransferase (IU/L)",
    "aspartate_aminotransferase": "Aspartate Aminotransferase (IU/L)",
    "liver_disease": "Liver Disease",
    # Rheumatology (RA)
    "crp": "CRP (mg/L)",
    "esr": "ESR (mm/hr)",
    "das28_score": "DAS28 Score",
    "tender_joint_count": "Tender Joint Count",
    "swollen_joint_count": "Swollen Joint Count",
    "flare": "RA Flare",
    # Haematology
    "mcv": "MCV (fL)",
    "mchc": "MCHC (g/dL)",
    "ferritin": "Ferritin (ng/mL)",
    "b12": "Vitamin B12 (pg/mL)",
    "folate": "Folate (ng/mL)",
    "anaemia_type": "Anaemia Type",
    # Dermatology
    "asymmetry_score": "Asymmetry Score",
    "border_irregularity": "Border Irregularity",
    "colour_variation": "Colour Variation",
    "diameter_mm": "Diameter (mm)",
    "evolution": "Lesion Evolution",
    "risk_level": "Risk Level",
    # Ophthalmology (DR)
    "microaneurysm_count": "Microaneurysm Count",
    "haemorrhage_count": "Haemorrhage Count",
    "hba1c": "HbA1c (%)",
    "diabetes_duration": "Diabetes Duration (years)",
    "dr_grade": "DR Grade",
    # Obstetrics
    "cervical_length_mm": "Cervical Length (mm)",
    "fibronectin_positive": "Fibronectin Positive",
    "previous_preterm": "Previous Preterm Birth",
    "gestational_age_weeks": "Gestational Age (weeks)",
    "preterm_birth": "Preterm Birth",
    # Paediatrics (sepsis)
    "temperature": "Temperature (°C)",
    "respiratory_rate": "Respiratory Rate (breaths/min)",
    "wbc_count": "WBC Count (×10³/μL)",
    "lactate": "Lactate (mmol/L)",
    "sepsis": "Sepsis",
    # Emergency Medicine
    "gcs_score": "GCS Score",
    "pain_score": "Pain Score (0–10)",
    "triage_level": "Triage Level",
    # Orthopaedics
    "asa_grade": "ASA Grade",
    "sodium": "Sodium (mEq/L)",
    "dementia": "Dementia",
    "mortality_30d": "30-day Mortality",
    # Infectious Disease
    "prior_antibiotics": "Prior Antibiotic Exposure",
    "hospital_acquired": "Hospital-Acquired Infection",
    "icu_stay": "ICU Stay",
    "previous_resistance": "Previous Resistance",
    "organism": "Causative Organism",
    "resistant": "Antibiotic Resistant",
    # Radiology
    "opacity_score": "Opacity Score",
    "consolidation": "Consolidation",
    "pleural_effusion": "Pleural Effusion",
    "cardiomegaly": "Cardiomegaly",
    "finding": "CXR Finding",
    # Geriatrics
    "tug_test_seconds": "TUG Test Time (seconds)",
    "medication_count": "Medication Count",
    "mmse_score": "MMSE Score",
    "previous_falls": "Previous Falls",
    "grip_strength": "Grip Strength (kg)",
    "fall_risk": "Fall Risk",
    # General Practice
    "adherence_score": "Medication Adherence Score",
    "bp_controlled": "BP Controlled",
}
