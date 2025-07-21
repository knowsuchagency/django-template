import { Routes, Route, Navigate } from "react-router"
import { AllauthProvider, useAllauth } from "@knowsuchagency/allauth-react"
import { ThemeProvider } from "@/contexts/ThemeContext"
import Layout from "@/components/Layout"
import { Dashboard } from "@/pages/Dashboard"
import { Login } from "@/pages/Login"
import { Signup } from "@/pages/Signup"

const ProtectedRoute: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const { isAuthenticated, isLoading } = useAllauth()
  
  if (isLoading) {
    return <div className="flex justify-center items-center h-screen">Loading...</div>
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />
  }
  
  return <>{children}</>
}

function AppRoutes() {
  const { isAuthenticated } = useAllauth()
  
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
    <ThemeProvider>
      <AllauthProvider
        baseUrl={import.meta.env.DEV ? 'http://localhost:8000' : window.location.origin}
        csrfTokenEndpoint="/api/v1/csrf-token"    >
        <AppRoutes />
      </AllauthProvider>
    </ThemeProvider>
  )
}

export default App
