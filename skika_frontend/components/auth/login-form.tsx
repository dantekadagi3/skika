"use client"

import type React from "react"

import { useState } from "react"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface LoginFormProps {
  onSubmit: (phoneNumber: string, password: string) => Promise<void>
  isLoading?: boolean
  error?: string
}

export default function LoginForm({ onSubmit, isLoading = false, error = "" }: LoginFormProps) {
  const [phoneNumber, setPhoneNumber] = useState("")
  const [password, setPassword] = useState("")
  const [localError, setLocalError] = useState("")

  const handleSubmit = async (e: React.FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    setLocalError("")

    // Validation
    if (!phoneNumber || !password) {
      setLocalError("Phone number and password are required")
      return
    }

    if (!/^[+]?[(]?[0-9]{3}[)]?[-\s.]?[0-9]{3}[-\s.]?[0-9]{4,6}$/.test(phoneNumber)) {
      setLocalError("Please enter a valid phone number")
      return
    }

    try {
      await onSubmit(phoneNumber, password)
    } catch (err) {
      setLocalError(err instanceof Error ? err.message : "Login failed")
    }
  }

  const displayError = error || localError

  return (
    <form onSubmit={handleSubmit} className="space-y-6">
      {displayError && (
        <div className="bg-destructive/10 text-destructive px-4 py-3 rounded-lg text-sm border border-destructive/20">
          {displayError}
        </div>
      )}

      <div>
        <label className="block text-sm font-medium text-foreground dark:text-foreground-dark mb-2">Phone Number</label>
        <Input
          type="tel"
          placeholder="+254712345678"
          value={phoneNumber}
          onChange={(e) => setPhoneNumber(e.target.value)}
          disabled={isLoading}
          className="w-full"
        />
        <p className="text-xs text-foreground-muted dark:text-foreground-dark-muted mt-1">
          Enter your registered phone number
        </p>
      </div>

      <div>
        <label className="block text-sm font-medium text-foreground dark:text-foreground-dark mb-2">Password</label>
        <Input
          type="password"
          placeholder="••••••••"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          disabled={isLoading}
          className="w-full"
        />
      </div>

      <Button
        type="submit"
        disabled={isLoading}
        className="w-full bg-primary hover:bg-primary-dark text-primary-foreground"
      >
        {isLoading ? (
          <span className="flex items-center gap-2">
            <span className="animate-spin rounded-full h-4 w-4 border-b-2 border-current"></span>
            Signing in...
          </span>
        ) : (
          "Sign In"
        )}
      </Button>

      <div className="grid grid-cols-2 gap-2">
        <div className="text-center py-2 px-2 bg-background-secondary dark:bg-background-dark-secondary rounded text-xs text-foreground-muted dark:text-foreground-dark-muted">
          Demo: +254712345678
        </div>
        <div className="text-center py-2 px-2 bg-background-secondary dark:bg-background-dark-secondary rounded text-xs text-foreground-muted dark:text-foreground-dark-muted">
          Password: demo123
        </div>
      </div>
    </form>
  )
}
