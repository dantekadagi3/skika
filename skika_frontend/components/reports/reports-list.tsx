"use client"

import { useState } from "react"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import StatusUpdateModal from "./status-update-modal"

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

interface ReportsListProps {
  reports: Report[]
  isLoading: boolean
  onRefresh: () => void
}

export default function ReportsList({ reports, isLoading, onRefresh }: ReportsListProps) {
  const [selectedReport, setSelectedReport] = useState<Report | null>(null)
  const [isModalOpen, setIsModalOpen] = useState(false)

  const getStatusColor = (status: string) => {
    const colors: Record<string, string> = {
      received: "bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200",
      under_review: "bg-yellow-100 text-yellow-800 dark:bg-yellow-900 dark:text-yellow-200",
      action_taken: "bg-purple-100 text-purple-800 dark:bg-purple-900 dark:text-purple-200",
      resolved: "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200",
      closed: "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200",
    }
    return colors[status] || "bg-gray-100 text-gray-800"
  }

  const getPriorityColor = (priority: string) => {
    const colors: Record<string, string> = {
      low: "text-green-600 dark:text-green-400",
      medium: "text-yellow-600 dark:text-yellow-400",
      high: "text-red-600 dark:text-red-400",
    }
    return colors[priority] || "text-gray-600"
  }

  return (
    <>
      <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle>All Reports</CardTitle>
            <CardDescription>
              {reports.length} report{reports.length !== 1 ? "s" : ""} found
            </CardDescription>
          </div>
          <Button onClick={onRefresh} variant="outline" size="sm">
            Refresh
          </Button>
        </CardHeader>
        <CardContent>
          {isLoading ? (
            <div className="flex items-center justify-center py-12">
              <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
            </div>
          ) : reports.length === 0 ? (
            <div className="text-center py-12 text-foreground-muted dark:text-foreground-dark-muted">
              No reports found
            </div>
          ) : (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border dark:border-border-dark">
                    <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                      Ref Code
                    </th>
                    <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                      Category
                    </th>
                    <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                      Status
                    </th>
                    <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                      Priority
                    </th>
                    <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                      Description
                    </th>
                    <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                      Actions
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {reports.map((report) => (
                    <tr
                      key={report.id}
                      className="border-b border-border dark:border-border-dark hover:bg-background-secondary dark:hover:bg-background-dark-secondary transition"
                    >
                      <td className="py-3 px-4 font-medium text-foreground dark:text-foreground-dark">
                        {report.ref_code}
                      </td>
                      <td className="py-3 px-4 text-foreground dark:text-foreground-dark capitalize">
                        {report.category_en.replace(/_/g, " ")}
                      </td>
                      <td className="py-3 px-4">
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-medium ${getStatusColor(report.status_en)}`}
                        >
                          {report.status_en.replace(/_/g, " ")}
                        </span>
                      </td>
                      <td className={`py-3 px-4 font-semibold ${getPriorityColor(report.priority_level_en)}`}>
                        {report.priority_level_en.toUpperCase()}
                      </td>
                      <td className="py-3 px-4 text-foreground dark:text-foreground-dark max-w-xs truncate">
                        {report.description}
                      </td>
                      <td className="py-3 px-4">
                        <Button
                          onClick={() => {
                            setSelectedReport(report)
                            setIsModalOpen(true)
                          }}
                          size="sm"
                          variant="outline"
                        >
                          Update
                        </Button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </CardContent>
      </Card>

      {/* Status Update Modal */}
      {selectedReport && (
        <StatusUpdateModal
          isOpen={isModalOpen}
          report={selectedReport}
          onClose={() => {
            setIsModalOpen(false)
            setSelectedReport(null)
          }}
          onSuccess={() => {
            onRefresh()
            setIsModalOpen(false)
            setSelectedReport(null)
          }}
        />
      )}
    </>
  )
}
