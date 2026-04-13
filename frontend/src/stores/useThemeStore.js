import { create } from 'zustand';

const STORAGE_KEY = 'health-ai-theme';

const applyTheme = (isDark) => {
  document.documentElement.dataset.theme = isDark ? 'dark' : 'light';
};

const useThemeStore = create((set) => {
  const saved = localStorage.getItem(STORAGE_KEY);
  const isDark = saved ? saved === 'dark' : true; // default: dark
  applyTheme(isDark);

  return {
    isDark,
    toggleTheme: () =>
      set((state) => {
        const next = !state.isDark;
        applyTheme(next);
        localStorage.setItem(STORAGE_KEY, next ? 'dark' : 'light');
        return { isDark: next };
      }),
  };
});

export default useThemeStore;
