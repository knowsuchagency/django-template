import { create } from 'zustand'
import { persist } from 'zustand/middleware'

type Theme = 'light' | 'dark' | 'system'

interface ThemeState {
  theme: Theme
  effectiveTheme: 'light' | 'dark'
  setTheme: (theme: Theme) => void
  updateEffectiveTheme: () => void
}

const getSystemTheme = (): 'light' | 'dark' => {
  if (typeof window === 'undefined') return 'light'
  return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
}

export const useThemeStore = create<ThemeState>()(
  persist(
    (set, get) => ({
      theme: 'system',
      effectiveTheme: getSystemTheme(),
      setTheme: (theme) => {
        set({ theme })
        get().updateEffectiveTheme()
      },
      updateEffectiveTheme: () => {
        const { theme } = get()
        const effectiveTheme = theme === 'system' ? getSystemTheme() : theme
        set({ effectiveTheme })
        
        // Update document class
        if (typeof document !== 'undefined') {
          const root = document.documentElement
          root.classList.remove('light', 'dark')
          root.classList.add(effectiveTheme)
        }
      },
    }),
    {
      name: 'theme-storage',
      onRehydrateStorage: () => (state) => {
        // Update effective theme after rehydration
        state?.updateEffectiveTheme()
      },
    }
  )
)