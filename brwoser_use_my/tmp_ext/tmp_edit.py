import asyncio

from brwoser_use_my.cdp.cdp_tools import create_browser
from pycdp import cdp

from pycdp.asyncio import connect_cdp
import time



def create_new_tab():
    import requests

    # URL for Chrome DevTools Protocol (CDP)
    CDP_URL = "http://localhost:9222/json/new"

    # Create a new empty tab
    response = requests.put(CDP_URL)

    if response.status_code == 200:
        tab_info = response.json()
        print(f"New tab created: {tab_info['id']} - {tab_info['webSocketDebuggerUrl']}")
    else:
        print("Failed to create a new tab")

async def main():
    create_new_tab()

    conn = await connect_cdp('http://localhost:9222')




    target_id = await conn.execute(cdp.target.create_browser_context())
    target_session = await conn.connect_session(target_id)


    url = f"https://www.mouser.tw/c/?q=ZX-LD100"
    target_id = await conn.execute(cdp.target.create_target(url=None))
    # target_id = await conn.execute(cdp.target.create_target(url=url))
    time.sleep(5)
    target_session = await conn.connect_session(target_id)

if __name__ == '__main__':
    create_browser()
    asyncio.run(main())