"use client"

import { useState } from "react"
import { apiClient } from "@/lib/api-client"
import { Button } from "@/components/ui/button"

interface Report {
  id: string
  ref_code: string
  status_en: string
}

interface StatusUpdateModalProps {
  isOpen: boolean
  report: Report
  onClose: () => void
  onSuccess: () => void
}

const statuses = ["received", "under_review", "action_taken", "resolved", "closed"]

export default function StatusUpdateModal({ isOpen, report, onClose, onSuccess }: StatusUpdateModalProps) {
  const [selectedStatus, setSelectedStatus] = useState(report.status_en)
  const [isLoading, setIsLoading] = useState(false)
  const [error, setError] = useState("")

  const handleUpdateStatus = async () => {
    if (selectedStatus === report.status_en) {
      onClose()
      return
    }

    setError("")
    setIsLoading(true)

    try {
      await apiClient.post(`/reports/${report.id}/update_status/`, {
        status_en: selectedStatus,
      })
      onSuccess()
    } catch (err) {
      const errorMessage = err instanceof Error ? err.message : "Failed to update status"
      setError(errorMessage)
    } finally {
      setIsLoading(false)
    }
  }

  if (!isOpen) return null

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4">
      <div className="bg-card dark:bg-card-bg-dark border border-border dark:border-border-dark rounded-lg shadow-lg max-w-md w-full p-6">
        <h2 className="text-xl font-bold text-foreground dark:text-foreground-dark mb-4">Update Report Status</h2>

        <div className="space-y-4">
          <div>
            <p className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted mb-2">
              Report: {report.ref_code}
            </p>
            <p className="text-sm font-medium text-foreground-muted dark:text-foreground-dark-muted mb-4">
              Current: {report.status_en.replace(/_/g, " ")}
            </p>
          </div>

          <div>
            <label className="block text-sm font-medium text-foreground dark:text-foreground-dark mb-2">
              New Status
            </label>
            <select
              value={selectedStatus}
              onChange={(e) => setSelectedStatus(e.target.value)}
              className="w-full px-3 py-2 border border-border dark:border-border-dark rounded-lg bg-background dark:bg-background-dark text-foreground dark:text-foreground-dark"
            >
              {statuses.map((status) => (
                <option key={status} value={status}>
                  {status.replace(/_/g, " ")}
                </option>
              ))}
            </select>
          </div>

          {error && <div className="bg-destructive/10 text-destructive px-3 py-2 rounded text-sm">{error}</div>}
        </div>

        <div className="flex gap-3 mt-6">
          <Button onClick={onClose} variant="outline" className="flex-1 bg-transparent">
            Cancel
          </Button>
          <Button
            onClick={handleUpdateStatus}
            disabled={isLoading}
            className="flex-1 bg-primary hover:bg-primary-dark text-primary-foreground"
          >
            {isLoading ? "Updating..." : "Update Status"}
          </Button>
        </div>
      </div>
    </div>
  )
}
