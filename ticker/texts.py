from ticker.constants import OFFERS_DISTANCE
from ticker.converter import convert_crypto_to_rub
from ticker.enum import CryptoCurrency, OrderType, FiatCurrency, SigenExchangePair
from ticker.exchange.cmc import CoinMarketCupExchange
from ticker.exchange.sigen import SigenExchange
from ticker.models.sigen.exchange import ExchangeResponse
from ticker.models.sigen.p2p import P2POffer, P2POffers


def get_fiat_currency_symbol(currency: FiatCurrency) -> str:
    return {FiatCurrency.rub: "₽"}[currency]


def get_p2p_text(
    offers: list[P2POffer],
    crypto_currency: CryptoCurrency,
    fiat_currency: FiatCurrency,
    order_type: OrderType,
) -> str:
    prices = sorted(
        [
            float(offer.price)
            for offer in offers
            if offer.crypto_cur == crypto_currency
            and offer.currency == fiat_currency
            and offer.type == order_type
        ],
        reverse=order_type == OrderType.buy,
    )[:OFFERS_DISTANCE]

    if not prices:
        return "Нет данных"

    fiat_symbol = get_fiat_currency_symbol(currency=fiat_currency)
    return f"{prices[0]:,.2f}{fiat_symbol} - {prices[-1]:,.2f}{fiat_symbol}"


def get_rod_p2p_buy_text(p2p_data: P2POffers) -> str:
    return get_p2p_text(
        offers=p2p_data.offers,
        crypto_currency=CryptoCurrency.rod,
        fiat_currency=FiatCurrency.rub,
        order_type=OrderType.buy,
    )


def get_rod_p2p_sell_text(p2p_data: P2POffers) -> str:
    return get_p2p_text(
        offers=p2p_data.offers,
        crypto_currency=CryptoCurrency.rod,
        fiat_currency=FiatCurrency.rub,
        order_type=OrderType.sale,
    )


def get_umi_p2p_buy_text(p2p_data: P2POffers) -> str:
    return get_p2p_text(
        offers=p2p_data.offers,
        crypto_currency=CryptoCurrency.umi,
        fiat_currency=FiatCurrency.rub,
        order_type=OrderType.buy,
    )


def get_umi_p2p_sell_text(p2p_data: P2POffers) -> str:
    return get_p2p_text(
        offers=p2p_data.offers,
        crypto_currency=CryptoCurrency.umi,
        fiat_currency=FiatCurrency.rub,
        order_type=OrderType.sale,
    )


def get_crypto_to_rub_text(
    crypto_from: CryptoCurrency,
    intermediary_crypto: CryptoCurrency,
    crypto_to_intermediary_rate: float,
    intermediary_to_rub_rate: float,
    real_currency_for_text: str | None = None,
) -> str:
    price = convert_crypto_to_rub(
        crypto_to_intermediary_rate=crypto_to_intermediary_rate,
        intermediary_to_rub_rate=intermediary_to_rub_rate,
    )

    currency_for_text = real_currency_for_text or intermediary_crypto
    return f"1 {crypto_from} = {price:,.2f}₽ (за {currency_for_text})"


def get_rod_btc_to_rub_exchange_text(
    exchange_data: ExchangeResponse, btc_rub_price: float
) -> str:
    return get_crypto_to_rub_text(
        crypto_from=CryptoCurrency.rod,
        intermediary_crypto=CryptoCurrency.btc,
        crypto_to_intermediary_rate=exchange_data.get_pair_last_price(
            pair=SigenExchangePair.ROD_BTC
        ),
        intermediary_to_rub_rate=btc_rub_price,
    )


def get_rod_usdt_to_rub_exchange_text(
    exchange_data: ExchangeResponse, usdt_rub_price: float
) -> str:
    return get_crypto_to_rub_text(
        crypto_from=CryptoCurrency.rod,
        intermediary_crypto=CryptoCurrency.usdt,
        crypto_to_intermediary_rate=exchange_data.get_pair_last_price(
            pair=SigenExchangePair.ROD_USDT
        ),
        intermediary_to_rub_rate=usdt_rub_price,
    )


def get_umi_btc_to_rub_exchange_text(
    exchange_data: ExchangeResponse, btc_rub_price: float
) -> str:
    return get_crypto_to_rub_text(
        crypto_from=CryptoCurrency.umi,
        intermediary_crypto=CryptoCurrency.btc,
        crypto_to_intermediary_rate=exchange_data.get_pair_last_price(
            pair=SigenExchangePair.UMI_BTC
        ),
        intermediary_to_rub_rate=btc_rub_price,
    )


def get_umi_usdt_to_rub_exchange_text(
    exchange_data: ExchangeResponse, usdt_rub_price: float
) -> str:
    return get_crypto_to_rub_text(
        crypto_from=CryptoCurrency.umi,
        intermediary_crypto=CryptoCurrency.usdt,
        crypto_to_intermediary_rate=exchange_data.get_pair_last_price(
            pair=SigenExchangePair.UMI_USDT
        ),
        intermediary_to_rub_rate=usdt_rub_price,
    )


def get_umi_ton_to_rub_exchange_text(
    exchange_data: ExchangeResponse, ton_rub_price: float
) -> str:
    return get_crypto_to_rub_text(
        crypto_from=CryptoCurrency.umi,
        intermediary_crypto=CryptoCurrency.ton,
        crypto_to_intermediary_rate=exchange_data.get_pair_last_price(
            pair=SigenExchangePair.UMI_TON
        ),
        intermediary_to_rub_rate=ton_rub_price,
    )


def get_umi_usdt_ton_to_rub_exchange_text(
    exchange_data: ExchangeResponse, usdt_rub_price: float
) -> str:
    return get_crypto_to_rub_text(
        crypto_from=CryptoCurrency.umi,
        intermediary_crypto=CryptoCurrency.ton,
        crypto_to_intermediary_rate=exchange_data.get_pair_last_price(
            pair=SigenExchangePair.UMI_USDTON
        ),
        intermediary_to_rub_rate=usdt_rub_price,
        real_currency_for_text=CryptoCurrency.ton_usdt,
    )


async def create_post_text(sigen: SigenExchange, cmc: CoinMarketCupExchange) -> str:
    p2p_data = await sigen.get_p2p_offers_public_list()
    sigen_exchange_data = await sigen.get_all_exchange()

    # calculate p2p

    rod_p2p_buy_text = get_rod_p2p_buy_text(p2p_data=p2p_data)
    rod_p2p_sell_text = get_rod_p2p_sell_text(p2p_data=p2p_data)

    umi_p2p_buy_text = get_umi_p2p_buy_text(p2p_data=p2p_data)
    umi_p2p_sell_text = get_umi_p2p_sell_text(p2p_data=p2p_data)

    # calculate exchange

    btc_rub_price = await cmc.get_cached_price(
        currency_from=CryptoCurrency.btc, currency_to=FiatCurrency.rub
    )
    usdt_rub_price = await cmc.get_cached_price(
        currency_from=CryptoCurrency.usdt, currency_to=FiatCurrency.rub
    )
    ton_rub_price = await cmc.get_cached_price(
        currency_from=CryptoCurrency.ton, currency_to=FiatCurrency.rub
    )

    rod_btc_exchange_text = get_rod_btc_to_rub_exchange_text(
        exchange_data=sigen_exchange_data, btc_rub_price=btc_rub_price
    )
    rod_usdt_exchange_text = get_rod_usdt_to_rub_exchange_text(
        exchange_data=sigen_exchange_data, usdt_rub_price=usdt_rub_price
    )

    umi_btc_exchange_text = get_umi_btc_to_rub_exchange_text(
        exchange_data=sigen_exchange_data, btc_rub_price=btc_rub_price
    )
    umi_usdt_exchange_text = get_umi_usdt_to_rub_exchange_text(
        exchange_data=sigen_exchange_data, usdt_rub_price=usdt_rub_price
    )
    umi_ton_exchange_text = get_umi_ton_to_rub_exchange_text(
        exchange_data=sigen_exchange_data, ton_rub_price=ton_rub_price
    )
    umi_usdt_ton_exchange_text = get_umi_usdt_ton_to_rub_exchange_text(
        exchange_data=sigen_exchange_data, usdt_rub_price=usdt_rub_price
    )

    return f"""<b>ROD:</b>
Продать: {rod_p2p_buy_text}
Купить: {rod_p2p_sell_text}

<b>UMI:</b>
Продать: {umi_p2p_buy_text}
Купить: {umi_p2p_sell_text}

<b>Биржа</b>
{rod_btc_exchange_text}
{rod_usdt_exchange_text}

{umi_btc_exchange_text}
{umi_usdt_exchange_text}
{umi_ton_exchange_text}
{umi_usdt_ton_exchange_text}"""
