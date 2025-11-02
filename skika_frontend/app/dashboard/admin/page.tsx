"use client"

import { useState } from "react"
import useSWR from "swr"
import { apiClient } from "@/lib/api-client"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import AuditLogs from "@/components/admin/audit-logs"
import UserManagement from "@/components/admin/user-management"

interface AuditLog {
  id: string
  user: string
  action_type: string
  table_name: string
  record_id: string
  description: string
  timestamp: string
}

interface Ward {
  id: string
  name: string
  constituency: string
  county: string
  population_estimate: number
}

export default function AdminPage() {
  const [activeTab, setActiveTab] = useState<"users" | "wards" | "audit">("users")

  const { data: wards } = useSWR<any>("/wards/", (endpoint: string) => apiClient.get(endpoint))

  // Normalize response (API may return { results: [...] } or { data: [...] })
  const wardsArray: Ward[] = Array.isArray(wards)
    ? wards
    : wards && (Array.isArray(wards.results) || Array.isArray(wards.data))
    ? (wards.results ?? wards.data)
    : []
  const { data: auditLogs } = useSWR<AuditLog[]>("/audit-logs/", (endpoint: string) => apiClient.get<AuditLog[]>(endpoint))

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-foreground dark:text-foreground-dark">Administration</h1>
        <p className="text-foreground-muted dark:text-foreground-dark-muted mt-2">
          System administration and user management
        </p>
      </div>

      {/* Tab Navigation */}
      <div className="flex gap-4 border-b border-border dark:border-border-dark">
        {(["users", "wards", "audit"] as const).map((tab) => (
          <button
            key={tab}
            onClick={() => setActiveTab(tab)}
            className={`pb-4 px-2 font-medium transition ${
              activeTab === tab
                ? "border-b-2 border-primary text-foreground dark:text-foreground-dark"
                : "text-foreground-muted dark:text-foreground-dark-muted hover:text-foreground dark:hover:text-foreground-dark"
            }`}
          >
            {tab === "users" && "Officers"}
            {tab === "wards" && "Wards"}
            {tab === "audit" && "Audit Logs"}
          </button>
        ))}
      </div>

      {/* Users Tab */}
      {activeTab === "users" && <UserManagement />}

      {/* Wards Tab */}
      {activeTab === "wards" && (
        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader>
            <CardTitle>Ward Management</CardTitle>
            <CardDescription>All wards in the system</CardDescription>
          </CardHeader>
          <CardContent>
            {wardsArray ? (
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="border-b border-border dark:border-border-dark">
                      <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                        Ward Name
                      </th>
                      <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                        Constituency
                      </th>
                      <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                        County
                      </th>
                      <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                        Population
                      </th>
                    </tr>
                  </thead>
                    <tbody>
                    {wardsArray.map((ward) => (
                      <tr
                        key={ward.id}
                        className="border-b border-border dark:border-border-dark hover:bg-background-secondary dark:hover:bg-background-dark-secondary"
                      >
                        <td className="py-3 px-4 font-medium text-foreground dark:text-foreground-dark">{ward.name}</td>
                        <td className="py-3 px-4 text-foreground dark:text-foreground-dark">{ward.constituency}</td>
                        <td className="py-3 px-4 text-foreground dark:text-foreground-dark">{ward.county}</td>
                        <td className="py-3 px-4 text-foreground dark:text-foreground-dark">
                          {ward.population_estimate.toLocaleString()}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            ) : (
              <div className="text-center py-12 text-foreground-muted dark:text-foreground-dark-muted">
                Loading wards...
              </div>
            )}
          </CardContent>
        </Card>
      )}

      {/* Audit Logs Tab */}
      {activeTab === "audit" && <AuditLogs logs={auditLogs || []} />}
    </div>
  )
}
