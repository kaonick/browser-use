import asyncio

from browser_use import DomService
from playwright.async_api import async_playwright

async def open_page():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        url="https://www.mouser.tw/c/?q=ZX-LD100"
        # url="https://scrapingant.com/"
        page = await context.new_page()
        await page.goto(url)
        print(await page.title())
        # do whatever scraping you need to

        # highlight elements
        dom_service = DomService(page)
        content = await dom_service.get_clickable_elements(
            focus_element=-1,
            viewport_expansion=0,
            highlight_elements=True,
        )


        await page.close()

        await context.close()
        await browser.close()

if __name__ == '__main__':

    asyncio.run(open_page())
