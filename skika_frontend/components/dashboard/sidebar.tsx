"use client"

import { useAuth } from "@/providers/auth-provider"
import Link from "next/link"
import { usePathname } from "next/navigation"
import { Button } from "@/components/ui/button"
import { useState } from "react"
import { HomeIcon, ToggleLeftIcon, LogOut, ToggleRightIcon, FileTextIcon, BriefcaseIcon, MessageCircleIcon, BarChart2Icon, SettingsIcon } from "lucide-react"

export default function Sidebar() {
  const { logout, user } = useAuth()
  const pathname = usePathname()
  const [isCollapsed, setIsCollapsed] = useState(false)

  const navItems: { href: string; label: string; Icon: React.ComponentType<React.SVGProps<SVGSVGElement>> }[] = [
    { href: "/dashboard", label: "Dashboard", Icon: HomeIcon },
    { href: "/dashboard/reports", label: "Reports", Icon: FileTextIcon },
    { href: "/dashboard/projects", label: "Projects", Icon: BriefcaseIcon },
    { href: "/dashboard/feedback", label: "Feedback", Icon: MessageCircleIcon },
    { href: "/dashboard/analytics", label: "Analytics", Icon: BarChart2Icon },
    { href: "/dashboard/admin", label: "Administration", Icon: SettingsIcon },
  ]

  return (
    <aside
      className={`bg-sidebar border-r border-sidebar-border transition-all duration-300 h-screen flex flex-col ${
        isCollapsed ? "w-20" : "w-64"
      }`}
    >
      <Button onClick={() => setIsCollapsed(!isCollapsed)} variant="ghost" className="w-full text-sidebar-foreground">
          {isCollapsed ? "→" : "←"}
        </Button>
      {/* Logo */}
      <div className="p-6 border-b border-sidebar-border">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-sidebar-primary rounded-lg flex items-center justify-center text-sidebar-primary-foreground font-bold">
            S
          </div>
          {!isCollapsed && (
            <div>
              <h1 className="font-bold text-sidebar-foreground">Skika</h1>
              <p className="text-xs text-sidebar-foreground/60">Officers</p>
            </div>
          )}
        </div>
      </div>

      {/* Navigation */}
      <nav className="flex-1 overflow-y-auto p-4 space-y-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href
          const Icon = item.Icon
          return (
            <Link key={item.href} href={item.href}>
              <Button
                variant={isActive ? "default" : "ghost"}
                className={`w-full justify-start gap-3 ${
                  isActive
                    ? "bg-sidebar-primary text-sidebar-primary-foreground"
                    : "text-sidebar-foreground hover:bg-sidebar-accent"
                }`}
                title={item.label}
              >
                <Icon className="w-5 h-5" />
                {!isCollapsed && <span>{item.label}</span>}
              </Button>
            </Link>
          )
        })}
      </nav>

      {/* Footer */}
      <div className="p-4 border-t border-sidebar-border space-y-4">
        {user && !isCollapsed && (
          <div className="text-sm">
            <p className="font-medium text-sidebar-foreground">
              {user.first_name} {user.last_name}
            </p>
            <p className="text-sidebar-foreground/60 text-xs capitalize">{user.role}</p>
          </div>
        )}
        <Button onClick={logout} variant="outline" className="w-full text-sidebar-foreground bg-transparent">
          {isCollapsed ? <LogOut className="w-4 h-4" /> : "Logout"}
        </Button>
        {/* <Button onClick={() => setIsCollapsed(!isCollapsed)} variant="ghost" className="w-full text-sidebar-foreground">
          {isCollapsed ? "→" : "←"}
        </Button> */}
      </div>
    </aside>
  )
}
