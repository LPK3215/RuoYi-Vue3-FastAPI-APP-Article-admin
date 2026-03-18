import { Button } from '@/ui/Button'
import { ThemeSwitcher } from '@/theme/layout-system'
import { Link } from 'react-router-dom'

export function Topbar(props: { userName?: string; onLogout: () => void }) {
  return (
    <header className="ds-topbar">
      <Link to="/admin/dashboard" className="ds-topbarLeft ds-brandLink" aria-label="回到管理首页">
        <div className="ds-topbarTitle">管理后台</div>
        <div className="ds-topbarHint">系统概览与账号管理</div>
      </Link>
      <div className="ds-topbarRight">
        <ThemeSwitcher />
        <div className="ds-topbarUser">
          <span className="ds-topbarUserDot" aria-hidden="true" />
          <span className="ds-topbarUserName">{props.userName || '—'}</span>
        </div>
        <Button variant="ghost" size="sm" onClick={props.onLogout}>
          退出登录
        </Button>
      </div>
    </header>
  )
}
