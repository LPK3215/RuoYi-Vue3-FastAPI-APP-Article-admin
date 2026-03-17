-- --------------------------------------------------------
-- 开发环境便捷脚本：启用登录验证码
-- 说明：
-- 1) 更新 sys_config 中验证码开关为 true
-- 2) 后端会把 sys_config 缓存到 Redis；执行本脚本后请重启后端（或清理/刷新 Redis 缓存）
-- --------------------------------------------------------

UPDATE sys_config
SET config_value = 'true'
WHERE config_key = 'sys.account.captchaEnabled';

