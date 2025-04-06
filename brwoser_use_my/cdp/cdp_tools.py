import json

from pycdp.browser import ChromeLauncher
from pycdp.asyncio import connect_cdp
import time
import requests
import websocket   # websocket-client
from pycdp.asyncio import CDPConnection


def create_browser():
    # Create a new browser instance
    browser = ChromeLauncher(
        binary='C:\Program Files\Google\Chrome\Application\chrome.exe',  # linux path
        # args=['--remote-debugging-port=9222', '--incognito']
        args = ['--remote-debugging-port=9222',"--remote-allow-origins=*"]
    )
    # Launch the browser
    browser.launch()
    return browser
########################################################################################
"""
CDP (Chrome DevTools Protocol) is a set of APIs that allows you to control and inspect the Chrome browser.
"""
request_id = 0
def run_command(ws, method, **kwargs):
    global request_id
    request_id += 1
    command = {'method': method,
               'id': request_id,
               'params': kwargs}
    ws.send(json.dumps(command))
    while True:
        msg = json.loads(ws.recv())
        if msg.get('id') == request_id:
            break
    return msg

def conn2ws(conn:CDPConnection):
    ws_url=conn._wsurl
    ws = websocket.create_connection(ws_url)
    return ws


def cdp_conn(url='http://localhost:9222')-> websocket.WebSocket:
    # r = requests.get('http://127.0.0.1:9222/json')  # 这是开启docker chrome headless的机器地址
    r = requests.get(f'{url}/json')
    if r.status_code != 200:
        raise ValueError("can not get the api ,please check if docker is ready")

    conn_api = r.json()[0].get('webSocketDebuggerUrl')
    return websocket.create_connection(conn_api)

def open_page(ws, url="about:blank"):
    result = run_command(ws, 'DOM.enable')
    result = run_command(ws, 'Page.enable')
    result = run_command(ws, 'Runtime.enable')
    result = run_command(ws, 'Page.navigate',url=url)

def get_dom(ws):
    # Step 5: Retrieve the document root node
    # ws.send('{"id":4,"method":"DOM.getDocument","params":{}}')
    result = run_command(ws, 'DOM.getDocument', params={})
    document_node_id = result["result"]["root"]["nodeId"]
    return document_node_id

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



def add_head(ws,item='<meta name="description" content="This is a test page">'):
    script = f"""
    document.head.innerHTML += `
        {item}
    `;
    """
    msg = run_command(ws, 'Runtime.evaluate', expression=script)



def get_base_url(ws):
    js = f"window.location.origin;"
    result = run_command(ws, 'Runtime.evaluate', expression=js)
    if result["result"]["result"]["value"]:
        base_url=result["result"]["result"]["value"]
    else:
        raise "base url not found"
    return base_url

def get_node(ws, node_id:int, selector:str):
    result=run_command(ws,"DOM.querySelector",nodeId=node_id,selector=selector)
    if result["result"]["nodeId"]:
        node_id=result["result"]["nodeId"]
    return node_id

def get_node_attr(ws, node_id:int,attr:str="innerText"):
    # request RemoteObject
    result=run_command(ws,"DOM.resolveNode",nodeId=node_id)
    if result["result"]["object"]:
        object_id=result["result"]["object"]["objectId"]
    else:
        raise "object not found"
    print(f"Resolved Object ID: {object_id}")
    # get attribute
    if attr=="innerText":
        result=run_command(ws,"Runtime.callFunctionOn",functionDeclaration='function() {return this.innerText;}',objectId=object_id,returnByValue=True)
    else:
        result=run_command(ws,"Runtime.callFunctionOn",functionDeclaration='function() {return this.getAttribute("'+attr+'");}',objectId=object_id,returnByValue=True)
    if result["result"]["result"]["value"]:
        value=result["result"]["result"]["value"]
        print(f"attribute Content: {value}")
        return value
    raise "attribute not found"



# *************************************************************************************************************
# not qulified

def add_function(ws,function:str):
    function = """
    function showMessage() {
        alert('Hello from CDP!');
    }
    """
    msg = run_command(ws, 'Runtime.evaluate', expression=function)

def call_function(ws, function_call:str):
    function_call = f"""
    showMessage()
    """
    result = run_command(ws, 'Runtime.evaluate', expression=function_call)
    return result


def add_element(ws, element:str):
    script = f"""
    document.body.innerHTML += `
        {element}
    `;
    """
    msg = run_command(ws, 'Runtime.evaluate', expression=script)

def get_element(ws, id:str):
    ws.send(json.dumps({
        "id": 4,
        "method": "DOM.getDocument",
        "params": {"depth": 1}
    }))

    params={
        "id": 4,
        "method": "DOM.getDocument",
        "params": {"depth": 1}
    }

    msg = run_command(ws, 'Runtime.evaluate', method="DOM.getDocument",params={"depth": 1})
    response = json.loads(ws.recv())
    return msg

def get_tag_id(ws, tag:str):
    js = f"document.querySelector('{tag}') ? document.querySelector('h1') : null"
    result = run_command(ws, 'Runtime.evaluate', expression=js)
    return result['result']['result']['objectId']
def get_tag_text(ws, tag:str):
    js = f"document.querySelector('{tag}') ? document.querySelector('h1').textContent.trim() : null"
    result = run_command(ws, 'Runtime.evaluate', expression=js)
    return result['result']['result']['value']

def get_by_id(ws, object_id:str,attr:str):
    result = run_command(ws, 'DOM.resolveNode', nodeId=object_id)
    return result['result']['result']['value']


def get_element_text(ws, selector:str):
    result = run_command(ws, 'Runtime.evaluate', expression=f"document.querySelector('{selector}').innerText")
    return result['result']['value']

def get_element_by_tag(ws, tag:str):
    js = f"document.querySelector('{tag}') ? document.querySelector('h1') : null"
    # js = f"document.querySelector('{tag}') ? document.querySelector('h1').textContent.trim() : null"
    result = run_command(ws, 'Runtime.evaluate', expression=js)
    return result['result']['result']['value']

def get_element_by_xpath(ws, xpath:str):
    js = f"let element = document.evaluate({xpath}, document, null, XPathResult.FIRST_ORDERED_NODE_TYPE, null).singleNodeValue;element;"
    result = run_command(ws, 'Runtime.evaluate', expression=js)
    return result['result']['value']



def add_element_in_element_child(ws, element:str):
    script = f"""
    document.body.children[0].innerHTML += `
        {element}
    `;
    """
    msg = run_command(ws, 'Runtime.evaluate', expression=script)