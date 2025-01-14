import logging
from typing import Dict

from litestar import Litestar, Response, get
from litestar.background_tasks import BackgroundTask, BackgroundTasks

logger = logging.getLogger(__name__)
greeted = set()


async def logging_task(name: str) -> None:
    logger.info("%s was greeted", name)


async def saving_task(name: str) -> None:
    greeted.add(name)


@get("/")
def greeter(name: str) -> Response[Dict[str, str]]:
    return Response(
        {"hello": name},
        background=BackgroundTasks(
            [
                BackgroundTask(logging_task, name),
                BackgroundTask(saving_task, name),
            ]
        ),
    )


app = Litestar(route_handlers=[greeter])
