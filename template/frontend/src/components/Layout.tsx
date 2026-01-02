import { Outlet, Link } from "react-router"
import { useAuth } from "@knowsuchagency/django-allauth"
import { useAuthStore } from "@/stores/authStore"
import { ThemeToggle } from "./ThemeToggle"

export default function Layout() {
  const { logout } = useAuth()
  const user = useAuthStore((state) => state.user)
  
  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b border-border bg-card">
        <div className="container mx-auto flex justify-between items-center px-4 py-3">
          <div className="flex gap-6">
            {/* No navigation links needed when logged in */}
          </div>
          <div className="flex gap-4 items-center">
            <ThemeToggle />
            {user ? (
              <>
                <span className="text-foreground">Welcome, {user.username || user.email || 'User'}!</span>
                <button
                  onClick={logout}
                  className="bg-primary text-primary-foreground hover:bg-primary/90 px-3 py-1.5 rounded-md text-sm font-medium transition-colors"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="text-muted-foreground hover:text-foreground transition-colors">
                  Login
                </Link>
                <Link to="/signup" className="text-muted-foreground hover:text-foreground transition-colors">
                  Sign Up
                </Link>
              </>
            )}
          </div>
        </div>
      </nav>
      <main>
        <Outlet />
      </main>
    </div>
  )
}