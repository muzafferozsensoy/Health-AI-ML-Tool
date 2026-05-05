import { steps } from '../../data/stepDefinitions';
import useAppStore from '../../stores/useAppStore';
import styles from './Stepper.module.css';

export default function Stepper() {
  const currentStep = useAppStore((s) => s.currentStep);
  const setStep = useAppStore((s) => s.setStep);

  return (
    <nav className={styles.stepper} aria-label="Workflow steps">
      <div className={styles.stepsContainer}>
        {steps.map((step) => {
          const isActive = step.number === currentStep;
          const isCompleted = step.number < currentStep;

          let stateClass = styles.future;
          if (isActive) stateClass = styles.active;
          if (isCompleted) stateClass = styles.completed;

          return (
            <button
              key={step.number}
              type="button"
              className={`${styles.step} ${stateClass}`}
              aria-current={isActive ? 'step' : undefined}
              aria-label={`Step ${step.number}: ${step.name}${isCompleted ? ' (completed)' : ''}`}
              onClick={() => setStep(step.number)}
            >
              <span className={styles.stepNumber} aria-hidden="true">
                {isCompleted ? '\u2713' : step.number}
              </span>
              <span className={styles.stepText}>
                <span className={styles.stepName}>
                  {step.number}. {step.name}
                </span>
                <span className={styles.stepSubtitle}>{step.subtitle}</span>
              </span>
            </button>
          );
        })}
      </div>
    </nav>
  );
}
