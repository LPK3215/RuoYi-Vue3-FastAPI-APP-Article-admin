-- --------------------------------------------------------
-- 教程/知识库（增量 SQL）
-- 说明：
-- 1) 适用于已导入 ruoyi-fastapi.sql / ruoyi-fastapi-software.sql 的库
-- 2) 新增：教程分类表 + 教程标签表 + 教程文章表 + 文章关联标签/软件表 + 管理端菜单与权限
-- --------------------------------------------------------

-- ----------------------------
-- 1、教程分类表（扁平 + 预留 parent_id）
-- ----------------------------
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

-- ----------------------------
-- 2、教程标签表
-- ----------------------------
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

-- ----------------------------
-- 3、教程文章表
-- ----------------------------
create table if not exists tool_kb_article (
  article_id        bigint(20)      not null auto_increment    comment '文章ID',
  category_id       bigint(20)      default null               comment '分类ID',
  title             varchar(200)    not null                   comment '标题',
  summary           varchar(500)    default null               comment '摘要',
  cover_url         varchar(500)    default null               comment '封面URL',
  content_md        text            default null               comment '正文（Markdown）',
  tags              varchar(500)    default null               comment '标签名称冗余缓存（逗号分隔）',
  publish_status    char(1)         default '0'                comment '发布状态（0草稿 1发布 2下线）',
  publish_time      datetime                                   comment '发布时间',
  article_sort      int(4)          default 0                  comment '显示顺序',
  status            char(1)         default '0'                comment '状态（0正常 1停用）',
  del_flag          char(1)         default '0'                comment '删除标志（0代表存在 2代表删除）',
  create_by         varchar(64)     default ''                 comment '创建者',
  create_time       datetime                                   comment '创建时间',
  update_by         varchar(64)     default ''                 comment '更新者',
  update_time       datetime                                   comment '更新时间',
  remark            varchar(500)    default null               comment '备注',
  primary key (article_id),
  index idx_kb_article_category_id (category_id),
  index idx_kb_article_publish_status (publish_status),
  index idx_kb_article_update_time (update_time)
) engine=innodb comment = '教程文章表';

-- ----------------------------
-- 4、文章关联标签表
-- ----------------------------
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

-- ----------------------------
-- 5、文章关联软件表
-- ----------------------------
create table if not exists tool_kb_article_software (
  id                bigint(20)      not null auto_increment    comment '主键ID',
  article_id        bigint(20)      not null                   comment '文章ID',
  software_id       bigint(20)      not null                   comment '软件ID',
  sort              int(4)          default 0                  comment '显示顺序',
  remark            varchar(500)    default null               comment '备注',
  create_time       datetime                                   comment '创建时间',
  primary key (id),
  unique key uk_kb_article_software (article_id, software_id),
  index idx_kb_article_id (article_id)
) engine=innodb comment = '教程文章关联软件表';

-- ----------------------------
-- 6、管理端菜单（独立“教程管理”一级菜单）
-- ----------------------------
insert ignore into sys_menu values('130',  '教程管理', '0',   '0', 'kb',       '',                   '', 'kb',         1, 0, 'M', '0', '0', '',                  'documentation', 'admin', sysdate(), '', null, '教程管理目录（独立模块）');
insert ignore into sys_menu values('131',  '分类管理', '130', '1', 'category', 'tool/kb/category/index', '', 'kbcategory', 1, 0, 'C', '0', '0', 'tool:kb:category:list', 'dict', 'admin', sysdate(), '', null, '教程分类管理菜单');
insert ignore into sys_menu values('132',  '标签管理', '130', '2', 'tag',      'tool/kb/tag/index',      '', 'kbtag',      1, 0, 'C', '0', '0', 'tool:kb:tag:list',      'collection-tag', 'admin', sysdate(), '', null, '教程标签管理菜单');
insert ignore into sys_menu values('124',  '教程文章', '130', '3', 'article',  'tool/kb/article/index',  '', 'kbarticle',  1, 0, 'C', '0', '0', 'tool:kb:article:list',  'documentation', 'admin', sysdate(), '', null, '教程文章管理菜单');

-- 按钮权限：教程文章
insert ignore into sys_menu values('1120', '教程查询', '124', '1',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:article:query',   '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1121', '教程新增', '124', '2',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:article:add',     '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1122', '教程修改', '124', '3',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:article:edit',    '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1123', '教程删除', '124', '4',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:article:remove',  '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1124', '教程发布', '124', '5',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:article:publish', '#', 'admin', sysdate(), '', null, '');

-- 按钮权限：教程分类
insert ignore into sys_menu values('1130', '分类查询', '131', '1',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:query',  '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1131', '分类新增', '131', '2',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:add',    '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1132', '分类修改', '131', '3',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:edit',   '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1133', '分类删除', '131', '4',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:remove', '#', 'admin', sysdate(), '', null, '');

-- 按钮权限：教程标签
insert ignore into sys_menu values('1140', '标签查询', '132', '1',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:tag:query',   '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1141', '标签新增', '132', '2',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:tag:add',     '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1142', '标签修改', '132', '3',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:tag:edit',    '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1143', '标签删除', '132', '4',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:tag:remove',  '#', 'admin', sysdate(), '', null, '');

-- ----------------------------
-- 7、角色菜单关联（普通角色 common）
-- ----------------------------
insert ignore into sys_role_menu values ('2', '130');
insert ignore into sys_role_menu values ('2', '131');
insert ignore into sys_role_menu values ('2', '132');
insert ignore into sys_role_menu values ('2', '124');
insert ignore into sys_role_menu values ('2', '1120');
insert ignore into sys_role_menu values ('2', '1121');
insert ignore into sys_role_menu values ('2', '1122');
insert ignore into sys_role_menu values ('2', '1123');
insert ignore into sys_role_menu values ('2', '1124');
insert ignore into sys_role_menu values ('2', '1130');
insert ignore into sys_role_menu values ('2', '1131');
insert ignore into sys_role_menu values ('2', '1132');
insert ignore into sys_role_menu values ('2', '1133');
insert ignore into sys_role_menu values ('2', '1140');
insert ignore into sys_role_menu values ('2', '1141');
insert ignore into sys_role_menu values ('2', '1142');
insert ignore into sys_role_menu values ('2', '1143');

-- ----------------------------
-- 8、（可选）种子数据：用于快速验证后台与 Portal 教程链路
-- ----------------------------
insert ignore into tool_kb_category (
  category_id, parent_id, category_code, category_name, category_sort,
  status, del_flag, create_by, create_time, update_by, update_time, remark
) values (
  31001, 0, 'getting-started', '入门', 10,
  '0', '0', 'admin', sysdate(), 'admin', sysdate(), 'seed'
);

insert ignore into tool_kb_tag (
  tag_id, tag_code, tag_name, tag_sort,
  status, del_flag, create_by, create_time, update_by, update_time, remark
) values
  (32001, 'getting-started', '入门', 10, '0', '0', 'admin', sysdate(), 'admin', sysdate(), 'seed'),
  (32002, 'desktops',        'DeskOps', 20, '0', '0', 'admin', sysdate(), 'admin', sysdate(), 'seed'),
  (32003, 'software-lib',    '软件库', 30, '0', '0', 'admin', sysdate(), 'admin', sysdate(), 'seed'),
  (32004, 'portal',          'Portal', 40, '0', '0', 'admin', sysdate(), 'admin', sysdate(), 'seed');

insert ignore into tool_kb_article (
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
  '1', sysdate(), 100, '0', '0',
  'admin', sysdate(), 'admin', sysdate(), 'seed'
);

insert ignore into tool_kb_article_tag (article_id, tag_id, sort, create_time) values
  (30001, 32001, 0, sysdate()),
  (30001, 32002, 1, sysdate()),
  (30001, 32003, 2, sysdate()),
  (30001, 32004, 3, sysdate());

insert ignore into tool_kb_article_software (article_id, software_id, sort, remark, create_time)
values (30001, 20001, 0, 'seed', sysdate());
