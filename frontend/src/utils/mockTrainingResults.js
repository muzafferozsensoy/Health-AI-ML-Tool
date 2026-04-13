/**
 * Generates deterministic mock training results when the backend is unavailable.
 * Uses a simple hash of model + params to produce consistent but varied results.
 */

function hashCode(str) {
  let hash = 0;
  for (let i = 0; i < str.length; i++) {
    hash = ((hash << 5) - hash + str.charCodeAt(i)) | 0;
  }
  return hash;
}

function seededRandom(seed) {
  const x = Math.sin(seed) * 10000;
  return x - Math.floor(x);
}

function clamp(val, min = 0, max = 1) {
  return Math.min(max, Math.max(min, val));
}

// ── Mock visualization generators ────────────────────────────────────────────

function generateMockVisualization(modelId, seed) {
  const r = (offset) => seededRandom(seed + offset);

  if (modelId === 'knn') {
    const scatter = [];
    for (let i = 0; i < 80; i++) {
      scatter.push({
        x: clamp(r(i * 3 + 100)),
        y: clamp(r(i * 3 + 101)),
        label: r(i * 3 + 102) > 0.45 ? '1' : '0',
        is_neighbor: i < 5,
      });
    }
    return {
      type: 'knn',
      feature_names: ['Ejection Fraction', 'Age'],
      scatter_points: scatter,
      query_point: { x: 0.52, y: 0.48 },
      radius: 0.18,
      k: 5,
      class_labels: ['0', '1'],
      pos_class: '1',
      clinical_meaning:
        'The KNN model identifies the 5 most similar patients to the query patient based on Ejection Fraction and Age. The majority class among these neighbors determines the prediction.',
    };
  }

  if (modelId === 'svm') {
    const scatter = [];
    for (let i = 0; i < 80; i++) {
      const x = clamp(r(i * 3 + 200));
      const y = clamp(r(i * 3 + 201));
      scatter.push({ x, y, label: x + y > 1.1 ? '1' : '0', is_support_vector: i < 6 });
    }
    const boundary = [];
    for (let i = 0; i <= 20; i++) {
      boundary.push({ x: i / 20, y: clamp(0.25 + i / 20 * 0.5 + (r(i + 300) - 0.5) * 0.1) });
    }
    return {
      type: 'svm',
      feature_names: ['Ejection Fraction', 'Age'],
      scatter_points: scatter,
      decision_boundary: boundary,
      class_labels: ['0', '1'],
      pos_class: '1',
      clinical_meaning:
        'The RBF kernel SVM draws a non-linear boundary separating patients. Patients on the boundary (support vectors, outlined) are the most critical cases.',
    };
  }

  if (modelId === 'dt') {
    return {
      type: 'decision_tree',
      nodes: [
        { id: 0, parent_id: null, depth: 0, feature: 'Ejection Fraction', threshold: 0.38, gini: 0.48, samples: 640, values: [310, 330], is_leaf: false, left_child: 1, right_child: 2, predicted_class_idx: 1, predicted_class: '1', probability: 0.52 },
        { id: 1, parent_id: 0, depth: 1, feature: 'Serum Creatinine', threshold: 1.2, gini: 0.26, samples: 184, values: [136, 48], is_leaf: false, left_child: 3, right_child: 4, predicted_class_idx: 0, predicted_class: '0', probability: 0.74 },
        { id: 2, parent_id: 0, depth: 1, feature: 'Age', threshold: 65, gini: 0.15, samples: 456, values: [174, 282], is_leaf: false, left_child: 5, right_child: 6, predicted_class_idx: 1, predicted_class: '1', probability: 0.62 },
        { id: 3, parent_id: 1, depth: 2, feature: null, threshold: null, gini: 0.14, samples: 120, values: [101, 19], is_leaf: true, left_child: null, right_child: null, predicted_class_idx: 0, predicted_class: '0', probability: 0.84 },
        { id: 4, parent_id: 1, depth: 2, feature: null, threshold: null, gini: 0.34, samples: 64, values: [35, 29], is_leaf: true, left_child: null, right_child: null, predicted_class_idx: 0, predicted_class: '0', probability: 0.55 },
        { id: 5, parent_id: 2, depth: 2, feature: null, threshold: null, gini: 0.28, samples: 175, values: [55, 120], is_leaf: true, left_child: null, right_child: null, predicted_class_idx: 1, predicted_class: '1', probability: 0.69 },
        { id: 6, parent_id: 2, depth: 2, feature: null, threshold: null, gini: 0.12, samples: 281, values: [119, 162], is_leaf: true, left_child: null, right_child: null, predicted_class_idx: 1, predicted_class: '1', probability: 0.58 },
      ],
      max_depth_used: 2,
      total_nodes: 7,
      gini_root: 0.48,
      model_confidence: 0.92,
      class_labels: ['0', '1'],
      clinical_meaning:
        'The tree first splits on Ejection Fraction, the strongest clinical predictor. Follow YES/NO branches to reach a prediction at each leaf node.',
    };
  }

  if (modelId === 'rf') {
    const verdicts = Array.from({ length: 100 }, (_, i) => (r(i + 400) > 0.35 ? 1 : 0));
    const n_readmit = verdicts.filter(v => v === 1).length;
    return {
      type: 'random_forest',
      n_trees: 100,
      votes: { '1': n_readmit, '0': 100 - n_readmit },
      ensemble_consistency: n_readmit > 70 ? 'HIGH' : n_readmit > 55 ? 'MEDIUM' : 'LOW',
      tree_verdicts: verdicts,
      class_labels: ['0', '1'],
      pos_class: '1',
      clinical_meaning: `${n_readmit} out of 100 trees predict readmission. Majority vote determines the final prediction.`,
    };
  }

  if (modelId === 'lr') {
    // Generate sigmoid curve
    const sigmoid_curve = Array.from({ length: 60 }, (_, i) => {
      const x = i / 59;
      const logit = 3.5 - 7 * x + (r(i + 500) - 0.5) * 0.2;
      const y = 1 / (1 + Math.exp(-logit));
      return { x: Math.round(x * 1000) / 1000, y: Math.round(y * 1000) / 1000 };
    });
    return {
      type: 'logistic_regression',
      feature_name: 'Ejection Fraction',
      sigmoid_curve,
      threshold_point: { x: 0.38, y: 0.5, label: 'EF=0.38 → 50% Risk' },
      solver: 'lbfgs',
      penalty: 'l2',
      class_labels: ['0', '1'],
      pos_class: '1',
      clinical_meaning:
        'The S-curve shows how Ejection Fraction drives readmission probability. At EF=0.38, the model predicts 50% risk — the clinical decision threshold.',
    };
  }

  if (modelId === 'nb') {
    return {
      type: 'naive_bayes',
      features: [
        { name: 'Ejection Fraction', raw_name: 'ejection_fraction', value: 0.2, log_ratio: 1.82, direction: 'increases', percentage: 45.2 },
        { name: 'Age', raw_name: 'age', value: 0.71, log_ratio: 0.85, direction: 'increases', percentage: 21.1 },
        { name: 'Serum Creatinine', raw_name: 'serum_creatinine', value: 0.13, log_ratio: 0.08, direction: 'increases', percentage: 2.0 },
        { name: 'Smoking', raw_name: 'smoking', value: 0.0, log_ratio: -0.20, direction: 'decreases', percentage: 5.0 },
        { name: 'Platelets', raw_name: 'platelets', value: 0.45, log_ratio: -0.62, direction: 'decreases', percentage: 15.4 },
      ],
      final_probability: 0.68,
      final_class: '1',
      final_percentage: 68.0,
      class_labels: ['0', '1'],
      pos_class: '1',
      clinical_meaning:
        'Naïve Bayes treats each measurement independently. Ejection Fraction is the strongest risk factor. Final combined probability: 68% readmission.',
    };
  }

  return null;
}

// ── Main export ───────────────────────────────────────────────────────────────

export function generateMockResults(modelId, params) {
  const seed = hashCode(modelId + JSON.stringify(params));

  const accuracy = clamp(0.65 + seededRandom(seed + 1) * 0.28, 0.4, 0.98);
  const precision = clamp(0.60 + seededRandom(seed + 2) * 0.32, 0.35, 0.97);
  const recall = clamp(0.55 + seededRandom(seed + 3) * 0.38, 0.30, 0.98);
  const specificity = clamp(0.68 + seededRandom(seed + 4) * 0.25, 0.40, 0.98);
  const f1 =
    precision + recall > 0
      ? (2 * precision * recall) / (precision + recall)
      : 0;
  const auc = clamp(0.60 + seededRandom(seed + 5) * 0.32, 0.40, 0.98);

  const total = 200;
  const positives = Math.round(total * 0.4);
  const negatives = total - positives;
  const tp = Math.round(positives * recall);
  const fn = positives - tp;
  const tn = Math.round(negatives * specificity);
  const fp = negatives - tn;

  // Generate ROC curve points
  const numPoints = 12;
  const fpr = [0];
  const tpr = [0];
  for (let i = 1; i < numPoints - 1; i++) {
    const t = i / (numPoints - 1);
    const baseFpr = t;
    const baseTpr = Math.pow(t, 1 / (1 + auc));
    fpr.push(clamp(baseFpr + seededRandom(seed + 10 + i) * 0.05 - 0.025));
    tpr.push(clamp(baseTpr + seededRandom(seed + 20 + i) * 0.05));
  }
  fpr.push(1);
  tpr.push(1);

  // Ensure monotonically increasing
  for (let i = 1; i < fpr.length; i++) {
    if (fpr[i] < fpr[i - 1]) fpr[i] = fpr[i - 1] + 0.01;
    if (tpr[i] < tpr[i - 1]) tpr[i] = tpr[i - 1] + 0.01;
  }

  return {
    model: modelId,
    params: { ...params },
    metrics: {
      accuracy: Math.round(accuracy * 1000) / 1000,
      precision: Math.round(precision * 1000) / 1000,
      recall: Math.round(recall * 1000) / 1000,
      specificity: Math.round(specificity * 1000) / 1000,
      f1: Math.round(f1 * 1000) / 1000,
      auc: Math.round(auc * 1000) / 1000,
    },
    confusionMatrix: { tn, fp, fn, tp },
    rocCurve: { fpr, tpr, auc: Math.round(auc * 1000) / 1000 },
    visualization: generateMockVisualization(modelId, seed),
  };
}
