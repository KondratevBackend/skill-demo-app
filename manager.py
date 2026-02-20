import asyncio
import logging

import typer

manager = typer.Typer()
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


@manager.command()
def run_telegram_bot():
    from src.bot import main

    asyncio.run(main.dp.start_polling(main.bot))


@manager.command()
def run_workers():
    pass


@manager.command()
def run_consumers():
    pass


if __name__ == "__main__":
    manager()
