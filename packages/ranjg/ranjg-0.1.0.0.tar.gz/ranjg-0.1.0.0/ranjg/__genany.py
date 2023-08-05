import ranjg

# 使用するスキーマ
__default_schema = {
    "type": "null",
}

def genany(schema: dict):
    return ranjg.gen(__default_schema)
