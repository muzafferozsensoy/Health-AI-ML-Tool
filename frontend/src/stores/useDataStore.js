import { create } from 'zustand';

const initialState = {
  dataSource: 'default',
  csvData: null,
  csvFileName: null,
  csvError: null,
  targetColumn: null,
  columnMappings: {},
  mapperSaved: false,
  mapperOpen: false,
  pipelineConfig: {
    imputation: 'mean',
    scaling: 'minmax',
    trainTestSplit: 80,
    smote: false,
  },
  pipelineStatus: 'idle',
  pipelineProgress: 0,
  pipelineLogs: [],
  pipelineDuration: null,
  // Backend integration state
  uploadLoading: false,
  uploadError: null,
  backendSummary: null,
  mappingLoading: false,
  mappingError: null,
  prepLoading: false,
  prepError: null,
  prepResult: null,
  prepOptions: null,
};

const useDataStore = create((set, get) => ({
  ...initialState,

  setCsvData: (data, fileName) =>
    set({
      csvData: data,
      csvFileName: fileName,
      csvError: null,
      dataSource: 'uploaded',
      mapperSaved: false,
      targetColumn: null,
      backendSummary: null,
      uploadError: null,
    }),

  setCsvError: (error) => set({ csvError: error }),

  useDefaultDataset: (data) =>
    set({
      csvData: data,
      dataSource: 'default',
      csvError: null,
      csvFileName: null,
      mapperSaved: false,
      targetColumn: null,
      backendSummary: null,
      uploadError: null,
    }),

  setTargetColumn: (col) => set({ targetColumn: col }),

  setColumnMappings: (mappings) => set({ columnMappings: mappings }),

  setMapperOpen: (open) => set({ mapperOpen: open }),

  saveMapper: () => set({ mapperSaved: true, mapperOpen: false }),

  setPipelineConfig: (key, value) =>
    set((s) => ({
      pipelineConfig: { ...s.pipelineConfig, [key]: value },
    })),

  setPipelineStatus: (status) => set({ pipelineStatus: status }),
  setPipelineProgress: (progress) => set({ pipelineProgress: progress }),
  addPipelineLog: (log) =>
    set((s) => ({ pipelineLogs: [...s.pipelineLogs, log] })),
  setPipelineDuration: (duration) => set({ pipelineDuration: duration }),

  // Backend integration setters
  setUploadLoading: (loading) => set({ uploadLoading: loading }),
  setUploadError: (error) => set({ uploadError: error }),
  setBackendSummary: (summary) => set({ backendSummary: summary }),
  setMappingLoading: (loading) => set({ mappingLoading: loading }),
  setMappingError: (error) => set({ mappingError: error }),
  setPrepLoading: (loading) => set({ prepLoading: loading }),
  setPrepError: (error) => set({ prepError: error }),
  setPrepResult: (result) => set({ prepResult: result }),
  setPrepOptions: (options) => set({ prepOptions: options }),

  resetPipeline: () =>
    set({
      pipelineStatus: 'idle',
      pipelineProgress: 0,
      pipelineLogs: [],
      pipelineDuration: null,
      prepResult: null,
      prepError: null,
    }),

  resetAll: () => set({ ...initialState }),
}));

export default useDataStore;
