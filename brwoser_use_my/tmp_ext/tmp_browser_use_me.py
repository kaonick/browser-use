from brwoser_use_my.browser.browser_client import Page
from brwoser_use_my.dom.service import DomService

import asyncio

from brwoser_use_my.cdp.cdp_tools import open_page, cdp_conn, get_dom, get_node, get_node_attr

import time

async def main():
    ws = cdp_conn(url="http://localhost:9222")

    # url = 'https://example.com/'
    url = 'https://scrapingant.com/'
    # open_page(ws=ws,url='about:blank')
    open_page(ws=ws,url=url)
    dom_node_id=get_dom(ws)

    # Give time for navigation to complete
    time.sleep(1)

    # node_id=get_node(ws=ws,node_id=dom_node_id,selector="h1")
    #
    # text=get_node_attr(ws=ws,node_id=node_id,attr="innerText")
    #
    #
    # node_id=get_node(ws=ws,node_id=dom_node_id,selector="a")
    #
    # text=get_node_attr(ws=ws,node_id=node_id,attr="href")

    # highlight elements
    page=Page(ws=ws,url=url)
    dom_service = DomService(page)
    content = await dom_service.get_clickable_elements(
        # focus_element=-1,
        focus_element=1,   # focus on which index element
        viewport_expansion=0,
        highlight_elements=True,
    )

    # Close WebSocket
    ws.close()


if __name__ == '__main__':

    asyncio.run(main())
