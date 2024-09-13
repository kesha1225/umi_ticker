import asyncio
import logging
import traceback

import aiogram
import aiohttp
from aiogram.enums import ParseMode

from ticker.exchange.cmc import CoinMarketCupExchange
from ticker.exchange.sigen import SigenExchange
from ticker.texts import create_post_text
from ticker_config import GROUP_ID, BOT_TOKEN


async def notify_forever():
    bot = aiogram.Bot(BOT_TOKEN)

    session = aiohttp.ClientSession()
    sigen = SigenExchange(session=session)
    cmc = CoinMarketCupExchange(session=session)

    while True:
        try:
            post_text = await create_post_text(sigen=sigen, cmc=cmc)
            await bot.send_message(
                chat_id=GROUP_ID, text=post_text, parse_mode=ParseMode.HTML
            )
            await asyncio.sleep(60)
        except Exception as e:
            logging.info(f"{e} - {traceback.format_exc()}")


if __name__ == "__main__":
    _log_format = f"%(asctime)s - [%(levelname)s] - %(name)s - (%(filename)s).%(funcName)s(%(lineno)d) - %(message)s"
    logging.basicConfig(filename="log.txt", format=_log_format, level="INFO")

    loop = asyncio.new_event_loop()
    loop.create_task(notify_forever())
    loop.run_forever()
