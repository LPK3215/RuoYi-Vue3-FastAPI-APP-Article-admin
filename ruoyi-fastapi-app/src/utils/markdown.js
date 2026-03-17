import { marked } from "marked";

const renderer = new marked.Renderer();
// 安全考虑：用户端展示时，移除 Markdown 中的原始 HTML
renderer.html = () => "";

marked.setOptions({
  gfm: true,
  breaks: false,
  headerIds: false,
  mangle: false,
  renderer,
});

export function mdToHtml(markdown) {
  const md = (markdown || "").trim();
  if (!md) return "<p>暂无内容</p>";
  return marked.parse(md);
}

