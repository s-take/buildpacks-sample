import os
import sys
import site

sp = os.path.join(sys.argv[1], "lib", f"python{sys.version_info.major}.{sys.version_info.minor}", "site-packages")
site.addsitedir(sp)

import uvicorn

from starlette.applications import Starlette
from starlette.responses import PlainTextResponse
from starlette.routing import Route


async def homepage(request):
    return PlainTextResponse("Homepage")

async def about(request):
    return PlainTextResponse("About")


routes = [
    Route("/", endpoint=homepage),
    Route("/about", endpoint=about),
]

app = Starlette(routes=routes)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, log_level="info")
