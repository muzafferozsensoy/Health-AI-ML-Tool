import { useState, useMemo, useEffect, useRef, useCallback } from 'react';
import styles from './DecisionTreeVisualization.module.css';

const NODE_W = 130;
const NODE_H = 72;
const H_GAP = 20;
const V_GAP = 60;

function buildLayout(nodes) {
  if (!nodes || nodes.length === 0) return { nodePositions: {}, svgWidth: 600, svgHeight: 300 };

  const byDepth = {};
  nodes.forEach(n => {
    if (!byDepth[n.depth]) byDepth[n.depth] = [];
    byDepth[n.depth].push(n);
  });

  const maxDepth = Math.max(...nodes.map(n => n.depth));
  const maxNodesAtLevel = Math.max(...Object.values(byDepth).map(arr => arr.length));
  const svgWidth = Math.max(600, maxNodesAtLevel * (NODE_W + H_GAP) + H_GAP);
  const svgHeight = (maxDepth + 1) * (NODE_H + V_GAP) + V_GAP + 20;

  const nodePositions = {};
  Object.entries(byDepth).forEach(([depth, levelNodes]) => {
    const d = parseInt(depth);
    const levelW = levelNodes.length * (NODE_W + H_GAP);
    const startX = (svgWidth - levelW) / 2;
    levelNodes.forEach((n, i) => {
      nodePositions[n.id] = {
        x: startX + i * (NODE_W + H_GAP),
        y: d * (NODE_H + V_GAP) + V_GAP / 2,
      };
    });
  });

  return { nodePositions, svgWidth, svgHeight };
}

export default function DecisionTreeVisualization({ data }) {
  const scrollRef = useRef(null);
  const [zoom, setZoom] = useState(1);
  const [fitZoom, setFitZoom] = useState(1);

  if (!data) return null;

  const {
    nodes = [],
    max_depth_used = 0,
    total_nodes = 0,
    gini_root = 0,
    model_confidence = 0,
    class_labels = ['0', '1'],
    clinical_meaning = '',
  } = data;

  const { nodePositions, svgWidth, svgHeight } = useMemo(() => buildLayout(nodes), [nodes]);
  const nodeMap = useMemo(() => {
    const m = {};
    nodes.forEach(n => { m[n.id] = n; });
    return m;
  }, [nodes]);

  const posClass = class_labels[class_labels.length - 1] ?? '1';

  // Auto-fit on mount / tree structure change — run once, don't re-run on zoom
  useEffect(() => {
    if (!scrollRef.current || svgWidth === 0) return;
    const containerW = scrollRef.current.clientWidth - 24;
    const calculated = Math.min(1, Math.max(0.3, containerW / svgWidth));
    setFitZoom(calculated);
    setZoom(calculated);
    // Reset scroll to top-left after fit so tree starts centered
    scrollRef.current.scrollLeft = 0;
    scrollRef.current.scrollTop = 0;
  }, [svgWidth]); // only when tree structure changes, not on zoom

  const handleFit = useCallback(() => {
    setZoom(fitZoom);
    if (scrollRef.current) {
      scrollRef.current.scrollLeft = 0;
      scrollRef.current.scrollTop = 0;
    }
  }, [fitZoom]);
  const handleZoomIn = useCallback(() => setZoom(z => Math.min(2, parseFloat((z + 0.15).toFixed(2)))), []);
  const handleZoomOut = useCallback(() => setZoom(z => Math.max(0.2, parseFloat((z - 0.15).toFixed(2)))), []);

  const scaledW = Math.round(svgWidth * zoom);
  const scaledH = Math.round(svgHeight * zoom);
  const zoomPct = Math.round(zoom * 100);

  return (
    <div className={styles.wrapper}>
      <div className={styles.header}>
        <div>
          <span className={styles.vizLabel}>DECISION TREE</span>
          <span className={styles.subLabel}>CLASSIFICATION HIERARCHY VISUALIZATION</span>
        </div>
        <div className={styles.controls}>
          <button className={styles.zoomBtn} onClick={handleZoomIn} title="Zoom in">+</button>
          <span className={styles.zoomPct}>{zoomPct}%</span>
          <button className={styles.zoomBtn} onClick={handleZoomOut} title="Zoom out">−</button>
          <button className={styles.zoomBtnFit} onClick={handleFit} title="Fit to screen">
            <svg width="14" height="14" viewBox="0 0 14 14" fill="none">
              <path d="M1 5V1h4M9 1h4v4M13 9v4H9M5 13H1V9" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round" strokeLinejoin="round"/>
            </svg>
          </button>
        </div>
      </div>

      <div className={styles.svgScroll} ref={scrollRef}>
        <svg
          width={scaledW}
          height={scaledH}
          viewBox={`0 0 ${svgWidth} ${svgHeight}`}
          style={{ display: 'block' }}
        >
          {/* Edges */}
          {nodes.map(n => {
            const pos = nodePositions[n.id];
            if (!pos || n.parent_id == null) return null;
            const parentPos = nodePositions[n.parent_id];
            if (!parentPos) return null;
            const x1 = parentPos.x + NODE_W / 2;
            const y1 = parentPos.y + NODE_H;
            const x2 = pos.x + NODE_W / 2;
            const y2 = pos.y;
            const midY = (y1 + y2) / 2;
            const parent = nodeMap[n.parent_id];
            const isLeft = parent && parent.left_child === n.id;
            return (
              <g key={`edge-${n.id}`}>
                <path
                  d={`M${x1},${y1} C${x1},${midY} ${x2},${midY} ${x2},${y2}`}
                  fill="none"
                  stroke="var(--color-border-light)"
                  strokeWidth="1.5"
                />
                <text
                  x={(x1 + x2) / 2}
                  y={midY - 4}
                  textAnchor="middle"
                  fontSize="9"
                  fill="var(--color-text-muted)"
                  fontWeight="600"
                >
                  {isLeft ? 'YES' : 'NO'}
                </text>
              </g>
            );
          })}

          {/* Nodes */}
          {nodes.map(n => {
            const pos = nodePositions[n.id];
            if (!pos) return null;
            const isRoot = n.parent_id == null;
            const isLeaf = n.is_leaf;
            const isPosLeaf = isLeaf && String(n.predicted_class) === String(posClass);
            const probPct = Math.round((n.probability ?? 0) * 100);

            let fillColor = 'var(--color-bg-tertiary)';
            let strokeColor = 'var(--color-border)';
            let strokeW = 1.5;
            if (isRoot) { strokeColor = 'var(--color-accent-green)'; strokeW = 2; }
            if (isLeaf && isPosLeaf) { fillColor = 'rgba(248,81,73,0.12)'; strokeColor = 'var(--color-accent-red)'; strokeW = 2; }
            if (isLeaf && !isPosLeaf) { fillColor = 'rgba(16,183,127,0.12)'; strokeColor = 'var(--color-accent-green)'; strokeW = 2; }

            return (
              <g key={n.id} transform={`translate(${pos.x},${pos.y})`}>
                {isRoot && (
                  <text x={NODE_W / 2} y={-6} textAnchor="middle" fontSize="8" fontWeight="700"
                    letterSpacing="0.06em" fill="var(--color-accent-green)">
                    ROOT NODE
                  </text>
                )}
                <rect
                  width={NODE_W} height={NODE_H}
                  rx="6" ry="6"
                  fill={fillColor}
                  stroke={strokeColor}
                  strokeWidth={strokeW}
                />
                {isLeaf ? (
                  <>
                    <text x={NODE_W / 2} y={14} textAnchor="middle" fontSize="8" fontWeight="700"
                      fill="var(--color-text-muted)" letterSpacing="0.08em">
                      RESULT
                    </text>
                    <text x={NODE_W / 2} y={32} textAnchor="middle" fontSize="14" fontWeight="700"
                      fill={isPosLeaf ? 'var(--color-accent-red)' : 'var(--color-accent-green)'}>
                      {String(n.predicted_class).toUpperCase()}
                    </text>
                    <text x={NODE_W / 2} y={48} textAnchor="middle" fontSize="10"
                      fill="var(--color-text-secondary)">
                      {probPct}% Probability
                    </text>
                    <text x={NODE_W / 2} y={62} textAnchor="middle" fontSize="9"
                      fill="var(--color-text-muted)">
                      n={n.samples}
                    </text>
                  </>
                ) : (
                  <>
                    <text x={NODE_W / 2} y={18} textAnchor="middle" fontSize="11" fontWeight="600"
                      fill="var(--color-text-primary)">
                      {n.feature
                        ? `${String(n.feature).replace(/_/g, ' ')} ${n.threshold != null ? `< ${n.threshold.toFixed(2)}?` : ''}`
                        : '?'}
                    </text>
                    <line x1={8} y1={26} x2={NODE_W - 8} y2={26} stroke="var(--color-border)" strokeWidth="0.8" />
                    <text x={NODE_W / 2} y={38} textAnchor="middle" fontSize="9"
                      fill="var(--color-text-muted)">
                      GINI: {n.gini?.toFixed(2)} | SAMPLES: {n.samples}
                    </text>
                    <text x={NODE_W / 2} y={52} textAnchor="middle" fontSize="9"
                      fill="var(--color-text-muted)">
                      [{(n.values ?? []).join(', ')}]
                    </text>
                  </>
                )}
              </g>
            );
          })}
        </svg>
      </div>

      <div className={styles.metricsRow}>
        <div className={styles.metric}>
          <span className={styles.metricLabel}>Gini Impurity</span>
          <span className={styles.metricValue}>{gini_root.toFixed(3)}</span>
        </div>
        <div className={styles.metric}>
          <span className={styles.metricLabel}>Node Count</span>
          <span className={styles.metricValue}>{total_nodes}</span>
        </div>
        <div className={styles.metric}>
          <span className={styles.metricLabel}>Depth Used</span>
          <span className={styles.metricValue}>{max_depth_used}</span>
        </div>
        <div className={styles.metric}>
          <span className={styles.metricLabel}>Model Confidence</span>
          <span className={styles.metricValueAccent}>{Math.round(model_confidence * 100)}%</span>
        </div>
      </div>

      <div className={styles.clinicalBar}>
        <svg width="16" height="16" viewBox="0 0 16 16" className={styles.clinicalIcon}>
          <rect x="2" y="2" width="12" height="12" rx="2" fill="none" stroke="var(--color-accent-green)" strokeWidth="1.5" />
          <path d="M5 8h6M8 5v6" stroke="var(--color-accent-green)" strokeWidth="1.5" strokeLinecap="round" />
        </svg>
        <div>
          <span className={styles.clinicalLabel}>CLINICAL MEANING</span>
          <p className={styles.clinicalText}>{clinical_meaning}</p>
        </div>
      </div>
    </div>
  );
}
