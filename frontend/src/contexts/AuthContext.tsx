import React, { createContext, useContext, useState, useEffect } from 'react'
import { allauthFetch } from '@/lib/auth'

interface User {
  id: number
  email: string
  username: string
}

interface AuthContextType {
  user: User | null
  loading: boolean
  login: (email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  signup: (email: string, password: string) => Promise<void>
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export const useAuth = () => {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error('useAuth must be used within an AuthProvider')
  }
  return context
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const [user, setUser] = useState<User | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    // Check if user is authenticated on mount
    fetchUser()
  }, [])

  const fetchUser = async () => {
    try {
      const response = await allauthFetch('/api/v1/auth/user')
      if (response.ok) {
        const data = await response.json()
        setUser(data)
      }
    } catch (error) {
      console.error('Failed to fetch user:', error)
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    const response = await allauthFetch('/accounts/login/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    
    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.message || 'Login failed')
    }

    await fetchUser()
  }

  const logout = async () => {
    await allauthFetch('/accounts/logout/', {
      method: 'POST',
    })
    setUser(null)
  }

  const signup = async (email: string, password: string) => {
    const response = await allauthFetch('/accounts/signup/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password1: password, password2: password }),
    })
    
    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.message || 'Signup failed')
    }

    await fetchUser()
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, signup }}>
      {children}
    </AuthContext.Provider>
  )
}