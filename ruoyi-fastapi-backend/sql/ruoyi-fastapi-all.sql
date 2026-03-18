-- --------------------------------------------------------
-- DeskOps / RuoYi-FastAPI（MySQL）汇总初始化入口
-- 说明：
-- 1) 这不是“第三个数据库”，而是“同一个数据库的一键汇总导入入口”
-- 2) 会依次导入：基础系统 + 软件库 + 教程/知识库
-- 3) 保留原有分拆 SQL，不影响按模块单独导入
--
-- 推荐用法（在仓库根目录执行）：
-- mysql -h 127.0.0.1 -u root -p ruoyi-fastapi < ruoyi-fastapi-backend/sql/ruoyi-fastapi-all.sql
--
-- 注意：
-- - 本文件使用的是 mysql 客户端的 source 命令
-- - 请从仓库根目录执行上面的命令，避免相对路径失效
-- --------------------------------------------------------

source ./ruoyi-fastapi-backend/sql/ruoyi-fastapi.sql;
source ./ruoyi-fastapi-backend/sql/ruoyi-fastapi-software.sql;
source ./ruoyi-fastapi-backend/sql/ruoyi-fastapi-kb.sql;
