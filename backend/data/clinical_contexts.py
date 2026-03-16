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
