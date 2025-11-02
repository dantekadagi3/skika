"use client"

import useSWR from "swr"
import { apiClient } from "@/lib/api-client"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import {
  AreaChart,
  Area,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts"

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

export default function AnalyticsPage() {
  const { data: stats } = useSWR<DashboardStats>("/dashboard-stats/", (endpoint) => apiClient.get(endpoint))

  // Create trend data (simulated)
  const trendData = [
    { month: "Jan", reports: 45, resolved: 12 },
    { month: "Feb", reports: 52, resolved: 18 },
    { month: "Mar", reports: 48, resolved: 22 },
    { month: "Apr", reports: 61, resolved: 28 },
    { month: "May", reports: 55, resolved: 32 },
    { month: "Jun", reports: 67, resolved: 38 },
  ]

  const reportCategoryData = stats?.reports.by_category_en
    ? Object.entries(stats.reports.by_category_en).map(([category, count]) => ({
        name: category.charAt(0).toUpperCase() + category.slice(1),
        value: count,
      }))
    : []

  const COLORS = ["#3b82f6", "#f59e0b", "#10b981", "#ef4444", "#8b5cf6", "#06b6d4"]

  // KPIs
  const totalReports = stats?.reports.total || 0
  const resolvedReports = (stats?.reports.by_status_en?.resolved || 0) + (stats?.reports.by_status_en?.closed || 0)
  const resolutionRate = totalReports > 0 ? Math.round((resolvedReports / totalReports) * 100) : 0
  const pendingReports = totalReports - resolvedReports

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground dark:text-foreground-dark">Analytics & Insights</h1>
        <p className="text-foreground-muted dark:text-foreground-dark-muted mt-2">
          Data-driven insights for transparent governance
        </p>
      </div>

      {/* KPIs */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Total Reports
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground dark:text-foreground-dark">{totalReports}</div>
            <p className="text-xs text-foreground-muted dark:text-foreground-dark-muted mt-1">All submissions</p>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Resolved
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-green-600 dark:text-green-400">{resolvedReports}</div>
            <p className="text-xs text-foreground-muted dark:text-foreground-dark-muted mt-1">Completed issues</p>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Pending
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-yellow-600 dark:text-yellow-400">{pendingReports}</div>
            <p className="text-xs text-foreground-muted dark:text-foreground-dark-muted mt-1">In progress</p>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Resolution Rate
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-blue-600 dark:text-blue-400">{resolutionRate}%</div>
            <p className="text-xs text-foreground-muted dark:text-foreground-dark-muted mt-1">Success rate</p>
          </CardContent>
        </Card>
      </div>

      {/* Trends */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader>
            <CardTitle>Reports Trend</CardTitle>
            <CardDescription>Monthly report submissions and resolutions</CardDescription>
          </CardHeader>
          <CardContent>
            <ResponsiveContainer width="100%" height={300}>
              <AreaChart data={trendData}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis dataKey="month" stroke="#64748b" />
                <YAxis stroke="#64748b" />
                <Tooltip />
                <Legend />
                <Area type="monotone" dataKey="reports" stackId="1" stroke="#3b82f6" fill="#3b82f6" />
                <Area type="monotone" dataKey="resolved" stackId="1" stroke="#10b981" fill="#10b981" />
              </AreaChart>
            </ResponsiveContainer>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader>
            <CardTitle>Reports by Category</CardTitle>
            <CardDescription>Distribution across issue types</CardDescription>
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
                No data
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Engagement */}
      <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
        <CardHeader>
          <CardTitle>Citizen Engagement</CardTitle>
          <CardDescription>Participation metrics across the platform</CardDescription>
        </CardHeader>
        <CardContent>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="text-center p-6 bg-background-secondary dark:bg-background-dark-secondary rounded-lg">
              <div className="text-4xl font-bold text-primary mb-2">{stats?.citizens || 0}</div>
              <p className="text-sm text-foreground-muted dark:text-foreground-dark-muted">Registered Citizens</p>
            </div>
            <div className="text-center p-6 bg-background-secondary dark:bg-background-dark-secondary rounded-lg">
              <div className="text-4xl font-bold text-accent-green mb-2">{stats?.projects || 0}</div>
              <p className="text-sm text-foreground-muted dark:text-foreground-dark-muted">Active Projects</p>
            </div>
            <div className="text-center p-6 bg-background-secondary dark:bg-background-dark-secondary rounded-lg">
              <div className="text-4xl font-bold text-accent-warm mb-2">{stats?.wards || 0}</div>
              <p className="text-sm text-foreground-muted dark:text-foreground-dark-muted">Wards Covered</p>
            </div>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
