def diff(base: list, removed: list) -> list: 
    result = list(base).copy()
    for value in removed:
        try:
            result.remove(value)
        except ValueError:
            # do nothing
            continue
    
    return result

def fix_length(base: list, length: int, padding_item) -> list:
    """リストの長さを変更したものを生成して返す。

    元の配列の長さが length と同じかそれより大きい場合、
    先頭から length-1 番目までの要素が list と一致するリストを生成して返す。

    元の配列の長さが length より小さい場合、
    list のコピーの末尾に padding_item を1つ以上追加して作った長さ length のリストを返す。

    Args:
        base (list): 元となるリスト
        length (int): 生成するリストの長さ
        padding_item: 要素が足りない場合に末尾に追加する要素

    Returns:
        list: base をもとにして生成される、長さ length のリスト
    """    

    if len(base) >= length:
        return base[:length]
    else:
        return base.copy() + [padding_item] * (length - len(base))
