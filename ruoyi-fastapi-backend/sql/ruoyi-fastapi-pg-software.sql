-- --------------------------------------------------------
-- 软件库（PostgreSQL 增量 SQL）
-- 说明：
-- 1) 适用于已导入 ruoyi-fastapi-pg.sql 的库
-- 2) 新增：软件分类/软件信息/多平台下载/资源表 + 管理端菜单与权限
-- --------------------------------------------------------

create table if not exists tool_software_category (
    category_id bigserial not null,
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

create table if not exists tool_software (
    software_id bigserial not null,
    category_id bigint default null,
    software_name varchar(200) not null,
    short_desc varchar(500) default null,
    icon_url varchar(500) default null,
    official_url varchar(500) default null,
    repo_url varchar(500) default null,
    author varchar(100) default null,
    team varchar(100) default null,
    license varchar(128) default null,
    open_source char(1) default '0',
    tags varchar(500) default null,
    description_md text default null,
    usage_md text default null,
    publish_status char(1) default '0',
    software_sort int4 default 0,
    status char(1) default '0',
    del_flag char(1) default '0',
    create_by varchar(64) default '',
    create_time timestamp(0),
    update_by varchar(64) default '',
    update_time timestamp(0),
    remark varchar(500) default null,
    primary key (software_id)
);

create table if not exists tool_software_download (
    download_id bigserial not null,
    software_id bigint not null,
    platform varchar(32) not null,
    download_url varchar(500) not null,
    version varchar(64) default null,
    checksum varchar(128) default null,
    sort int4 default 0,
    remark varchar(500) default null,
    create_time timestamp(0),
    primary key (download_id)
);

create table if not exists tool_software_resource (
    resource_id bigserial not null,
    software_id bigint not null,
    resource_type varchar(32) not null,
    title varchar(200) default null,
    resource_url varchar(500) not null,
    sort int4 default 0,
    remark varchar(500) default null,
    create_time timestamp(0),
    primary key (resource_id)
);

create index if not exists idx_tool_software_category_status on tool_software_category(status);
create index if not exists idx_tool_software_category_sort on tool_software_category(category_sort);
create index if not exists idx_tool_software_category_code on tool_software_category(category_code);
create index if not exists idx_tool_software_category_id on tool_software(category_id);
create index if not exists idx_tool_software_publish_status on tool_software(publish_status);
create index if not exists idx_tool_software_update_time on tool_software(update_time);
create index if not exists idx_tool_software_download_software_id on tool_software_download(software_id);
create index if not exists idx_tool_software_resource_software_id on tool_software_resource(software_id);

insert into sys_menu (
    menu_id, menu_name, parent_id, order_num, path, component, query, route_name,
    is_frame, is_cache, menu_type, visible, status, perms, icon,
    create_by, create_time, update_by, update_time, remark
) values
    (120, '软件管理', 0, 0, 'software', '', '', 'software', 1, 0, 'M', '0', '0', '', 'download', 'admin', current_timestamp, '', null, '软件管理目录（用户业务核心）'),
    (121, '分类管理', 120, 1, 'category', 'tool/software/category/index', '', 'softwarecategory', 1, 0, 'C', '0', '0', 'tool:software:category:list', 'dict', 'admin', current_timestamp, '', null, '软件分类管理菜单'),
    (122, '软件列表', 120, 2, 'item', 'tool/software/item/index', '', 'softwareitem', 1, 0, 'C', '0', '0', 'tool:software:item:list', 'component', 'admin', current_timestamp, '', null, '软件列表菜单'),
    (123, '软件详情', 120, 3, 'detail', 'tool/software/item/detail/index', '', 'softwaredetail', 1, 0, 'C', '0', '0', 'tool:software:item:list', 'component', 'admin', current_timestamp, '', null, '软件详情页（查看/编辑）菜单'),
    (1100, '分类查询', 121, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:category:query', '#', 'admin', current_timestamp, '', null, ''),
    (1101, '分类新增', 121, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:category:add', '#', 'admin', current_timestamp, '', null, ''),
    (1102, '分类修改', 121, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:category:edit', '#', 'admin', current_timestamp, '', null, ''),
    (1103, '分类删除', 121, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:category:remove', '#', 'admin', current_timestamp, '', null, ''),
    (1110, '软件查询', 122, 1, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:item:query', '#', 'admin', current_timestamp, '', null, ''),
    (1111, '软件新增', 122, 2, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:item:add', '#', 'admin', current_timestamp, '', null, ''),
    (1112, '软件修改', 122, 3, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:item:edit', '#', 'admin', current_timestamp, '', null, ''),
    (1113, '软件删除', 122, 4, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:item:remove', '#', 'admin', current_timestamp, '', null, ''),
    (1114, '软件发布', 122, 5, '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:item:publish', '#', 'admin', current_timestamp, '', null, '')
on conflict (menu_id) do nothing;

insert into sys_role_menu (role_id, menu_id) values
    (2, 120),
    (2, 121),
    (2, 122),
    (2, 123),
    (2, 1100),
    (2, 1101),
    (2, 1102),
    (2, 1103),
    (2, 1110),
    (2, 1111),
    (2, 1112),
    (2, 1113),
    (2, 1114)
on conflict (role_id, menu_id) do nothing;
