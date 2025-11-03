"use client"

import type React from "react"
import { createContext, useContext, useState, useEffect } from "react"
import { apiClient } from "@/lib/api-client"

export interface User {
  id: string
  phone_number: string
  first_name: string
  last_name: string
  role: "admin" | "officer" | "leader"
  ward: string
}

interface AuthContextType {
  user: User | null
  isLoading: boolean
  login: (phoneNumber: string, password: string) => Promise<void>
  logout: () => void
  isAuthenticated: boolean
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<User | null>(null)
  const [isLoading, setIsLoading] = useState(true)

  useEffect(() => {
    const initAuth = async () => {
      apiClient.loadTokens()

      // If we have tokens, attempt to restore the user from localStorage.
      // We store the user on successful login so that refreshes can keep the
      // session without an extra network request. If the stored user is
      // missing, the app will still work but the user will be unauthenticated
      // until an explicit re-login or a profile fetch is implemented.
      if (apiClient.hasAccessToken()) {
        const stored = localStorage.getItem("skika_user")
        if (stored) {
          try {
            setUser(JSON.parse(stored))
          } catch (e) {
            // If parsing fails, clear the stored user
            localStorage.removeItem("skika_user")
          }
        }
      }

      setIsLoading(false)
    }
    initAuth()
  }, [])

  const login = async (phoneNumber: string, password: string) => {
    setIsLoading(true)
    try {
      const response = await apiClient.unauthenticatedPost<{
        access: string
        refresh: string
        user: User
      }>("/dashboard-login/", {
        phone_number: phoneNumber,
        password,
      })

      apiClient.setTokens(response.access, response.refresh)
      setUser(response.user)
      // Persist the user so refreshes can restore authentication state
      try {
        localStorage.setItem("skika_user", JSON.stringify(response.user))
      } catch (e) {
        /* ignore storage errors */
      }
    } finally {
      setIsLoading(false)
    }
  }

  const logout = () => {
    apiClient.clearTokens()
    setUser(null)
    localStorage.removeItem("skika_user")
  }

  return (
    <AuthContext.Provider
      value={{
        user,
        isLoading,
        login,
        logout,
        isAuthenticated: !!user,
      }}
    >
      {children}
    </AuthContext.Provider>
  )
}

export function useAuth() {
  const context = useContext(AuthContext)
  if (!context) {
    throw new Error("useAuth must be used within AuthProvider")
  }
  return context
}
