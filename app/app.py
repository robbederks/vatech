#!/usr/bin/env python3

import time
import socket
import struct

IP = "192.168.1.80"
PORT = 20000

DATA_LEN = 0x84

if __name__ == "__main__":
  with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s2:
      s.connect((IP, PORT))
      s2.connect((IP, PORT + 1))

      sect = 1
      cmd = 0x10
      data = struct.pack("<HH", cmd, sect)
      # data = struct.pack("<HH", sect, cmd)
      print(data)
      data += b"\x00" * (DATA_LEN - len(data))

      print(len(data))

      s.send(data)
      print('sent')
      print(s.recv(DATA_LEN))

      s2.send(data)
      print('sent 2')