import websocket
from pydantic.v1 import BaseModel


class Page(BaseModel):
    """
    Page class to represent a web page.
    """

    url: str
    title: str
    content: str

    def __init__(self, ws:websocket.WebSocket,url: str):
        super().__init__(url=url)
        self.ws = ws
        self.frames=[]


    async def locator(self, selector: str) -> str:
        """
        Locate an element on the page using a CSS selector.
        """
        self.ws.send(f"document.querySelector('{selector}').outerHTML")
        return self.ws.recv()

    async def evaluate(self, js_code:str, args=None) -> {}:
        """
        Evaluate JavaScript code on the page.
        """





        if args is None:
            args = {}
        self.ws.send(f"eval({js_code})")
        return self.ws.recv()


