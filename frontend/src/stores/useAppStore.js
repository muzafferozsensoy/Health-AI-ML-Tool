import { create } from 'zustand';

const useAppStore = create((set) => ({
  currentStep: 1,
  selectedDomainId: 'cardiology',
  showHelp: false,
  clinicalContext: null,
  contextLoading: false,
  contextError: null,

  setStep: (step) => set({ currentStep: step }),
  nextStep: () =>
    set((s) => ({ currentStep: Math.min(s.currentStep + 1, 7) })),
  prevStep: () =>
    set((s) => ({ currentStep: Math.max(s.currentStep - 1, 1) })),
  setDomain: (id) => set({ selectedDomainId: id }),
  toggleHelp: () => set((s) => ({ showHelp: !s.showHelp })),
  setClinicalContext: (ctx) => set({ clinicalContext: ctx }),
  setContextLoading: (loading) => set({ contextLoading: loading }),
  setContextError: (error) => set({ contextError: error }),
  reset: () =>
    set({
      currentStep: 1,
      selectedDomainId: 'cardiology',
      showHelp: false,
      clinicalContext: null,
      contextLoading: false,
      contextError: null,
    }),
}));

export default useAppStore;
