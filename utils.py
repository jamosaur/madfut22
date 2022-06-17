import base64
import re


def xor(data, xorkey):
    d = []
    for i in range(len(data)):
        d.append(chr(data[i % len(data)] ^ xorkey[i % len(xorkey)]))
    return ''.join(d)


xor_key = bytearray([0x46, 0x64, 0x4b])


def encrypt(data, xorkey):
    return base64.b64encode(
        str.encode(
            xor(
                str.encode(data),
                xorkey
            ),
            'latin1'
        )
    ).decode()


def decrypt(data, xorkey):
    # convert from latin1
    encoded_base64 = u''.join(data).encode()
    base64_decoded = base64.b64decode(encoded_base64)
    decoded_xor = xor(base64_decoded, xorkey)
    decoded_string = bytes(decoded_xor, 'latin1')
    return decoded_string.decode('latin1')


def write_line(key, value):
    return "{0}{1}{2}{3}{4}\n".format(
        '    <string name="',
        key,
        '">',
        value,
        '</string>'
    )


item_regex = re.compile(r'\s*<string\s+name="([^"]+)">([^<]+)</string>')

