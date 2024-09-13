def convert_crypto_to_rub(
    crypto_to_intermediary_rate: float,
    intermediary_to_rub_rate: float,
) -> float:
    return round(crypto_to_intermediary_rate * intermediary_to_rub_rate, 3)
