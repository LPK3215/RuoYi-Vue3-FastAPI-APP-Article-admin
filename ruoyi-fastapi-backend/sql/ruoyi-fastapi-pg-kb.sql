-- --------------------------------------------------------
-- 教程/知识库（PostgreSQL 增量 SQL）
-- 说明：
-- 1) 适用于已导入 ruoyi-fastapi-pg.sql / ruoyi-fastapi-pg-software.sql 的库
-- 2) 新增：教程分类/标签/文章/关联表 + 管理端菜单与权限 + 基础种子数据
-- --------------------------------------------------------

create table if not exists tool_kb_category (
    category_id bigserial not null,
    parent_id bigint default 0,
    category_code varchar(64) default null,
    category_name varchar(100) not null,
    category_sort int4 default 0,
    status char(1) default '0',
    del_flag char(1) default '0',
    create_by varchar(64) default '',
    create_time timestamp(0),
    update_by varchar(64) default '',
    update_time timestamp(0),
    remark varchar(500) default null,
    primary key (category_id)
);

create table if not exists tool_kb_tag (
    tag_id bigserial not null,
    tag_code varchar(64) default null,
    tag_name varchar(100) not null,
    tag_sort int4 default 0,
    status char(1) default '0',
    del_flag char(1) default '0',
    create_by varchar(64) default '',
    create_time timestamp(0),
    update_by varchar(64) default '',
    update_time timestamp(0),
    remark varchar(500) default null,
    primary key (tag_id)
);

create table if not exists tool_kb_article (
    article_id bigserial not null,
    category_id bigint default null,
    title varchar(200) not null,
    summary varchar(500) default null,
    cover_url varchar(500) default null,
    content_md text default null,
    article_type varchar(32) default null,
    tags varchar(500) default null,
    attachments varchar(4000) default null,
    publish_status char(1) default '0',
    publish_time timestamp(0),
    article_sort int4 default 0,
    status char(1) default '0',
    del_flag char(1) default '0',
    create_by varchar(64) default '',
    create_time timestamp(0),
    update_by varchar(64) default '',
    update_time timestamp(0),
    remark varchar(500) default null,
    primary key (article_id)
);

create table if not exists tool_kb_article_tag (
    id bigserial not null,
    article_id bigint not null,
    tag_id bigint not null,
    sort int4 default 0,
    create_time timestamp(0),
    primary key (id)
);

create table if not exists tool_kb_article_software (
    id bigserial not null,
    article_id bigint not null,
    software_id bigint not null,
    sort int4 default 0,
    remark varchar(500) default null,
    create_time timestamp(0),
    primary key (id)
);

create unique index if not exists uk_kb_tag_name on tool_kb_tag(tag_name);
create unique index if not exists uk_kb_tag_code on tool_kb_tag(tag_code);
create unique index if not exists uk_kb_article_tag on tool_kb_article_tag(article_id, tag_id);
create unique index if not exists uk_kb_article_software on tool_kb_article_software(article_id, software_id);
create index if not exists idx_kb_category_parent_id on tool_kb_category(parent_id);
create index if not exists idx_kb_category_status on tool_kb_category(status);
create index if not exists idx_kb_tag_status on tool_kb_tag(status);
create index if not exists idx_kb_article_category_id on tool_kb_article(category_id);
create index if not exists idx_kb_article_publish_status on tool_kb_article(publish_status);
create index if not exists idx_kb_article_update_time on tool_kb_article(update_time);
create index if not exists idx_kb_article_tag_article_id on tool_kb_article_tag(article_id);
create index if not exists idx_kb_article_tag_tag_id on tool_kb_article_tag(tag_id);
create index if not exists idx_kb_article_software_article_id on tool_kb_article_software(article_id);

insert into sys_menu (
    menu_id, menu_name, parent_id, order_num, path, component, query, route_name,
    is_frame, is_cache, menu_type, visible, status, perms, icon,
    create_by, create_time, update_by, update_time, remark
) values
    (130, '教程管理', 0, 0, 'kb', '', '', 'kb', 1, 0, 'M', '0', '0', '', 'documentation', 'admin', current_timestamp, '', null, '教程管理目录（独立模块）'),
    (131, '分类管理', 130, 1, 'category', 'tool/kb/category/index', '', 'kbcategory', 1, 0, 'C', '0', '0', 'tool:kb:category:list', 'dict', 'admin', current_timestamp, '', null, '教程分类管理菜单'),
    (132, '标签管理', 130, 2, 'tag', 'tool/kb/tag/index', '', 'kbtag', 1, 0, 'C', '0', '0', 'tool:kb:tag:list', 'collection-tag', 'admin', current_timestamp, '', null, '教程标签管理菜单'),
    (124, '教程文章', 130, 3, 'article', 'tool/kb/article/index', '', 'kbarticle', 1, 0, 'C', '0', '0', 'tool:kb:article:list', 'documentation', 'admin', current_timestamp, '', null, '教程文章管理菜单'),
    (1120, '教程查询', 124, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:article:query', '#', 'admin', current_timestamp, '', null, ''),
    (1121, '教程新增', 124, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:article:add', '#', 'admin', current_timestamp, '', null, ''),
    (1122, '教程修改', 124, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:article:edit', '#', 'admin', current_timestamp, '', null, ''),
    (1123, '教程删除', 124, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:article:remove', '#', 'admin', current_timestamp, '', null, ''),
    (1124, '教程发布', 124, 5, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:article:publish', '#', 'admin', current_timestamp, '', null, ''),
    (1130, '分类查询', 131, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:query', '#', 'admin', current_timestamp, '', null, ''),
    (1131, '分类新增', 131, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:add', '#', 'admin', current_timestamp, '', null, ''),
    (1132, '分类修改', 131, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:edit', '#', 'admin', current_timestamp, '', null, ''),
    (1133, '分类删除', 131, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:remove', '#', 'admin', current_timestamp, '', null, ''),
    (1140, '标签查询', 132, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:tag:query', '#', 'admin', current_timestamp, '', null, ''),
    (1141, '标签新增', 132, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:tag:add', '#', 'admin', current_timestamp, '', null, ''),
    (1142, '标签修改', 132, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:tag:edit', '#', 'admin', current_timestamp, '', null, ''),
    (1143, '标签删除', 132, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:tag:remove', '#', 'admin', current_timestamp, '', null, '')
on conflict (menu_id) do nothing;

insert into sys_role_menu (role_id, menu_id) values
    (2, 130),
    (2, 131),
    (2, 132),
    (2, 124),
    (2, 1120),
    (2, 1121),
    (2, 1122),
    (2, 1123),
    (2, 1124),
    (2, 1130),
    (2, 1131),
    (2, 1132),
    (2, 1133),
    (2, 1140),
    (2, 1141),
    (2, 1142),
    (2, 1143)
on conflict (role_id, menu_id) do nothing;

insert into tool_kb_category (
    category_id, parent_id, category_code, category_name, category_sort,
    status, del_flag, create_by, create_time, update_by, update_time, remark
) values (
    31001, 0, 'getting-started', '入门', 10,
    '0', '0', 'admin', current_timestamp, 'admin', current_timestamp, 'seed'
)
on conflict (category_id) do nothing;

insert into tool_kb_tag (
    tag_id, tag_code, tag_name, tag_sort,
    status, del_flag, create_by, create_time, update_by, update_time, remark
) values
    (32001, 'getting-started', '入门', 10, '0', '0', 'admin', current_timestamp, 'admin', current_timestamp, 'seed'),
    (32002, 'desktops', 'DeskOps', 20, '0', '0', 'admin', current_timestamp, 'admin', current_timestamp, 'seed'),
    (32003, 'software-lib', '软件库', 30, '0', '0', 'admin', current_timestamp, 'admin', current_timestamp, 'seed'),
    (32004, 'portal', 'Portal', 40, '0', '0', 'admin', current_timestamp, 'admin', current_timestamp, 'seed')
on conflict (tag_id) do nothing;

insert into tool_kb_article (
    article_id, category_id, title, summary, cover_url, content_md, tags,
    publish_status, publish_time, article_sort, status, del_flag,
    create_by, create_time, update_by, update_time, remark
) values (
    30001,
    31001,
    'DeskOps 软件库上手：如何快速找到并下载软件',
    '本教程演示如何使用 DeskOps Portal 搜索/筛选并下载软件，并在文末展示“本文用到的软件”。',
    null,
    '# DeskOps 软件库上手\n\n你可以通过以下方式快速找到需要的软件：\n\n- 关键词搜索（名称/描述/作者/标签）\n- 分类筛选\n- 许可证筛选\n- 平台筛选（仅展示有对应下载配置的软件）\n\n## 下载\n\n进入软件详情页后，在右侧「下载」区域选择平台即可。\n\n## 本文用到的软件\n\n下方会展示本文关联的软件卡片，点击可直接跳转到下载页。',
    '入门,DeskOps,软件库,Portal',
    '1', current_timestamp, 100, '0', '0',
    'admin', current_timestamp, 'admin', current_timestamp, 'seed'
)
on conflict (article_id) do nothing;

insert into tool_kb_article_tag (article_id, tag_id, sort, create_time) values
    (30001, 32001, 0, current_timestamp),
    (30001, 32002, 1, current_timestamp),
    (30001, 32003, 2, current_timestamp),
    (30001, 32004, 3, current_timestamp)
on conflict (article_id, tag_id) do nothing;

insert into tool_kb_article_software (article_id, software_id, sort, remark, create_time)
values (30001, 20001, 0, 'seed', current_timestamp)
on conflict (article_id, software_id) do nothing;

select setval(pg_get_serial_sequence('tool_kb_category', 'category_id'), coalesce((select max(category_id) from tool_kb_category), 1), true);
select setval(pg_get_serial_sequence('tool_kb_tag', 'tag_id'), coalesce((select max(tag_id) from tool_kb_tag), 1), true);
select setval(pg_get_serial_sequence('tool_kb_article', 'article_id'), coalesce((select max(article_id) from tool_kb_article), 1), true);
