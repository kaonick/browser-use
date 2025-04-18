import asyncio

from brwoser_use_my.cdp.cdp_tools import open_page, cdp_conn, get_dom, get_node, get_node_attr, create_browser, \
    get_targets

import time





async def main():

    ws = cdp_conn(url="http://localhost:9222")




    # Step 3: Enable the Page domain
    # ws.send('{"id":1,"method":"Page.enable"}')
    # # Step 4: Navigate to an empty HTML page
    # ws.send('{"id":2,"method":"Page.navigate","params":{"url":"about:blank"}}')

    # open_page(ws=ws,url='about:blank')
    target_id=open_page(ws=ws,url='https://example.com/')
    dom_node_id=get_dom(ws)

    # Give time for navigation to complete
    time.sleep(1)

    get_targets(ws=ws)


    node_id=get_node(ws=ws,node_id=dom_node_id,selector="h1")

    text=get_node_attr(ws=ws,node_id=node_id,attr="innerText")


    node_id=get_node(ws=ws,node_id=dom_node_id,selector="a")

    text=get_node_attr(ws=ws,node_id=node_id,attr="href")







    # Close WebSocket
    ws.close()


if __name__ == '__main__':
    # create_browser()
    asyncio.run(main())