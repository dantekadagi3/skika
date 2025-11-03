"use client"

import useSWR from "swr"
import { apiClient } from "@/lib/api-client"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from "recharts"

interface DashboardStats {
  reports: {
    total: number
    by_status_en: Record<string, number>
    by_category_en: Record<string, number>
  }
  citizens: number
  projects: number
  wards: number
}

export default function Dashboard() {
  const {
    data: stats,
    isLoading,
    error,
  } = useSWR<DashboardStats>("/dashboard-stats/", (endpoint) => apiClient.get(endpoint))

  const reportStatusData = stats?.reports.by_status_en
    ? Object.entries(stats.reports.by_status_en).map(([status, count]) => ({
        name: status.replace(/_/g, " ").toUpperCase(),
        value: count,
      }))
    : []

  const reportCategoryData = stats?.reports.by_category_en
    ? Object.entries(stats.reports.by_category_en).map(([category, count]) => ({
        name: category.toUpperCase(),
        value: count,
      }))
    : []

  const COLORS = ["#3b82f6", "#f59e0b", "#10b981", "#ef4444", "#8b5cf6"]

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-foreground dark:text-foreground-dark">Dashboard Overview</h1>
        <p className="text-foreground-muted dark:text-foreground-dark-muted mt-2">
          Real-time insights into citizen engagement and project status
        </p>
      </div>

      {/* Key Metrics */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Total Reports
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground dark:text-foreground-dark">
              {stats?.reports.total || 0}
            </div>
            <p className="text-xs text-foreground-muted dark:text-foreground-dark-muted mt-1">All submissions</p>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Citizens
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground dark:text-foreground-dark">{stats?.citizens || 0}</div>
            <p className="text-xs text-foreground-muted dark:text-foreground-dark-muted mt-1">Active participants</p>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Projects
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground dark:text-foreground-dark">{stats?.projects || 0}</div>
            <p className="text-xs text-foreground-muted dark:text-foreground-dark-muted mt-1">Active initiatives</p>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Wards
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground dark:text-foreground-dark">{stats?.wards || 0}</div>
            <p className="text-xs text-foreground-muted dark:text-foreground-dark-muted mt-1">Locations covered</p>
          </CardContent>
        </Card>
      </div>

      {/* Charts */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        {/* Reports by Status */}
        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader>
            <CardTitle>Reports by Status</CardTitle>
            <CardDescription>Distribution across all statuses</CardDescription>
          </CardHeader>
          <CardContent>
            {reportStatusData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={reportStatusData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="name" stroke="#64748b" />
                  <YAxis stroke="#64748b" />
                  <Tooltip />
                  <Bar dataKey="value" fill="#3b82f6" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-80 flex items-center justify-center text-foreground-muted dark:text-foreground-dark-muted">
                No data available
              </div>
            )}
          </CardContent>
        </Card>

        {/* Reports by Category */}
        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader>
            <CardTitle>Reports by Category</CardTitle>
            <CardDescription>Issue distribution</CardDescription>
          </CardHeader>
          <CardContent>
            {reportCategoryData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <PieChart>
                  <Pie
                    data={reportCategoryData}
                    cx="50%"
                    cy="50%"
                    labelLine={false}
                    label={({ name, value }) => `${name}: ${value}`}
                    outerRadius={100}
                    fill="#8884d8"
                    dataKey="value"
                  >
                    {reportCategoryData.map((entry, index) => (
                      <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-80 flex items-center justify-center text-foreground-muted dark:text-foreground-dark-muted">
                No data available
              </div>
            )}
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
