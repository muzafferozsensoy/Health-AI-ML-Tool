import styles from './LogisticRegressionVisualization.module.css';

const W = 480;
const H = 300;
const PAD = { top: 30, right: 40, bottom: 50, left: 58 };
const PLOT_W = W - PAD.left - PAD.right;
const PLOT_H = H - PAD.top - PAD.bottom;

function toSvg(x, y) {
  return {
    sx: PAD.left + x * PLOT_W,
    sy: PAD.top + (1 - y) * PLOT_H,
  };
}

const Y_TICKS = [0, 0.25, 0.5, 0.75, 1.0];
const Y_LABELS = ['0%', '25%', '50%', '75%', '100%'];

export default function LogisticRegressionVisualization({ data }) {
  if (!data) return null;

  const {
    feature_name = 'Feature',
    sigmoid_curve = [],
    threshold_point,
    solver = 'lbfgs',
    penalty = 'l2',
    clinical_meaning = '',
    pos_class = '1',
  } = data;

  // Build polyline points
  const curvePts = sigmoid_curve
    .map(pt => {
      const { sx, sy } = toSvg(pt.x, pt.y);
      return `${sx},${sy}`;
    })
    .join(' ');

  const tp = threshold_point;
  const tpSvg = tp ? toSvg(tp.x, tp.y) : null;
  const featDisplay = feature_name.replace(/_/g, ' ').replace(/\b\w/g, c => c.toUpperCase());

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <span className={styles.vizLabel}>PROBABILITY S-CURVE (SIGMOID)</span>
        <span className={styles.subLabel}>● RISK FUNCTION</span>
      </div>

      <svg viewBox={`0 0 ${W} ${H}`} className={styles.svg}>
        {/* Grid lines */}
        {Y_TICKS.map((t, i) => {
          const sy = PAD.top + (1 - t) * PLOT_H;
          return (
            <g key={t}>
              <line x1={PAD.left} y1={sy} x2={PAD.left + PLOT_W} y2={sy}
                stroke="var(--color-border)" strokeWidth="0.5" strokeDasharray="3 3" />
              <text x={PAD.left - 6} y={sy + 4} textAnchor="end" fontSize="10" fill="var(--color-text-muted)">
                {Y_LABELS[i]}
              </text>
            </g>
          );
        })}

        {/* X grid */}
        {[0.25, 0.5, 0.75].map(t => (
          <line key={t} x1={PAD.left + t * PLOT_W} y1={PAD.top} x2={PAD.left + t * PLOT_W} y2={PAD.top + PLOT_H}
            stroke="var(--color-border)" strokeWidth="0.5" strokeDasharray="3 3" />
        ))}

        {/* Plot border */}
        <rect x={PAD.left} y={PAD.top} width={PLOT_W} height={PLOT_H}
          fill="none" stroke="var(--color-border)" strokeWidth="1" />

        {/* Threshold crosshairs */}
        {tpSvg && (
          <>
            <line x1={tpSvg.sx} y1={PAD.top} x2={tpSvg.sx} y2={tpSvg.sy}
              stroke="var(--color-accent-red)" strokeWidth="1" strokeDasharray="5 3" opacity="0.6" />
            <line x1={PAD.left} y1={tpSvg.sy} x2={tpSvg.sx} y2={tpSvg.sy}
              stroke="var(--color-accent-red)" strokeWidth="1" strokeDasharray="5 3" opacity="0.6" />
          </>
        )}

        {/* Sigmoid curve */}
        {curvePts && (
          <polyline
            points={curvePts}
            fill="none"
            stroke="var(--color-accent-green)"
            strokeWidth="2.5"
            strokeLinecap="round"
            strokeLinejoin="round"
          />
        )}

        {/* Threshold dot + label */}
        {tpSvg && (
          <>
            <circle cx={tpSvg.sx} cy={tpSvg.sy} r={7} fill="var(--color-accent-red)" />
            <circle cx={tpSvg.sx} cy={tpSvg.sy} r={4} fill="#fff" />
            {/* Label box */}
            <g transform={`translate(${tpSvg.sx + 10},${tpSvg.sy - 22})`}>
              <rect x="-4" y="-14" width={Math.max(140, (tp.label?.length ?? 0) * 7)} height="20"
                rx="4" fill="var(--color-bg-card)" stroke="var(--color-accent-red)" strokeWidth="1" />
              <text x="2" y="-1" fontSize="10" fill="var(--color-text-primary)" fontWeight="600">
                CLINICAL THRESHOLD
              </text>
            </g>
            <text x={tpSvg.sx + 6} y={tpSvg.sy + 16} fontSize="10" fill="var(--color-accent-red)" fontWeight="700">
              {tp.label}
            </text>
          </>
        )}

        {/* Axis labels */}
        <text x={PAD.left + PLOT_W / 2} y={H - 4}
          textAnchor="middle" fontSize="11" fill="var(--color-text-secondary)">
          {featDisplay} — Patient Health
        </text>
        <text x={14} y={PAD.top + PLOT_H / 2}
          textAnchor="middle" fontSize="10" fill="var(--color-text-secondary)"
          transform={`rotate(-90,14,${PAD.top + PLOT_H / 2})`}>
          P(readmission) — 0% to 100%
        </text>

        {/* Annotation: solver + penalty */}
        <text x={W - PAD.right - 4} y={PAD.top + PLOT_H - 4}
          textAnchor="end" fontSize="9" fill="var(--color-text-muted)" fontFamily="var(--font-mono)">
          SOLVER: {solver.toUpperCase()} | PENALTY: {penalty.toUpperCase()}
        </text>
      </svg>

      <div className={styles.clinicalBar}>
        <svg width="16" height="16" viewBox="0 0 16 16" className={styles.clinicalIcon}>
          <circle cx="8" cy="8" r="7" fill="none" stroke="var(--color-accent-green)" strokeWidth="1.5" />
          <path d="M5 8l2 2 4-4" stroke="var(--color-accent-green)" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round" fill="none" />
        </svg>
        <div>
          <span className={styles.clinicalLabel}>CLINICAL MEANING</span>
          <p className={styles.clinicalText}>{clinical_meaning}</p>
        </div>
      </div>
    </div>
  );
}
