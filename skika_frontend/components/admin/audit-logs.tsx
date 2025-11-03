"use client"

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"

interface AuditLog {
  id: string
  user: string
  action_type: string
  table_name: string
  record_id: string
  description: string
  timestamp: string
}

interface AuditLogsProps {
  logs: AuditLog[]
}

export default function AuditLogs({ logs }: AuditLogsProps) {
  return (
    <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
      <CardHeader>
        <CardTitle>Audit Trail</CardTitle>
        <CardDescription>All administrative actions logged</CardDescription>
      </CardHeader>
      <CardContent>
        {logs && logs.length > 0 ? (
          <div className="space-y-4">
            {logs.map((log) => (
              <div key={log.id} className="border border-border dark:border-border-dark rounded-lg p-4">
                <div className="flex items-start justify-between mb-2">
                  <div>
                    <p className="font-medium text-foreground dark:text-foreground-dark">
                      {log.action_type.replace(/_/g, " ")}
                    </p>
                    <p className="text-sm text-foreground-muted dark:text-foreground-dark-muted">
                      Table: {log.table_name} | Record: {log.record_id}
                    </p>
                  </div>
                  <span className="text-xs text-foreground-muted dark:text-foreground-dark-muted">
                    {new Date(log.timestamp).toLocaleString()}
                  </span>
                </div>
                <p className="text-sm text-foreground dark:text-foreground-dark bg-background-secondary dark:bg-background-dark-secondary p-2 rounded">
                  {log.description}
                </p>
              </div>
            ))}
          </div>
        ) : (
          <div className="text-center py-12 text-foreground-muted dark:text-foreground-dark-muted">
            No audit logs available
          </div>
        )}
      </CardContent>
    </Card>
  )
}
