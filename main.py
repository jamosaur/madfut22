# This is a sample Python script.
import os
import re
import adbutils
import json

from utils import decrypt, xor_key, item_regex, encrypt, write_line


def generate_ids():
    with open("players.json") as json_data:
        data = json.load(json_data)
        json_data.close()

    for key in data:
        data[key] = 500

    return json.dumps(data).replace(" ", "")


def madfut():
    adb = adbutils.AdbClient(host="127.0.0.1", port=5037)

    devices = adb.device_list()

    if len(devices) == 0:
        print('No devices')
        quit()

    device = devices[0]

    print(f'Connected to {device}')
    device_user = device.shell('su -c stat -c "%U" /data/data/com.madfut.madfut22/shared_prefs/MainActivity.xml')

    if not os.path.exists('workdir'):
        os.mkdir('workdir')

    # Pull the file from the device
    contents = device.shell('su -c cat /data/data/com.madfut.madfut22/shared_prefs/MainActivity.xml')
    file = open('workdir/MainActivity.xml', 'w')
    file.write(str.encode(contents).decode('latin1'))
    file.close()

    # Decrypt the file!
    encrypted = open('workdir/MainActivity.xml', 'r')
    file = open('workdir/Decrypted.xml', 'w')
    for line in encrypted:
        if item_regex.match(line):
            matches = re.search(item_regex, line)
            key = decrypt(matches.group(1), xor_key)
            data = matches.group(2)

            new_line = "{0}{1}{2}{3}{4}\n".format(
                '    <string name="',
                key,
                '">',
                decrypt(data, xor_key),
                '</string>'
            )
            file.write(new_line)
        else:
            file.write(line)
    file.close()

    # Time to edit the decrypted file I guess.
    decrypted = open('workdir/Decrypted.xml', 'r')
    modified = open('workdir/Edited.xml', 'w')
    for line in decrypted:
        if item_regex.match(line):
            matches = re.search(item_regex, line)
            key = matches.group(1)
            data = matches.group(2)

            if key == 'coins':
                new_line = write_line('coins', '2000000000')
            elif key == 'ltmPoints':
                new_line = write_line('ltmPoints', '2000000000')
            elif key == 'ids':
                new_line = write_line('ids', generate_ids())
            else:
                new_line = write_line(key, data)

            modified.write(new_line)
        else:
            modified.write(line)
    modified.close()
    decrypted.close()

    # re-encrypt the file and push it back!
    modified = open('workdir/Edited.xml', 'r')
    encrypted = open('workdir/Encrypted.xml', 'w')
    for line in modified:
        if item_regex.match(line):
            matches = re.search(item_regex, line)
            key = matches.group(1)
            data = matches.group(2)

            new_line = write_line(
                key=encrypt(key, xor_key),
                value=encrypt(data, xor_key)
            )

            encrypted.write(new_line)
        else:
            encrypted.write(line)
    modified.close()
    encrypted.close()

    device.sync.push('workdir/Encrypted.xml', '/sdcard/Download/Encrypted.xml')
    device.shell(
        'su -c mv /sdcard/Download/Encrypted.xml /data/data/com.madfut.madfut22/shared_prefs/MainActivity.xml'
    )

    device.shell(
        'su -c chown '
        .join(device_user)
        .join(':')
        .join(device_user)
        .join(' /data/data/com.madfut.madfut22/shared_prefs/MainActivity.xml')
    )

    print('Completed!')


if __name__ == '__main__':
    madfut()

