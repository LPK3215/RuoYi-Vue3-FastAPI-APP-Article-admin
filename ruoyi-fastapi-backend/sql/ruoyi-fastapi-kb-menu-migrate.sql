-- --------------------------------------------------------
-- 教程/知识库菜单迁移：将“教程文章”从“软件管理”下移出，调整为一级菜单「教程管理」
-- 适用场景：你已经执行过旧版 ruoyi-fastapi-kb.sql（menu_id=124 挂在 软件管理(120) 下）
-- --------------------------------------------------------

-- 1) 顶级目录：menu_id=130 -> 一级菜单（教程管理）
insert ignore into sys_menu values('130',  '教程管理', '0',   '0', 'kb',       '',                   '', '', 1, 0, 'M', '0', '0', '',                  'documentation', 'admin', sysdate(), '', null, '教程管理目录（独立模块）');

-- 2) 子菜单：分类管理（menu_id=131）
insert ignore into sys_menu values('131',  '分类管理', '130', '1', 'category', 'tool/kb/category/index', '', '', 1, 0, 'C', '0', '0', 'tool:kb:category:list', 'dict', 'admin', sysdate(), '', null, '教程分类管理菜单');

-- 3) 子菜单：menu_id=124 -> 挂到「教程管理(130)」下，并统一命名/排序/路由
update sys_menu
set parent_id = 130,
    order_num = 2,
    menu_name = '教程文章',
    path = 'article',
    component = 'tool/kb/article/index',
    menu_type = 'C',
    perms = 'tool:kb:article:list',
    icon = 'documentation',
    remark = '教程/博客文章管理菜单'
where menu_id = 124;

-- 4) 按钮权限：分类管理
insert ignore into sys_menu values('1130', '分类查询', '131', '1',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:query',  '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1131', '分类新增', '131', '2',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:add',    '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1132', '分类修改', '131', '3',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:edit',   '#', 'admin', sysdate(), '', null, '');
insert ignore into sys_menu values('1133', '分类删除', '131', '4',  '', '', '', '', 1, 0, 'F', '0', '0', 'tool:kb:category:remove', '#', 'admin', sysdate(), '', null, '');

-- 5) 角色菜单关联（普通角色 common）：补齐父菜单授权
insert ignore into sys_role_menu values ('2', '130');
insert ignore into sys_role_menu values ('2', '131');
insert ignore into sys_role_menu values ('2', '1130');
insert ignore into sys_role_menu values ('2', '1131');
insert ignore into sys_role_menu values ('2', '1132');
insert ignore into sys_role_menu values ('2', '1133');
insert ignore into sys_role_menu values ('2', '124');
