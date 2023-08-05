import random
import ranjg
from ranjg.util.listutil import diff

# required 項目の値の生成に使用するスキーマのデフォルト値。
# properties に当該キーの指定がない場合に使用する。
__default_required_schema = {
    "type": "number",
    "minimum": 0,
    "maximum": 0,
}

__default_options = {
    "prob_not_required_properties": 0.5,
}

def gendict(schema: dict, options: dict = {}) -> dict:

    generated = dict()

    options = __normalize_options(options)

    # すでに生成or棄却が済んだキー
    # それぞれのキーは生成された場合は True, 棄却された場合は False を値に持つ。
    generatedKeys = dict()

    required: list = schema.get("required", [])
    properties: dict = schema.get("properties", {})
    not_required = diff(properties.keys(), required)

    # 必須項目を生成する
    for required_key in required:
        # すでに生成済みの項目は生成しない。ただし、棄却済みであるものは生成する。
        if generatedKeys.get(required_key) is True:
            continue

        generated[required_key] = ranjg.gen(properties.get(required_key, __default_required_schema))
        generatedKeys[required_key] = True

    # 必須でない項目を生成する
    for prop_key in not_required:
        # すでに生成or棄却済みの項目は生成しない。
        if generatedKeys.get(prop_key) is not None:
            continue

        # 一定確率 (options に指定) で生成しない。
        if random.random() >= options["prob_not_required_properties"]:
            generatedKeys[prop_key] = False
            continue

        generated[prop_key] = ranjg.gen(properties[prop_key])
        generatedKeys[prop_key] = True

    return generated

def __normalize_options(options: dict) -> dict:
    """オプションの正規化。乱数生成に使用しやすくするため、オプションの項目を設定する。

    Args:
        options (dict): 乱数生成のオプションを表現するマップ

    Returns:
        dict: options が持つ値とデフォルト値によって新たに作られた乱数生成オプション。
    """

    nOptions = __default_options.copy()
    nOptions.update(options)

    return nOptions


if __name__ == "__main__":
    schema = {
        "required": ["aaa", "bbb"],
        "properties": {
            "bbb": {
                "type": "object",
                "required": ["bbbaaa"],
            },
            "ccc": {
                "type": "number",
                "minimum": 1,
            },
        },
    }
    dict1 = gendict(schema)
    print(dict1)
    dict2 = gendict({})
    print(dict2)
