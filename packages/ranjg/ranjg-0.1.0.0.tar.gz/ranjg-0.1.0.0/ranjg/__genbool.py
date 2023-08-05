import random

def genbool(schema: dict) -> bool:
    """スキーマに適合する真偽値を生成する。

    Args:
        schema (dict): boolean 型についての JsonSchema を表現するマップ

    Returns:
        bool: 生成された真偽値
    """

    return random.random() < 0.5
