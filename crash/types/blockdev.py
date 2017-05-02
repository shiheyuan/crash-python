# -*- coding: utf-8 -*-
# vim:set shiftwidth=4 softtabstop=4 expandtab textwidth=79:

from __future__ import absolute_import
from __future__ import print_function
from __future__ import division

import gdb
import sys
from crash.infra import CrashBaseClass, export, delayed_init
from crash.types.classdev import for_each_class_device
from crash.util import container_of, get_symbol_value

if sys.version_info.major >= 3:
    long = int

@delayed_init
class BlockDeviceClass(CrashBaseClass):
    def __init__(self):
        self.block_class = gdb.lookup_global_symbol("block_class").value()
        self.gendisk_type = gdb.lookup_type('struct gendisk')
        self.hd_struct_type = gdb.lookup_type('struct hd_struct')
        self.device_type = gdb.lookup_type('struct device')
        self.device_type_type = gdb.lookup_type('struct device_type')
        self.bdev_inode_type = gdb.lookup_type('struct bdev_inode')
        self.disk_type = get_symbol_value('disk_type')
        self.part_type = get_symbol_value('part_type')
        self.blockdev_superblock = gdb.lookup_global_symbol('blockdev_superblock').value()
        if self.disk_type.type != self.device_type_type:
            raise TypeError("disk_type expected to be {} not {}"
                            .format(self.device_type_type,
                                    self.disk_type.type))
        self.device_type_type = self.disk_type.type
        if self.part_type.type != self.device_type_type:
            raise TypeError("part_type expected to be {} not {}"
                            .format(self.device_type_type,
                                    self.disk_type.type))

    @export
    def dev_to_gendisk(self, dev):
        return container_of(dev, self.gendisk_type, 'part0.__dev')

    @export
    def dev_to_part(self, dev):
        return container_of(dev, self.hd_struct_type, '__dev')

    @export
    def gendisk_to_dev(self, gendisk):
        return gendisk['part0']['__dev'].address

    @export
    def part_to_dev(self, part):
        return part['__dev'].address

    @export
    def for_each_block_device(self, subtype=None):
        if subtype:
            if subtype.type == self.device_type_type:
                subtype = subtype.address
            elif subtype.type != self.device_type_type.pointer():
                raise TypeError("subtype must be {} not {}"
                                .format(self.device_type_type.pointer(),
                                        subtype.type))
        for dev in for_each_class_device(self.block_class, subtype):
            if dev['type'] == self.disk_type.address:
                yield self.dev_to_gendisk(dev)
            elif dev['type'] == self.part_type.address:
                yield self.dev_to_part(dev)
            else:
                raise RuntimeError("Encountered unexpected device type {}"
                                   .format(dev['type']))

    @export
    def for_each_disk(self):
        return self.for_each_block_device(self.disk_type)

    @export
    def gendisk_name(self, gendisk):
        if gendisk.type.code == gdb.TYPE_CODE_PTR:
            gendisk = gendisk.dereference()

        if gendisk.type == self.gendisk_type:
            return gendisk['disk_name'].string()
        elif gendisk.type == self.hd_struct_type:
            parent = self.dev_to_gendisk(self.part_to_dev(gendisk)['parent'])
            return "{}{:d}".format(self.gendisk_name(parent),
                                   int(gendisk['partno']))
        else:
            raise TypeError("expected {} or {}, not {}"
                            .format(self.gendisk_type, self.hd_struct_type,
                            gendisk.type))

    @export
    def block_device_name(self, bdev):
        return self.gendisk_name(bdev['bd_disk'])

    @export
    def is_bdev_inode(self, inode):
        return inode['i_sb'] == self.blockdev_superblock

    @export
    def inode_to_block_device(self, inode):
        if inode['i_sb'] != self.blockdev_superblock:
            raise TypeError("inode does not correspond to block device")
        return container_of(inode, self.bdev_inode_type, 'vfs_inode')['bdev']

    @export
    def inode_on_bdev(self, inode):
        if self.is_bdev_inode(inode):
            return self.inode_to_block_device(inode)
        else:
            return inode['i_sb']['s_bdev']