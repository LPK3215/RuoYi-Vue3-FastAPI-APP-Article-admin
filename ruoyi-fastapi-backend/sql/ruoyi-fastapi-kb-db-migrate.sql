-- --------------------------------------------------------
-- 教程/知识库表结构迁移（MySQL）
-- 适用场景：你已经执行过旧版 ruoyi-fastapi-kb.sql，但缺少教程分类表或 tool_kb_article.category_id
-- 说明：
-- - 兼容 MySQL 5.7+（使用 information_schema + 动态 SQL）
-- - 重复执行安全（已存在则跳过）
-- --------------------------------------------------------

-- 1) 新增：教程分类表（扁平 + 预留 parent_id）
create table if not exists tool_kb_category (
  category_id       bigint(20)      not null auto_increment    comment '分类ID',
  parent_id         bigint(20)      default 0                  comment '父级ID（0为顶级）',
  category_code     varchar(64)     default null               comment '分类编码',
  category_name     varchar(100)    not null                   comment '分类名称',
  category_sort     int(4)          default 0                  comment '显示顺序',
  status            char(1)         default '0'                comment '状态（0正常 1停用）',
  del_flag          char(1)         default '0'                comment '删除标志（0代表存在 2代表删除）',
  create_by         varchar(64)     default ''                 comment '创建者',
  create_time       datetime                                   comment '创建时间',
  update_by         varchar(64)     default ''                 comment '更新者',
  update_time       datetime                                   comment '更新时间',
  remark            varchar(500)    default null               comment '备注',
  primary key (category_id),
  index idx_kb_category_parent_id (parent_id),
  index idx_kb_category_status (status)
) engine=innodb comment = '教程分类表';

-- 2) 新增：tool_kb_article.category_id（若不存在）
set @kb_article_has_category_id := (
  select count(1)
  from information_schema.columns
  where table_schema = database()
    and table_name = 'tool_kb_article'
    and column_name = 'category_id'
);

set @kb_article_add_category_id_sql := if(
  @kb_article_has_category_id = 0,
  "alter table tool_kb_article add column category_id bigint(20) default null comment '分类ID' after article_id",
  "select 1"
);

prepare stmt from @kb_article_add_category_id_sql;
execute stmt;
deallocate prepare stmt;

-- 3) 新增索引：idx_kb_article_category_id（若不存在）
set @kb_article_has_category_idx := (
  select count(1)
  from information_schema.statistics
  where table_schema = database()
    and table_name = 'tool_kb_article'
    and index_name = 'idx_kb_article_category_id'
);

set @kb_article_add_category_idx_sql := if(
  @kb_article_has_category_idx = 0,
  "create index idx_kb_article_category_id on tool_kb_article(category_id)",
  "select 1"
);

prepare stmt2 from @kb_article_add_category_idx_sql;
execute stmt2;
deallocate prepare stmt2;

