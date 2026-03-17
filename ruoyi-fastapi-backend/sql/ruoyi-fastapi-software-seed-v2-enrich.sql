-- --------------------------------------------------------
-- 软件库（演示数据补充：V2 字段/资源 URL）
-- 说明：
-- 1) 依赖 ruoyi-fastapi.sql + ruoyi-fastapi-software.sql + ruoyi-fastapi-software-seed.sql 已执行
-- 2) 本脚本用于补充：官网/仓库/作者/团队/许可证/开源/标签 + 资源URL
-- 3) 可重复执行：更新使用 update；资源使用固定 resource_id + insert ignore
-- --------------------------------------------------------

-- ----------------------------
-- 1、补充软件元信息（V2）
-- ----------------------------
update tool_software
set
  official_url = 'https://code.visualstudio.com/',
  repo_url     = 'https://github.com/microsoft/vscode',
  author       = 'Microsoft',
  team         = 'Microsoft',
  license      = 'MIT',
  open_source  = '1',
  tags         = 'dev,editor,ide'
where software_id = 10001;

update tool_software
set
  official_url = 'https://git-scm.com/',
  repo_url     = 'https://github.com/git/git',
  author       = 'Git Community',
  team         = 'git',
  license      = 'GPL-2.0-only',
  open_source  = '1',
  tags         = 'dev,vcs,git'
where software_id = 10002;

update tool_software
set
  official_url = 'https://www.python.org/',
  repo_url     = 'https://github.com/python/cpython',
  author       = 'Python Software Foundation',
  team         = 'PSF',
  license      = 'PSF-2.0',
  open_source  = '1',
  tags         = 'dev,language,script,python'
where software_id = 20001;

update tool_software
set
  official_url = 'https://nodejs.org/',
  repo_url     = 'https://github.com/nodejs/node',
  author       = 'OpenJS Foundation',
  team         = 'Node.js',
  license      = 'MIT',
  open_source  = '1',
  tags         = 'dev,language,javascript,node'
where software_id = 20002;

update tool_software
set
  official_url = 'https://go.dev/',
  repo_url     = 'https://github.com/golang/go',
  author       = 'Google',
  team         = 'Go',
  license      = 'BSD-3-Clause',
  open_source  = '1',
  tags         = 'dev,language,go,backend'
where software_id = 20003;

update tool_software
set
  official_url = 'https://www.rust-lang.org/',
  repo_url     = 'https://github.com/rust-lang/rust',
  author       = 'Rust Project',
  team         = 'Rust Foundation',
  license      = 'MIT/Apache-2.0',
  open_source  = '1',
  tags         = 'dev,language,rust,cli'
where software_id = 20004;

update tool_software
set
  official_url = 'https://www.google.com/chrome/',
  repo_url     = 'https://chromium.googlesource.com/chromium/src',
  author       = 'Google',
  team         = 'Chrome',
  license      = 'Proprietary (Chrome) / BSD (Chromium)',
  open_source  = '0',
  tags         = 'daily,browser,web'
where software_id = 10005;

-- ----------------------------
-- 2、补充资源 URL（固定ID，便于重复执行）
-- ----------------------------
insert ignore into tool_software_resource
  (resource_id, software_id, resource_type, title, resource_url, sort, remark, create_time)
values
  -- VS Code
  (510001, 10001, 'doc',  '官方文档',  'https://code.visualstudio.com/docs',  1, 'V2演示数据', sysdate()),
  (510002, 10001, 'link', '下载页面',  'https://code.visualstudio.com/Download', 2, 'V2演示数据', sysdate()),

  -- Git
  (510101, 10002, 'doc',  '官方文档',  'https://git-scm.com/doc',  1, 'V2演示数据', sysdate()),
  (510102, 10002, 'link', '下载页面',  'https://git-scm.com/downloads', 2, 'V2演示数据', sysdate()),

  -- Python
  (510201, 20001, 'doc',  'Python 文档', 'https://docs.python.org/3/', 1, 'V2演示数据', sysdate()),
  (510202, 20001, 'link', '下载页面',   'https://www.python.org/downloads/', 2, 'V2演示数据', sysdate()),
  (510203, 20001, 'link', 'PyPI',       'https://pypi.org/', 3, 'V2演示数据', sysdate()),

  -- Node.js
  (510301, 20002, 'doc',  '官方文档', 'https://nodejs.org/en/learn', 1, 'V2演示数据', sysdate()),
  (510302, 20002, 'link', '下载页面', 'https://nodejs.org/en/download', 2, 'V2演示数据', sysdate()),

  -- Go
  (510401, 20003, 'doc',  '官方文档', 'https://go.dev/doc/', 1, 'V2演示数据', sysdate()),
  (510402, 20003, 'link', '下载页面', 'https://go.dev/dl/', 2, 'V2演示数据', sysdate()),

  -- Rust
  (510501, 20004, 'doc',  '官方文档', 'https://doc.rust-lang.org/', 1, 'V2演示数据', sysdate()),
  (510502, 20004, 'link', '安装说明', 'https://www.rust-lang.org/tools/install', 2, 'V2演示数据', sysdate()),

  -- Chrome / Chromium
  (510601, 10005, 'link', 'Chrome 下载', 'https://www.google.com/chrome/', 1, 'V2演示数据', sysdate()),
  (510602, 10005, 'link', 'Chromium',    'https://www.chromium.org/', 2, 'V2演示数据', sysdate());

