import asyncio
import logging

import typer
import uvicorn

manager = typer.Typer()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@manager.command()
def run_telegram_bot():
    from src.bot import main

    asyncio.run(main.dp.start_polling(main.bot))


@manager.command()
def run_webhook():
    from src.webhook import main

    uvicorn.run(
        "src.webhook.main:app",
        host="0.0.0.0",  # noqa: S104
        port=main.config.webhook.port,
        loop="uvloop",
        reload=main.config.webhook.reload,
        workers=main.config.webhook.workers,
        root_path=main.config.webhook.root_path,
        use_colors=True,
    )



@manager.command()
def run_consumers():
    pass


if __name__ == "__main__":
    manager()
