/**
 * Brand / product configuration.
 *
 * Keep all “what is this system called” values in one place so the UI can be
 * rebranded without hunting through components.
 */

export const APP_TITLE = import.meta.env.VITE_APP_TITLE || "管理后台";

// Sidebar logo text can be shorter than the page title.
export const APP_LOGO_TEXT =
  import.meta.env.VITE_APP_LOGO_TEXT || APP_TITLE;

// Optional: used in login page footer, etc.
export const APP_FOOTER = import.meta.env.VITE_APP_FOOTER || "";

