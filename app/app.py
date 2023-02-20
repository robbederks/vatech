#!/usr/bin/env python3

import time
import socket
import struct

IP = "192.168.1.80"
DEBUG = True

class Xmaru:
  class FlagOptn:
    def __init__(self, scan, intb, eoss, ag00, ag01, ag02, oeoe, fctl, sped):
      self.scan = scan
      self.intb = intb
      self.eoss = eoss
      self.ag00 = ag00
      self.ag01 = ag01
      self.ag02 = ag02
      self.oeoe = oeoe
      self.fctl = fctl
      self.sped = sped

    def __bytes__(self):
      # different order on the receive side
      return struct.pack("<BBBBBBBBB", self.fctl, self.intb, self.oeoe, self.scan, self.sped, self.eoss, self.ag00, self.ag01, self.ag02)

  class FlagFunc:
    def __init__(self, patn, elon, aexp, fx01, fx02, fx03, stvl, dark):
      self.patn = patn
      self.elon = elon
      self.aexp = aexp
      self.fx01 = fx01
      self.fx02 = fx02
      self.fx03 = fx03
      self.stvl = stvl
      self.dark = dark

    def __bytes__(self):
      return struct.pack("<BBBBBBBB", self.patn, self.elon, self.aexp, self.fx01, self.fx02, self.fx03, self.stvl, self.dark)

  DEFAULT_OPTN = FlagOptn(
    scan=1,
    intb=0,
    eoss=1,
    ag00=1,
    ag01=0,
    ag02=1,
    oeoe=0,
    fctl=1,
    sped=0
  )

  DEFAULT_FUNC = FlagFunc(
    patn=0,
    elon=0,
    aexp=0,
    fx01=1,
    fx02=1,
    fx03=0,
    stvl=0,
    dark=0
  )

  def __init__(self, ip):
    self.ip = ip
    self.ctrl_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.ctrl_socket.connect((self.ip, 20000))

    self.img_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.img_socket.connect((self.ip, 20001))
    DEBUG and print(f"Connected to {self.ip}")

  def __del__(self):
    self.ctrl_socket.close()
    self.img_socket.close()
    DEBUG and print("Disconnected")

  def _ctrl_msg(self, sect, cmd, data=b""):
    msg = struct.pack("<HH", cmd, sect) + data
    self.ctrl_socket.send(msg)
    return self.ctrl_socket.recv(0x84)

  def _get_img(self):
    self.img_socket.send(b"\x00")
    return self.img_socket.recv(0x8000)

  def cmd_aux_def_status(self):
    resp = self._ctrl_msg(1, 0)
    code = struct.unpack("<I", resp[:4])[0]
    msg = resp[4:].split(b'\x00', 1)[0].decode("utf-8")
    return code, msg

  def cmd_aux_led_status(self):
    resp = self._ctrl_msg(1, 1)
    code, status = struct.unpack("<II", resp[:8])
    return code, status

  def cmd_aux_fw_version(self):
    resp = self._ctrl_msg(1, 0x10)
    code = struct.unpack("<I", resp[:4])[0]
    version = resp[4:].split(b'\x00', 1)[0].decode("utf-8")
    return code, version

  def cmd_aux_fpga_version(self):
    resp = self._ctrl_msg(1, 0x11)
    code = struct.unpack("<I", resp[:4])[0]
    version = resp[4:].split(b'\x00', 1)[0].decode("utf-8")
    return code, version

  def cmd_aux_mainboard_version(self):
    resp = self._ctrl_msg(1, 0x12)
    code = struct.unpack("<I", resp[:4])[0]
    version = resp[4:].split(b'\x00', 1)[0].decode("utf-8")
    return code, version

  def cmd_aux_tft_version(self):
    resp = self._ctrl_msg(1, 0x13)
    code = struct.unpack("<I", resp[:4])[0]
    version = resp[4:].split(b'\x00', 1)[0].decode("utf-8")
    return code, version

  def cmd_aux_csi_version(self):
    resp = self._ctrl_msg(1, 0x14)
    code = struct.unpack("<I", resp[:4])[0]
    version = resp[4:].split(b'\x00', 1)[0].decode("utf-8")
    return code, version

  # TODO: 0x20, 0x21, 0x23

  def cmd_aux_self_xtst(self):
    resp = self._ctrl_msg(1, 0x24)
    code = struct.unpack("<I", resp[:4])[0]
    response = resp[4:].split(b'\x00', 1)[0].decode("utf-8")
    return code, response

  def cmd_aux_test_pattern(self):
    resp = self._ctrl_msg(1, 0x30)
    code = struct.unpack("<I", resp[:4])[0]
    response = resp[4:].split(b'\x00', 1)[0].decode("utf-8")
    return code, response

  def cmd_init(self, optn=DEFAULT_OPTN, func=DEFAULT_FUNC):
    resp = self._ctrl_msg(0, 1, bytes(optn) + bytes(func))
    code = struct.unpack("<I", resp[:4])[0]
    resp2 = self.ctrl_socket.recv(0x84)
    return code, resp2

  def cmd_start(self):
    resp = self._ctrl_msg(0, 2)
    code = struct.unpack("<I", resp[:4])[0]
    resp2 = self.ctrl_socket.recv(0x84)
    return code, resp2

  def cmd_abort(self):
    resp = self._ctrl_msg(0, 3)
    code = struct.unpack("<I", resp[:4])[0]
    resp2 = self.ctrl_socket.recv(0x84)
    return code, resp2

  def cmd_msg_data_done(self):
    resp = self._ctrl_msg(0, 0xFF)
    code = struct.unpack("<I", resp[:4])[0]
    return code


if __name__ == "__main__":
  x = Xmaru(IP)
  # print(x.cmd_aux_def_status())
  # print(x.cmd_aux_led_status())
  # print(x.cmd_aux_fw_version())
  # print(x.cmd_aux_fpga_version())
  # print(x.cmd_aux_mainboard_version())
  # print(x.cmd_aux_tft_version())
  # print(x.cmd_aux_csi_version())
  print(x.cmd_init())
  print(x.cmd_msg_data_done())
  print(x.cmd_start())
  # print(x.cmd_abort())
  # time.sleep(1)
  print(x.cmd_aux_self_xtst())
  print(x.cmd_aux_test_pattern())
  print(x._get_img())