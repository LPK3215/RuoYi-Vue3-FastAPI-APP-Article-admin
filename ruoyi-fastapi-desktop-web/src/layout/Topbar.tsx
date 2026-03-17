import { Button } from '@/ui/Button'

export function Topbar(props: { userName?: string; onLogout: () => void }) {
  return (
    <header className="ds-topbar">
      <div className="ds-topbarLeft">
        <div className="ds-topbarTitle">管理后台</div>
        <div className="ds-topbarHint">系统概览与账号管理</div>
      </div>
      <div className="ds-topbarRight">
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
