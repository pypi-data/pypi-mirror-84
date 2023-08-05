import string
import re
import rstr

__default_schema = {
    "pattern": None,
    "minLength": 1,
    "maxLength": 100,
}

def genstr(schema: dict) -> str:
    """スキーマに適合する文字列を生成する。

    Args:
        schema (dict): string 型についての JsonSchema を表現するマップ

    Returns:
        str: 生成された文字列
    """

    schema = __normalize_schema(schema)
    
    pattern = re.compile(schema["pattern"]) if schema["pattern"] is not None else None
    minLength = schema["minLength"]
    maxLength = schema["maxLength"]

    generated = ""

    # pattern の指定がある場合、それを使用する
    if pattern is not None:
        generated = rstr.xeger(pattern)
    # maxLength が 0 の場合、空文字でよい
    elif maxLength is not None and maxLength <= 0:
        generated = ""
    # いずれにも当てはまらない場合、英字列を生成する。
    else:
        generated = rstr.rstr(string.ascii_letters, start_range=minLength, end_range=maxLength)

    return generated

def __normalize_schema(schema: dict) -> dict:
    """スキーマの正規化。乱数生成に使用しやすくするため、JsonSchema の未設定の項目を設定する。

    Args:
        schema (dict): number 型についての JsonSchema を表現するマップ

    Returns:
        dict: schema が持つ値とデフォルト値によって新たに作られた JsonSchema。
    """

    nSchema = __default_schema.copy()
    nSchema.update(schema)

    # maxLength = 0 の場合、minLength は無視する。
    if nSchema["maxLength"] <= 0:
        nSchema["minLength"] = None

    return nSchema
