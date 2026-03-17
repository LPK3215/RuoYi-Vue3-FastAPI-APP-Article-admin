-- --------------------------------------------------------
-- 教程/知识库菜单迁移：
-- 1) 将“教程文章”从旧菜单位置统一迁到一级菜单「教程管理」下
-- 2) 补齐「分类管理」「标签管理」「教程文章」三块独立菜单与权限
-- --------------------------------------------------------

-- 1) 顶级目录：menu_id=130 -> 一级菜单（教程管理）
insert ignore into sys_menu values('130',  '教程管理', '0',   '0', 'kb',       '',                  '', 'kb',         1, 0, 'M', '0', '0', '',                     'documentation', 'admin', sysdate(), '', null, '教程管理目录（独立模块）');

-- 2) 子菜单：分类管理（menu_id=131）
insert ignore into sys_menu values('131',  '分类管理', '130', '1', 'category', 'tool/kb/category/index', '', 'kbcategory', 1, 0, 'C', '0', '0', 'tool:kb:category:list', 'dict',           'admin', sysdate(), '', null, '教程分类管理菜单');

-- 3) 子菜单：标签管理（menu_id=132）
insert ignore into sys_menu values('132',  '标签管理', '130', '2', 'tag',      'tool/kb/tag/index',      '', 'kbtag',      1, 0, 'C', '0', '0', 'tool:kb:tag:list',      'collection-tag', 'admin', sysdate(), '', null, '教程标签管理菜单');

-- 4) 子菜单：menu_id=124 -> 挂到「教程管理(130)」下，并统一命名/排序/路由
update sys_menu
set parent_id = 130,
    order_num = 3,
    menu_name = '教程文章',
    path = 'article',
    component = 'tool/kb/article/index',
    route_name = 'kbarticle',
    menu_type = 'C',
    perms = 'tool:kb:article:list',
    icon = 'documentation',
    remark = '教程文章管理菜单'
where menu_id = 124;

-- 5) 按钮权限：分类管理
insert ignore into sys_menu values('1130', '分类查询', '131', '1',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:query',  '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1131', '分类新增', '131', '2',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:add',    '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1132', '分类修改', '131', '3',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:edit',   '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1133', '分类删除', '131', '4',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:remove', '#', 'admin', sysdate(), '', null, '');

-- 6) 按钮权限：标签管理
insert ignore into sys_menu values('1140', '标签查询', '132', '1',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:tag:query',   '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1141', '标签新增', '132', '2',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:tag:add',     '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1142', '标签修改', '132', '3',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:tag:edit',    '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1143', '标签删除', '132', '4',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:tag:remove',  '#', 'admin', sysdate(), '', null, '');

-- 7) 角色菜单关联（普通角色 common）：补齐父菜单授权
insert ignore into sys_role_menu values ('2', '130');
insert ignore into sys_role_menu values ('2', '131');
insert ignore into sys_role_menu values ('2', '132');
insert ignore into sys_role_menu values ('2', '124');
insert ignore into sys_role_menu values ('2', '1130');
insert ignore into sys_role_menu values ('2', '1131');
insert ignore into sys_role_menu values ('2', '1132');
insert ignore into sys_role_menu values ('2', '1133');
insert ignore into sys_role_menu values ('2', '1140');
insert ignore into sys_role_menu values ('2', '1141');
insert ignore into sys_role_menu values ('2', '1142');
insert ignore into sys_role_menu values ('2', '1143');
