import { getInfo, logout } from '@/api/auth'
import { clearToken } from '@/auth/token'
import { Spinner } from '@/ui/Spinner'
import { useQuery } from '@tanstack/react-query'
import { Outlet, useNavigate } from 'react-router-dom'
import { Sidebar } from './Sidebar'
import { Topbar } from './Topbar'

export function ShellLayout() {
  const navigate = useNavigate()
  const infoQuery = useQuery({
    queryKey: ['auth', 'getInfo'],
    queryFn: getInfo,
  })

  async function handleLogout() {
    try {
      await logout()
    } finally {
      clearToken()
      navigate('/admin/login', { replace: true })
    }
  }

  return (
    <div className="ds-shell">
      <Sidebar />

      <div className="ds-frame">
        <Topbar userName={infoQuery.data?.user?.userName} onLogout={handleLogout} />
        <main className="ds-main">
          {infoQuery.isLoading ? (
            <div className="ds-pad">
              <Spinner label="正在加载用户信息…" />
            </div>
          ) : infoQuery.isError ? (
            <div className="ds-pad">
              <div className="ds-errorCard">
                <div className="ds-errorTitle">获取用户信息失败</div>
                <div className="ds-errorText">
                  {(infoQuery.error as Error)?.message || '请检查后端是否已启动'}
                </div>
                <div className="ds-errorActions">
                  <button className="ds-link" onClick={() => infoQuery.refetch()}>
                    重试
                  </button>
                  <button className="ds-link" onClick={handleLogout}>
                    重新登录
                  </button>
                </div>
              </div>
            </div>
          ) : (
            <Outlet />
          )}
        </main>
      </div>
    </div>
  )
}
