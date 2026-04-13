import { apiPost } from './client';

/**
 * Fetch feature importance for the trained model.
 * @param {string} domain - The currently selected domain ID
 * @param {number} topN - Number of top features to return
 */
export async function getFeatureImportance(domain = '', topN = 10) {
  return apiPost('/step6/feature-importance', { domain, top_n: topN });
}

/**
 * Get prediction and contribution waterfall for one of 3 representative patients.
 * @param {number} patientIndex - 0, 1, or 2 (maps to Patient A/B/C)
 */
export async function predictPatient(patientIndex) {
  return apiPost('/step6/patient-predict', { patient_index: patientIndex });
}

/**
 * Compute what-if probability shift by changing a feature value.
 * @param {number} patientIndex - 0, 1, or 2
 * @param {string} featureName - snake_case feature column name
 * @param {number} deltaStd - How many standard deviations to shift the feature
 */
export async function computeWhatIf(patientIndex, featureName, deltaStd = 1.0) {
  return apiPost('/step6/what-if', {
    patient_index: patientIndex,
    feature_name: featureName,
    delta_std: deltaStd,
  });
}
