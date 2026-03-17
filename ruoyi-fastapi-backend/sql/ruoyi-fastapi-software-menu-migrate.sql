-- --------------------------------------------------------
-- 软件库菜单迁移：将“软件管理”调整为一级菜单（放在首页后面）
-- 适用场景：你已经执行过旧版 ruoyi-fastapi-software.sql（挂在“系统工具”下）
-- --------------------------------------------------------

-- 1) 顶级目录：menu_id=120 -> 一级菜单
update sys_menu
set parent_id = 0,
    order_num = 0,
    menu_name = '软件管理',
    path = 'software',
    remark = '软件管理目录（用户业务核心）'
where menu_id = 120;

-- 2) 子菜单顺序：分类管理 -> 软件列表 -> 软件详情
update sys_menu set order_num = 1, menu_name = '分类管理' where menu_id = 121;
update sys_menu set order_num = 2, menu_name = '软件列表' where menu_id = 122;
update sys_menu set order_num = 3, menu_name = '软件详情' where menu_id = 123;
