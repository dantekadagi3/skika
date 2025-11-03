"use client"

import { useState } from "react"
import { useRouter } from "next/navigation"
import { useAuth } from "@/providers/auth-provider"
import LoginForm from "@/components/auth/login-form"

export default function LoginPage() {
  const router = useRouter()
  const { login } = useAuth()
  const [error, setError] = useState<string>("")
  const [isLoading, setIsLoading] = useState(false)

  const handleLogin = async (phoneNumber: string, password: string) => {
    setError("")
    setIsLoading(true)
    try {
      await login(phoneNumber, password)
      router.push("/dashboard")
    } catch (err: unknown) {
      const errorMessage = err instanceof Error ? err.message : "Login failed"
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-background to-background-secondary dark:from-background-dark dark:to-background-dark-secondary">
      <div className="w-full max-w-md px-4">
        <div className="bg-card dark:bg-card-bg-dark border border-border dark:border-border-dark rounded-lg shadow-lg p-8">
          <div className="text-center mb-8">
            <div className="inline-flex items-center justify-center w-12 h-12 bg-primary rounded-lg mb-4">
              <span className="text-white font-bold text-xl">S</span>
            </div>
            <h1 className="text-3xl font-bold text-foreground dark:text-foreground-dark">Skika</h1>
            <p className="text-foreground-muted dark:text-foreground-dark-muted mt-2">Officers Dashboard</p>
          </div>

          <LoginForm onSubmit={handleLogin} isLoading={isLoading} error={error} />

          <div className="mt-8 pt-6 border-t border-border dark:border-border-dark">
            <p className="text-sm text-foreground-muted dark:text-foreground-dark-muted text-center">
              Empower transparent governance
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}
