"use client"

import { useState } from "react"
import useSWR from "swr"
import { apiClient } from "@/lib/api-client"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import ReportsList from "@/components/reports/reports-list"

interface Report {
  id: string
  ref_code: string
  citizen: string
  ward: string
  category_en: string
  description: string
  status_en: string
  priority_level_en: string
  created_at: string
}

export default function ReportsPage() {
  const [filters, setFilters] = useState({
    ward: "",
    category_en: "",
    status_en: "",
  })

  const queryParams = new URLSearchParams()
  if (filters.ward) queryParams.append("ward", filters.ward)
  if (filters.category_en) queryParams.append("category_en", filters.category_en)
  if (filters.status_en) queryParams.append("status_en", filters.status_en)

  const {
    data: reports,
    isLoading,
    mutate,
  } = useSWR<any>(`/reports/?${queryParams.toString()}`, (endpoint: string) => apiClient.get(endpoint))

  // Ensure we always pass an array to the list component. The API may return
  // an object shape like { results: [...] } or { data: [...] } or the array
  // directly. Normalize all cases to an array to avoid runtime errors.
  const reportsArray: Report[] = Array.isArray(reports)
    ? reports
    : reports && (Array.isArray(reports.results) || Array.isArray(reports.data))
    ? (reports.results ?? reports.data)
    : []

  const categories = ["infrastructure", "health", "education", "security", "water", "environment", "other"]
  const statuses = ["received", "under_review", "action_taken", "resolved", "closed"]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground dark:text-foreground-dark">Reports Management</h1>
        <p className="text-foreground-muted dark:text-foreground-dark-muted mt-2">
          View and manage citizen reports from all wards
        </p>
      </div>

      {/* Filters */}
      <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
        <CardHeader>
          <CardTitle>Filter Reports</CardTitle>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-foreground dark:text-foreground-dark mb-2">
                Category
              </label>
              <select
                value={filters.category_en}
                onChange={(e) => setFilters({ ...filters, category_en: e.target.value })}
                className="w-full px-3 py-2 border border-border dark:border-border-dark rounded-lg bg-background dark:bg-background-dark text-foreground dark:text-foreground-dark"
              >
                <option value="">All Categories</option>
                {categories.map((cat) => (
                  <option key={cat} value={cat}>
                    {cat.charAt(0).toUpperCase() + cat.slice(1)}
                  </option>
                ))}
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-foreground dark:text-foreground-dark mb-2">Status</label>
              <select
                value={filters.status_en}
                onChange={(e) => setFilters({ ...filters, status_en: e.target.value })}
                className="w-full px-3 py-2 border border-border dark:border-border-dark rounded-lg bg-background dark:bg-background-dark text-foreground dark:text-foreground-dark"
              >
                <option value="">All Statuses</option>
                {statuses.map((status) => (
                  <option key={status} value={status}>
                    {status.replace(/_/g, " ").toUpperCase()}
                  </option>
                ))}
              </select>
            </div>

            <div className="flex items-end">
              <Button
                onClick={() => setFilters({ ward: "", category_en: "", status_en: "" })}
                variant="outline"
                className="w-full"
              >
                Reset Filters
              </Button>
            </div>
          </div>
        </CardContent>
      </Card>

      {/* Reports Table */}
  <ReportsList reports={reportsArray} isLoading={isLoading} onRefresh={mutate} />
    </div>
  )
}
