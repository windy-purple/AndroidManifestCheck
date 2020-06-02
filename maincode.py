import binascii
import os
import sys

class checkcode:

    checkresult = {'headermagic':1,'stringchunktype':1,'resourcechunktype':1,'startnamespacechunktype':1,'starttagtype':1}
    flag = 1
    filename = ''

    def __init__(self,fn):
        self.filename = fn

    def check(self):
        f = open(self.filename,'rb',True)
        f.seek(0x00)
        headmagic = f.read(4)
        headmagic = binascii.b2a_hex(headmagic)
        headmagic = str(headmagic,encoding='utf-8')
        f.seek(0x08)
        stringchunktype = f.read(4)
        stringchunktype = binascii.b2a_hex(stringchunktype)
        stringchunktype = str(stringchunktype,encoding='utf-8')
        f.seek(0x0c)
        stringcount = f.read(4)
        resourceoffset = 0x08 + self.getAddress(stringcount)
        f.seek(resourceoffset)
        resourcechunktype = f.read(4)
        resourcechunktype = binascii.b2a_hex(resourcechunktype)
        resourcechunktype = str(resourcechunktype,encoding='utf-8')
        f.seek(resourceoffset + 0x04)
        resourcesize = f.read(4)
        resourcesize = self.getAddress(resourcesize)
        strartnameoffset = resourceoffset + resourcesize
        f.seek(strartnameoffset)
        startnamechunktype = f.read(4)
        startnamechunktype = binascii.b2a_hex(startnamechunktype)
        startnamechunktype = str(startnamechunktype,encoding='utf-8')
        f.seek(strartnameoffset + 0x04)
        startnamesize = f.read(4)
        startnamesize = self.getAddress(startnamesize)
        f.seek(strartnameoffset + startnamesize)
        starttagtype = f.read(4)
        starttagtype = binascii.b2a_hex(starttagtype)
        starttagtype = str(starttagtype,encoding='utf-8')
        if headmagic != '03000800':
            self.checkresult['headermagic'] = 0
            self.flag = 0
        if stringchunktype != '01001c00':
            self.checkresult['stringchunktype'] = 0
            self.flag = 0
        if resourcechunktype != '80010800':
            self.checkresult['resourcechunktype'] = 0
            self.flag = 0
        if startnamechunktype != '00011000':
            self.checkresult['startnamespacechunktype'] = 0
            self.flag = 0
        if starttagtype != '02011000':
            self.checkresult['starttagtype'] = 0
            self.flag = 0
        f.close()

    def correction(self):
        f = open(self.filename,'rb+',True)
        fdata = f.read()
        f.close()
        f = open(self.filename,'wb+',True)
        f.write(fdata)
        f.seek(0x0c)
        stringcount = f.read(4)
        resourceoffset = 0x08 + self.getAddress(stringcount)
        f.seek(resourceoffset + 0x04)
        resourcesize = f.read(4)
        resourcesize = self.getAddress(resourcesize)
        strartnameoffset = resourceoffset + resourcesize
        f.seek(strartnameoffset + 0x04)
        startnamesize = f.read(4)
        startnamesize = self.getAddress(startnamesize)
        starttagoffest = strartnameoffset + startnamesize
        if self.checkresult['headermagic'] == 0:
            f.seek(0x00)
            data = bytearray(b'\x03\x00\x08\x00')
            f.write(data)
        if self.checkresult['stringchunktype'] == 0:
            f.seek(0x08)
            data = bytearray(b'\x01\x00\x1c\x00')
            f.write(data)
            f.seek(0x20)
            data = bytearray(b'\x00\x00\x00\x00')
            f.write(data)
        if self.checkresult['resourcechunktype'] == 0:
            f.seek(resourceoffset)
            data = bytearray(b'\x80\x01\x08\x00')
            f.write(data)
        if self.checkresult['startnamespacechunktype'] == 0:
            f.seek(strartnameoffset)
            data = bytearray(b'\x00\x01\x10\x00')
            f.write(data)
        if self.checkresult['starttagtype'] == 0:
            f.seek(starttagoffest)
            data = bytearray(b'\x02\x01\x10\x00')
            f.write(data)
        f.close()


    def getAddress(self,addr):
        address = bytearray(addr)
        address.reverse()
        address = bytes(address)
        address = str(binascii.b2a_hex(address),encoding='UTF-8')
        address = int(address,16)
        return address