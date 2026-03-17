import clsx from 'clsx'
import { NavLink, Outlet } from 'react-router-dom'

export function PortalLayout() {
  return (
    <div className="ds-portal">
      <header className="ds-portalHeader">
        <div className="ds-portalBrand">
          <div className="ds-brandMark" aria-hidden="true">
            <span />
          </div>
          <div className="ds-portalBrandText">
            <div className="ds-portalBrandTitle">
              {import.meta.env.VITE_APP_TITLE || 'SoftwareHub'}
            </div>
            <div className="ds-portalBrandSub">软件库 · 教程 · Portal</div>
          </div>
        </div>

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
          <div className="ds-portalHeaderHint">支持搜索与筛选 · 无需登录即可使用</div>
        </div>
      </header>

      <main className="ds-portalMain">
        <Outlet />
      </main>
    </div>
  )
}
