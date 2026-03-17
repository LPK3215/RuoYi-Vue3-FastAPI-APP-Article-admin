import pytest
from playwright.async_api import async_playwright, expect

from common.base_page_test import BasePageTest
from common.config import Config


class SwaggerTest(BasePageTest):
    async def check_swagger_interface(self) -> None:
        """测试系统接口页面 (Swagger UI)"""

        # 1. 直接导航到系统接口页面
        await self.goto_page(Config.frontend_url + '/tool/swagger')

        # 2. 验证页面加载
        # 等待 iframe 出现
        iframe = self.page.locator('iframe')
        await expect(iframe).to_be_visible()

        # 获取 iframe 内容框架
        frame = self.page.frame_locator('iframe')

        # 后端未禁用Swagger时，验证 iframe 内部的标题包含 "RuoYi-FastAPI"
        # 当前生产环境已默认禁用Swagger，此处验证标题是否包含默认禁用提示
        h1_locator = frame.locator('h1')
        await expect(h1_locator).to_be_visible(timeout=15000)

        # In dev env Swagger is usually enabled; in prod it may be disabled.
        # Accept either state to keep the test stable across environments.
        h1_text = (await h1_locator.first.inner_text()).strip()
        assert (
            'Swagger UI has been disabled. Please enable it first.' in h1_text or 'RuoYi-FastAPI' in h1_text
        ), f'unexpected swagger iframe title: {h1_text!r}'


@pytest.mark.asyncio
async def test_swagger_page() -> None:
    """测试系统接口页面功能"""
    async with async_playwright() as p:
        test_instance = SwaggerTest()
        await test_instance.setup(p)
        try:
            await test_instance.check_swagger_interface()
        finally:
            await test_instance.teardown()
