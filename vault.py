#!/usr/bin/env python3

"""
    This program is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
"""

# requires pycrypto

import signal
import sys
import time
import base64
from getpass import getpass
from Crypto.Cipher import AES
from Crypto import Random
from Crypto.Hash import RIPEMD

BS = 16
b2a = base64.b64encode
a2b = base64.b64decode

loadedlines = []

def getkey():
    # should i use PBKDF2 instead?
    key = getpass("  key[masked]: ")
    h = RIPEMD.new()
    h.update(key)
    return h.digest()[0:BS]

def confirmkey():
    key = getkey()
    while True:
        print('   again to confirm')
        key2 = getkey()
        if(key == key2):
            break
    return key

def getmessage():
    msg = getpass("  msg[masked]: ")
    if(input(' Show message? y/n: ') == 'y'):
        burn(msg)
    if(len(msg) % BS == 0):
        return msg
    msg = msg.ljust((int(len(msg) / BS) + 1) * BS)
    return msg

def encrypt(iv,plain):
    key = confirmkey()
    aes = AES.new(key, AES.MODE_CBC, iv)
    cipher = aes.encrypt(plain)
    plain = ''
    return cipher

def decrypt(iv,cipher):
    key = getkey()
    aes = AES.new(key, AES.MODE_CBC, iv)
    plain = aes.decrypt(cipher)
    return plain

def show(line_num):
    try:
        line = loadedlines[line_num].split(':')
        entry = line[0]
        raw = a2b(line[1])
        iv = raw[0:BS]
        cipher = raw[BS:len(raw)]
        plain = decrypt(iv,cipher).decode('utf-8').strip()
        burn(plain)
        plain=''
    except Exception:
        print('Nope!')

def burn(text):
    sleep = int(input('   seconds to show (0 forever): '))
    length = len(text)
    print('    ' + text,end='')
    text = ''
    sys.stdout.flush()
    if(sleep > 0):
        while sleep > 0:
            print('\r' + str(sleep).ljust(4),end='')
            time.sleep(1)
            sleep -= 1
        print('\r    ' + ''.join('x' for i in range(length)))
    else:
        print('')

def load(filename,silent=False):
    global loadedlines
    loadedlines = []
    with open(filename, 'r') as file:
        loadedlines = file.readlines()
    count = 0
    if(not silent):
        for x in loadedlines:
            entry = x.split(':')[0]
            print('  ' + str(count) + ' ' + entry)
            count += 1

def write(filename):
    with open(filename, 'a') as file:
        while True:
            entry = input(" New entry: ")
            if(entry == ''):
                print('Bye')
                break;

            iv = Random.new().read(BS)
            msg = getmessage()
            cipher = encrypt(iv,msg)

            file.write(entry + ':' + b2a(iv + cipher).decode('utf-8') + '\n')
            file.flush()

def signal_handler(signal, frame):
    print('\nBye')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

if __name__ == "__main__":
    if(len(sys.argv) < 3):
        print('Usage: vault [add|load] <filename>')
    else:
        cmd = sys.argv[1]
        param = sys.argv[2]
        if(cmd == 'add'):
            write(param)
        elif(cmd == 'load'):
            try:
                load(param)
                while True:
                    line = input('Show which line?: ')
                    if(line == ''):
                        print('Bye')
                        break
                    show(int(line))
            except IOError:
                print("file '"+param+"' not found")
        else:
            print("unknown command '" + cmd + "'")
