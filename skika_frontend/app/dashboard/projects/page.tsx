"use client"

import { useState } from "react"
import useSWR from "swr"
import { apiClient } from "@/lib/api-client"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from "recharts"

interface Project {
  id: string
  project_code: string
  title_en: string
  description_en: string
  ward: string
  category_en: string
  status_en: string
  budget_allocated: string
  budget_used: string
  start_date: string
  end_date: string
  created_at: string
}

export default function ProjectsPage() {
  const [showForm, setShowForm] = useState(false)

  const { data: projects, isLoading, mutate } = useSWR<any>("/projects/", (endpoint: string) =>
    apiClient.get(endpoint)
  )

  // Normalize API response to always be an array. Backend might return
  // { results: [...] } or { data: [...] } or the array directly.
  const projectsArray: Project[] = Array.isArray(projects)
    ? projects
    : projects && (Array.isArray(projects.results) || Array.isArray(projects.data))
    ? (projects.results ?? projects.data)
    : []

  // Calculate progress analytics
  const progressData =
    projectsArray
      .map((p) => {
        const allocated = Number.parseFloat(p.budget_allocated)
        const used = Number.parseFloat(p.budget_used)
        const progress = allocated > 0 ? (used / allocated) * 100 : 0
        return {
          name: p.project_code,
          progress: Math.round(progress),
          budget: allocated,
        }
      })
      .slice(0, 8) || []

  const statusDistribution =
    projectsArray.reduce(
      (acc, p) => {
        const status = p.status_en
        acc[status] = (acc[status] || 0) + 1
        return acc
      },
      {} as Record<string, number>,
    ) || {}

  const statusData = Object.entries(statusDistribution).map(([status, count]) => ({
    name: status.replace(/_/g, " ").toUpperCase(),
    value: count,
  }))

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-foreground dark:text-foreground-dark">Projects Management</h1>
          <p className="text-foreground-muted dark:text-foreground-dark-muted mt-2">
            Track development initiatives across wards
          </p>
        </div>
        <Button
          onClick={() => setShowForm(!showForm)}
          className="bg-primary hover:bg-primary-dark text-primary-foreground"
        >
          {showForm ? "Cancel" : "New Project"}
        </Button>
      </div>

      {/* Projects Overview */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Total Projects
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground dark:text-foreground-dark">{projectsArray.length || 0}</div>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Active Projects
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground dark:text-foreground-dark">
              {projectsArray.filter((p) => p.status_en === "ongoing").length || 0}
            </div>
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader className="pb-2">
            <CardTitle className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted">
              Completed
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="text-3xl font-bold text-foreground dark:text-foreground-dark">
              {projectsArray.filter((p) => p.status_en === "completed").length || 0}
            </div>
          </CardContent>
        </Card>
      </div>

      {/* Analytics */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader>
            <CardTitle>Budget Utilization</CardTitle>
            <CardDescription>Percentage of allocated budget used</CardDescription>
          </CardHeader>
          <CardContent>
            {progressData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={progressData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="name" stroke="#64748b" />
                  <YAxis stroke="#64748b" />
                  <Tooltip />
                  <Bar dataKey="progress" fill="#10b981" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-80 flex items-center justify-center text-foreground-muted dark:text-foreground-dark-muted">
                No data available
              </div>
            )}
          </CardContent>
        </Card>

        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader>
            <CardTitle>Projects by Status</CardTitle>
            <CardDescription>Distribution across statuses</CardDescription>
          </CardHeader>
          <CardContent>
            {statusData.length > 0 ? (
              <ResponsiveContainer width="100%" height={300}>
                <BarChart data={statusData}>
                  <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                  <XAxis dataKey="name" stroke="#64748b" />
                  <YAxis stroke="#64748b" />
                  <Tooltip />
                  <Bar dataKey="value" fill="#7c3aed" />
                </BarChart>
              </ResponsiveContainer>
            ) : (
              <div className="h-80 flex items-center justify-center text-foreground-muted dark:text-foreground-dark-muted">
                No data available
              </div>
            )}
          </CardContent>
        </Card>
      </div>

      {/* Projects List */}
      <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
        <CardHeader>
          <CardTitle>All Projects</CardTitle>
          <CardDescription>Complete list of all development initiatives</CardDescription>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : projectsArray && projectsArray.length > 0 ? (
            <div className="space-y-4">
              {projectsArray.map((project) => {
                const allocated = Number.parseFloat(project.budget_allocated)
                const used = Number.parseFloat(project.budget_used)
                const progress = allocated > 0 ? (used / allocated) * 100 : 0

                return (
                  <div
                    key={project.id}
                    className="border border-border dark:border-border-dark rounded-lg p-4 hover:bg-background-secondary dark:hover:bg-background-dark-secondary transition"
                  >
                    <div className="flex items-start justify-between mb-3">
                      <div>
                        <h3 className="font-semibold text-foreground dark:text-foreground-dark">{project.title_en}</h3>
                        <p className="text-sm text-foreground-muted dark:text-foreground-dark-muted">
                          {project.project_code}
                        </p>
                      </div>
                      <span
                        className={`px-3 py-1 rounded-full text-xs font-medium ${
                          project.status_en === "ongoing"
                            ? "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200"
                            : project.status_en === "completed"
                              ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
                              : "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200"
                        }`}
                      >
                        {project.status_en}
                      </span>
                    </div>

                    <p className="text-sm text-foreground dark:text-foreground-dark mb-3">{project.description_en}</p>

                    {/* Progress Bar */}
                    <div className="mb-3">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-xs font-medium text-foreground-muted dark:text-foreground-dark-muted">
                          Budget: KES {used.toLocaleString()} / {allocated.toLocaleString()}
                        </span>
                        <span className="text-xs font-bold text-foreground dark:text-foreground-dark">
                          {Math.round(progress)}%
                        </span>
                      </div>
                      <div className="w-full bg-border dark:bg-border-dark rounded-full h-2">
                        <div
                          className="bg-accent-green h-2 rounded-full"
                          style={{ width: `${Math.min(progress, 100)}%` }}
                        ></div>
                      </div>
                    </div>

                    <div className="grid grid-cols-2 text-xs text-foreground-muted dark:text-foreground-dark-muted">
                      <div>Start: {new Date(project.start_date).toLocaleDateString()}</div>
                      <div>End: {new Date(project.end_date).toLocaleDateString()}</div>
                    </div>
                  </div>
                )
              })}
            </div>
          ) : (
            <div className="text-center py-12 text-foreground-muted dark:text-foreground-dark-muted">
              No projects available
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
