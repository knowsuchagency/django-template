import { useEffect } from "react"
import { Routes, Route, Navigate } from "react-router"
import { AllauthProvider, useAuth } from "@knowsuchagency/django-allauth"
import { useAuthStore } from "@/stores/authStore"
import { useThemeStore } from "@/stores/themeStore"
import Layout from "@/components/Layout"
import { Dashboard } from "@/pages/Dashboard"
import { Login } from "@/pages/Login"
import { Signup } from "@/pages/Signup"

const AuthSync = () => {
  const { user, isAuthenticated, isLoading } = useAuth()
  const { setUser, setIsAuthenticated, setIsLoading } = useAuthStore()
  
  useEffect(() => {
    setUser(user)
    setIsAuthenticated(isAuthenticated)
    setIsLoading(isLoading)
  }, [user, isAuthenticated, isLoading, setUser, setIsAuthenticated, setIsLoading])
  
  return null
}

const ThemeSync = () => {
  const updateEffectiveTheme = useThemeStore((state) => state.updateEffectiveTheme)
  
  useEffect(() => {
    // Listen for system theme changes
    const mediaQuery = window.matchMedia('(prefers-color-scheme: dark)')
    const handleChange = () => updateEffectiveTheme()
    
    mediaQuery.addEventListener('change', handleChange)
    return () => mediaQuery.removeEventListener('change', handleChange)
  }, [updateEffectiveTheme])
  
  return null
}

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAuthStore()
  
  if (isLoading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}

function AppRoutes() {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated)
  
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={
          <Navigate to={isAuthenticated ? "/dashboard" : "/login"} replace />
        } />
        <Route path="login" element={<Login />} />
        <Route path="signup" element={<Signup />} />
        <Route path="dashboard" element={
          <ProtectedRoute>
            <Dashboard />
          </ProtectedRoute>
        } />
      </Route>
    </Routes>
  )
}

function App() {
  return (
    <AllauthProvider
      baseUrl={import.meta.env.DEV ? 'http://localhost:8000' : window.location.origin}
      csrfTokenEndpoint="/api/v1/csrf-token"
    >
      <AuthSync />
      <ThemeSync />
      <AppRoutes />
    </AllauthProvider>
  )
}

export default App