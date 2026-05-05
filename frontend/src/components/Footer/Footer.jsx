import useAppStore from '../../stores/useAppStore';
import useDataStore from '../../stores/useDataStore';
import useModelStore from '../../stores/useModelStore';
import styles from './Footer.module.css';

const stepLabels = {
  1: 'Process to step 2: Data Exploration',
  2: 'Proceed to Step 3: Data Preparation',
  3: 'Proceed to Step 4: Model & Parameters',
  4: 'Proceed to Step 5: Results',
  5: 'Proceed to Step 6: Explainability',
  6: 'Proceed to Step 7: Ethics & Bias',
};

export default function Footer() {
  const currentStep = useAppStore((s) => s.currentStep);
  const nextStep = useAppStore((s) => s.nextStep);
  const prevStep = useAppStore((s) => s.prevStep);
  const mapperSaved = useDataStore((s) => s.mapperSaved);
  const pipelineStatus = useDataStore((s) => s.pipelineStatus);
  const trainingStatus = useModelStore((s) => s.trainingStatus);

  const isStep2NextBlocked = currentStep === 2 && !mapperSaved;
  const isStep3NextBlocked = currentStep === 3 && pipelineStatus !== 'complete';
  const isStep4NextBlocked = currentStep === 4 && trainingStatus !== 'complete';
  const isStep5NextBlocked = currentStep === 5 && trainingStatus !== 'complete';
  const isNextDisabled =
    isStep2NextBlocked ||
    isStep3NextBlocked ||
    isStep4NextBlocked ||
    isStep5NextBlocked ||
    currentStep >= 7;

  const label = stepLabels[currentStep] || `Proceed to Step ${currentStep + 1}`;

  return (
    <footer className={styles.footer} role="contentinfo">
      <nav className={styles.footerInner} aria-label="Workflow navigation">
        {currentStep > 1 && (
          <button
            type="button"
            className={styles.backBtn}
            onClick={prevStep}
            aria-label="Go back to previous step"
          >
            <span aria-hidden="true">&larr;</span> Back
          </button>
        )}
        <div className={styles.spacer} />
        {currentStep < 7 && (
          <div className={styles.nextWrapper}>
            {isStep2NextBlocked && (
              <span className={styles.tooltip} role="status">
                Save Column Mapper in Step 2 first
              </span>
            )}
            {isStep3NextBlocked && (
              <span className={styles.tooltip} role="status">
                Complete the pipeline before proceeding
              </span>
            )}
            {isStep4NextBlocked && (
              <span className={styles.tooltip} role="status">
                Train a model before viewing results
              </span>
            )}
            {isStep5NextBlocked && (
              <span className={styles.tooltip} role="status">Train a model before proceeding</span>
            )}
            <button
              type="button"
              className={`${styles.nextBtn} ${isNextDisabled ? styles.disabled : ''}`}
              onClick={isNextDisabled ? undefined : nextStep}
              disabled={isNextDisabled}
              aria-label={label}
            >
              {label} <span aria-hidden="true">&rarr;</span>
            </button>
          </div>
        )}
      </nav>
    </footer>
  );
}
