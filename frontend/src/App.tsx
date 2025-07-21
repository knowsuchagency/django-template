import { Routes, Route, Navigate } from "react-router"
import { AllauthProvider, useAllauth } from "@knowsuchagency/allauth-react"
import Layout from "@/components/Layout"
import Home from "@/pages/Home"
import About from "@/pages/About"
import Contact from "@/pages/Contact"
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
  return (
    <Routes>
      <Route element={<Layout />}>
        <Route index element={<Home />} />
        <Route path="about" element={<About />} />
        <Route path="contact" element={<Contact />} />
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
      csrfTokenEndpoint="/api/v1/csrf-token"    >
      <AppRoutes />
    </AllauthProvider>
  )
}

export default App
