"use client"

import type React from "react"

import { useState } from "react"
import useSWR from "swr"
import { apiClient } from "@/lib/api-client"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"

interface DashboardUser {
  id: string
  phone_number: string
  first_name: string
  last_name: string
  email: string
  role: string
  is_active: boolean
  date_joined: string
}

export default function UserManagement() {
  const [showForm, setShowForm] = useState(false)
  const [formData, setFormData] = useState({
    phone_number: "",
    first_name: "",
    last_name: "",
    email: "",
    password: "",
    role: "officer",
  })

  const { data: users, mutate } = useSWR<any>("/dashboard-users/", (endpoint: string) => apiClient.get(endpoint))

  // Normalize response to array (API might return { results: [...] } or { data: [...] })
  const usersArray: DashboardUser[] = Array.isArray(users)
    ? users
    : users && (Array.isArray(users.results) || Array.isArray(users.data))
    ? (users.results ?? users.data)
    : []

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    try {
      await apiClient.post("/dashboard-users/", formData)
      setFormData({
        phone_number: "",
        first_name: "",
        last_name: "",
        email: "",
        password: "",
        role: "officer",
      })
      setShowForm(false)
      mutate()
    } catch (err) {
      console.error("Error creating user:", err)
    }
  }

  return (
    <div className="space-y-6">
      {/* Create User Form */}
      {showForm && (
        <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
          <CardHeader>
            <CardTitle>Add New Officer</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-4">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-foreground dark:text-foreground-dark mb-2">
                    First Name
                  </label>
                  <Input
                    type="text"
                    value={formData.first_name}
                    onChange={(e) => setFormData({ ...formData, first_name: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground dark:text-foreground-dark mb-2">
                    Last Name
                  </label>
                  <Input
                    type="text"
                    value={formData.last_name}
                    onChange={(e) => setFormData({ ...formData, last_name: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground dark:text-foreground-dark mb-2">
                    Phone Number
                  </label>
                  <Input
                    type="tel"
                    value={formData.phone_number}
                    onChange={(e) => setFormData({ ...formData, phone_number: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground dark:text-foreground-dark mb-2">
                    Email
                  </label>
                  <Input
                    type="email"
                    value={formData.email}
                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground dark:text-foreground-dark mb-2">
                    Password
                  </label>
                  <Input
                    type="password"
                    value={formData.password}
                    onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                    required
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-foreground dark:text-foreground-dark mb-2">
                    Role
                  </label>
                  <select
                    value={formData.role}
                    onChange={(e) => setFormData({ ...formData, role: e.target.value })}
                    className="w-full px-3 py-2 border border-border dark:border-border-dark rounded-lg bg-background dark:bg-background-dark text-foreground dark:text-foreground-dark"
                  >
                    <option value="officer">Officer</option>
                    <option value="admin">Admin</option>
                    <option value="leader">Leader</option>
                  </select>
                </div>
              </div>
              <div className="flex gap-3">
                <Button type="submit" className="bg-primary hover:bg-primary-dark text-primary-foreground">
                  Create Officer
                </Button>
                <Button onClick={() => setShowForm(false)} variant="outline">
                  Cancel
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>
      )}

      {/* Users List */}
      <Card className="bg-card dark:bg-card-bg-dark border-border dark:border-border-dark">
        <CardHeader className="flex flex-row items-center justify-between">
          <div>
            <CardTitle>Officers</CardTitle>
            <CardDescription>{usersArray.length || 0} total officers</CardDescription>
          </div>
          <Button onClick={() => setShowForm(!showForm)} className="bg-primary hover:bg-primary-dark">
            {showForm ? "Cancel" : "Add Officer"}
          </Button>
        </CardHeader>
        <CardContent>
          {usersArray ? (
            <div className="overflow-x-auto">
              <table className="w-full text-sm">
                <thead>
                  <tr className="border-b border-border dark:border-border-dark">
                    <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                      Name
                    </th>
                    <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                      Phone
                    </th>
                    <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                      Email
                    </th>
                    <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                      Role
                    </th>
                    <th className="text-left py-3 px-4 font-semibold text-foreground dark:text-foreground-dark">
                      Status
                    </th>
                  </tr>
                </thead>
                <tbody>
                  {usersArray.map((user) => (
                    <tr
                      key={user.id}
                      className="border-b border-border dark:border-border-dark hover:bg-background-secondary dark:hover:bg-background-dark-secondary"
                    >
                      <td className="py-3 px-4 font-medium text-foreground dark:text-foreground-dark">
                        {user.first_name} {user.last_name}
                      </td>
                      <td className="py-3 px-4 text-foreground dark:text-foreground-dark">{user.phone_number}</td>
                      <td className="py-3 px-4 text-foreground dark:text-foreground-dark">{user.email}</td>
                      <td className="py-3 px-4">
                        <span className="px-3 py-1 rounded-full text-xs font-medium bg-blue-100 text-blue-800 dark:bg-blue-900 dark:text-blue-200 capitalize">
                          {user.role}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span
                          className={`px-3 py-1 rounded-full text-xs font-medium ${
                            user.is_active
                              ? "bg-green-100 text-green-800 dark:bg-green-900 dark:text-green-200"
                              : "bg-gray-100 text-gray-800 dark:bg-gray-900 dark:text-gray-200"
                          }`}
                        >
                          {user.is_active ? "Active" : "Inactive"}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          ) : (
            <div className="text-center py-12 text-foreground-muted dark:text-foreground-dark-muted">
              Loading officers...
            </div>
          )}
        </CardContent>
      </Card>
    </div>
  )
}
