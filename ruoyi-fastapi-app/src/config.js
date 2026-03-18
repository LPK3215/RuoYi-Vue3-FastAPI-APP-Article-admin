const baseUrl = (import.meta.env.VITE_API_BASE_URL || "http://localhost:9099").trim();

// 应用全局配置
export default {
  baseUrl,
  // 应用信息
  appInfo: {
    // 应用名称
    name: "DeskOps",
    // 应用版本
    version: "1.9.0",
    // 应用logo
    logo: "/static/logo.png",
    // 官方网站
    site_url: "",
    // 政策协议
    agreements: [
      {
        title: "隐私政策",
        url: "",
      },
      {
        title: "用户服务协议",
        url: "",
      },
    ],
  },
};
