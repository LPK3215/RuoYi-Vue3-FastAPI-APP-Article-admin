import type { ReactNode } from 'react'
import { Navigate, useLocation } from 'react-router-dom'
import { getToken } from './token'

export function RequireAuth(props: { children: ReactNode }) {
  const location = useLocation()
  const token = getToken()

  if (!token) {
    return <Navigate to="/admin/login" replace state={{ from: location }} />
  }

  return props.children
}
