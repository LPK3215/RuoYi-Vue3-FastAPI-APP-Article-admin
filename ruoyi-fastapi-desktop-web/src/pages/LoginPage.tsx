import { getCaptchaImage, login } from '@/api/auth'
import { setToken } from '@/auth/token'
import { Button } from '@/ui/Button'
import { Input } from '@/ui/Input'
import { Spinner } from '@/ui/Spinner'
import { useMutation, useQuery } from '@tanstack/react-query'
import { useEffect, useMemo, useState } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

const REMEMBER_KEY = 'deskops_remember_username'

export function LoginPage() {
  const navigate = useNavigate()
  const location = useLocation()
  const redirectTo = useMemo(() => {
    const state = location.state as unknown as { from?: { pathname?: string } } | null
    return state?.from?.pathname || '/admin/dashboard'
  }, [location.state])

  const [username, setUsername] = useState(() => localStorage.getItem(REMEMBER_KEY) ?? '')
  const [password, setPassword] = useState('')
  const [remember, setRemember] = useState(true)
  const [code, setCode] = useState('')
  const [errorText, setErrorText] = useState<string | null>(null)

  useEffect(() => {
    document.title = import.meta.env.VITE_APP_TITLE || 'DeskOps'
  }, [])

  const captchaQuery = useQuery({
    queryKey: ['auth', 'captchaImage'],
    queryFn: getCaptchaImage,
    refetchOnWindowFocus: false,
    retry: 0,
  })

  const captchaEnabled =
    captchaQuery.data?.captchaEnabled === undefined
      ? true
      : Boolean(captchaQuery.data.captchaEnabled)
  const captchaUuid = captchaEnabled ? captchaQuery.data?.uuid : undefined
  const captchaImgBase64 =
    captchaEnabled && captchaQuery.data?.img
      ? `data:image/gif;base64,${captchaQuery.data.img}`
      : undefined
  const captchaFailed = captchaEnabled && captchaQuery.isError

  const loginMutation = useMutation({
    mutationFn: () =>
      login({
        username: username.trim(),
        password,
        code: captchaEnabled ? code.trim() : '',
        uuid: captchaEnabled ? captchaUuid || '' : '',
      }),
    onMutate: () => {
      setErrorText(null)
    },
    onSuccess: (res) => {
      setToken(res.token)
      if (remember) localStorage.setItem(REMEMBER_KEY, username.trim())
      else localStorage.removeItem(REMEMBER_KEY)
      navigate(redirectTo, { replace: true })
    },
    onError: (err) => {
      setErrorText((err as Error)?.message || '登录失败')
      if (captchaEnabled) {
        setCode('')
        void captchaQuery.refetch()
      }
    },
  })

  const captchaReady = !captchaEnabled || Boolean(captchaUuid)
  const canSubmit =
    username.trim().length > 0 &&
    password.length > 0 &&
    captchaReady &&
    (!captchaEnabled || code.trim().length > 0) &&
    !loginMutation.isPending

  return (
    <div className="ds-login">
      <div className="ds-loginCard">
        <div className="ds-loginHeader">
          <div className="ds-loginTitle">DeskOps</div>
          <div className="ds-loginSubtitle">管理后台登录 · 仅限授权用户</div>
        </div>

        <div className="ds-loginForm">
          <Input
            label="账号"
            name="username"
            autoComplete="username"
            autoCapitalize="none"
            autoCorrect="off"
            spellCheck={false}
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="请输入账号"
          />
          <Input
            label="密码"
            type="password"
            name="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="请输入密码"
            onKeyDown={(e) => {
              if (e.key === 'Enter' && canSubmit) loginMutation.mutate()
            }}
          />

          {captchaEnabled ? (
            <div className="ds-loginCaptcha">
              <Input
                label="验证码"
                name="captcha"
                autoComplete="off"
                autoCapitalize="none"
                autoCorrect="off"
                spellCheck={false}
                value={code}
                onChange={(e) => setCode(e.target.value)}
                placeholder="请输入验证码"
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && canSubmit) loginMutation.mutate()
                }}
              />
              <button
                type="button"
                className="ds-captchaImgBtn"
                onClick={() => void captchaQuery.refetch()}
                title="点击刷新验证码"
                aria-label="刷新验证码"
              >
                {captchaImgBase64 ? (
                  <img
                    className="ds-captchaImg"
                    src={captchaImgBase64}
                    alt="验证码"
                    width={140}
                    height={58}
                  />
                ) : (
                  <span className="ds-captchaImgPlaceholder">
                    {captchaFailed ? '服务暂不可用' : '加载中…'}
                  </span>
                )}
              </button>
            </div>
          ) : null}

          <label className="ds-check">
            <input
              type="checkbox"
              checked={remember}
              onChange={(e) => setRemember(e.target.checked)}
            />
            <span>记住账号</span>
          </label>

          {captchaFailed ? (
            <div className="ds-alert ds-alert--error" role="alert">
              验证码服务暂不可用，请稍后重试或联系管理员。
            </div>
          ) : null}

          {errorText ? (
            <div className="ds-alert ds-alert--error" role="alert">
              {errorText}
            </div>
          ) : null}

          <Button
            disabled={!canSubmit}
            onClick={() => loginMutation.mutate()}
            className="ds-loginSubmit"
          >
            {loginMutation.isPending ? <Spinner label="登录中…" /> : '登录'}
          </Button>
        </div>

        <div className="ds-loginMeta">
          <div>如需开通账号或重置密码，请联系系统管理员。</div>
        </div>
      </div>

      <div className="ds-loginAside">
        <div className="ds-loginAsideCard">
          <div className="ds-loginAsideTitle">登录后可以做什么？</div>
          <ul className="ds-loginAsideList">
            <li>1) 查看系统概览</li>
            <li>2) 管理用户账号</li>
            <li>3) 安全退出登录</li>
          </ul>
        </div>
      </div>
    </div>
  )
}
