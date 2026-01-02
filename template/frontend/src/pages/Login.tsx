import React, { useState } from 'react'
import { useNavigate, Link } from 'react-router'
import { useAuth } from '@knowsuchagency/django-allauth'
import { Button } from '@/components/ui/button'

export const Login: React.FC = () => {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const { login, isLoggingIn, loginError } = useAuth()
  const navigate = useNavigate()

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    
    try {
      await login({ email, password })
      navigate('/dashboard')
    } catch {
      // Error is handled via loginError from useAuth
    }
  }

  return (
    <div className="flex items-center justify-center min-h-screen bg-background">
      <div className="w-full max-w-md">
        <form onSubmit={handleSubmit} className="bg-card border border-border rounded-lg px-8 pt-6 pb-8 mb-4">
          <h2 className="text-2xl font-bold mb-6 text-center text-foreground">Login</h2>
          
          {loginError && (
            <div className="bg-destructive/10 border border-destructive/30 text-destructive px-4 py-3 rounded-md mb-4">
              {loginError instanceof Error ? loginError.message : 'Login failed'}
            </div>
          )}
          
          <div className="mb-4">
            <label className="block text-foreground text-sm font-medium mb-2" htmlFor="email">
              Email
            </label>
            <input
              id="email"
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="appearance-none border border-input rounded-md w-full py-2 px-3 text-foreground bg-background leading-tight focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
              required
            />
          </div>
          
          <div className="mb-6">
            <label className="block text-foreground text-sm font-medium mb-2" htmlFor="password">
              Password
            </label>
            <input
              id="password"
              type="password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="appearance-none border border-input rounded-md w-full py-2 px-3 text-foreground bg-background leading-tight focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
              required
            />
          </div>
          
          <div className="flex items-center justify-between">
            <Button type="submit" disabled={isLoggingIn} className="w-full">
              {isLoggingIn ? 'Logging in...' : 'Login'}
            </Button>
          </div>
          
          <p className="text-center mt-4 text-sm text-muted-foreground">
            Don't have an account?{' '}
            <Link to="/signup" className="text-primary hover:text-primary/80 transition-colors">
              Sign up
            </Link>
          </p>
        </form>
      </div>
    </div>
  )
}