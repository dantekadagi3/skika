"use client"

import React, { type ReactNode } from "react"

interface ThemeProviderProps {
  children: ReactNode
  attribute?: string
  defaultTheme?: string
  enableSystem?: boolean
}

export function ThemeProvider({ children, defaultTheme = "system" }: ThemeProviderProps) {
  React.useEffect(() => {
    const theme = localStorage.getItem("theme") || defaultTheme
    const isDark = theme === "dark" || (theme === "system" && window.matchMedia("(prefers-color-scheme: dark)").matches)

    if (isDark) {
      document.documentElement.classList.add("dark")
    } else {
      document.documentElement.classList.remove("dark")
    }
  }, [defaultTheme])

  return <>{children}</>
}
