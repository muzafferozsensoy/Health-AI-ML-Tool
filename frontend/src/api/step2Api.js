import { apiUploadFile, apiPost } from './client';

export async function uploadCsv(file) {
  return apiUploadFile('/step2/upload', file);
}

export async function saveColumnMapping(targetColumn, featureColumns, dropColumns = []) {
  return apiPost('/step2/column-mapping', {
    target_column: targetColumn,
    feature_columns: featureColumns,
    drop_columns: dropColumns,
  });
}
