import { useEffect } from 'react';
import useDataStore from '../../stores/useDataStore';
import { fetchPrepOptions } from '../../api';
import styles from './PipelineConfig.module.css';

const FALLBACK_OPTIONS = {
  missing_strategies: [
    { value: 'mean', label: 'Replace with Mean' },
    { value: 'median', label: 'Replace with Median' },
    { value: 'mode', label: 'Replace with Mode' },
    { value: 'drop', label: 'Drop Rows with Missing Values' },
  ],
  normalisation_methods: [
    { value: 'minmax', label: 'Min-Max (scale to 0-1)' },
    { value: 'standard', label: 'Standard (Z-score, mean=0)' },
    { value: 'none', label: 'No Normalisation' },
  ],
  test_size_range: { min: 0.1, max: 0.4, step: 0.05, default: 0.2 },
  smote: { label: 'Apply SMOTE (balance classes)', default: false },
};

export default function PipelineConfig({ onApply }) {
  const config = useDataStore((s) => s.pipelineConfig);
  const setPipelineConfig = useDataStore((s) => s.setPipelineConfig);
  const pipelineStatus = useDataStore((s) => s.pipelineStatus);
  const prepOptions = useDataStore((s) => s.prepOptions);
  const setPrepOptions = useDataStore((s) => s.setPrepOptions);

  useEffect(() => {
    fetchPrepOptions().then(({ data }) => {
      if (data) setPrepOptions(data);
    });
  }, []);

  const opts = prepOptions || FALLBACK_OPTIONS;
  const isRunning = pipelineStatus === 'running';

  // Convert trainTestSplit (train%) to test_size range for slider
  // Backend: test_size 0.1-0.4 → train% 60-90
  const minTrain = Math.round((1 - (opts.test_size_range?.max || 0.4)) * 100);
  const maxTrain = Math.round((1 - (opts.test_size_range?.min || 0.1)) * 100);

  return (
    <div className={styles.wrapper}>
      <h3 className={styles.title}>Pipeline Configuration</h3>

      <div className={styles.field}>
        <label className={styles.label} htmlFor="imputation">
          Missing Value Imputation
        </label>
        <select
          id="imputation"
          className={styles.select}
          value={config.imputation}
          onChange={(e) => setPipelineConfig('imputation', e.target.value)}
          disabled={isRunning}
        >
          {(opts.missing_strategies || FALLBACK_OPTIONS.missing_strategies).map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
      </div>

      <div className={styles.field}>
        <label className={styles.label} htmlFor="scaling">
          Feature Scaling
        </label>
        <select
          id="scaling"
          className={styles.select}
          value={config.scaling}
          onChange={(e) => setPipelineConfig('scaling', e.target.value)}
          disabled={isRunning}
        >
          {(opts.normalisation_methods || FALLBACK_OPTIONS.normalisation_methods).map((o) => (
            <option key={o.value} value={o.value}>{o.label}</option>
          ))}
        </select>
      </div>

      <div className={styles.field}>
        <label className={styles.label} htmlFor="split">
          Train / Test Split: {config.trainTestSplit}% / {100 - config.trainTestSplit}%
        </label>
        <input
          id="split"
          type="range"
          min={minTrain}
          max={maxTrain}
          step="5"
          value={config.trainTestSplit}
          onChange={(e) =>
            setPipelineConfig('trainTestSplit', Number(e.target.value))
          }
          className={styles.slider}
          disabled={isRunning}
        />
        <div className={styles.sliderLabels}>
          <span>{minTrain}%</span>
          <span>{maxTrain}%</span>
        </div>
      </div>

      <div className={styles.field}>
        <label className={styles.label}>
          <input
            type="checkbox"
            checked={config.smote || false}
            onChange={(e) => setPipelineConfig('smote', e.target.checked)}
            disabled={isRunning}
            style={{ marginRight: 8 }}
          />
          {opts.smote?.label || 'Apply SMOTE (balance classes)'}
        </label>
      </div>

      <button
        className={`${styles.applyBtn} ${isRunning ? styles.disabled : ''}`}
        onClick={isRunning ? undefined : onApply}
        disabled={isRunning}
      >
        {isRunning ? 'Processing...' : 'Apply Pipeline'}
      </button>
    </div>
  );
}
