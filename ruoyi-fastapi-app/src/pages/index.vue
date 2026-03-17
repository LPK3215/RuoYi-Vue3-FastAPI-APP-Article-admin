<template>
  <view class="flex h-full flex-col bg-[#0b0f14]">
    <view class="px-4 pt-6">
      <view class="relative overflow-hidden rounded-3xl bg-gradient-to-br from-slate-950 via-slate-900 to-indigo-900 p-6 shadow-xl shadow-black/40">
        <view class="absolute -right-14 -top-16 size-40 rounded-full bg-indigo-400/20 blur-2xl"></view>
        <view class="absolute -left-10 -bottom-14 size-40 rounded-full bg-white/10 blur-2xl"></view>

        <view class="relative z-10">
          <view class="flex items-center justify-between">
            <view>
              <view class="text-[22px] font-bold text-white tracking-wide">DeskOps</view>
              <view class="mt-1 text-xs text-white/70">软件库 · 教程 · 下载</view>
            </view>
            <view class="flex items-center space-x-2">
              <view class="px-3 py-1 rounded-full bg-white/10 text-white/80 text-[11px]">移动端</view>
            </view>
          </view>

          <view class="mt-5 grid grid-cols-2 gap-3">
            <view class="rounded-2xl bg-white/10 border border-white/10 p-4 active:opacity-80" @click="goTab('/pages/software/index')">
              <view class="flex items-center justify-between">
                <view>
                  <view class="text-white font-semibold">软件库</view>
                  <view class="mt-1 text-white/60 text-xs">分类 · 标签 · 下载</view>
                </view>
                <view class="i-mdi-download-box-outline text-2xl text-white/90"></view>
              </view>
            </view>
            <view class="rounded-2xl bg-white/10 border border-white/10 p-4 active:opacity-80" @click="goTab('/pages/article/index')">
              <view class="flex items-center justify-between">
                <view>
                  <view class="text-white font-semibold">教程</view>
                  <view class="mt-1 text-white/60 text-xs">类型 · 附件 · 关联软件</view>
                </view>
                <view class="i-mdi-book-open-page-variant text-2xl text-white/90"></view>
              </view>
            </view>
          </view>

          <view class="mt-4 text-[11px] text-white/55">建议：把“软件/教程/我的”作为三大入口，其他系统管理留在后台。</view>
        </view>
      </view>
    </view>

    <view class="px-4 pt-4 pb-24">
      <view class="rounded-2xl bg-white p-4">
        <view class="text-sm font-bold text-gray-900">提示</view>
        <view class="mt-2 text-xs text-gray-600 leading-5">
          这个移动端只保留你日常真正会用到的功能：浏览软件、看教程、下载附件。管理/新增/导入等操作仍建议在后台完成。
        </view>
      </view>
    </view>
  </view>
</template>

<script setup>
function goTab(url) {
  // tabBar 页面用 switchTab，避免返回栈混乱
  uni.switchTab({ url })
}
</script>
