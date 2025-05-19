import numpy as np

def hash_to_128_bit_md5_int(md5):
    return int.from_bytes(md5.digest(), 'big') # 128 bits worth.

def hash_to_64_bit_reals_in_unit_interval(md5):
    # An md5 sum is 64 bits long so we get two such reals.

    x = hash_to_128_bit_md5_int(md5)
    bot_64_bits = x & 0xffFFffFFffFFffFF
    top_64_bits = x >> 64
    return np.float64(top_64_bits)/(1 << 64), np.float64(bot_64_bits)/(1 << 64)

