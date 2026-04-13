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
            <div
              key={step.number}
              className={`${styles.step} ${stateClass}`}
              aria-current={isActive ? 'step' : undefined}
              onClick={() => setStep(step.number)}
              style={{ cursor: 'pointer' }}
            >
              <span className={styles.stepNumber}>
                {isCompleted ? '\u2713' : step.number}
              </span>
              <div className={styles.stepText}>
                <span className={styles.stepName}>
                  {step.number}. {step.name}
                </span>
                <span className={styles.stepSubtitle}>{step.subtitle}</span>
              </div>
            </div>
          );
        })}
      </div>
    </nav>
  );
}
