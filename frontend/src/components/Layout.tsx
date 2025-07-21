import { Outlet, Link } from "react-router"
import { useAllauth } from "@knowsuchagency/allauth-react"

export default function Layout() {
  const { user, logout } = useAllauth()
  
  return (
    <div className="min-h-screen">
      <nav className="bg-gray-800 text-white p-4">
        <div className="container mx-auto flex justify-between items-center">
          <div className="flex gap-6">
            <Link to="/" className="hover:text-gray-300">
              Home
            </Link>
            <Link to="/about" className="hover:text-gray-300">
              About
            </Link>
            <Link to="/contact" className="hover:text-gray-300">
              Contact
            </Link>
            {user && (
              <Link to="/dashboard" className="hover:text-gray-300">
                Dashboard
              </Link>
            )}
          </div>
          <div className="flex gap-4 items-center">
            {user ? (
              <>
                <span>Welcome, {user.username}!</span>
                <button
                  onClick={logout}
                  className="bg-red-600 hover:bg-red-700 px-3 py-1 rounded"
                >
                  Logout
                </button>
              </>
            ) : (
              <>
                <Link to="/login" className="hover:text-gray-300">
                  Login
                </Link>
                <Link to="/signup" className="hover:text-gray-300">
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