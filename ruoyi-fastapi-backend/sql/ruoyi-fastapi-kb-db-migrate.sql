-- --------------------------------------------------------
-- 教程/知识库表结构迁移（MySQL）
-- 适用场景：
-- 1) 你已经执行过旧版 ruoyi-fastapi-kb.sql，但缺少教程分类表或 tool_kb_article.category_id
-- 2) 你需要将教程模块升级为「分类 + 标签 + 教程文章 + 文章标签/软件关系」的独立结构
-- 说明：
-- - 兼容 MySQL 5.7+（使用 information_schema + 动态 SQL）
-- - 重复执行安全（已存在则跳过）
-- --------------------------------------------------------

-- 1) 教程分类表
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

-- 2) 教程标签表
create table if not exists tool_kb_tag (
  tag_id            bigint(20)      not null auto_increment    comment '标签ID',
  tag_code          varchar(64)     default null               comment '标签编码',
  tag_name          varchar(100)    not null                   comment '标签名称',
  tag_sort          int(4)          default 0                  comment '显示顺序',
  status            char(1)         default '0'                comment '状态（0正常 1停用）',
  del_flag          char(1)         default '0'                comment '删除标志（0代表存在 2代表删除）',
  create_by         varchar(64)     default ''                 comment '创建者',
  create_time       datetime                                   comment '创建时间',
  update_by         varchar(64)     default ''                 comment '更新者',
  update_time       datetime                                   comment '更新时间',
  remark            varchar(500)    default null               comment '备注',
  primary key (tag_id),
  unique key uk_kb_tag_name (tag_name),
  unique key uk_kb_tag_code (tag_code),
  index idx_kb_tag_status (status)
) engine=innodb comment = '教程标签表';

-- 3) 文章表补字段：category_id
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

-- 4) 文章表 category_id 索引
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

-- 5) 文章表 tags 字段注释保持兼容（如果字段不存在则补上）
set @kb_article_has_tags := (
  select count(1)
  from information_schema.columns
  where table_schema = database()
    and table_name = 'tool_kb_article'
    and column_name = 'tags'
);

set @kb_article_add_tags_sql := if(
  @kb_article_has_tags = 0,
  "alter table tool_kb_article add column tags varchar(500) default null comment '标签名称冗余缓存（逗号分隔）' after content_md",
  "select 1"
);

prepare stmt3 from @kb_article_add_tags_sql;
execute stmt3;
deallocate prepare stmt3;

-- 5.1) 文章表补字段：article_type
set @kb_article_has_article_type := (
  select count(1)
  from information_schema.columns
  where table_schema = database()
    and table_name = 'tool_kb_article'
    and column_name = 'article_type'
);

set @kb_article_add_article_type_sql := if(
  @kb_article_has_article_type = 0,
  "alter table tool_kb_article add column article_type varchar(32) default null comment '文章类型（字典 kb_article_type）' after content_md",
  "select 1"
);

prepare stmt4 from @kb_article_add_article_type_sql;
execute stmt4;
deallocate prepare stmt4;

-- 5.2) 文章表补字段：attachments
set @kb_article_has_attachments := (
  select count(1)
  from information_schema.columns
  where table_schema = database()
    and table_name = 'tool_kb_article'
    and column_name = 'attachments'
);

set @kb_article_add_attachments_sql := if(
  @kb_article_has_attachments = 0,
  "alter table tool_kb_article add column attachments varchar(4000) default null comment '附件（JSON字符串：[{name,url,size}]）' after tags",
  "select 1"
);

prepare stmt5 from @kb_article_add_attachments_sql;
execute stmt5;
deallocate prepare stmt5;

-- 6) 教程文章关联标签表
create table if not exists tool_kb_article_tag (
  id                bigint(20)      not null auto_increment    comment '主键ID',
  article_id        bigint(20)      not null                   comment '文章ID',
  tag_id            bigint(20)      not null                   comment '标签ID',
  sort              int(4)          default 0                  comment '显示顺序',
  create_time       datetime                                   comment '创建时间',
  primary key (id),
  unique key uk_kb_article_tag (article_id, tag_id),
  index idx_kb_article_tag_article_id (article_id),
  index idx_kb_article_tag_tag_id (tag_id)
) engine=innodb comment = '教程文章关联标签表';
