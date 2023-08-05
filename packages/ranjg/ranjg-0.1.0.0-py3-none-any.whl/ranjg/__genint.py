import sys
import random

def genint(schema: dict) -> int:
    """スキーマに適合する整数を生成する。

    Args:
        schema (dict): integer 型についての JsonSchema を表現するマップ

    Returns:
        int: 生成された整数
    """

    schema = __normalize_schema(schema)

    minimum: int = schema["minimum"]
    maximum: int = schema["maximum"]

    if(minimum > maximum):
        raise Exception("Minimum value must be lower than or equal to the maximum value.")

    return random.randint(minimum, maximum)

def __normalize_schema(schema: dict) -> dict:
    """スキーマの正規化。乱数生成に使用しやすくするため、JsonSchema の未設定の項目を設定する。

    Args:
        schema (dict): integer 型についての JsonSchema を表現するマップ

    Returns:
        dict: schema が持つ値とデフォルト値によって新たに作られた JsonSchema。
    """

    # 生成する数値の最小値
    inclusiveMinimum = schema.get("minimum", None)
    exclusiveMinimum = schema.get("exclusiveMinimum", None)
    if exclusiveMinimum == True:
        exclusiveMinimum = inclusiveMinimum
        inclusiveMinimum = None
    elif exclusiveMinimum == False:
        exclusiveMinimum = None
    minimum = 0
    if inclusiveMinimum is not None and exclusiveMinimum is not None:
        minimum = max(inclusiveMinimum, exclusiveMinimum + 1)
    elif exclusiveMinimum is not None:
        minimum = exclusiveMinimum + 1
    elif inclusiveMinimum is not None:
        minimum = inclusiveMinimum

    # 生成する数値の最大値
    inclusiveMaximum = schema.get("maximum", None)
    exclusiveMaximum = schema.get("exclusiveMaximum", None)
    if exclusiveMaximum == True:
        exclusiveMaximum = inclusiveMaximum
        inclusiveMaximum = None
    elif exclusiveMaximum == False:
        exclusiveMaximum = None
    maximum = 100
    if inclusiveMaximum is not None and exclusiveMaximum is not None:
        maximum = min(inclusiveMaximum, exclusiveMaximum - 1)
    elif exclusiveMaximum is not None:
        maximum = exclusiveMaximum - 1
    elif inclusiveMaximum is not None:
        maximum = inclusiveMaximum

    return {
        "minimum": minimum,
        "maximum": maximum,
    }
