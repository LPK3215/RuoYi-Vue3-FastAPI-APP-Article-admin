-- --------------------------------------------------------
-- 软件库（演示数据）
-- 说明：
-- 1) 依赖 ruoyi-fastapi.sql + ruoyi-fastapi-software.sql 已执行
-- 2) 本脚本仅用于本地演示：插入少量分类/软件/下载配置（可重复执行）
-- --------------------------------------------------------

-- ----------------------------
-- 1、演示分类
-- ----------------------------
insert ignore into tool_software_category
  (category_id, category_code, category_name, category_sort, status, del_flag, create_by, create_time, update_by, update_time, remark)
values
  (10001, 'dev',  '开发工具',   1, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '演示数据：开发类工具'),
  (10002, 'daily','日常软件',   2, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '演示数据：日常使用软件'),
  (10003, 'prod', '效率工具',   3, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '演示数据：效率/笔记类工具'),
  (10004, 'media','媒体影音',   4, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '演示数据：影音播放/录屏/转码等'),
  (10005, 'sys',  '系统工具',   5, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '演示数据：系统/磁盘/网络/终端工具'),
  (10006, 'comm', '协作沟通',   6, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '演示数据：聊天/会议/团队协作'),
  (10007, 'design','设计创作',  7, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '演示数据：图片/矢量/3D/绘画');

-- ----------------------------
-- 2、演示软件（默认上架 publish_status=1）
-- ----------------------------
insert ignore into tool_software
  (software_id, category_id, software_name, short_desc, icon_url, description_md, usage_md, publish_status, software_sort, status, del_flag, create_by, create_time, update_by, update_time, remark)
values
  (
    10001, 10001, 'Visual Studio Code', '轻量但强大的代码编辑器',
    'https://code.visualstudio.com/favicon.ico',
    '# VS Code\n\n- 适合：前端/后端/脚本\n- 特点：插件生态完善、调试方便\n\n> 演示数据：内容可在管理端用 Markdown 编辑。',
    '## 安装\n\n1. 选择你的平台下载\n2. 安装完成后，建议安装常用扩展（Python、ESLint 等）\n\n## 使用\n\n- 使用工作区管理项目\n- 开启自动保存与格式化（可选）',
    '1', 1, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '演示数据'
  ),
  (
    10002, 10001, 'Git', '最常用的版本控制工具',
    'https://git-scm.com/favicon.ico',
    '# Git\n\n- 适合：源码管理、多人协作\n- 提示：建议同时配置 SSH Key',
    '## 常用命令\n\n- `git clone`\n- `git status`\n- `git add/commit/push`\n\n## 推荐\n\n- 配置用户名邮箱\n- 使用图形客户端（可选）',
    '1', 2, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '演示数据'
  ),
  (
    10003, 10002, '7-Zip', '高压缩率的解压缩工具',
    'https://www.7-zip.org/favicon.ico',
    '# 7-Zip\n\n- 适合：压缩/解压\n- 支持：7z/zip/rar 等（部分格式需依赖）',
    '## 使用\n\n- 右键菜单直接压缩/解压\n- 大文件建议使用 `7z` 格式',
    '1', 3, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '演示数据'
  ),
  (
    10004, 10003, 'Obsidian', '本地优先的 Markdown 笔记工具',
    'https://obsidian.md/favicon.ico',
    '# Obsidian\n\n- 适合：知识库/笔记\n- 特点：双链、插件、同步（可选）',
    '## 建议\n\n- 建一个 `Vault` 作为你的知识库\n- 使用标签/双链组织内容\n\n## 同步\n\n- 可选：iCloud/网盘/官方 Sync',
    '1', 4, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '演示数据'
  ),
  (
    10005, 10002, 'Google Chrome', '常用浏览器（含开发者工具）',
    'https://www.google.com/chrome/static/images/favicons/favicon.ico',
    '# Chrome\n\n- 适合：日常浏览 + 开发调试\n- 特点：开发者工具强大',
    '## 使用\n\n- 登录账号同步书签（可选）\n- 开发：F12 打开 DevTools',
    '1', 5, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '演示数据'
  );

-- ----------------------------
-- 2.1、更多演示软件（用于分页/筛选/渲染验证）
-- 说明：
-- - 大部分为“已上架”，少量为草稿/下架，用于测试不同状态
-- - 下载链接尽量使用软件官网或官方 Release 页面（不追求直链）
-- ----------------------------
insert ignore into tool_software
  (software_id, category_id, software_name, short_desc, icon_url, description_md, usage_md, publish_status, software_sort, status, del_flag, create_by, create_time, update_by, update_time, remark)
values
  -- Dev / 开发工具
  (
    20001, 10001, 'Python', '通用编程语言与运行时',
    'https://www.python.org/favicon.ico',
    '# Python\n\n- 领域：脚本/自动化/后端/数据\n- 特点：生态丰富、跨平台\n- 官网：https://www.python.org/\n\n> 演示数据：内容可在管理端编辑。',
    '## 安装\n\n1. 选择平台下载安装\n2. 可选：勾选添加到 PATH\n\n## 验证\n\n- `python --version`\n- `pip --version`',
    '1', 10, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20002, 10001, 'Node.js', '前端与服务端通用的 JavaScript 运行时',
    'https://nodejs.org/static/images/favicons/favicon.png',
    '# Node.js\n\n- 领域：前端工程化/服务端\n- 特点：npm 生态、跨平台\n- 官网：https://nodejs.org/\n\n> 建议同时了解 `npm` 与 `pnpm`。',
    '## 安装\n\n1. 下载 LTS 版本\n2. 安装后重开终端\n\n## 验证\n\n- `node -v`\n- `npm -v`',
    '1', 11, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20003, 10001, 'Go', '高性能、易部署的编程语言（Golang）',
    'https://go.dev/favicon.ico',
    '# Go\n\n- 领域：后端/CLI/云原生\n- 特点：编译为单文件、跨平台\n- 官网：https://go.dev/\n\n> 适合做工具与微服务。',
    '## 安装\n\n1. 下载并安装\n2. 配置 `GOPATH`（可选）\n\n## 验证\n\n- `go version`',
    '1', 12, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20004, 10001, 'Rust', '安全且高性能的系统级编程语言',
    'https://www.rust-lang.org/static/images/favicon.ico',
    '# Rust\n\n- 领域：系统/性能敏感场景/跨平台 CLI\n- 特点：内存安全、工具链完善\n- 官网：https://www.rust-lang.org/\n\n> 常用工具：`rustup`、`cargo`。',
    '## 安装\n\n1. 使用 `rustup` 安装\n2. 选择 stable 工具链\n\n## 验证\n\n- `rustc -V`\n- `cargo -V`',
    '1', 13, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/安装页'
  ),
  (
    20005, 10001, 'Temurin (OpenJDK)', '高质量的 OpenJDK 发行版（Eclipse Adoptium）',
    'https://adoptium.net/favicon.ico',
    '# Temurin (OpenJDK)\n\n- 领域：Java/Kotlin/构建工具\n- 特点：长期支持（LTS）、多平台\n- 官网：https://adoptium.net/\n\n> 下载时注意选择 JDK 版本与架构（x64/ARM）。',
    '## 安装\n\n1. 选择 JDK 版本（建议 LTS）\n2. 安装后配置 `JAVA_HOME`\n\n## 验证\n\n- `java -version`',
    '1', 14, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20006, 10001, 'Docker Desktop', '本地容器开发与运行环境（含 GUI）',
    'https://www.docker.com/favicon.ico',
    '# Docker Desktop\n\n- 领域：容器化开发/本地环境\n- 特点：镜像/容器管理、Kubernetes（可选）\n- 官网：https://www.docker.com/\n\n> Windows 建议开启 WSL2。',
    '## 安装\n\n1. 下载安装包\n2. Windows：启用 WSL2（推荐）\n\n## 常用\n\n- `docker version`\n- `docker ps`',
    '1', 15, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/文档页'
  ),
  (
    20007, 10001, 'Postman', 'API 调试与协作工具',
    'https://www.postman.com/favicon.ico',
    '# Postman\n\n- 领域：接口调试/测试\n- 特点：集合、环境变量、Mock（可选）\n- 官网：https://www.postman.com/\n\n> 适合配合后端 Swagger 使用。',
    '## 使用\n\n1. 新建请求（GET/POST...）\n2. 保存到 Collection\n\n## 提示\n\n- 善用环境变量（dev/prod）',
    '1', 16, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20008, 10001, 'Insomnia', '轻量的 API 调试工具（草稿示例）',
    'https://insomnia.rest/favicon.ico',
    '# Insomnia\n\n- 领域：API 调试\n- 特点：界面简洁、上手快\n- 官网：https://insomnia.rest/\n\n> 演示：此条为“草稿”，用户端不展示。',
    '## 使用\n\n- 新建请求并保存\n- 组织到 Workspace',
    '0', 17, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '草稿示例'
  ),
  (
    20009, 10001, 'DBeaver', '跨平台数据库管理工具',
    'https://dbeaver.io/favicon.ico',
    '# DBeaver\n\n- 领域：数据库管理\n- 特点：多数据库支持、ER 图（部分版本）\n- 官网：https://dbeaver.io/\n\n> 适合同时管理 MySQL/PostgreSQL/SQLite。',
    '## 使用\n\n1. 新建连接\n2. 配置驱动/地址/账号\n\n## 提示\n\n- 使用 SSH 隧道（可选）',
    '1', 18, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20010, 10001, 'GitHub Desktop', 'Git 图形客户端（官方）',
    'https://desktop.github.com/favicon.ico',
    '# GitHub Desktop\n\n- 领域：版本控制\n- 特点：可视化提交/分支、PR 流程更直观\n- 官网：https://desktop.github.com/\n\n> 适合入门或日常简单操作。',
    '## 使用\n\n1. 登录 GitHub\n2. 克隆仓库并提交\n\n## 提示\n\n- 与命令行 Git 可以混用',
    '1', 19, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20011, 10001, 'Notepad++', '轻量文本编辑器（Windows）',
    'https://notepad-plus-plus.org/favicon.ico',
    '# Notepad++\n\n- 领域：文本编辑\n- 特点：启动快、插件丰富\n- 官网：https://notepad-plus-plus.org/\n\n> 适合快速查看/编辑配置文件。',
    '## 使用\n\n- 打开文本文件\n- 可选：安装常用插件（对比/格式化等）',
    '1', 20, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  );

insert ignore into tool_software
  (software_id, category_id, software_name, short_desc, icon_url, description_md, usage_md, publish_status, software_sort, status, del_flag, create_by, create_time, update_by, update_time, remark)
values
  -- Sys / 系统工具
  (
    20020, 10005, 'Everything', '极速文件名搜索工具（Windows）',
    'https://www.voidtools.com/favicon.ico',
    '# Everything\n\n- 领域：文件检索\n- 特点：几乎秒搜（基于索引）\n- 官网：https://www.voidtools.com/\n\n> 适合替代系统自带搜索。',
    '## 使用\n\n1. 安装后等待索引完成\n2. 直接输入关键字搜索\n\n## 提示\n\n- 支持正则/通配符（可选）',
    '1', 30, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20021, 10005, 'Microsoft PowerToys', '微软官方系统增强工具集（草稿示例）',
    'https://learn.microsoft.com/favicon.ico',
    '# PowerToys\n\n- 领域：系统增强\n- 特点：窗口管理、快捷工具等\n- 官网：https://learn.microsoft.com/\n\n> 演示：此条为“草稿”，用户端不展示。',
    '## 使用\n\n- 打开 PowerToys 设置\n- 按需开启模块（如 FancyZones）',
    '0', 31, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '草稿示例'
  ),
  (
    20022, 10005, 'Rufus', 'USB 启动盘制作工具（Windows）',
    'https://rufus.ie/favicon.ico',
    '# Rufus\n\n- 领域：启动盘制作\n- 特点：速度快、兼容性好\n- 官网：https://rufus.ie/\n\n> 适合制作 Windows/Linux 安装盘。',
    '## 使用\n\n1. 选择 ISO\n2. 选择 U 盘\n3. 开始写入（注意数据会被清空）',
    '1', 32, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20023, 10005, 'Ventoy', '免反复格式化的多系统启动盘工具',
    'https://www.ventoy.net/favicon.ico',
    '# Ventoy\n\n- 领域：启动盘\n- 特点：把 ISO 直接拷贝到 U 盘即可引导\n- 官网：https://www.ventoy.net/\n\n> 适合维护多个系统镜像。',
    '## 使用\n\n1. 初始化 U 盘为 Ventoy\n2. 直接拷贝 ISO 到 U 盘\n3. 重启选择引导',
    '1', 33, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20024, 10005, 'WinSCP', 'SFTP/SCP 文件传输工具（Windows）',
    'https://winscp.net/favicon.ico',
    '# WinSCP\n\n- 领域：远程文件传输\n- 特点：SFTP/SCP、可视化操作\n- 官网：https://winscp.net/\n\n> 适合与服务器交换文件。',
    '## 使用\n\n1. 新建站点（Host/User/Key）\n2. 连接后拖拽上传下载\n\n## 提示\n\n- 建议使用 SSH Key',
    '1', 34, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20025, 10005, 'PuTTY', 'SSH/Telnet 客户端（Windows）',
    'https://www.putty.org/favicon.ico',
    '# PuTTY\n\n- 领域：远程登录\n- 特点：轻量、稳定\n- 官网：https://www.putty.org/\n\n> 适合快速连接到服务器。',
    '## 使用\n\n- 填写 Host/Port\n- 选择 SSH 并连接\n\n## 提示\n\n- 可保存 Session 便于复用',
    '1', 35, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20026, 10005, 'Sysinternals Suite', '微软 Sysinternals 工具合集',
    'https://learn.microsoft.com/favicon.ico',
    '# Sysinternals Suite\n\n- 领域：系统诊断\n- 特点：进程/启动项/网络等排查工具\n- 官网：https://learn.microsoft.com/sysinternals/\n\n> 常用：Process Explorer、Autoruns。',
    '## 使用\n\n1. 解压/下载\n2. 以管理员运行需要的工具\n\n## 提示\n\n- 部分工具会被杀软提示（正常现象）',
    '1', 36, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20027, 10005, 'WizTree', '磁盘空间分析工具（下架示例）',
    'https://diskanalyzer.com/favicon.ico',
    '# WizTree\n\n- 领域：磁盘空间分析\n- 特点：快速扫描、可视化\n- 官网：https://diskanalyzer.com/\n\n> 演示：此条为“下架”，用户端不展示。',
    '## 使用\n\n- 选择磁盘\n- 扫描后按文件夹/类型查看占用',
    '2', 37, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '下架示例'
  );

insert ignore into tool_software
  (software_id, category_id, software_name, short_desc, icon_url, description_md, usage_md, publish_status, software_sort, status, del_flag, create_by, create_time, update_by, update_time, remark)
values
  -- Media / 媒体影音
  (
    20030, 10004, 'VLC media player', '开源跨平台播放器（几乎全格式）',
    'https://www.videolan.org/favicon.ico',
    '# VLC\n\n- 领域：音视频播放\n- 特点：格式支持广、跨平台\n- 官网：https://www.videolan.org/\n\n> 常用：本地播放/网络串流。',
    '## 使用\n\n- 打开文件或网络流\n- 可选：字幕/音轨切换',
    '1', 40, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20031, 10004, 'OBS Studio', '直播/录屏/推流工具',
    'https://obsproject.com/favicon.ico',
    '# OBS Studio\n\n- 领域：录屏/直播\n- 特点：场景/来源、插件生态\n- 官网：https://obsproject.com/\n\n> 适合录教程、直播推流。',
    '## 使用\n\n1. 新建场景与来源\n2. 选择分辨率与码率\n3. 开始录制或推流',
    '1', 41, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20032, 10004, 'HandBrake', '视频转码工具（开源）',
    'https://handbrake.fr/favicon.ico',
    '# HandBrake\n\n- 领域：视频转码\n- 特点：预设丰富、支持批量\n- 官网：https://handbrake.fr/\n\n> 常用：H.264/H.265 压制。',
    '## 使用\n\n1. 选择源文件\n2. 选择预设\n3. 开始编码',
    '1', 42, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20033, 10004, 'FFmpeg', '音视频处理命令行工具集合',
    'https://ffmpeg.org/favicon.ico',
    '# FFmpeg\n\n- 领域：音视频处理\n- 特点：剪辑/转码/推流\n- 官网：https://ffmpeg.org/\n\n> 演示：建议配合示例命令使用。',
    '## 常用示例\n\n- `ffmpeg -i in.mp4 out.mp4`\n- `ffmpeg -i in.mkv -c copy out.mkv`\n\n## 提示\n\n- Windows 可下载已编译版本',
    '1', 43, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  );

insert ignore into tool_software
  (software_id, category_id, software_name, short_desc, icon_url, description_md, usage_md, publish_status, software_sort, status, del_flag, create_by, create_time, update_by, update_time, remark)
values
  -- Productivity / 效率工具
  (
    20040, 10003, 'Joplin', '开源笔记工具（Markdown + 同步）',
    'https://joplinapp.org/favicon.ico',
    '# Joplin\n\n- 领域：笔记/知识库\n- 特点：Markdown、端到端加密（可选）\n- 官网：https://joplinapp.org/\n\n> 适合多端同步笔记。',
    '## 使用\n\n1. 新建笔记本/笔记\n2. 可选：配置同步（WebDAV/网盘等）\n\n## 提示\n\n- 支持插件扩展',
    '1', 50, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20041, 10003, 'Logseq', '本地优先的双链知识库（开源）',
    'https://logseq.com/favicon.ico',
    '# Logseq\n\n- 领域：知识管理\n- 特点：块级引用、双链、插件\n- 官网：https://logseq.com/\n\n> 适合做个人知识库。',
    '## 使用\n\n- 新建 Graph\n- 使用标签与双链组织内容',
    '1', 51, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/Release'
  ),
  (
    20042, 10003, 'Notion', '多合一协作笔记（下架示例）',
    'https://www.notion.com/favicon.ico',
    '# Notion\n\n- 领域：协作/文档/数据库\n- 特点：模板丰富、多人协作\n- 官网：https://www.notion.com/\n\n> 演示：此条为“下架”，用户端不展示。',
    '## 使用\n\n- 创建页面与数据库\n- 使用模板快速搭建',
    '2', 52, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '下架示例'
  ),
  (
    20043, 10003, 'Bitwarden', '跨平台密码管理器（含浏览器插件）',
    'https://bitwarden.com/favicon.ico',
    '# Bitwarden\n\n- 领域：密码管理\n- 特点：多端同步、支持自建（可选）\n- 官网：https://bitwarden.com/\n\n> 建议开启二次验证。',
    '## 使用\n\n1. 创建账号/导入密码\n2. 安装浏览器插件（可选）\n3. 启用自动填充（可选）',
    '1', 53, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  );

insert ignore into tool_software
  (software_id, category_id, software_name, short_desc, icon_url, description_md, usage_md, publish_status, software_sort, status, del_flag, create_by, create_time, update_by, update_time, remark)
values
  -- Daily / 日常软件
  (
    20050, 10002, 'Mozilla Firefox', '隐私友好的跨平台浏览器',
    'https://www.mozilla.org/favicon.ico',
    '# Firefox\n\n- 领域：浏览器\n- 特点：隐私保护、扩展生态\n- 官网：https://www.mozilla.org/firefox/\n\n> 适合开发调试与日常使用。',
    '## 使用\n\n- 安装常用扩展（可选）\n- 开发：F12 打开开发者工具',
    '1', 60, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20051, 10002, 'Brave Browser', '注重隐私与性能的浏览器',
    'https://brave.com/favicon.ico',
    '# Brave\n\n- 领域：浏览器\n- 特点：默认拦截广告/跟踪（可选）\n- 官网：https://brave.com/\n\n> 适合更清爽的浏览体验。',
    '## 使用\n\n- 导入书签（可选）\n- 按需调整隐私/盾牌设置',
    '1', 61, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  );

insert ignore into tool_software
  (software_id, category_id, software_name, short_desc, icon_url, description_md, usage_md, publish_status, software_sort, status, del_flag, create_by, create_time, update_by, update_time, remark)
values
  -- Communication / 协作沟通
  (
    20060, 10006, 'Telegram Desktop', '跨平台聊天工具（桌面端）',
    'https://telegram.org/favicon.ico',
    '# Telegram Desktop\n\n- 领域：沟通\n- 特点：多端同步、频道/群组\n- 官网：https://telegram.org/\n\n> 适合个人/小团队沟通。',
    '## 使用\n\n- 登录账号\n- 加入群组/频道\n\n## 提示\n\n- 注意隐私设置',
    '1', 70, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20061, 10006, 'Discord', '社区/语音聊天与协作工具',
    'https://discord.com/favicon.ico',
    '# Discord\n\n- 领域：沟通/社区\n- 特点：语音频道、丰富机器人生态\n- 官网：https://discord.com/\n\n> 适合语音讨论与社群协作。',
    '## 使用\n\n- 加入服务器\n- 创建频道并邀请成员',
    '1', 71, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20062, 10006, 'Slack', '团队协作聊天工具',
    'https://slack.com/favicon.ico',
    '# Slack\n\n- 领域：团队协作\n- 特点：频道、搜索、应用集成\n- 官网：https://slack.com/\n\n> 适合工作沟通与通知聚合。',
    '## 使用\n\n- 加入工作区（Workspace）\n- 使用频道/私信沟通\n\n## 提示\n\n- 可集成 GitHub/日历/CI 通知（可选）',
    '1', 72, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  );

insert ignore into tool_software
  (software_id, category_id, software_name, short_desc, icon_url, description_md, usage_md, publish_status, software_sort, status, del_flag, create_by, create_time, update_by, update_time, remark)
values
  -- Design / 设计创作
  (
    20070, 10007, 'Blender', '开源 3D 建模/渲染/动画工具',
    'https://www.blender.org/favicon.ico',
    '# Blender\n\n- 领域：3D\n- 特点：建模/动画/渲染/合成\n- 官网：https://www.blender.org/\n\n> 适合 3D 创作与学习。',
    '## 使用\n\n- 选择模板场景\n- 学习基础快捷键（G/R/S）\n\n## 提示\n\n- 推荐跟随官方/社区教程',
    '1', 80, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20071, 10007, 'GIMP', '开源图片编辑工具（类似 Photoshop）',
    'https://www.gimp.org/favicon.ico',
    '# GIMP\n\n- 领域：图片编辑\n- 特点：开源、跨平台\n- 官网：https://www.gimp.org/\n\n> 适合图片修图与简单设计。',
    '## 使用\n\n- 打开图片\n- 使用图层/选择/滤镜完成编辑',
    '1', 81, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20072, 10007, 'Inkscape', '开源矢量图编辑工具（SVG）',
    'https://inkscape.org/favicon.ico',
    '# Inkscape\n\n- 领域：矢量图\n- 特点：SVG、跨平台\n- 官网：https://inkscape.org/\n\n> 适合做 Logo/图标/插画。',
    '## 使用\n\n- 新建画布\n- 使用钢笔/形状工具绘制\n\n## 导出\n\n- 导出 PNG/SVG/PDF',
    '1', 82, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  ),
  (
    20073, 10007, 'Krita', '开源数字绘画工具',
    'https://krita.org/favicon.ico',
    '# Krita\n\n- 领域：绘画/插画\n- 特点：笔刷丰富、跨平台\n- 官网：https://krita.org/\n\n> 适合数位板绘画与插画创作。',
    '## 使用\n\n- 新建画布\n- 选择笔刷开始绘制\n\n## 提示\n\n- 善用图层与快捷键',
    '1', 83, '0', '0', 'seed', sysdate(), 'seed', sysdate(), '官网/下载页'
  );

-- ----------------------------
-- 3、演示多平台下载配置
-- ----------------------------
insert ignore into tool_software_download
  (download_id, software_id, platform, download_url, version, checksum, sort, remark, create_time)
values
  -- VS Code
  (10001, 10001, 'windows', 'https://code.visualstudio.com/Download', 'latest', null, 1, '官方下载页', sysdate()),
  (10002, 10001, 'mac',     'https://code.visualstudio.com/Download', 'latest', null, 2, '官方下载页', sysdate()),
  (10003, 10001, 'linux',   'https://code.visualstudio.com/Download', 'latest', null, 3, '官方下载页', sysdate()),
  -- Git
  (10011, 10002, 'windows', 'https://git-scm.com/download/win', 'latest', null, 1, '官方', sysdate()),
  (10012, 10002, 'mac',     'https://git-scm.com/download/mac', 'latest', null, 2, '官方', sysdate()),
  (10013, 10002, 'linux',   'https://git-scm.com/download/linux', 'latest', null, 3, '官方', sysdate()),
  -- 7-Zip
  (10021, 10003, 'windows', 'https://www.7-zip.org/download.html', 'latest', null, 1, '官方', sysdate()),
  -- Obsidian
  (10031, 10004, 'windows', 'https://obsidian.md/download', 'latest', null, 1, '官方下载页', sysdate()),
  (10032, 10004, 'mac',     'https://obsidian.md/download', 'latest', null, 2, '官方下载页', sysdate()),
  (10033, 10004, 'linux',   'https://obsidian.md/download', 'latest', null, 3, '官方下载页', sysdate()),
  -- Chrome
  (10041, 10005, 'windows', 'https://www.google.com/chrome/', 'latest', null, 1, '官方下载页', sysdate()),
  (10042, 10005, 'mac',     'https://www.google.com/chrome/', 'latest', null, 2, '官方下载页', sysdate()),
  (10043, 10005, 'linux',   'https://www.google.com/chrome/', 'latest', null, 3, '官方下载页', sysdate());

-- ----------------------------
-- 3.1、更多演示下载配置
-- 说明：download_id 使用“software_id * 10 + 序号”的方式，便于重复执行且不冲突
-- ----------------------------
insert ignore into tool_software_download
  (download_id, software_id, platform, download_url, version, checksum, sort, remark, create_time)
values
  -- Python
  (200011, 20001, 'windows', 'https://www.python.org/downloads/', 'latest', null, 1, '官网', sysdate()),
  (200012, 20001, 'mac',     'https://www.python.org/downloads/', 'latest', null, 2, '官网', sysdate()),
  (200013, 20001, 'linux',   'https://www.python.org/downloads/', 'latest', null, 3, '官网', sysdate()),
  -- Node.js
  (200021, 20002, 'windows', 'https://nodejs.org/en/download/', 'latest', null, 1, '官网', sysdate()),
  (200022, 20002, 'mac',     'https://nodejs.org/en/download/', 'latest', null, 2, '官网', sysdate()),
  (200023, 20002, 'linux',   'https://nodejs.org/en/download/', 'latest', null, 3, '官网', sysdate()),
  -- Go
  (200031, 20003, 'windows', 'https://go.dev/dl/', 'latest', null, 1, '官网', sysdate()),
  (200032, 20003, 'mac',     'https://go.dev/dl/', 'latest', null, 2, '官网', sysdate()),
  (200033, 20003, 'linux',   'https://go.dev/dl/', 'latest', null, 3, '官网', sysdate()),
  -- Rust
  (200041, 20004, 'windows', 'https://www.rust-lang.org/tools/install', 'latest', null, 1, 'rustup', sysdate()),
  (200042, 20004, 'mac',     'https://www.rust-lang.org/tools/install', 'latest', null, 2, 'rustup', sysdate()),
  (200043, 20004, 'linux',   'https://www.rust-lang.org/tools/install', 'latest', null, 3, 'rustup', sysdate()),
  -- Temurin (OpenJDK)
  (200051, 20005, 'windows', 'https://adoptium.net/temurin/releases/', 'latest', null, 1, '官网', sysdate()),
  (200052, 20005, 'mac',     'https://adoptium.net/temurin/releases/', 'latest', null, 2, '官网', sysdate()),
  (200053, 20005, 'linux',   'https://adoptium.net/temurin/releases/', 'latest', null, 3, '官网', sysdate()),
  -- Docker Desktop
  (200061, 20006, 'windows', 'https://docs.docker.com/get-docker/', 'latest', null, 1, '官方文档', sysdate()),
  (200062, 20006, 'mac',     'https://docs.docker.com/get-docker/', 'latest', null, 2, '官方文档', sysdate()),
  -- Postman
  (200071, 20007, 'windows', 'https://www.postman.com/downloads/', 'latest', null, 1, '官网', sysdate()),
  (200072, 20007, 'mac',     'https://www.postman.com/downloads/', 'latest', null, 2, '官网', sysdate()),
  (200073, 20007, 'linux',   'https://www.postman.com/downloads/', 'latest', null, 3, '官网', sysdate()),
  -- Insomnia（草稿）
  (200081, 20008, 'windows', 'https://insomnia.rest/download', 'latest', null, 1, '官网', sysdate()),
  (200082, 20008, 'mac',     'https://insomnia.rest/download', 'latest', null, 2, '官网', sysdate()),
  (200083, 20008, 'linux',   'https://insomnia.rest/download', 'latest', null, 3, '官网', sysdate()),
  -- DBeaver
  (200091, 20009, 'windows', 'https://dbeaver.io/download/', 'latest', null, 1, '官网', sysdate()),
  (200092, 20009, 'mac',     'https://dbeaver.io/download/', 'latest', null, 2, '官网', sysdate()),
  (200093, 20009, 'linux',   'https://dbeaver.io/download/', 'latest', null, 3, '官网', sysdate()),
  -- GitHub Desktop
  (200101, 20010, 'windows', 'https://desktop.github.com/', 'latest', null, 1, '官网', sysdate()),
  (200102, 20010, 'mac',     'https://desktop.github.com/', 'latest', null, 2, '官网', sysdate()),
  -- Notepad++
  (200111, 20011, 'windows', 'https://notepad-plus-plus.org/downloads/', 'latest', null, 1, '官网', sysdate()),

  -- Everything
  (200201, 20020, 'windows', 'https://www.voidtools.com/downloads/', 'latest', null, 1, '官网', sysdate()),
  -- PowerToys（草稿）
  (200211, 20021, 'windows', 'https://github.com/microsoft/PowerToys/releases', 'latest', null, 1, 'Release', sysdate()),
  -- Rufus
  (200221, 20022, 'windows', 'https://rufus.ie/en/', 'latest', null, 1, '官网', sysdate()),
  -- Ventoy
  (200231, 20023, 'windows', 'https://www.ventoy.net/en/download.html', 'latest', null, 1, '官网', sysdate()),
  (200232, 20023, 'linux',   'https://www.ventoy.net/en/download.html', 'latest', null, 2, '官网', sysdate()),
  -- WinSCP
  (200241, 20024, 'windows', 'https://winscp.net/eng/download.php', 'latest', null, 1, '官网', sysdate()),
  -- PuTTY
  (200251, 20025, 'windows', 'https://www.putty.org/', 'latest', null, 1, '官网', sysdate()),
  -- Sysinternals Suite
  (200261, 20026, 'windows', 'https://learn.microsoft.com/en-us/sysinternals/downloads/sysinternals-suite', 'latest', null, 1, '官方文档', sysdate()),
  -- WizTree（下架）
  (200271, 20027, 'windows', 'https://diskanalyzer.com/download', 'latest', null, 1, '官网', sysdate()),

  -- VLC
  (200301, 20030, 'windows', 'https://www.videolan.org/vlc/', 'latest', null, 1, '官网', sysdate()),
  (200302, 20030, 'mac',     'https://www.videolan.org/vlc/', 'latest', null, 2, '官网', sysdate()),
  (200303, 20030, 'linux',   'https://www.videolan.org/vlc/', 'latest', null, 3, '官网', sysdate()),
  -- OBS Studio
  (200311, 20031, 'windows', 'https://obsproject.com/download', 'latest', null, 1, '官网', sysdate()),
  (200312, 20031, 'mac',     'https://obsproject.com/download', 'latest', null, 2, '官网', sysdate()),
  (200313, 20031, 'linux',   'https://obsproject.com/download', 'latest', null, 3, '官网', sysdate()),
  -- HandBrake
  (200321, 20032, 'windows', 'https://handbrake.fr/downloads.php', 'latest', null, 1, '官网', sysdate()),
  (200322, 20032, 'mac',     'https://handbrake.fr/downloads.php', 'latest', null, 2, '官网', sysdate()),
  (200323, 20032, 'linux',   'https://handbrake.fr/downloads.php', 'latest', null, 3, '官网', sysdate()),
  -- FFmpeg
  (200331, 20033, 'windows', 'https://ffmpeg.org/download.html', 'latest', null, 1, '官网', sysdate()),
  (200332, 20033, 'mac',     'https://ffmpeg.org/download.html', 'latest', null, 2, '官网', sysdate()),
  (200333, 20033, 'linux',   'https://ffmpeg.org/download.html', 'latest', null, 3, '官网', sysdate()),

  -- Joplin
  (200401, 20040, 'windows', 'https://joplinapp.org/download/', 'latest', null, 1, '官网', sysdate()),
  (200402, 20040, 'mac',     'https://joplinapp.org/download/', 'latest', null, 2, '官网', sysdate()),
  (200403, 20040, 'linux',   'https://joplinapp.org/download/', 'latest', null, 3, '官网', sysdate()),
  (200404, 20040, 'android', 'https://joplinapp.org/download/', 'latest', null, 4, '官网', sysdate()),
  (200405, 20040, 'ios',     'https://joplinapp.org/download/', 'latest', null, 5, '官网', sysdate()),
  -- Logseq
  (200411, 20041, 'windows', 'https://github.com/logseq/logseq/releases', 'latest', null, 1, 'Release', sysdate()),
  (200412, 20041, 'mac',     'https://github.com/logseq/logseq/releases', 'latest', null, 2, 'Release', sysdate()),
  (200413, 20041, 'linux',   'https://github.com/logseq/logseq/releases', 'latest', null, 3, 'Release', sysdate()),
  -- Notion（下架）
  (200421, 20042, 'windows', 'https://www.notion.com/desktop', 'latest', null, 1, '官网', sysdate()),
  (200422, 20042, 'mac',     'https://www.notion.com/desktop', 'latest', null, 2, '官网', sysdate()),
  (200423, 20042, 'web',     'https://www.notion.com/', 'latest', null, 3, 'Web', sysdate()),
  -- Bitwarden
  (200431, 20043, 'windows', 'https://bitwarden.com/download/', 'latest', null, 1, '官网', sysdate()),
  (200432, 20043, 'mac',     'https://bitwarden.com/download/', 'latest', null, 2, '官网', sysdate()),
  (200433, 20043, 'linux',   'https://bitwarden.com/download/', 'latest', null, 3, '官网', sysdate()),
  (200434, 20043, 'android', 'https://bitwarden.com/download/', 'latest', null, 4, '官网', sysdate()),
  (200435, 20043, 'ios',     'https://bitwarden.com/download/', 'latest', null, 5, '官网', sysdate()),
  (200436, 20043, 'web',     'https://bitwarden.com/download/', 'latest', null, 6, '官网', sysdate()),

  -- Firefox
  (200501, 20050, 'windows', 'https://www.mozilla.org/firefox/new/', 'latest', null, 1, '官网', sysdate()),
  (200502, 20050, 'mac',     'https://www.mozilla.org/firefox/new/', 'latest', null, 2, '官网', sysdate()),
  (200503, 20050, 'linux',   'https://www.mozilla.org/firefox/new/', 'latest', null, 3, '官网', sysdate()),
  -- Brave
  (200511, 20051, 'windows', 'https://brave.com/download/', 'latest', null, 1, '官网', sysdate()),
  (200512, 20051, 'mac',     'https://brave.com/download/', 'latest', null, 2, '官网', sysdate()),
  (200513, 20051, 'linux',   'https://brave.com/download/', 'latest', null, 3, '官网', sysdate()),

  -- Telegram
  (200601, 20060, 'windows', 'https://telegram.org/desktop', 'latest', null, 1, '官网', sysdate()),
  (200602, 20060, 'mac',     'https://telegram.org/desktop', 'latest', null, 2, '官网', sysdate()),
  (200603, 20060, 'linux',   'https://telegram.org/desktop', 'latest', null, 3, '官网', sysdate()),
  (200604, 20060, 'android', 'https://telegram.org/android', 'latest', null, 4, '官网', sysdate()),
  (200605, 20060, 'ios',     'https://telegram.org/ios', 'latest', null, 5, '官网', sysdate()),
  -- Discord
  (200611, 20061, 'windows', 'https://discord.com/download', 'latest', null, 1, '官网', sysdate()),
  (200612, 20061, 'mac',     'https://discord.com/download', 'latest', null, 2, '官网', sysdate()),
  (200613, 20061, 'linux',   'https://discord.com/download', 'latest', null, 3, '官网', sysdate()),
  -- Slack
  (200621, 20062, 'windows', 'https://slack.com/downloads', 'latest', null, 1, '官网', sysdate()),
  (200622, 20062, 'mac',     'https://slack.com/downloads', 'latest', null, 2, '官网', sysdate()),
  (200623, 20062, 'linux',   'https://slack.com/downloads', 'latest', null, 3, '官网', sysdate()),

  -- Blender
  (200701, 20070, 'windows', 'https://www.blender.org/download/', 'latest', null, 1, '官网', sysdate()),
  (200702, 20070, 'mac',     'https://www.blender.org/download/', 'latest', null, 2, '官网', sysdate()),
  (200703, 20070, 'linux',   'https://www.blender.org/download/', 'latest', null, 3, '官网', sysdate()),
  -- GIMP
  (200711, 20071, 'windows', 'https://www.gimp.org/downloads/', 'latest', null, 1, '官网', sysdate()),
  (200712, 20071, 'mac',     'https://www.gimp.org/downloads/', 'latest', null, 2, '官网', sysdate()),
  (200713, 20071, 'linux',   'https://www.gimp.org/downloads/', 'latest', null, 3, '官网', sysdate()),
  -- Inkscape
  (200721, 20072, 'windows', 'https://inkscape.org/release/', 'latest', null, 1, '官网', sysdate()),
  (200722, 20072, 'mac',     'https://inkscape.org/release/', 'latest', null, 2, '官网', sysdate()),
  (200723, 20072, 'linux',   'https://inkscape.org/release/', 'latest', null, 3, '官网', sysdate()),
  -- Krita
  (200731, 20073, 'windows', 'https://krita.org/en/download/krita-desktop/', 'latest', null, 1, '官网', sysdate()),
  (200732, 20073, 'mac',     'https://krita.org/en/download/krita-desktop/', 'latest', null, 2, '官网', sysdate()),
  (200733, 20073, 'linux',   'https://krita.org/en/download/krita-desktop/', 'latest', null, 3, '官网', sysdate());
