import { useEffect } from 'react';
import { domains } from '../../data/domains';
import useAppStore from '../../stores/useAppStore';
import { fetchClinicalContext } from '../../api';
import MLJourneyTable from '../../components/MLJourneyTable/MLJourneyTable';
import styles from './Step1ClinicalContext.module.css';

export default function Step1ClinicalContext() {
  const selectedDomainId = useAppStore((s) => s.selectedDomainId);
  const clinicalContext = useAppStore((s) => s.clinicalContext);
  const contextLoading = useAppStore((s) => s.contextLoading);
  const setClinicalContext = useAppStore((s) => s.setClinicalContext);
  const setContextLoading = useAppStore((s) => s.setContextLoading);

  const domain = domains.find((d) => d.id === selectedDomainId) || domains[0];

  useEffect(() => {
    let cancelled = false;
    setClinicalContext(null);
    setContextLoading(true);

    fetchClinicalContext(selectedDomainId).then(({ data, error }) => {
      if (cancelled) return;
      setContextLoading(false);
      if (!error && data) setClinicalContext(data);
    });

    return () => { cancelled = true; };
  }, [selectedDomainId]);

  return (
    <div className={styles.layout}>
      <div className={styles.leftPanel}>
        <div className={styles.scenarioCard}>
          <div className={styles.scenarioHeader}>
            <span className={styles.scenarioIcon}>🩺</span>
            <div>
              <h2 className={styles.scenarioTitle}>Clinical Scenario</h2>
              <span className={styles.focusLabel}>{domain.focusLabel}</span>
            </div>
          </div>

          <blockquote className={styles.problemBlock}>
            &ldquo;PROBLEM: {domain.scenario}&rdquo;
          </blockquote>

          {/* Backend-enriched ML context */}
          {contextLoading && (
            <div className={styles.tipCard}>
              <p className={styles.tipText}>Loading clinical context...</p>
            </div>
          )}

          {clinicalContext && (
            <div className={styles.tipCard}>
              <div className={styles.tipHeader}>
                <span className={styles.tipDot}>●</span>
                <span className={styles.tipLabel}>ML CONTEXT</span>
              </div>
              <p className={styles.tipText}>
                <strong>Goal:</strong> {clinicalContext.goal}
              </p>
              <p className={styles.tipText}>
                <strong>Target Column:</strong> {clinicalContext.target_column}
              </p>
              <p className={styles.tipText}>
                <strong>Recommended Features:</strong>{' '}
                {clinicalContext.recommended_features.join(', ')}
              </p>
              <p className={styles.tipText}>
                <strong>Class Labels:</strong>{' '}
                {Object.entries(clinicalContext.class_labels)
                  .map(([k, v]) => `${k} = ${v}`)
                  .join(', ')}
              </p>
            </div>
          )}

          <div className={styles.tipCard}>
            <div className={styles.tipHeader}>
              <span className={styles.tipDot}>●</span>
              <span className={styles.tipLabel}>EDUCATIONAL TIP</span>
            </div>
            <p className={styles.tipText}>{domain.tip}</p>
          </div>

          <div className={styles.disclaimer}>
            <span className={styles.disclaimerIcon}>☑</span>
            <p>
              <strong>Remember:</strong> {domain.disclaimer}
            </p>
          </div>

          <div className={styles.imagePlaceholder}>
            <div className={styles.imageInner}>
              <span className={styles.imageIcon}>📊</span>
              <span className={styles.imageAlt}>{domain.imageAlt}</span>
            </div>
          </div>
        </div>
      </div>

      <div className={styles.rightPanel}>
        <MLJourneyTable currentStep={1} />
      </div>
    </div>
  );
}
