import { create } from 'zustand';

const defaultParams = {
  knn: { k: 5, distanceMetric: 'euclidean' },
  svm: { C: 0, kernel: 'rbf', gamma: 'scale' },
  dt: { maxDepth: 5, criterion: 'gini', minSamplesSplit: 2 },
  rf: { nEstimators: 100, maxDepth: 5, criterion: 'gini' },
  lr: { C: 0, solver: 'lbfgs', maxIter: 100 },
  nb: { varSmoothing: -9 },
};

const initialState = {
  selectedModel: 'knn',
  modelParams: JSON.parse(JSON.stringify(defaultParams)),
  autoRetrain: false,
  trainingStatus: 'idle',
  trainingError: null,
  trainingResults: null,
  visualizationData: null,
  comparisonList: [],
};

const useModelStore = create((set) => ({
  ...initialState,

  // Switching models clears stale visualization and resets training status
  setSelectedModel: (id) => set({ selectedModel: id, visualizationData: null, trainingStatus: 'idle', trainingError: null }),

  setModelParam: (modelId, key, value) =>
    set((s) => ({
      modelParams: {
        ...s.modelParams,
        [modelId]: { ...s.modelParams[modelId], [key]: value },
      },
    })),

  setAutoRetrain: (val) => set({ autoRetrain: val }),

  setTrainingStatus: (status) => set({ trainingStatus: status }),
  setTrainingError: (error) => set({ trainingError: error }),
  setTrainingResults: (results) => set({
    trainingResults: results,
    visualizationData: results?.visualization ?? null,
  }),

  addToComparison: (entry) =>
    set((s) => ({
      comparisonList: [
        ...s.comparisonList.filter((e) => e.model !== entry.model),
        entry,
      ],
    })),

  removeFromComparison: (modelName) =>
    set((s) => ({
      comparisonList: s.comparisonList.filter((e) => e.model !== modelName),
    })),

  clearComparison: () => set({ comparisonList: [] }),

  resetModel: () =>
    set({ ...initialState, modelParams: JSON.parse(JSON.stringify(defaultParams)) }),
}));

export default useModelStore;
