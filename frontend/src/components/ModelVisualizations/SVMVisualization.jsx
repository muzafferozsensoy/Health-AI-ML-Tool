import styles from './SVMVisualization.module.css';

const W = 480;
const H = 340;
const PAD = { top: 36, right: 20, bottom: 44, left: 48 };
const PLOT_W = W - PAD.left - PAD.right;
const PLOT_H = H - PAD.top - PAD.bottom;

function toSvg(x, y) {
  return {
    sx: PAD.left + x * PLOT_W,
    sy: PAD.top + (1 - y) * PLOT_H,
  };
}

export default function SVMVisualization({ data }) {
  if (!data) return null;

  const {
    feature_names = ['Feature 1', 'Feature 2'],
    scatter_points = [],
    decision_boundary = [],
    class_labels = ['0', '1'],
    pos_class = '1',
    clinical_meaning = '',
  } = data;

  // Build polyline points string for decision boundary
  const boundaryPts = decision_boundary
    .map(pt => {
      const { sx, sy } = toSvg(pt.x, pt.y);
      return `${sx},${sy}`;
    })
    .join(' ');

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <span className={styles.vizLabel}>SVM DECISION BOUNDARY</span>
        <div className={styles.legend}>
          <span className={styles.legendItem}>
            <svg width="10" height="10"><circle cx="5" cy="5" r="5" fill="var(--color-accent-green)" /></svg>
            SAFE
          </span>
          <span className={styles.legendItem}>
            <svg width="10" height="10"><circle cx="5" cy="5" r="5" fill="var(--color-accent-red)" /></svg>
            READMITTED
          </span>
          <span className={styles.legendItem}>
            <svg width="12" height="12">
              <circle cx="6" cy="6" r="5" fill="none" stroke="#fff" strokeWidth="1.5" />
            </svg>
            SUPPORT VECTOR
          </span>
        </div>
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} className={styles.svg}>
        {/* Grid lines */}
        {[0.25, 0.5, 0.75].map(t => (
          <g key={t}>
            <line x1={PAD.left + t * PLOT_W} y1={PAD.top} x2={PAD.left + t * PLOT_W} y2={PAD.top + PLOT_H}
              stroke="var(--color-border)" strokeWidth="0.5" strokeDasharray="3 3" />
            <line x1={PAD.left} y1={PAD.top + t * PLOT_H} x2={PAD.left + PLOT_W} y2={PAD.top + t * PLOT_H}
              stroke="var(--color-border)" strokeWidth="0.5" strokeDasharray="3 3" />
          </g>
        ))}

        <rect x={PAD.left} y={PAD.top} width={PLOT_W} height={PLOT_H}
          fill="none" stroke="var(--color-border)" strokeWidth="1" />

        {/* Decision boundary */}
        {boundaryPts && (
          <polyline
            points={boundaryPts}
            fill="none"
            stroke="#ffffff"
            strokeWidth="2"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        )}

        {/* Scatter points */}
        {scatter_points.map((pt, i) => {
          const { sx, sy } = toSvg(pt.x, pt.y);
          const isPos = String(pt.label) === String(pos_class);
          const fill = isPos ? 'var(--color-accent-red)' : 'var(--color-accent-green)';
          return (
            <g key={i}>
              {pt.is_support_vector && (
                <circle cx={sx} cy={sy} r={9} fill="none" stroke="#ffffff" strokeWidth="2" />
              )}
              <circle cx={sx} cy={sy} r={5} fill={fill} opacity="0.85" />
            </g>
          );
        })}

        {/* Axis labels */}
        <text x={PAD.left + PLOT_W / 2} y={H - 4}
          textAnchor="middle" fontSize="11" fill="var(--color-text-secondary)">
          {feature_names[0]}
        </text>
        <text x={12} y={PAD.top + PLOT_H / 2}
          textAnchor="middle" fontSize="11" fill="var(--color-text-secondary)"
          transform={`rotate(-90,12,${PAD.top + PLOT_H / 2})`}>
          {feature_names[1]}
        </text>
      </svg>

      <div className={styles.clinicalBar}>
        <svg width="16" height="16" viewBox="0 0 16 16" className={styles.clinicalIcon}>
          <rect x="2" y="2" width="12" height="12" rx="2" fill="none" stroke="var(--color-accent-green)" strokeWidth="1.5" />
          <line x1="8" y1="5" x2="8" y2="11" stroke="var(--color-accent-green)" strokeWidth="1.5" strokeLinecap="round" />
          <line x1="5" y1="8" x2="11" y2="8" stroke="var(--color-accent-green)" strokeWidth="1.5" strokeLinecap="round" />
        </svg>
        <div>
          <span className={styles.clinicalLabel}>CLINICAL MEANING</span>
          <p className={styles.clinicalText}>{clinical_meaning}</p>
        </div>
      </div>
    </div>
  );
}
