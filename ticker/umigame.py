import json

import asyncpg

from ticker.models.umi_game import UmiGameRate
from ticker_config import UMI_GAME_BOT_DB_URL


async def get_umi_game_data() -> UmiGameRate | None:
    conn = await asyncpg.connect(UMI_GAME_BOT_DB_URL)
    row = await conn.fetchrow("SELECT * FROM option WHERE title = $1", "ROD_RUB")
    if row is None:
        return
    await conn.close()

    amount = json.loads(row["data"])["value"]
    return UmiGameRate(sell_levels_rate=amount, buy_tokens_rate=amount * 1.2)
