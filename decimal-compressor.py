from decimal import Decimal, getcontext

def x_over_xdotx_compressor(decimal_str, precision=20):
    decimal_part = decimal_str[2:]  # skip '0.'
    for d in range(1, len(decimal_part) // 2):
        pattern = '9' * d + '0' * d
        if decimal_part.startswith(pattern * 2):
            denominator = Decimal(10) ** d + 1
            numerator = Decimal(10) ** d
            value = numerator / denominator
            if str(value).startswith('0.' + pattern):
                return {"type": "x_over_xdotx", "d": d}
    return {"type": "raw", "value": decimal_str}


def x_over_xdotx_decompress(obj, precision=20):
    if obj["type"] != "x_over_xdotx":
        return obj["value"]
    d = obj["d"]
    getcontext().prec = precision + 5
    result = Decimal(10) ** d / (Decimal(10) ** d + 1)
    return str(result)[:str(result).find('.') + precision + 1]


def compress_list_of_values(values, precision=20):
    return [x_over_xdotx_compressor(v, precision) for v in values]


def decompress_list_of_values(compressed_list, precision=20):
    return [x_over_xdotx_decompress(c, precision) for c in compressed_list]
