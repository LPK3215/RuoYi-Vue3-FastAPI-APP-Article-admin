-- --------------------------------------------------------
-- 软件库（增量 SQL）
-- 说明：
-- 1) 适用于已导入 ruoyi-fastapi.sql 的库
-- 2) 仅新增：软件分类/软件信息/多平台下载表 + 管理端菜单与权限
-- --------------------------------------------------------

-- ----------------------------
-- 1、软件分类表
-- ----------------------------
create table if not exists tool_software_category (
  category_id       bigint(20)      not null auto_increment    comment '分类ID',
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
  primary key (category_id)
) engine=innodb comment = '软件分类表';

-- ----------------------------
-- 2、软件信息表
-- ----------------------------
create table if not exists tool_software (
  software_id       bigint(20)      not null auto_increment    comment '软件ID',
  category_id       bigint(20)      default null               comment '分类ID',
  software_name     varchar(200)    not null                   comment '软件名称',
  short_desc        varchar(500)    default null               comment '简短描述',
  icon_url          varchar(500)    default null               comment '图标URL',
  official_url      varchar(500)    default null               comment '官网地址',
  repo_url          varchar(500)    default null               comment '开源地址/仓库地址',
  author            varchar(100)    default null               comment '作者',
  team              varchar(100)    default null               comment '团队/组织',
  license           varchar(128)    default null               comment '许可证',
  open_source       char(1)         default '0'                comment '是否开源（0否 1是）',
  tags              varchar(500)    default null               comment '标签（逗号分隔）',
  description_md    text            default null               comment '介绍（Markdown）',
  usage_md          text            default null               comment '使用说明（Markdown）',
  publish_status    char(1)         default '0'                comment '发布状态（0草稿 1上架 2下架）',
  software_sort     int(4)          default 0                  comment '显示顺序',
  status            char(1)         default '0'                comment '状态（0正常 1停用）',
  del_flag          char(1)         default '0'                comment '删除标志（0代表存在 2代表删除）',
  create_by         varchar(64)     default ''                 comment '创建者',
  create_time       datetime                                   comment '创建时间',
  update_by         varchar(64)     default ''                 comment '更新者',
  update_time       datetime                                   comment '更新时间',
  remark            varchar(500)    default null               comment '备注',
  primary key (software_id)
) engine=innodb comment = '软件信息表';

-- ----------------------------
-- 3、软件多平台下载配置表
-- ----------------------------
create table if not exists tool_software_download (
  download_id       bigint(20)      not null auto_increment    comment '下载ID',
  software_id       bigint(20)      not null                   comment '软件ID',
  platform          varchar(32)     not null                   comment '平台标识（windows/mac/linux/android/ios/web/other等）',
  download_url      varchar(500)    not null                   comment '下载地址',
  version           varchar(64)     default null               comment '版本',
  checksum          varchar(128)    default null               comment '校验值（可选）',
  sort              int(4)          default 0                  comment '显示顺序',
  remark            varchar(500)    default null               comment '备注',
  create_time       datetime                                   comment '创建时间',
  primary key (download_id)
) engine=innodb comment = '软件多平台下载配置表';

-- ----------------------------
-- 3.1、软件资源表（截图/文档/链接等，当前先只存 URL）
-- ----------------------------
create table if not exists tool_software_resource (
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

-- ----------------------------
-- 4、管理端菜单（一级菜单：放在首页后面）
-- ----------------------------
-- 目录：软件管理（用户业务核心）
insert ignore into sys_menu values('120',  '软件管理', '0',   '0', 'software',  '',                          '', '', 1, 0, 'M', '0', '0', '',                          'download', 'admin', sysdate(), '', null, '软件管理目录（用户业务核心）');
-- 菜单：分类管理 / 软件列表 / 软件详情（详情页用于查看&编辑单个软件的完整信息）
insert ignore into sys_menu values('121',  '分类管理', '120', '1', 'category',  'tool/software/category/index', '', '', 1, 0, 'C', '0', '0', 'tool:software:category:list', 'dict',     'admin', sysdate(), '', null, '软件分类管理菜单');
insert ignore into sys_menu values('122',  '软件列表', '120', '2', 'item',      'tool/software/item/index',     '', '', 1, 0, 'C', '0', '0', 'tool:software:item:list',     'component','admin', sysdate(), '', null, '软件列表菜单');
insert ignore into sys_menu values('123',  '软件详情', '120', '3', 'detail',    'tool/software/item/detail/index', '', '', 1, 0, 'C', '0', '0', 'tool:software:item:list',     'component','admin', sysdate(), '', null, '软件详情页（查看/编辑）菜单');

-- 按钮权限：分类管理
insert ignore into sys_menu values('1100', '分类查询', '121', '1',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:category:query',  '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1101', '分类新增', '121', '2',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:category:add',    '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1102', '分类修改', '121', '3',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:category:edit',   '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1103', '分类删除', '121', '4',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:category:remove', '#', 'admin', sysdate(), '', null, '');

-- 按钮权限：软件管理
insert ignore into sys_menu values('1110', '软件查询', '122', '1',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:item:query',   '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1111', '软件新增', '122', '2',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:item:add',     '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1112', '软件修改', '122', '3',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:item:edit',    '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1113', '软件删除', '122', '4',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:item:remove',  '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1114', '软件发布', '122', '5',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:software:item:publish', '#', 'admin', sysdate(), '', null, '');

-- ----------------------------
-- 5、角色菜单关联（普通角色 common）
-- ----------------------------
insert ignore into sys_role_menu values ('2', '120');
insert ignore into sys_role_menu values ('2', '121');
insert ignore into sys_role_menu values ('2', '122');
insert ignore into sys_role_menu values ('2', '123');
insert ignore into sys_role_menu values ('2', '1100');
insert ignore into sys_role_menu values ('2', '1101');
insert ignore into sys_role_menu values ('2', '1102');
insert ignore into sys_role_menu values ('2', '1103');
insert ignore into sys_role_menu values ('2', '1110');
insert ignore into sys_role_menu values ('2', '1111');
insert ignore into sys_role_menu values ('2', '1112');
insert ignore into sys_role_menu values ('2', '1113');
insert ignore into sys_role_menu values ('2', '1114');
