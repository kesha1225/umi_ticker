import dataclasses


@dataclasses.dataclass
class UmiGameRate:
    buy_tokens_rate: float
    sell_levels_rate: float
