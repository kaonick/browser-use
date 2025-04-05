import websocket
from pydantic.v1 import BaseModel

from brwoser_use_my.tmp.tools import run_command


class Page():
    """
    Page class to represent a web page.
    """




    def __init__(self, ws:websocket.WebSocket,url: str):
        self.url = url
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
        # args:{} to list
        if args is None:
            args = {}
        args_list=[{k:v} for k,v in args.items()]

        register_script = f"""
        (() => {{
          const fn = {js_code}
          return fn;
        }})()
        """

        arguments=[
            {"value": args}
        ]

        # result=run_command(self.ws, 'Runtime.evaluate', expression=js_code)
        result=run_command(self.ws, 'Runtime.evaluate', expression=register_script)
        if result['result']['result']['type'] is not None:
            type=result['result']['result']['type']
            if type=="number":
                return result['result']['result']['value']
            elif type=="function":
                # get objectId
                objectId=result['result']['result']['objectId']
                # get value
                result=run_command(self.ws, 'Runtime.callFunctionOn',
                                   functionDeclaration="function(arg) { return this(arg); }",
                                   # arguments=args_list,
                                   arguments=arguments,
                                   objectId=objectId,
                                   returnByValue=True
                )
                if result['result']['result']['value']:
                    return result['result']['result']['value']
        eval_page: dict ={}
        return eval_page


