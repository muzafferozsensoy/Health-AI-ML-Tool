import { apiGet, apiPost } from './client';

export async function fetchPrepOptions() {
  return apiGet('/step3/options');
}

export async function runDataPreparation(config) {
  const body = {
    missing_strategy: config.imputation,
    normalisation: config.scaling,
    test_size: (100 - config.trainTestSplit) / 100,
    apply_smote: config.smote || false,
    random_state: 42,
  };
  return apiPost('/step3/prepare', body);
}
