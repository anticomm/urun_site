def parse_price(text: str) -> float:
    """
    '₺ 1.809,10', '1.659,17 TL' → 1809.10, 1659.17
    """
    cleaned = (
        text.replace("TL", "")
            .replace("₺", "")
            .replace(".", "")
            .replace(",", ".")
            .strip()
    )
    try:
        return float(cleaned)
    except:
        return 0.0
