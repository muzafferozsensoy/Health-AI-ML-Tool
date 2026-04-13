import styles from './KNNVisualization.module.css';

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

function StarPath(cx, cy, outerR = 9, innerR = 4, points = 6) {
  const pts = [];
  for (let i = 0; i < points * 2; i++) {
    const angle = (Math.PI / points) * i - Math.PI / 2;
    const r = i % 2 === 0 ? outerR : innerR;
    pts.push(`${cx + r * Math.cos(angle)},${cy + r * Math.sin(angle)}`);
  }
  return pts.join(' ');
}

export default function KNNVisualization({ data }) {
  if (!data) return null;

  const {
    feature_names = ['Feature 1', 'Feature 2'],
    scatter_points = [],
    query_point,
    radius = 0.18,
    k = 5,
    class_labels = ['0', '1'],
    pos_class = '1',
    clinical_meaning = '',
  } = data;

  const negClass = class_labels.find(c => c !== pos_class) ?? class_labels[0];
  const qp = query_point ?? { x: 0.5, y: 0.5 };
  const { sx: qsx, sy: qsy } = toSvg(qp.x, qp.y);
  const svgRadius = radius * PLOT_W;

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <span className={styles.vizLabel}>LIVE VISUALIZATION</span>
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
            <svg width="12" height="12"><polygon points={StarPath(6, 6, 6, 2.5, 6)} fill="#fff" /></svg>
            QUERY PATIENT
          </span>
        </div>
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} className={styles.svg}>
        {/* Grid lines */}
        {[0.25, 0.5, 0.75].map(t => (
          <g key={t}>
            <line
              x1={PAD.left + t * PLOT_W} y1={PAD.top}
              x2={PAD.left + t * PLOT_W} y2={PAD.top + PLOT_H}
              stroke="var(--color-border)" strokeWidth="0.5" strokeDasharray="3 3"
            />
            <line
              x1={PAD.left} y1={PAD.top + t * PLOT_H}
              x2={PAD.left + PLOT_W} y2={PAD.top + t * PLOT_H}
              stroke="var(--color-border)" strokeWidth="0.5" strokeDasharray="3 3"
            />
          </g>
        ))}

        {/* Plot border */}
        <rect x={PAD.left} y={PAD.top} width={PLOT_W} height={PLOT_H}
          fill="none" stroke="var(--color-border)" strokeWidth="1" />

        {/* Neighbor circle */}
        <circle
          cx={qsx} cy={qsy} r={svgRadius}
          fill="rgba(16,183,127,0.06)"
          stroke="var(--color-accent-green)"
          strokeWidth="1.5"
          strokeDasharray="6 3"
        />

        {/* Scatter points */}
        {scatter_points.map((pt, i) => {
          const { sx, sy } = toSvg(pt.x, pt.y);
          const isPos = String(pt.label) === String(pos_class);
          const fill = isPos ? 'var(--color-accent-red)' : 'var(--color-accent-green)';
          return (
            <g key={i}>
              {pt.is_neighbor && (
                <circle cx={sx} cy={sy} r={9} fill="none" stroke="#fff" strokeWidth="1.5" opacity="0.5" />
              )}
              <circle cx={sx} cy={sy} r={5} fill={fill} opacity="0.85" />
            </g>
          );
        })}

        {/* Query patient star */}
        <circle cx={qsx} cy={qsy} r={16} fill="rgba(255,255,255,0.06)" />
        <polygon
          points={StarPath(qsx, qsy, 9, 4, 6)}
          fill="#fff"
          stroke="var(--color-accent-green)"
          strokeWidth="1"
        />

        {/* Axis labels */}
        <text
          x={PAD.left + PLOT_W / 2} y={H - 4}
          textAnchor="middle" fontSize="11" fill="var(--color-text-secondary)"
        >
          {feature_names[0]}
        </text>
        <text
          x={12} y={PAD.top + PLOT_H / 2}
          textAnchor="middle" fontSize="11" fill="var(--color-text-secondary)"
          transform={`rotate(-90,12,${PAD.top + PLOT_H / 2})`}
        >
          {feature_names[1]}
        </text>

        {/* K label on circle */}
        <text
          x={qsx + svgRadius + 4} y={qsy - 4}
          fontSize="10" fill="var(--color-accent-green)"
        >
          K={k}
        </text>
      </svg>

      <div className={styles.clinicalBar}>
        <svg width="16" height="16" viewBox="0 0 16 16" className={styles.clinicalIcon}>
          <circle cx="8" cy="8" r="7" fill="none" stroke="var(--color-accent-green)" strokeWidth="1.5" />
          <path d="M8 4v4l3 2" stroke="var(--color-accent-green)" strokeWidth="1.5" strokeLinecap="round" fill="none" />
        </svg>
        <div>
          <span className={styles.clinicalLabel}>CLINICAL MEANING</span>
          <p className={styles.clinicalText}>{clinical_meaning}</p>
        </div>
      </div>
    </div>
  );
}
