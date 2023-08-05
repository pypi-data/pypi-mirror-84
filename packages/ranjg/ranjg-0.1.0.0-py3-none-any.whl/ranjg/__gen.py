import json
from .__gennone import gennone
from .__genbool import genbool
from .__genint import genint
from .__gennum import gennum
from .__genstr import genstr
from .__gendict import gendict
from .__genlist import genlist
from .__genany import genany
from .util.nonesafe import dfor

def gen(schema: dict = None, schema_file: str = None, output_file: str = None, output_fp = None):
    # TODO: schema と schema_file がともに None であるとき、エラー
    # TODO: output_file と output_fp がともに指定されたとき、エラー

    schema = dfor(schema, {})

    # スキーマファイルを読み込み
    if schema_file is not None:
        with open(schema_file) as fp:
            loaded_schema = json.load(fp)
            loaded_schema.update(schema)
            schema = loaded_schema

    # TODO: Type が複数の場合の処理

    generated = None
    if "type" not in schema:
        generated = genany(schema)
    elif schema["type"] == "null":
        generated = gennone(schema)
    elif schema["type"] == "integer":
        generated = genint(schema)
    elif schema["type"] == "number":
        generated = gennum(schema)
    elif schema["type"] == "boolean":
        generated = genbool(schema)
    elif schema["type"] == "string":
        generated = genstr(schema)
    elif schema["type"] == "object":
        generated = gendict(schema)
    elif schema["type"] == "array":
        generated = genlist(schema)
    else:
        raise Exception("Unsuported type: {}".format(schema["type"]))

    # 出力先指定がある場合、JSONとして出力する
    if output_file is not None:
        with open(output_file, "w+") as fp:
            json.dump(generated, fp)
    if output_fp is not None:
        json.dump(generated, output_fp)

    return generated
