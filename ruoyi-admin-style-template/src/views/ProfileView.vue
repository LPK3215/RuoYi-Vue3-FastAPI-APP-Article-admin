<template>
  <div class="profile-grid">
    <el-card class="panel-card profile-card" shadow="never">
      <div class="profile-head">
        <el-avatar :size="72" class="profile-avatar">管</el-avatar>
        <div>
          <h2>管理员</h2>
          <p>这个页面模拟了头像菜单里的“个人中心”，用来演示布局和卡片样式。</p>
        </div>
      </div>

      <el-descriptions :column="1" border>
        <el-descriptions-item label="角色">系统管理员</el-descriptions-item>
        <el-descriptions-item label="模板用途">后台布局样式参考项目</el-descriptions-item>
        <el-descriptions-item label="可复用能力">主题、布局、菜单、设置抽屉、切换动画</el-descriptions-item>
      </el-descriptions>
    </el-card>

    <el-card class="panel-card" shadow="never">
      <template #header>
        <div class="panel-header">
          <span>后续建议</span>
          <el-tag type="primary" effect="plain">可以继续扩</el-tag>
        </div>
      </template>

      <ul class="guide-points">
        <li>把你自己的菜单结构替换到 `src/config/navigation.js`。</li>
        <li>把默认页面替换成业务页后，布局和主题系统仍然能直接沿用。</li>
        <li>如果你后面想加企业品牌风格，只需要继续扩展主题变量和设置抽屉。</li>
      </ul>
    </el-card>
  </div>
</template>
