import React, { createContext, useContext, useState, useEffect } from 'react'
import { allauthFetch } from '@/lib/auth'

interface User {
  id: number
  email: string
  username: string
  display?: string
  has_verified_email?: boolean
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
      const response = await allauthFetch('/_allauth/browser/v1/auth/session')
      if (response.ok) {
        const data = await response.json()
        if (data.status === 200 && data.data?.user) {
          setUser(data.data.user)
        } else {
          setUser(null)
        }
      }
    } catch (error) {
      console.error('Failed to fetch user:', error)
    } finally {
      setLoading(false)
    }
  }

  const login = async (email: string, password: string) => {
    const response = await allauthFetch('/_allauth/browser/v1/auth/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    
    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.errors?.[0]?.message || 'Login failed')
    }

    await fetchUser()
  }

  const logout = async () => {
    await allauthFetch('/_allauth/browser/v1/auth/logout', {
      method: 'POST',
    })
    setUser(null)
  }

  const signup = async (email: string, password: string) => {
    const response = await allauthFetch('/_allauth/browser/v1/auth/signup', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })
    
    if (!response.ok) {
      const data = await response.json()
      throw new Error(data.errors?.[0]?.message || 'Signup failed')
    }

    await fetchUser()
  }

  return (
    <AuthContext.Provider value={{ user, loading, login, logout, signup }}>
      {children}
    </AuthContext.Provider>
  )
}