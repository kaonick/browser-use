import asyncio

from brwoser_use_my.cdp.cdp_tools import run_command, add_head, open_page, get_element_by_tag, get_dom, get_tag_id, get_by_id


async def main():
    import requests
    import time
    from websocket import create_connection #websocket-client

    # Step 1: Create a new tab
    NEW_TAB_URL = "http://localhost:9222/json/new"
    response = requests.put(NEW_TAB_URL)
    tab_info = response.json()

    if 'webSocketDebuggerUrl' not in tab_info:
        print("Failed to create a new tab")
        exit()

    ws_url = tab_info['webSocketDebuggerUrl']
    print(f"Connected to: {ws_url}")

    # Step 2: Connect to WebSocket
    # ws = cdp_wsconn(url="localhost:9222")
    ws = create_connection(ws_url)



    # Step 3: Enable the Page domain
    # ws.send('{"id":1,"method":"Page.enable"}')
    # # Step 4: Navigate to an empty HTML page
    # ws.send('{"id":2,"method":"Page.navigate","params":{"url":"about:blank"}}')

    # open_page(ws=ws,url='about:blank')
    open_page(ws=ws,url='https://example.com/')
    dom_node_id=get_dom(ws)

    # Give time for navigation to complete
    time.sleep(1)

    add_head(ws=ws)
    # Step 5: Inject an H1 title with red text
    script = """
    document.body.innerHTML = '<h1 style="color:red;">Hello, CDP!</h1>';
    """
    msg = run_command(ws, 'Runtime.evaluate', expression=script)
    time.sleep(1)

    # print(msg.get('result')['result']['value'])

    # ws.send(f'{{"id":3,"method":"Runtime.evaluate","params":{{"expression":{script!r}}}}}')

    # add_function(ws,function=None)
    # call_function(ws,function_call=None)

    # Step 6: Print the entire HTML content to verify the <h1> element is added
    print("Fetching entire HTML to verify <h1> element presence...")

    fetch_html_script = "let content= document.documentElement.outerHTML;content"
    # ws.send(f'{{"id":5,"method":"Runtime.evaluate","params":{{"expression":{fetch_html_script!r}}}}}')
    result=run_command(ws, 'Runtime.evaluate', expression=fetch_html_script)
    print("Page HTML:", result)


    print("Injected H1 with red text!")

    # get_element(ws,id='h1')
    object_id=get_tag_id(ws, tag='h1')
    get_by_id(ws, object_id=object_id,attr="text")


    ele_text=get_element_by_tag(ws,tag='h1')
    # Close WebSocket
    ws.close()


if __name__ == '__main__':
    # create_browser()
    asyncio.run(main())