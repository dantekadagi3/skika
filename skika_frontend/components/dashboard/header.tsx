"use client"

import { Button } from "@/components/ui/button"
import { useAuth } from "@/providers/auth-provider"
import { useState } from "react"
import { SunIcon,MoonIcon } from "lucide-react"

export default function DashboardHeader() {
  const { user } = useAuth()
  const [isDarkMode, setIsDarkMode] = useState(false)

  const toggleTheme = () => {
    setIsDarkMode(!isDarkMode)
    if (document.documentElement.classList.contains("dark")) {
      document.documentElement.classList.remove("dark")
      localStorage.setItem("theme", "light")
    } else {
      document.documentElement.classList.add("dark")
      localStorage.setItem("theme", "dark")
    }
  }

  return (
    <header className="bg-card dark:bg-card-bg-dark border-b border-border dark:border-border-dark px-6 py-4 flex items-center justify-between">
      <div>
        <h2 className="text-xl font-semibold text-foreground dark:text-foreground-dark">
          Welcome back, {user?.first_name}
        </h2>
        <p className="text-sm text-foreground-muted dark:text-foreground-dark-muted">
          Manage citizen reports and projects
        </p>
      </div>
      <div className="flex items-center gap-4">
        <Button onClick={toggleTheme} variant="outline" size="sm">
          {isDarkMode ? <MoonIcon className="w-4 h-4" /> : <SunIcon className="w-4 h-4" />}
        </Button>
      </div>
    </header>
  )
}
