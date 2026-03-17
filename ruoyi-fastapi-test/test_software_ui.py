import socket

import pytest
from playwright.async_api import async_playwright

from common.config import Config


def _is_port_open(host: str, port: int, timeout: float = 1.0) -> bool:
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except OSError:
        return False


@pytest.mark.asyncio
async def test_admin_software_menu_and_list_render() -> None:
    """
    管理端：验证「软件管理」一级菜单可见，且「软件列表」能渲染出种子数据（如 Python）
    """
    if not _is_port_open("127.0.0.1", 80):
        pytest.skip("admin frontend is not running on http://localhost:80")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        # Login
        await page.goto(Config.frontend_url + "/login")
        await page.wait_for_selector('input[placeholder="账号"]')
        await page.fill('input[placeholder="账号"]', "admin")
        await page.fill('input[placeholder="密码"]', "admin123")
        # The login button text may contain a space (e.g. "登 录"), so prefer type selector
        try:
            await page.click('button[type="submit"]', timeout=5000)
        except Exception:
            await page.click("button")

        await page.wait_for_url("**/index**", timeout=15000)

        # Sidebar -> 软件管理 -> 软件列表
        await page.wait_for_selector("text=软件管理", timeout=15000)
        await page.click("text=软件管理")
        await page.click("text=软件列表")

        # Search for a seeded item to make the test stable across pagination
        await page.wait_for_selector('input[placeholder*="名称"]', timeout=15000)
        await page.fill('input[placeholder*="名称"]', "Python")
        await page.click('button:has-text("搜索")')

        await page.wait_for_selector("text=Python", timeout=15000)

        await browser.close()


@pytest.mark.asyncio
async def test_portal_web_software_list_and_detail_render() -> None:
    """
    使用端 Web（Portal）：验证软件库列表页与详情页渲染（依赖 `npm run dev` 已启动）
    """
    if not _is_port_open("127.0.0.1", 5175):
        pytest.skip("portal web is not running on http://localhost:5175 (run `npm run dev` in ruoyi-fastapi-desktop-web)")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("http://localhost:5175/")
        await page.wait_for_selector("text=软件库", timeout=15000)

        # Search keyword to make it stable
        await page.fill('input[placeholder*="软件名称"]', "Python")
        await page.click('button:has-text("搜索")')
        await page.wait_for_selector("text=Python", timeout=15000)

        # Click entry -> detail page
        await page.click("text=Python")
        await page.wait_for_url("**/software/**", timeout=15000)
        await page.wait_for_selector('text=下载', timeout=15000)

        await browser.close()


@pytest.mark.asyncio
async def test_portal_web_article_list_render() -> None:
    """
    使用端 Web（Portal）：验证教程文章列表页可访问且能渲染（无文章时显示空状态也视为通过）
    """
    if not _is_port_open("127.0.0.1", 5175):
        pytest.skip("portal web is not running on http://localhost:5175")

    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto("http://localhost:5175/articles")
        await page.wait_for_selector("text=教程", timeout=15000)

        # If there is at least one article card, click into detail and check it renders.
        cards = await page.query_selector_all("a.ds-softCard")
        if cards:
            await cards[0].click()
            await page.wait_for_url("**/article/**", timeout=15000)
            await page.wait_for_selector("text=正文", timeout=15000)

        await browser.close()
