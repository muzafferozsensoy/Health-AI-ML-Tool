import { apiPost } from './client';

// All 6 models mapped to backend IDs
const MODEL_ID_MAP = {
  knn: 'knn',
  svm: 'svm',
  dt: 'decision_tree',
  rf: 'random_forest',
  lr: 'logistic_regression',
  nb: 'naive_bayes',
};

/**
 * Convert frontend param format to what the backend expects.
 */
function mapParamsForBackend(modelId, params) {
  if (modelId === 'knn') {
    return {
      n_neighbors: params.k,
      metric: params.distanceMetric,
    };
  }
  if (modelId === 'svm') {
    return {
      kernel: params.kernel,
      C: Math.pow(10, params.C), // frontend stores log-scale exponent
      gamma: params.gamma,
    };
  }
  if (modelId === 'dt') {
    return {
      max_depth: params.maxDepth,
      criterion: params.criterion,
      min_samples_split: params.minSamplesSplit,
    };
  }
  if (modelId === 'rf') {
    return {
      n_estimators: params.nEstimators,
      max_depth: params.maxDepth ?? null,
    };
  }
  if (modelId === 'lr') {
    return {
      C: Math.pow(10, params.C), // log-scale exponent, same pattern as SVM
      solver: params.solver,
      max_iter: params.maxIter,
    };
  }
  if (modelId === 'nb') {
    return {
      var_smoothing: Math.pow(10, params.varSmoothing), // log-scale exponent
    };
  }
  return params;
}

/**
 * Transform backend TrainResponse into the shape frontend components expect.
 */
function transformResponse(data, frontendModelId, frontendParams) {
  const cm = data.confusion_matrix;
  const isBinary = cm.length === 2 && cm[0].length === 2;

  // Confusion matrix: 2D array → named object (binary) or null
  let confusionMatrix = null;
  if (isBinary) {
    confusionMatrix = {
      tn: cm[0][0],
      fp: cm[0][1],
      fn: cm[1][0],
      tp: cm[1][1],
    };
  }

  // Specificity: use backend value, fallback to client-side computation
  let specificity = data.specificity;
  if (specificity == null && isBinary) {
    const tn = cm[0][0];
    const fp = cm[0][1];
    specificity = (tn + fp) > 0 ? tn / (tn + fp) : 0;
    specificity = Math.round(specificity * 10000) / 10000;
  }

  // ROC curve
  const rocCurve = data.roc_curve
    ? { fpr: data.roc_curve.fpr, tpr: data.roc_curve.tpr, auc: data.roc_curve.auc }
    : null;

  return {
    model: frontendModelId,
    params: { ...frontendParams },
    metrics: {
      accuracy: data.accuracy,
      precision: data.precision,
      recall: data.recall,
      specificity: specificity ?? null,
      f1: data.f1,
      auc: data.auc ?? rocCurve?.auc ?? null,
    },
    confusionMatrix,
    rocCurve,
    visualization: data.visualization ?? null,
  };
}

export async function trainModel(modelId, params) {
  const backendModelId = MODEL_ID_MAP[modelId];
  if (!backendModelId) {
    return { data: null, error: `Model '${modelId}' is not yet supported by the backend.` };
  }

  const backendParams = mapParamsForBackend(modelId, params);
  const { data, error } = await apiPost('/step4/train', {
    model: backendModelId,
    params: backendParams,
  });

  if (error || !data) {
    return { data: null, error: error || 'Unknown error' };
  }

  return { data: transformResponse(data, modelId, params), error: null };
}
