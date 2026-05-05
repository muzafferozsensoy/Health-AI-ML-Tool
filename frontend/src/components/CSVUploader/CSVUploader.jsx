import { useRef } from 'react';
import Papa from 'papaparse';
import useAppStore from '../../stores/useAppStore';
import useDataStore from '../../stores/useDataStore';
import { getDefaultDataset } from '../../data/defaultDatasets';
import { validateCSVFile, validateCSVContent, parseCSV } from '../../utils/csvParser';
import { uploadCsv } from '../../api';
import styles from './CSVUploader.module.css';

function syncToBackend(file) {
  const store = useDataStore.getState();
  store.setUploadLoading(true);
  store.setUploadError(null);

  uploadCsv(file).then(({ data, error }) => {
    const s = useDataStore.getState();
    s.setUploadLoading(false);
    if (error) {
      s.setUploadError(error);
    } else {
      s.setBackendSummary(data);
    }
  });
}

export default function CSVUploader() {
  const fileInputRef = useRef(null);
  const selectedDomainId = useAppStore((s) => s.selectedDomainId);
  const setCsvData = useDataStore((s) => s.setCsvData);
  const setCsvError = useDataStore((s) => s.setCsvError);
  const useDefaultDatasetAction = useDataStore((s) => s.useDefaultDataset);
  const csvError = useDataStore((s) => s.csvError);
  const csvFileName = useDataStore((s) => s.csvFileName);
  const dataSource = useDataStore((s) => s.dataSource);
  const uploadLoading = useDataStore((s) => s.uploadLoading);
  const uploadError = useDataStore((s) => s.uploadError);

  const handleDefault = () => {
    const dataset = getDefaultDataset(selectedDomainId);
    if (dataset) {
      useDefaultDatasetAction(dataset.rows);

      // Convert to CSV and upload to backend
      const csvString = Papa.unparse(dataset.rows);
      const blob = new Blob([csvString], { type: 'text/csv' });
      const file = new File([blob], `${selectedDomainId}_default.csv`, { type: 'text/csv' });
      syncToBackend(file);
    }
  };

  const handleDemo = async () => {
    const apiBase = import.meta.env.VITE_API_URL || '/api';
    try {
      const res = await fetch(`${apiBase}/step2/demo-dataset`);
      if (!res.ok) throw new Error(`Demo dataset request failed (${res.status})`);
      const blob = await res.blob();
      const file = new File([blob], 'heart_disease_demo_bias.csv', { type: 'text/csv' });
      const parsed = await parseCSV(file);
      const contentValidation = validateCSVContent(parsed);
      if (!contentValidation.valid) {
        setCsvError(contentValidation.error);
        return;
      }
      setCsvData(parsed.data, file.name);
      syncToBackend(file);
    } catch (err) {
      setCsvError(`Failed to load demo dataset: ${err.message}`);
    }
  };

  const handleUploadClick = () => {
    fileInputRef.current?.click();
  };

  const handleFileChange = async (e) => {
    const file = e.target.files?.[0];
    if (!file) return;

    const fileValidation = validateCSVFile(file);
    if (!fileValidation.valid) {
      setCsvError(fileValidation.error);
      e.target.value = '';
      return;
    }

    try {
      const parsed = await parseCSV(file);
      const contentValidation = validateCSVContent(parsed);
      if (!contentValidation.valid) {
        setCsvError(contentValidation.error);
        e.target.value = '';
        return;
      }
      setCsvData(parsed.data, file.name);

      // Upload to backend in parallel
      syncToBackend(file);
    } catch {
      setCsvError('Failed to parse the CSV file. Please check the file format.');
    }

    e.target.value = '';
  };

  return (
    <div className={styles.wrapper} role="group" aria-label="Dataset source">
      <span className={styles.sectionLabel} id="csv-config-label">CONFIGURATION</span>

      <button
        type="button"
        className={styles.defaultBtn}
        onClick={handleDefault}
        aria-describedby="csv-config-label"
      >
        Use Default Dataset
      </button>

      <button
        type="button"
        className={styles.uploadBtn}
        onClick={handleUploadClick}
        aria-describedby="csv-config-label"
      >
        Upload Your CSV
      </button>

      <button
        type="button"
        className={styles.demoBtn}
        onClick={handleDemo}
        aria-describedby="csv-config-label"
        title="Educational dataset with intentionally introduced bias for fairness analysis"
      >
        Load Demo Dataset (Bias Showcase)
      </button>

      <input
        ref={fileInputRef}
        type="file"
        accept=".csv"
        onChange={handleFileChange}
        className={styles.hiddenInput}
        data-testid="csv-file-input"
        aria-label="CSV file"
        tabIndex="-1"
      />

      {csvError && (
        <div className={styles.error} role="alert">
          {csvError}
        </div>
      )}

      {uploadError && uploadError !== 'Backend is not reachable.' && (
        <div className={styles.error} role="alert">
          Backend sync failed: {uploadError}
        </div>
      )}

      {dataSource === 'uploaded' && csvFileName && (
        <div className={styles.fileInfo}>
          Using: {csvFileName}
          {uploadLoading && <span> (syncing...)</span>}
        </div>
      )}

      {dataSource === 'default' && (
        <div className={styles.fileInfo}>
          Using: Default dataset
          {uploadLoading && <span> (syncing...)</span>}
        </div>
      )}
    </div>
  );
}
