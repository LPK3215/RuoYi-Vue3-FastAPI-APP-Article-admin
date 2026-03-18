-- --------------------------------------------------------
-- DeskOps / RuoYi-FastAPI（PostgreSQL）汇总初始化入口
-- 说明：
-- 1) 这不是“第三个数据库”，而是“同一个数据库的一键汇总导入入口”
-- 2) 会依次导入：基础系统 + 软件库 + 教程/知识库
-- 3) 保留原有分拆 SQL，不影响按模块单独导入
--
-- 推荐用法（在仓库根目录执行）：
-- psql -h 127.0.0.1 -U postgres -d ruoyi-fastapi -f ruoyi-fastapi-backend/sql/ruoyi-fastapi-pg-all.sql
--
-- 注意：
-- - 本文件使用的是 psql 客户端的 \i 命令
-- - 请从仓库根目录执行上面的命令，避免相对路径失效
-- --------------------------------------------------------

\i ./ruoyi-fastapi-backend/sql/ruoyi-fastapi-pg.sql
\i ./ruoyi-fastapi-backend/sql/ruoyi-fastapi-pg-software.sql
\i ./ruoyi-fastapi-backend/sql/ruoyi-fastapi-pg-kb.sql
