# TO USE: launch ZC, launch this and close ZC, launch ZC when prompted

import netifaces
import requests
import socket
import binascii
import time
from _thread import *
from multiprocessing import Queue
import sys

addrs = netifaces.ifaddresses('en0')
addr = addrs[2]

ipv4 = addr[0]['addr']
port = 21587

bearer = 'eyJhbGciOiJSUzI1NiIsInR5cCIgOiAiSldUIiwia2lkIiA6ICJPLUVjXzJJNjg5bW9peGJIZzFfNDZDVFlGeEdZMDViaDluYm5Mcjl0RzY4In0.eyJqdGkiOiIwYWU1YWM0ZS1mZGU2LTQyMzYtYTIwOS1jYWYyMzhmYTFiM2MiLCJleHAiOjE1NTI5MDAyMzgsIm5iZiI6MCwiaWF0IjoxNTUyODc4NjM4LCJpc3MiOiJodHRwczovL3NlY3VyZS56d2lmdC5jb20vYXV0aC9yZWFsbXMvendpZnQiLCJhdWQiOiJad2lmdF9Nb2JpbGVfTGluayIsInN1YiI6IjEzYzM0MTUwLTVhNmQtNGYyYi05ZmQ1LThlYTc2NzgxYmVkMSIsInR5cCI6IkJlYXJlciIsImF6cCI6Ilp3aWZ0X01vYmlsZV9MaW5rIiwiYXV0aF90aW1lIjowLCJzZXNzaW9uX3N0YXRlIjoiMGY3ZGJjOTMtODE5OS00Mjk0LWJiNmEtYWFhZGNhOTI4MmU1IiwiYWNyIjoiMSIsImFsbG93ZWQtb3JpZ2lucyI6W10sInJlYWxtX2FjY2VzcyI6eyJyb2xlcyI6WyJldmVyeWJvZHkiLCJ0cmlhbC1zdWJzY3JpYmVyIiwiZXZlcnlvbmUiLCJiZXRhLXRlc3RlciJdfSwicmVzb3VyY2VfYWNjZXNzIjp7Im15LXp3aWZ0Ijp7InJvbGVzIjpbImF1dGhlbnRpY2F0ZWQtdXNlciJdfSwiR2FtZV9MYXVuY2hlciI6eyJyb2xlcyI6WyJhdXRoZW50aWNhdGVkLXVzZXIiXX0sInNzby1nYXRld2F5Ijp7InJvbGVzIjpbImF1dGhlbnRpY2F0ZWQtdXNlciJdfSwiWndpZnQgUkVTVCBBUEkgLS0gcHJvZHVjdGlvbiI6eyJyb2xlcyI6WyJhdXRob3JpemVkLXBsYXllciIsImF1dGhlbnRpY2F0ZWQtdXNlciJdfSwiWndpZnQgWmVuZGVzayI6eyJyb2xlcyI6WyJhdXRoZW50aWNhdGVkLXVzZXIiXX0sIlp3aWZ0IFJlbGF5IFJFU1QgQVBJIC0tIHByb2R1Y3Rpb24iOnsicm9sZXMiOlsiYXV0aG9yaXplZC1wbGF5ZXIiXX0sImVjb20tc2VydmVyIjp7InJvbGVzIjpbImF1dGhlbnRpY2F0ZWQtdXNlciJdfSwiYWNjb3VudCI6eyJyb2xlcyI6WyJtYW5hZ2UtYWNjb3VudCIsIm1hbmFnZS1hY2NvdW50LWxpbmtzIiwidmlldy1wcm9maWxlIl19fSwibmFtZSI6IlRyZXZvciBBbGZzdGFkIiwicHJlZmVycmVkX3VzZXJuYW1lIjoidHJldm9yYWxmc3RhZEBnbWFpbC5jb20iLCJnaXZlbl9uYW1lIjoiVHJldm9yIiwiZmFtaWx5X25hbWUiOiJBbGZzdGFkIiwiZW1haWwiOiJ0cmV2b3JhbGZzdGFkQGdtYWlsLmNvbSJ9.A_iExeTSUbxyzpkMkTjEj4Ou01oa5VCtljJRby2CUuu_yooQXG24s0It4gz9bboCxAnB7Tgg5lJPAVhNTDY5uTxFUdDnHkFX5n7dwD4AJ5fTAAr5rrKkyNSRtC4Q1tiNRpgol1HsMFiboGT7ypSklTl-FVMD3h6vQcc-jkm4icw80ieeWPXYf8nNxSA5FCkB1T1N7YWB776mT-YLI1kF9wvHrleExYKXutbKtsiltl1rw01IxIH3Ku2fMCwTo6ylqZD6LUrnKMBw1MGrI3pkvEWf5D42t5OGy9KeoQJ1n9_xboOpOhpqVcjn0tP4zpL0TJTfxULGmrXHG2oD1MIbIA'

url = "https://us-or-rly101.zwift.com/relay/profiles/me/phone"

headers = {
    'Authorization': 'Bearer %s' % (bearer),
}

payload = {
    "protocol": "TCP",
    "mobileEnvironment": {
        "systemHardware": "iPhone11,6",
        "appBuild": 565,
        "systemOSVersion": "12.1.2",
        "appVersion": "3.1.3",
        "systemOS": "iOS",
        "appDisplayName": "Companion"
    },
    "phoneAddress": ipv4,
    "port": port
}

print('# Getting the Actual Zwift Companion IP')
actualZC = requests.get(url=url, headers=headers).json()
zc_ip = actualZC['phoneAddress']
ZC_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ZC_ServerAddress = (zc_ip, port)
print(zc_ip)

if zc_ip == ipv4:
    print('ZC cant be this computer')
    sys.exit()

print('# Telling Zwift we are the ZC. Should return 204')
resp = requests.put(url=url, json=payload, headers=headers)
print(resp)

print('# Creating a fake Zwift Companion. Make sure to have Zwift running on another device')
# open socket on port and read raw bytes in
ZwiftApp_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ZwiftApp_Socket.bind(('0.0.0.0', port))
ZwiftApp_Socket.listen(1)
conn, addr = ZwiftApp_Socket.accept()



def ZCForwarder(connZC, connZA):
    while True:
        try:
            data = connZC.recv(2)
            msgLength = int.from_bytes(data, byteorder='big')
            msg = connZC.recv(msgLength)

            print("Got Message From Zwift Companion:")
            print(msg)

            ba = bytearray(data)
            ba += bytearray(msg)
            # send this data to ZA
            connZA.sendall(ba)
        except Exception as e:
            print(e)


#
#
#
not_connected = True
while True:
    try:
        data = conn.recv(2)
        msgLength = int.from_bytes(data, byteorder='big')
        msg = conn.recv(msgLength)

        while not_connected:
            try:
                print('connecting to', ZC_ServerAddress)
                ZC_Socket.connect(ZC_ServerAddress)
                not_connected = False
                print('>>> Starting ZCForwarder')
                start_new_thread(ZCForwarder, (ZC_Socket, conn))
            except Exception as e:
                print(e)
                ZC_Socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                print('ZC not connected. Please open your Zwift Companion App now')
                time.sleep(5)

        print("Got Message From Zwift App:")
        print(msg)

        ba = bytearray(data)
        ba += bytearray(msg)
        # send this data to ZC
        ZC_Socket.sendall(ba)
    except Exception as e:
        print(e)

conn.close()
