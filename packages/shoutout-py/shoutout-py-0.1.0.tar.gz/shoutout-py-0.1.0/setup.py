# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['shoutout']

package_data = \
{'': ['*']}

install_requires = \
['aioredis>=1.3.1,<2.0.0']

setup_kwargs = {
    'name': 'shoutout-py',
    'version': '0.1.0',
    'description': 'Realtime messaging with Redis PUB/SUB.',
    'long_description': '# Shoutout\n\n## Realtime messaging with Redis PUB/SUB.\n\nShout-out is designed to work with [FastAPI websocket](https://fastapi.tiangolo.com/advanced/websockets/), while running behind [Gunicorn](https://gunicorn.org/) with multiple [Uvicorn workers](https://www.uvicorn.org/deployment/#gunicorn). Where a centralized caching layer (Redis) is required to maintain state (messages) across workers.\n\nYou can also use Shoutout as a standalone asynchronous application.\n\n## Usage\n\n### Standalone\n\n```python\nimport asyncio\n\nfrom shoutout.broadcast import Broadcast\n\nbroadcast = Broadcast("redis://localhost:6379")\n\n\nasync def main():\n    await broadcast.connect()\n    async with broadcast.subscribe("hello") as subscriber:\n        if subscriber:\n            await broadcast.publish("hello", message={\n                "channel": "hello", "message": "Hello World!"})\n            async for _, msg in subscriber:\n                print(msg)\n                break\n\n\nif __name__ == "__main__":\n    asyncio.run(main())\n```\n_The example above is complete and should run as is._\n\n\n### FastAPI\n\n```python\nfrom fastapi import FastAPI, WebSocket\nfrom fastapi.responses import HTMLResponse\nfrom shoutout.broadcast import Broadcast\nfrom starlette.concurrency import run_until_first_complete\n\nbroadcast = Broadcast("redis://localhost:6379")\napp = FastAPI(on_startup=[broadcast.connect], on_shutdown=[broadcast.disconnect])\n\n\nasync def ws_receiver(websocket):\n    async for message in websocket.iter_text():\n        await broadcast.publish(channel="shout", message={"msg": message})\n\n\nasync def ws_sender(websocket):\n    async with broadcast.subscribe(channel="shout") as subscriber:\n        if subscriber:\n            async for _, msg in subscriber:\n                await websocket.send_json(msg)\n\n\n@app.websocket("/ws")\nasync def websocket_endpoint(websocket: WebSocket):\n    await websocket.accept()\n    await run_until_first_complete(\n        (ws_receiver, {"websocket": websocket}),\n        (ws_sender, {"websocket": websocket}),\n    )\n\n\nhtml = """\n<!DOCTYPE html>\n<html>\n    <head>\n        <title>Chat</title>\n    </head>\n    <body>\n        <h1>WebSocket Chat</h1>\n        <form action="" onsubmit="sendMessage(event)">\n            <input type="text" id="messageText" autocomplete="off"/>\n            <button>Send</button>\n        </form>\n        <ul id=\'messages\'>\n        </ul>\n        <script>\n            var ws = new WebSocket("ws://localhost:8000/ws");\n            ws.onmessage = function(event) {\n                var messages = document.getElementById(\'messages\')\n                var message = document.createElement(\'li\')\n                var content = document.createTextNode(event.data)\n                message.appendChild(content)\n                messages.appendChild(message)\n            };\n            function sendMessage(event) {\n                var input = document.getElementById("messageText")\n                ws.send(input.value)\n                input.value = \'\'\n                event.preventDefault()\n            }\n        </script>\n    </body>\n</html>\n"""\n\n\n@app.get("/")\nasync def get():\n    return HTMLResponse(html)\n```\n_The example above is complete and should run as is._\n\nRun it:\n```shell\nuvicorn main:app --reload\n```',
    'author': 'Alexander van Zyl',
    'author_email': 'vanzyl.alex@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/alexvanzyl/shoutout',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
