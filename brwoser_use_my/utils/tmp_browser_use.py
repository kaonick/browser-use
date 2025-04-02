from browser_use import Agent, BrowserConfig, Browser
from llm_proxy import llm
config = BrowserConfig(
    headless=False,
    disable_security=True
)

browser = Browser(config=config)

async def ask(message: str) -> str:
    agent = Agent(
        browser=browser,
        task=message,
        llm=llm,
    )
    result = await agent.run()
    return result.final_result()


if __name__ == '__main__':
    import asyncio

    # message = input("请输入您的指令: ")

    message="Go to Reddit, search for 'browser-use' in the search bar, click on the first post and return the first comment."
    message="Go to mouser, search for 'browser-use' in the search bar, click on the first post and return the first comment."

    message=f"""
    * 開啟mouser網站
    * 搜尋「ZX-LD100」
    * 讀取搜尋的品項名稱、價格、明細網址
    * 在第一個品項點擊進入明細頁面。
    """
    message=f"""
    * 開啟momo網站
    * 搜尋「電冰箱」
    * 讀取搜尋的前10個品項的名稱、價格、明細網址
    * 在第一個品項點擊進入明細頁面。
    """

    result = asyncio.run(ask(message))
    print(result)