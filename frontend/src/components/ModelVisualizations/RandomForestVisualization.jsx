import styles from './RandomForestVisualization.module.css';

function TreeIcon({ voted1, size = 22 }) {
  const fill = voted1 ? 'var(--color-accent-red)' : 'var(--color-accent-green)';
  return (
    <svg width={size} height={size} viewBox="0 0 22 22">
      <polygon points="11,2 20,19 2,19" fill={fill} opacity="0.85" />
      <rect x="9" y="17" width="4" height="3" fill={fill} opacity="0.6" />
    </svg>
  );
}

export default function RandomForestVisualization({ data }) {
  if (!data) return null;

  const {
    n_trees = 100,
    votes = {},
    ensemble_consistency = 'MEDIUM',
    tree_verdicts = [],
    class_labels = ['0', '1'],
    pos_class = '1',
    clinical_meaning = '',
  } = data;

  const negClass = class_labels.find(c => c !== pos_class) ?? class_labels[0];
  const readmitCount = votes[String(pos_class)] ?? tree_verdicts.filter(v => v === 1).length;
  const safeCount = votes[String(negClass)] ?? (tree_verdicts.length - readmitCount);
  const total = readmitCount + safeCount || 1;
  const readmitPct = Math.round((readmitCount / total) * 100);
  const safePct = 100 - readmitPct;

  const consistencyColor = {
    HIGH: 'var(--color-accent-green)',
    MEDIUM: 'var(--color-accent-orange)',
    LOW: 'var(--color-accent-red)',
  }[ensemble_consistency] ?? 'var(--color-text-secondary)';

  const displayVerdicts = tree_verdicts.slice(0, 100);

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <span className={styles.vizLabel}>RANDOM FOREST — VOTE VISUALIZATION</span>
      </div>

      <div className={styles.body}>
        {/* Tree icon grid */}
        <div className={styles.treeGrid}>
          {displayVerdicts.map((v, i) => (
            <TreeIcon key={i} voted1={v === 1} size={20} />
          ))}
        </div>

        {/* Vote bars */}
        <div className={styles.voteBars}>
          <div className={styles.voteRow}>
            <span className={styles.voteLabel} style={{ color: 'var(--color-accent-red)' }}>
              {String(pos_class).toUpperCase()}: {readmitPct}%
            </span>
            <div className={styles.barTrack}>
              <div className={styles.barFill}
                style={{ width: `${readmitPct}%`, background: 'var(--color-accent-red)' }} />
            </div>
          </div>
          <div className={styles.voteRow}>
            <span className={styles.voteLabel} style={{ color: 'var(--color-accent-green)' }}>
              {String(negClass).toUpperCase()}: {safePct}%
            </span>
            <div className={styles.barTrack}>
              <div className={styles.barFill}
                style={{ width: `${safePct}%`, background: 'var(--color-accent-green)' }} />
            </div>
          </div>
        </div>

        {/* Model status */}
        <div className={styles.statusRow}>
          <div className={styles.statusBadge}>
            <svg width="16" height="16" viewBox="0 0 16 16">
              <circle cx="8" cy="8" r="7" fill="none" stroke={consistencyColor} strokeWidth="1.5" />
              <path d="M5 8l2 2 4-4" stroke={consistencyColor} strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
            </svg>
            <span className={styles.statusText}>
              Ensemble Consistency:{' '}
              <strong style={{ color: consistencyColor }}>{ensemble_consistency}</strong>
            </span>
          </div>
          <span className={styles.statusValidated}>MODEL STATUS: VALIDATED</span>
        </div>
      </div>

      <div className={styles.clinicalBar}>
        <svg width="16" height="16" viewBox="0 0 16 16" className={styles.clinicalIcon}>
          <circle cx="8" cy="8" r="7" fill="none" stroke="var(--color-accent-green)" strokeWidth="1.5" />
          <path d="M8 4v4l3 2" stroke="var(--color-accent-green)" strokeWidth="1.5" strokeLinecap="round" fill="none" />
        </svg>
        <div>
          <div className={styles.clinicalHeader}>
            <span className={styles.clinicalLabel}>CLINICAL MEANING</span>
            <span className={styles.confidenceBadge}>CONFIDENCE: {readmitPct}%</span>
          </div>
          <p className={styles.clinicalText}>{clinical_meaning}</p>
        </div>
      </div>
    </div>
  );
}
