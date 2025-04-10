import asyncio

from brwoser_use_my.cdp.cdp_tools import run_command, open_page, cdp_conn, get_dom

import time





async def main():

    ws = cdp_conn(url="http://localhost:9222")




    # Step 3: Enable the Page domain
    # ws.send('{"id":1,"method":"Page.enable"}')
    # # Step 4: Navigate to an empty HTML page
    # ws.send('{"id":2,"method":"Page.navigate","params":{"url":"about:blank"}}')

    # open_page(ws=ws,url='about:blank')
    open_page(ws=ws,url='https://example.com/')
    dom_node_id=get_dom(ws)

    # Give time for navigation to complete
    time.sleep(1)

    # Step 4: Select an <h1> element using querySelector
    # ws.send(json.dumps({
    #     "id": 3,
    #     "method": "DOM.querySelector",
    #     "params": {"nodeId": dom_node_id, "selector": "h1"}
    # }))
    # response = json.loads(ws.recv())


    # # Extract the node ID of the selected element
    # h1_node_id = response["result"]["nodeId"]

    result=run_command(ws,"DOM.querySelector",nodeId=dom_node_id,selector="h1")
    h1_node_id=result["result"]["nodeId"]


    # Step 5: Resolve the node to get its JavaScript object
    # ws.send(json.dumps({
    #     "id": 4,
    #     "method": "DOM.resolveNode",
    #     "params": {"nodeId": h1_node_id}
    # }))
    # response = json.loads(ws.recv())
    #
    # # Extract objectId (JavaScript reference to the node)
    # object_id = response["result"]["object"]["objectId"]
    result=run_command(ws,"DOM.resolveNode",nodeId=h1_node_id)
    object_id=result["result"]["object"]["objectId"]
    print(f"Resolved Object ID: {object_id}")

    # Step 6: Use the resolved object in JavaScript
    # ws.send(json.dumps({
    #     "id": 5,
    #     "method": "Runtime.callFunctionOn",
    #     "params": {
    #         "functionDeclaration": "(node) => node.textContent",
    #         "objectId": object_id
    #     }
    # }))
    # response = json.loads(ws.recv())
    #
    # # Extract and print the text content of the <h1> element
    # h1_text = response["result"]["result"]["value"]
    #
    # result=run_command(ws,"Runtime.callFunctionOn",functionDeclaration="(node) => node.textContent",objectId=object_id)
    result=run_command(ws,"Runtime.callFunctionOn",functionDeclaration="function() {return this.innerText;}",objectId=object_id,returnByValue=True)
    h1_text=result["result"]["result"]["value"]
    print(f"H1 Text Content: {h1_text}")







    # Close WebSocket
    ws.close()


if __name__ == '__main__':
    # create_browser()
    asyncio.run(main())