import clsx from 'clsx'
import { ThemeSwitcher } from '@/theme/layout-system'
import { Link, NavLink, Outlet } from 'react-router-dom'

export function PortalLayout() {
  return (
    <div className="ds-portal">
      <header className="ds-portalHeader">
        <Link to="/" className="ds-portalBrand ds-brandLink" aria-label="回到首页">
          <div className="ds-brandMark" aria-hidden="true">
            <span />
          </div>
          <div className="ds-portalBrandText">
            <div className="ds-portalBrandTitle">
              {import.meta.env.VITE_APP_TITLE || 'SoftwareHub'}
            </div>
            <div className="ds-portalBrandSub">软件库 · 教程 · 下载</div>
          </div>
        </Link>

        <div className="ds-portalHeaderRight">
          <nav className="ds-portalNav" aria-label="Portal navigation">
            <NavLink
              to="/"
              end
              className={({ isActive }) =>
                clsx('ds-chip', 'ds-chip--sm', 'ds-chip--neutral', isActive && 'ds-chip--selected')
              }
            >
              软件库
            </NavLink>
            <NavLink
              to="/articles"
              className={({ isActive }) =>
                clsx('ds-chip', 'ds-chip--sm', 'ds-chip--neutral', isActive && 'ds-chip--selected')
              }
            >
              教程
            </NavLink>
          </nav>
          <ThemeSwitcher />
          <div className="ds-portalHeaderHint">支持搜索与筛选 · 打开即用</div>
        </div>
      </header>

      <main className="ds-portalMain">
        <Outlet />
      </main>
    </div>
  )
}
