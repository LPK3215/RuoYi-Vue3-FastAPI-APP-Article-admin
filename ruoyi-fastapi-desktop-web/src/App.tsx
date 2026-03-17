import { Navigate, Route, Routes } from 'react-router-dom'
import { RequireAuth } from './auth/RequireAuth'
import { PortalLayout } from './layout/PortalLayout'
import { ShellLayout } from './layout/ShellLayout'
import { ArticleDetailPage } from './pages/ArticleDetailPage'
import { ArticleHubPage } from './pages/ArticleHubPage'
import { DashboardPage } from './pages/DashboardPage'
import { LoginPage } from './pages/LoginPage'
import { SoftwareDetailPage } from './pages/SoftwareDetailPage'
import { SoftwareHubPage } from './pages/SoftwareHubPage'
import { UsersPage } from './pages/UsersPage'

export default function App() {
  return (
    <Routes>
      {/* Public portal (no login required) */}
      <Route path="/" element={<PortalLayout />}>
        <Route index element={<SoftwareHubPage />} />
        <Route path="articles" element={<ArticleHubPage />} />
        <Route path="article/:articleId" element={<ArticleDetailPage />} />
        <Route path="software/:softwareId" element={<SoftwareDetailPage />} />
      </Route>

      {/* Admin sandbox (kept for debugging / internal ops) */}
      <Route path="/admin/login" element={<LoginPage />} />
      <Route
        path="/admin"
        element={
          <RequireAuth>
            <ShellLayout />
          </RequireAuth>
        }
      >
        <Route index element={<Navigate to="/admin/dashboard" replace />} />
        <Route path="dashboard" element={<DashboardPage />} />
        <Route path="system/users" element={<UsersPage />} />
      </Route>

      {/* Backward compat */}
      <Route path="/login" element={<Navigate to="/admin/login" replace />} />
      <Route path="/dashboard" element={<Navigate to="/admin/dashboard" replace />} />
      <Route path="/system/users" element={<Navigate to="/admin/system/users" replace />} />

      <Route path="*" element={<Navigate to="/" replace />} />
    </Routes>
  )
}
