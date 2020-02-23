"""
    生成JWT
"""
import base64
import copy
import hmac
import json
import time


class Jwt:
    def __init__(self):
        pass

    @staticmethod
    def encode(payload, key, exp=300):
        # dict----b'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9PQ=='
        header_dict = {'alg': 'HS256', 'typ': 'JWT'}
        header_json = json.dumps(header_dict, separators=(',', ':'), sort_keys=True)
        header_b64 = Jwt.b64encode(header_json.encode())
        # dict----b'eyJleHAiOjE1NzgwNDExMjQsInVzZXJuYW1lIjoiZ3VveGlhb25hbyJ9PT0='
        payload_dict = copy.deepcopy(payload)
        payload_dict['exp'] = int(time.time() + exp)
        payload_json = json.dumps(payload_dict, separators=(',', ':'), sort_keys=True)
        payload_b64 = Jwt.b64encode(payload_json.encode())
        # key和（header_b64+payload_b64）做SHA256
        sign_bytes = header_b64 + b'.' + payload_b64
        if isinstance(key, str):
            key = key.encode()
        hmac_obj = hmac.new(key, sign_bytes, digestmod='SHA256')
        sign = hmac_obj.digest()
        sign_b64 = Jwt.b64encode(sign)
        return header_b64 + b'.' + payload_b64 + b'.' + sign_b64

    @staticmethod
    def b64encode(str_bytes):
        # b'guo'----b'Z3VvanVueXU='----去等号
        result = base64.urlsafe_b64encode(str_bytes).replace(b'=', b'')
        return result

    @staticmethod
    def b64decode(bs):
        # b'Z3VvanVueXU'----b'Z3VvanVueXU='
        rem = len(bs) % 4
        if rem:
            bs += b'=' * (4 - rem)
        return base64.urlsafe_b64decode(bs)

    @staticmethod
    # 校验
    def decode(token, key):
        header_b64, payload_b64, sign = token.split(b'.')
        if isinstance(key, str):
            key = key.encode()
        hmac_obj = hmac.new(key, header_b64 + b'.' + payload_b64, digestmod='SHA256')
        sign1 = hmac_obj.digest()
        new_sign = Jwt.b64encode(sign1)
        if sign != new_sign:
            raise JwtError('Your token is invalid!')
        payload_json_bytes = Jwt.b64decode(payload_b64)
        payload_dict = json.loads(payload_json_bytes.decode())
        if time.time() > payload_dict['exp']:
            raise JwtError('Your token is expired!')
        return payload_dict


class JwtError(Exception):
    def __init__(self, error_msg):
        self.error = error_msg

    def __str__(self):
        return '<JwtError error is %s>' % (self.error)


if __name__ == '__main__':
    res = Jwt.encode({'username': 'guoxiaonao'}, '198717', 2)
    print(Jwt.decode(res, '198717'), res)
