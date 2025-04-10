import json
import time
import websocket
import uuid
import argparse


def extract_h1_content(url, chrome_debug_url="localhost:9222"):
    """
    Extract H1 content from a webpage using Chrome DevTools Protocol via websocket-client

    Args:
        url (str): URL of the webpage to extract H1 content from
        chrome_debug_url (str): Chrome debug URL (default: localhost:9222)

    Returns:
        str: Content of the first H1 element found, or None if not found
    """
    # Step 1: Get available pages
    import requests
    resp = requests.get(f"http://{chrome_debug_url}/json")
    pages = resp.json()

    # Create a new tab if no pages available
    if not pages or len(pages) == 0:
        resp = requests.get(f"http://{chrome_debug_url}/json/new")
        pages = [resp.json()]

    # Get the WebSocket URL
    ws_url = pages[0]["webSocketDebuggerUrl"]

    # Connect to the WebSocket
    ws = websocket.create_connection(ws_url)

    # Generate request IDs
    navigate_id = 1 #str(uuid.uuid4())
    evaluate_id = 2 #str(uuid.uuid4())

    # Navigate to the URL
    ws.send(json.dumps({
        "id": navigate_id,
        "method": "Page.navigate",
        "params": {"url": url}
    }))

    # Wait for navigation to complete
    while True:
        result = json.loads(ws.recv())
        if result.get("id") == navigate_id:
            break

    # Wait a bit for page to load
    time.sleep(2)

    # Execute JavaScript to get the H1 content
    ws.send(json.dumps({
        "id": evaluate_id,
        "method": "Runtime.evaluate",
        "params": {
            "expression": "document.querySelector('h1') ? document.querySelector('h1').textContent.trim() : null"
        }
    }))

    # Get the result
    h1_content = None
    while True:
        result = json.loads(ws.recv())
        if result.get("id") == evaluate_id:
            if "result" in result and "result" in result["result"]:
                h1_content = result["result"]["result"].get("value")
            break

    # Close the WebSocket connection
    ws.close()

    return h1_content


if __name__ == "__main__":

    url="https://example.com/"
    chrome_debug="localhost:9222"

    try:
        content = extract_h1_content(url, chrome_debug)
        if content:
            print(f"H1 Content: {content}")
        else:
            print("No H1 element found on the page")
    except Exception as e:
        print(f"Error: {e}")