-- --------------------------------------------------------
-- 软件库（V2 迁移脚本 - MySQL）
-- 说明：
-- 1) 适用于已执行 ruoyi-fastapi.sql + ruoyi-fastapi-software.sql 的库
-- 2) 本脚本为 MySQL 5.7+ 兼容写法：通过 information_schema 判断字段是否存在后再 ALTER
-- 3) 新增：tool_software 扩展字段 + tool_software_resource 资源表（当前资源先只存 URL）
-- --------------------------------------------------------

SET @db := DATABASE();

-- tool_software: official_url
SET @exist := (
  SELECT COUNT(*)
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'tool_software' AND COLUMN_NAME = 'official_url'
);
SET @sql := IF(
  @exist = 0,
  'ALTER TABLE tool_software ADD COLUMN official_url varchar(500) DEFAULT NULL COMMENT ''官网地址'' AFTER icon_url',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- tool_software: repo_url
SET @exist := (
  SELECT COUNT(*)
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'tool_software' AND COLUMN_NAME = 'repo_url'
);
SET @sql := IF(
  @exist = 0,
  'ALTER TABLE tool_software ADD COLUMN repo_url varchar(500) DEFAULT NULL COMMENT ''开源地址/仓库地址'' AFTER official_url',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- tool_software: author
SET @exist := (
  SELECT COUNT(*)
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'tool_software' AND COLUMN_NAME = 'author'
);
SET @sql := IF(
  @exist = 0,
  'ALTER TABLE tool_software ADD COLUMN author varchar(100) DEFAULT NULL COMMENT ''作者'' AFTER repo_url',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- tool_software: team
SET @exist := (
  SELECT COUNT(*)
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'tool_software' AND COLUMN_NAME = 'team'
);
SET @sql := IF(
  @exist = 0,
  'ALTER TABLE tool_software ADD COLUMN team varchar(100) DEFAULT NULL COMMENT ''团队/组织'' AFTER author',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- tool_software: license
SET @exist := (
  SELECT COUNT(*)
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'tool_software' AND COLUMN_NAME = 'license'
);
SET @sql := IF(
  @exist = 0,
  'ALTER TABLE tool_software ADD COLUMN license varchar(128) DEFAULT NULL COMMENT ''许可证'' AFTER team',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- tool_software: open_source
SET @exist := (
  SELECT COUNT(*)
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'tool_software' AND COLUMN_NAME = 'open_source'
);
SET @sql := IF(
  @exist = 0,
  'ALTER TABLE tool_software ADD COLUMN open_source char(1) DEFAULT ''0'' COMMENT ''是否开源（0否 1是）'' AFTER license',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- tool_software: tags
SET @exist := (
  SELECT COUNT(*)
  FROM information_schema.COLUMNS
  WHERE TABLE_SCHEMA = @db AND TABLE_NAME = 'tool_software' AND COLUMN_NAME = 'tags'
);
SET @sql := IF(
  @exist = 0,
  'ALTER TABLE tool_software ADD COLUMN tags varchar(500) DEFAULT NULL COMMENT ''标签（逗号分隔）'' AFTER open_source',
  'SELECT 1'
);
PREPARE stmt FROM @sql; EXECUTE stmt; DEALLOCATE PREPARE stmt;

-- tool_software_resource: resources table
CREATE TABLE IF NOT EXISTS tool_software_resource (
  resource_id       bigint(20)      not null auto_increment    comment '资源ID',
  software_id       bigint(20)      not null                   comment '软件ID',
  resource_type     varchar(32)     not null                   comment '资源类型（screenshot/doc/link/video/other等）',
  title             varchar(200)    default null               comment '标题',
  resource_url      varchar(500)    not null                   comment '资源URL',
  sort              int(4)          default 0                  comment '显示顺序',
  remark            varchar(500)    default null               comment '备注',
  create_time       datetime                                   comment '创建时间',
  primary key (resource_id)
) engine=innodb comment = '软件资源表';

