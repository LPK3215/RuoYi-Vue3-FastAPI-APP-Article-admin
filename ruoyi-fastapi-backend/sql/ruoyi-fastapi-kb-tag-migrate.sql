-- --------------------------------------------------------
-- 教程/知识库标签迁移：新增标签表 + 文章标签关联表（幂等）
-- 适用场景：你已经有教程文章数据，但还没有独立的标签管理结构
-- 说明：MySQL 5.7+ 兼容写法，重复执行安全
-- --------------------------------------------------------

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

prepare stmt from @kb_article_add_tags_sql;
execute stmt;
deallocate prepare stmt;

