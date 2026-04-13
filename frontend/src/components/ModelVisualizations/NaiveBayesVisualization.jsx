import styles from './NaiveBayesVisualization.module.css';

export default function NaiveBayesVisualization({ data }) {
  if (!data) return null;

  const {
    features = [],
    final_probability = 0,
    final_class = '',
    final_percentage = 0,
    class_labels = ['0', '1'],
    pos_class = '1',
    clinical_meaning = '',
  } = data;

  const isReadmit = String(final_class) === String(pos_class);
  const finalPct = final_percentage > 0 ? final_percentage : Math.round(final_probability * 100);

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <span className={styles.vizLabel}>HOW EACH FEATURE AFFECTS RISK</span>
      </div>

      <div className={styles.body}>
        {features.map((feat, i) => {
          const isIncrease = feat.direction === 'increases';
          const barColor = isIncrease ? 'var(--color-accent-red)' : 'var(--color-accent-green)';
          const pct = Math.min(100, Math.max(2, feat.percentage));
          const sign = isIncrease ? '+' : '-';
          const impactLabel = `${isIncrease ? 'INCREASES' : 'DECREASES'} RISK BY ${sign}${Math.round(feat.percentage)}%`;

          return (
            <div key={i} className={styles.featureRow}>
              <div className={styles.featureInfo}>
                <span className={styles.featureName}>{feat.name}</span>
                <span className={styles.featureValue}>= {typeof feat.value === 'number' ? feat.value.toFixed(2) : feat.value}</span>
              </div>
              <div className={styles.barArea}>
                <div className={styles.barTrack}>
                  <div
                    className={styles.barFill}
                    style={{
                      width: `${pct}%`,
                      background: barColor,
                      opacity: 0.85,
                    }}
                  />
                </div>
              </div>
              <span
                className={styles.impactLabel}
                style={{ color: barColor }}
              >
                {impactLabel}
              </span>
            </div>
          );
        })}

        {/* Final probability box */}
        <div
          className={styles.finalBox}
          style={{
            background: isReadmit ? 'rgba(248,81,73,0.12)' : 'rgba(16,183,127,0.12)',
            borderColor: isReadmit ? 'var(--color-accent-red)' : 'var(--color-accent-green)',
          }}
        >
          <span className={styles.finalLabel}>FINAL COMBINED PROBABILITY</span>
          <span
            className={styles.finalValue}
            style={{ color: isReadmit ? 'var(--color-accent-red)' : 'var(--color-accent-green)' }}
          >
            {finalPct}% {String(final_class).toUpperCase()}
          </span>
        </div>
      </div>

      <div className={styles.clinicalBar}>
        <svg width="16" height="16" viewBox="0 0 16 16" className={styles.clinicalIcon}>
          <circle cx="8" cy="8" r="7" fill="none" stroke="var(--color-accent-green)" strokeWidth="1.5" />
          <path d="M5 8l2 2 4-4" stroke="var(--color-accent-green)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
        </svg>
        <div>
          <span className={styles.clinicalLabel}>Clinical Meaning</span>
          <p className={styles.clinicalText}>{clinical_meaning}</p>
        </div>
      </div>
    </div>
  );
}
