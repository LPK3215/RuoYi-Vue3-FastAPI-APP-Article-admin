# RuoYi Admin Style Template

一个独立的后台前端样式模板项目，专门抽取自当前后端管理系统里最值得复用的布局主题能力，方便后续新项目直接参考或二次复制。

## 包含内容

- 深色 / 浅色主题切换
- 点击触发的圆形 `view transition` 过渡动画
- 左侧菜单 / 混合菜单 / 顶部菜单三种布局模式
- 头像下拉菜单和“布局设置”抽屉
- 主题主色设置与本地持久化
- Tags View、固定 Header、Logo、页脚、动态标题等布局选项
- 几个示例页面，用来观察主题和组件状态

## 运行

```bash
npm install
npm run dev
```

## 目录说明

- `src/layout`：后台骨架布局
- `src/stores/layout.js`：布局状态、持久化、主题设置
- `src/utils/view-transition.js`：主题切换动画
- `src/styles/index.css`：主题变量、布局样式、抽屉和示例页面样式
