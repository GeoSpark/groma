#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module:: totalstations
    :platform: Linux, Windows
    :synopsis: Total station file loader

.. moduleauthor::Zoltan Siki <siki@agt.bme.hu>
"""
import math
import re

# noinspection PyUnresolvedReferences
from qgis.core import QgsMessageLog, Qgis
from . import config
from .base_classes import Angle, FOOT2M, ANGLE_UNITS_STORE


class TotalStation(object):
    """ Base class to load different total station data format
    """

    def __init__(self, fname, separator):
        """ Initialize a new instance

            :param fname: input file name (string)
            :param separator: field separator in input (string/regexp)
        """
        self.fname = fname
        if separator is not None:
            self.separator = re.compile(separator)
        else:
            self.separator = None
        self.fp = None

    def open(self):
        """ Open data set

            :returns: 0 on success/1 on failure
        """
        if self.fp is None:
            try:
                self.fp = open(self.fname, 'r')
            except IOError:
                self.fp = None
                return -1
        return 0

    def close(self):
        """ Close dataset
        """
        if self.fp is not None:
            try:
                self.fp.close()
            except IOError:
                pass
            self.fp = None

    def get_line(self):
        """ Read & split a single line
        """
        buf = self.fp.readline()
        if buf == '':
            # end of file
            return None
        if self.separator is not None:
            return self.separator.split(buf.strip('\r\n'))
        return buf.strip('\r\n')

    @staticmethod
    def trim_left(s, ch):
        """ Strip left part of a string

            :param s: string to left trim
            :param ch: character to trim
            :returns: left trimmed string
        """
        s = re.sub('^' + ch + '+', '', s)
        if len(s) == 0:
            s = ch
        return s

    def parse_next(self):
        """ Parse one line/logical unit of input, implemented in derived classes
        """
        raise NotImplementedError


class LeicaGsi(TotalStation):
    """ Class to read leica GSI 8/16 data
    """

    def __init__(self, fname, separator=' '):
        """ Initialize a new instance

            :param fname: file name to open (str)
            :param separator: field separator (str)
        """
        super(LeicaGsi, self).__init__(fname, separator)

    @staticmethod
    def convert(val, unit):
        """ Convert angle to radian, distance to meter

            :param val: value to convert (float)
            :param unit: unit & decimals (int)
            :returns: converted value (float)
        """
        res = None
        if unit == 0:
            # meter, 3 decimals
            res = val / 1000.0
        elif unit == 1:
            # feet, 3 decimals
            res = val / 1000.0 * FOOT2M
        elif unit == 2:
            # gon
            res = Angle(val / 100000.0, 'GON').get_angle(ANGLE_UNITS_STORE[config.angle_stored])
        elif unit == 3:
            # DEG
            res = Angle(val / 10000.0, 'DEG').get_angle(ANGLE_UNITS_STORE[config.angle_stored])
        elif unit == 4:
            # DMS
            res = Angle(val / 100000.0, 'PDEG').get_angle(ANGLE_UNITS_STORE[config.angle_stored])
        elif unit == 5:
            # mil
            res = val / 6400.0 * math.pi * 2
        elif unit == 6:
            # meter, 4 decimals
            res = val / 10000.0
        elif unit == 7:
            # feet, 4 decimals
            res = val / 1000.0 * 0.3048
        elif unit == 8:
            # meter, 5 decimals
            res = val / 100000.0
        return res

    def parse_next(self):
        """ Parse single line from input

            :returns: list of values
        """
        if self.fp is None:
            return None
        res = {}
        buf = self.get_line()
        if buf is None:
            return None
        if len(buf) == 0:
            return {}
        if buf[0][0] == '*':
            buf[0] = buf[0].strip('*')
        for i, val in enumerate(buf):
            item_code = val[0:2]
            if item_code == '11':
                res['point_id'] = self.trim_left(val[7:], '0')
            elif item_code == '21':
                # horizontal angle
                res['hz'] = self.convert(float(self.trim_left(val[7:], '0')), int(val[5]))
                res['station'] = None
            elif item_code == '22':
                # vertical angle
                res['v'] = self.convert(float(self.trim_left(val[7:], '0')), int(val[5]))
                res['station'] = None
            elif item_code == '31':
                # slope distance
                res['sd'] = self.convert(float(self.trim_left(val[7:], '0')), int(val[5]))
                res['station'] = None
            elif item_code == '32':
                # horizontal distance
                res['hd'] = self.convert(float(self.trim_left(val[7:], '0')), int(val[5]))
                res['station'] = None
            elif item_code == '33':
                # vertical distance
                res['vd'] = self.convert(float(self.trim_left(val[7:], '0')), int(val[5]))
                res['station'] = None
            elif item_code == '41':
                # new station
                pass
            elif item_code == '42':
                # station number
                res['point_id'] = self.trim_left(val[7:], '0')
                res['station'] = 'station'
            elif item_code == '43':
                # instument height
                res['ih'] = self.convert(float(self.trim_left(val[7:], '0')), 0)
            elif item_code == '71':
                # code (first remark)
                res['code'] = self.trim_left(val[7:], '0')
            elif item_code == '81':
                # easting
                res['e'] = self.convert(float(self.trim_left(val[7:], '0')), int(val[5]))
            elif item_code == '82':
                # northing
                res['n'] = self.convert(float(self.trim_left(val[7:], '0')), int(val[5]))
            elif item_code == '83':
                # elevation
                res['z'] = self.convert(float(self.trim_left(val[7:], '0')), int(val[5]))
            elif item_code == '84':
                # station easting
                res['station_e'] = self.convert(float(self.trim_left(val[7:], '0')), int(val[5]))
                res['station'] = 'station'
            elif item_code == '85':
                # station northing
                res['station_n'] = self.convert(float(self.trim_left(val[7:], '0')), int(val[5]))
                res['station'] = 'station'
            elif item_code == '86':
                # station elevation
                res['station_z'] = self.convert(float(self.trim_left(val[7:], '0')), int(val[5]))
                res['station'] = 'station'
            elif item_code == '87':
                # reflector height
                res['th'] = self.convert(float(self.trim_left(val[7:], '0')), int(val[5]))
            elif item_code == '88':
                # station height
                res['ih'] = self.convert(float(self.trim_left(val[7:], '0')), int(val[5]))
                res['station'] = 'station'
        return res


class JobAre(TotalStation):
    """ Class to import JOB/ARE data from file
    """

    def __init__(self, fname, separator='='):
        """ Initialize a new instance

            :param fname: file name to open (str)
            :param separator: field separator (str)
        """
        super(JobAre, self).__init__(fname, separator)
        self.angle_unit = 'PDEG'
        self.distance_unit = 'm'
        self.res = {}

    def dist_conv(self, dist):
        """ Convert distance/coordinate to meter using distance_unit

            :param dist: value to convert
            :returns: distance in meters
        """
        if self.distance_unit == 'f':
            return dist * FOOT2M
        else:
            return dist

    def parse_next(self):
        """ Parse an observation/station from input

            :returns: list of observation data
        """
        if self.fp is None:
            return None
        while True:
            buf = self.get_line()
            if buf is None:
                ret = self.res
                self.res = {}
                if len(ret) > 0:
                    return ret
                else:
                    return None
            if len(buf) < 2:
                continue
            item_code = buf[0].strip()
            if item_code == '2':
                ret = self.res
                self.res = {'point_id': buf[1].strip(), 'station': 'station'}
                # station point id
                if len(ret):
                    return ret
            elif item_code == '3':
                # instrument height
                self.res['th'] = self.dist_conv(float(buf[1].strip()))
            elif item_code == '4':
                # point code
                self.res['code'] = buf[1].strip()
            elif item_code == '5' or item_code == '62':
                ret = self.res
                self.res = {'point_id': buf[1].strip()}
                # target point id
                if len(ret):
                    return ret
            elif item_code == '6':
                # target height
                self.res['th'] = self.dist_conv(float(buf[1].strip()))
            elif item_code == '7' or item_code == '21':
                # horizontal angle
                self.res['hz'] = Angle(float(buf[1]), self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
                self.res['station'] = None
            elif item_code == '8':
                # zenit angle
                self.res['v'] = Angle(float(buf[1]), self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
                self.res['station'] = None
            elif item_code == '9':
                # slope distance
                self.res['sd'] = self.dist_conv(float(buf[1].strip()))
                self.res['station'] = None
            elif item_code == '10':
                # vertical distance
                self.res['vd'] = self.dist_conv(float(buf[1].strip()))
            elif item_code == '11':
                # horizontal distance stored as slope
                self.res['sd'] = self.dist_conv(float(buf[1].strip()))
                self.res['v'] = Angle(90, 'DEG').get_angle(ANGLE_UNITS_STORE[config.angle_stored])
            elif item_code == '23':
                # units
                self.angle_unit = {'1': 'GON', '2': 'DMS', '3': 'DEG', '4': 'MIL'}[buf[3]]
                self.distance_unit = {'1': 'm', '2': 'f'}[buf[2:3]]
            elif item_code == '37':
                # northing
                self.res['station_n'] = self.dist_conv(float(buf[1].strip()))
            elif item_code == '38':
                # easting
                self.res['station_e'] = self.dist_conv(float(buf[1].strip()))
            elif item_code == '39':
                # elevation
                self.res['station_z'] = self.dist_conv(float(buf[1].strip()))


class Sdr(TotalStation):
    """ Class to import Sokkia field books
    """

    def __init__(self, fname, separator=None):
        """ Initialize a new instance

            :param fname: input file name (string)
            :param separator: field separator in input (string/regexp)
        """
        super(Sdr, self).__init__(fname, separator)
        self.angle_unit = 'DEG'  # 1-DEG, 2-GON, 3-MIL
        self.distance_unit = 1  # 1-meter, 2-feet
        self.coord_order = 2  # 1-North, East, 2-East, North
        self.angle_dir = 1  # 1-Clockwise, 2-Counter clockwise
        self.pn_length = 4  # point id length (default srd20)
        self.th = None  # default target height

    def dist(self, value):
        """ Change distance to meters

            :param value: value to convert
            :returns: distance in meters
        """

        if self.distance_unit == 2:
            return value * FOOT2M
        return value

    def angle(self, value):
        """ Convert angle to Gon

            :param value: angle to convert
            :returns: angle in Gon
        """
        return Angle(value, self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])

    def pn(self, pbuf):
        """ Get point id from input buffer removing leading zeros

            :param pbuf: input buffer
            :returns: point id
        """
        p = pbuf[0:self.pn_length].strip()
        while p[0] == '0' and len(p) > 0:
            p = p[1:]
        return p

    def parse_next(self):
        """ Load next observation, station

            :returns: observation data
        """
        res = {}
        while True:
            buf = self.get_line()
            if buf is None:
                return None
            line_code = buf[0:2]
            if line_code == '00':
                # header
                if buf[4:9] == 'SDR33':
                    self.pn_length = 16
                elif buf[4:9] == 'SDR20':
                    self.pn_length = 4
                else:
                    return None
                w = int(buf[40:41])
                if w == 1:
                    self.angle_unit = 'DEG'
                elif w == 2:
                    self.angle_unit = 'GON'
                elif w == 3:
                    self.angle_unit = 'MIL'
                self.distance_unit = int(buf[41:42])
                self.coord_order = int(buf[44:45])
                self.angle_dir = int(buf[45:46])
            elif line_code == '02':
                # station record
                res['point_id'] = self.pn(buf[4:])
                if self.pn_length == 16:
                    w = buf[20:36].strip()
                    if len(w):
                        res['station_e'] = self.dist(float(w))
                    w = buf[36:52].strip()
                    if len(w):
                        res['station_n'] = self.dist(float(w))
                    w = buf[52:68].strip()
                    if len(w):
                        res['station_z'] = self.dist(float(w))
                    res['th'] = self.dist(float(buf[68:84].strip()))
                    res['pc'] = buf[84:90].strip()
                else:
                    w = buf[8:18].strip()
                    if len(w):
                        res['station_e'] = self.dist(float(w))
                    w = buf[18:28].strip()
                    if len(w):
                        res['station_n'] = self.dist(float(w))
                    w = buf[28:38].strip()
                    if len(w):
                        res['station_z'] = self.dist(float(w))
                    res['th'] = self.dist(float(buf[38:48].strip()))
                    res['pc'] = buf[48:64].strip()
                if self.coord_order == 1:
                    try:
                        res['station_e'], res['station_n'] = \
                            res['station_n'], res['station_e']
                    except KeyError:
                        pass
                res['station'] = 'station'
                return res
            elif line_code == '03':
                # target height
                self.th = float(self.dist(buf[4:].strip()))
            elif line_code == '07':
                # orientation
                pass
            elif line_code == '08':
                # coordinate
                res['point_id'] = self.pn(buf[4:])
                if self.pn_length == 16:
                    w = buf[20:36].strip()
                    if len(w):
                        res['station_e'] = self.dist(float(w))
                    w = buf[36:52].strip()
                    if len(w):
                        res['station_n'] = self.dist(float(w))
                    w = buf[52:68].strip()
                    if len(w):
                        res['station_z'] = self.dist(float(w))
                    res['pc'] = buf[68:84].strip()
                else:
                    w = buf[8:18].strip()
                    if len(w):
                        res['station_e'] = self.dist(float(w))
                    w = buf[18:28].strip()
                    if len(w):
                        res['station_n'] = self.dist(float(w))
                    w = buf[28:38].strip()
                    if len(w):
                        res['station_z'] = self.dist(float(w))
                    res['pc'] = buf[38:54].strip()
                if self.coord_order == 1:
                    try:
                        res['station_e'], res['station_n'] = \
                            res['station_n'], res['station_e']
                    except KeyError:
                        pass
                return res
            elif line_code == '09':
                # observation
                if buf[2:4] == 'F1' or buf[2:4] == 'MD':
                    # face left only
                    if self.pn_length == 16:
                        res['point_id'] = self.pn(buf[20:])
                        w = buf[36:52].strip()
                        if len(w):
                            res['sd'] = self.dist(float(w))
                        res['v'] = self.angle(float(buf[52:68].strip()))
                        res['hz'] = self.angle(float(buf[68:84].strip()))
                        res['pc'] = buf[84:100].strip()
                    else:
                        res['point_id'] = self.pn(buf[8:])
                        w = buf[12:22].strip()
                        if len(w):
                            res['sd'] = self.dist(float(w))
                        res['v'] = self.angle(float(buf[22:32].strip()))
                        res['hz'] = self.angle(float(buf[32:42].strip()))
                        res['pc'] = buf[42:58].strip()
                    if self.th is not None:
                        res['th'] = self.th
                    res['station'] = None
                    return res


class SurvCE(TotalStation):
    """ Class to import SurvCE rw5 files
    """

    def __init__(self, fname, separator=','):
        """ Initialize a new instance

            :param fname: input file name (string)
            :param separator: field separator in input (string/regexp)
        """
        super(SurvCE, self).__init__(fname, separator)
        self.angle_unit = 'PDEG'
        self.distance_unit = 1  # 0-feet 1-meter
        self.res = {}
        self.ih = None  # instrument height
        self.th = None  # target height
        self.dist_mul = 1.0  # distance convert constant to meter

    def parse_next(self):
        """ Load next observation, station

            :returns: observation data
        """
        self.res = {}
        if self.fp is None:
            return None
        while True:
            buf = self.get_line()
            if buf is None:
                return None
            line_code = buf[0]
            if line_code == 'GPS':  # log, lan
                for field in buf[1:]:
                    fcode = field[0:2]
                    if fcode == 'PN':
                        self.res['point_id'] = field[2:].strip()
                    elif fcode == 'LA':
                        self.res['n'] = float(field[2:].strip())
                    elif fcode == 'LN':
                        self.res['e'] = float(field[2:].strip())
                    elif fcode == 'EL':
                        self.res['z'] = float(field[2:].strip())
                    elif fcode == '--':
                        self.res['pc'] = field[2:].strip()
                return self.res
            elif line_code == '--GS' or line_code == 'SP':
                # projected coordinates overwrite lot,lan!
                for field in buf[1:]:
                    fcode = field[0:2]
                    if fcode == 'PN':
                        self.res['point_id'] = field[2:].strip()
                    elif fcode == 'N ':
                        self.res['n'] = float(field[2:].strip())
                    elif fcode == 'E ':
                        self.res['e'] = float(field[2:].strip())
                    elif fcode == 'EL':
                        self.res['z'] = float(field[2:].strip())
                    elif fcode == '--':
                        self.res['pc'] = field[2:].strip()
                return self.res
            elif line_code in ('TR', 'SS', 'BD', 'BR', 'FD', 'FR'):
                self.res['station'] = None
                for field in buf[1:]:
                    fcode = field[0:2]
                    if fcode == 'OP':
                        pass
                    elif fcode == 'FP':
                        self.res['point_id'] = field[2:].strip()
                    elif fcode == 'AL':
                        self.res['hz'] = 400 - Angle(float(field[2:].strip()),
                                                     self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
                    elif fcode == 'AR':
                        self.res['hz'] = Angle(float(field[2:].strip()),
                                               self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
                    elif fcode == 'ZE':
                        self.res['v'] = Angle(float(field[2:].strip()),
                                              self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
                    elif fcode == 'VA':
                        self.res['hz'] = 100 - Angle(float(field[2:].strip()),
                                                     self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
                    elif fcode == 'SD':
                        self.res['sd'] = float(field[2:].strip()) * self.dist_mul
                    elif fcode == '--':
                        self.res['pc'] = field[2:].strip()
                    # AZ/BR/DR/DL/CE/HD ignored
                if self.th is not None:
                    self.res['th'] = self.th
                return self.res
            elif line_code == 'OC':
                self.res['station'] = 'station'
                for field in buf[1:]:
                    fcode = field[0:2]
                    if fcode == 'OP':
                        self.res['point_id'] = field[2:].strip()
                    elif fcode == 'N ':
                        self.res['n'] = float(field[2:].strip())
                    elif fcode == 'E ':
                        self.res['e'] = float(field[2:].strip())
                    elif fcode == 'EL':
                        self.res['z'] = float(field[2:].strip())
                    elif fcode == '--':
                        self.res['pc'] = field[2:].strip()
                if self.ih is not None:
                    self.res['th'] = self.ih
                return self.res
            elif line_code == 'BK':
                self.res['station'] = None
                for field in buf[1:]:
                    fcode = field[0:2]
                    if fcode == 'OP':
                        pass
                    elif fcode == 'BP':
                        self.res['point_id'] = field[2:].strip()
                    elif fcode == 'BS':
                        self.res['hz'] = Angle(float(field[2:].strip()),
                                               self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
                    # BC ignored
                return self.res
            elif line_code == 'LS':
                for field in buf[1:]:
                    fcode = field[0:2]
                    if fcode == 'HI':
                        self.ih = float(field[2:].strip())
                    elif fcode == 'HR':
                        self.th = float(field[2:].strip())
            elif line_code == 'MO':
                for field in buf[1:]:
                    fcode = field[0:2]
                    if fcode == 'UN':
                        if int(field[2:].strip()) == 0:
                            self.dist_mul = 0.3048
                        else:
                            self.dist_mul = 1.0
                    # other codes are ignored (AD/SF/EC/EO)


class Stonex(TotalStation):
    """ Class to import STONEX ascii file
    """

    def __init__(self, fname, separator=','):
        """ Initialize a new instance

            :param fname: input file name (string)
            :param separator: field separator in input (string/regexp)
        """
        super(Stonex, self).__init__(fname, separator)
        self.angle_unit = 'GON'
        self.distance_unit = 1  # 0-feet 1-meter
        self.res = {}

    def parse_next(self):
        """ Load next observation, station

            :returns: observation data
        """
        last_res = {}
        if self.fp is None:
            return None
        while True:
            buf = self.get_line()
            if buf is None:
                if len(self.res):
                    last_res = self.res
                    self.res = {}
                    return last_res
                else:
                    return None
            if buf[0] not in ('K', 'E', 'B', 'C', 'L'):
                continue  # skip unknown/job lines
            point_id = buf[1].strip()
            if 'point_id' in list(self.res.keys()) and self.res['point_id'] != point_id:
                last_res = self.res  # save previous data to return
                self.res = {}  # clear for new point
            if buf[0] == 'K':
                self.res['point_id'] = point_id
                self.res['n'] = float(buf[2].strip())
                self.res['e'] = float(buf[3].strip())
                self.res['z'] = float(buf[4].strip())
                self.res['hz'] = Angle(float(buf[5].strip()) / 10000.0, self.angle_unit).get_angle(
                    ANGLE_UNITS_STORE[config.angle_stored])
                self.res['th'] = float(buf[6].strip())
                self.res['station'] = 'station'
            elif buf[0] == 'E':  # observation
                self.res['point_id'] = point_id
                self.res['hz'] = Angle(float(buf[2].strip()) / 10000.0, self.angle_unit).get_angle(
                    ANGLE_UNITS_STORE[config.angle_stored])
                self.res['v'] = Angle(float(buf[3].strip()) / 10000.0, self.angle_unit).get_angle(
                    ANGLE_UNITS_STORE[config.angle_stored])
                self.res['th'] = float(buf[4].strip())
                self.res['sd'] = float(buf[6].strip())
                self.res['station'] = None
            elif buf[0] == 'B':  # coordinate record
                self.res['point_id'] = point_id
                self.res['n'] = float(buf[2].strip())
                self.res['e'] = float(buf[3].strip())
                self.res['z'] = float(buf[4].strip())
            elif buf[0] == 'C':  # coordinate + ????
                self.res['point_id'] = point_id
                self.res['n'] = float(buf[2].strip())
                self.res['e'] = float(buf[3].strip())
                self.res['z'] = float(buf[4].strip())
            elif buf[0] == 'L':  # coordinate + hz ???
                self.res['point_id'] = point_id
                self.res['n'] = float(buf[2].strip())
                self.res['e'] = float(buf[3].strip())
                self.res['z'] = float(buf[4].strip())
                self.res['hz'] = Angle(float(buf[5].strip()) / 10000.0, self.angle_unit).get_angle(
                    ANGLE_UNITS_STORE[config.angle_stored])
                self.res['th'] = float(buf[6].strip())
                self.res['station'] = None
            if len(last_res):
                return last_res


class Dump(TotalStation):
    """ Class to import geoeasy dump ascii file
    """

    def __init__(self, fname, separator='[;\t ]'):
        """ Initialize a new instance

            :param fname: input file name (string)
            :param separator: field separator in input (string/regexp)
        """
        super(Dump, self).__init__(fname, separator)
        self.last_station = ""  # stores last used station
        self.stack = None

    @staticmethod
    def conv_angle(val):
        """ Convert angle from DMS to radians if necessary

            :param val: angle value (string) radian or DMS (e.g. 12-23-34)
            :returns: angle in GON (float)
        """
        ret = None
        val = val.strip()
        if len(val):
            try:
                ret = Angle(float(val)).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
            except (ValueError, TypeError):
                ret = Angle(val, 'DMS').get_angle(ANGLE_UNITS_STORE[config.angle_stored])
        return ret

    @staticmethod
    def conv_dist(val):
        """ Convert angle from DMS to radians if necessary

            :param val: angle value (string) radian or DMS (e.g. 12-23-34)
            :returns: angle in radians (float)
        """
        ret = None
        val = val.strip()
        if len(val):
            try:
                ret = float(val)
            except ValueError:
                pass
        return ret

    def parse_next(self):
        """ Load next observation, station

            :returns: observation data
        """
        res = {}
        if self.stack:
            w = self.stack
            self.stack = None
            return w
        if self.fp is None:
            return None
        while True:
            buf = self.get_line()
            if buf is None:
                return None
            if len(buf) == 0:
                continue
            station_id = buf[0].strip()
            if station_id != self.last_station:
                # new station starts
                self.last_station = station_id
                res['point_id'] = station_id
                res['station'] = 'station'
                res['ih'] = self.conv_dist(buf[6])
                # save observation
                self.stack = {'point_id': buf[1].strip(), 'hz': self.conv_angle(buf[2]), 'v': self.conv_angle(buf[3]),
                              'sd': self.conv_dist(buf[4]), 'th': self.conv_dist(buf[5])}
            else:
                # observation from the same station
                res['point_id'] = buf[1].strip()
                res['station'] = ''
                res['hz'] = self.conv_angle(buf[2])
                res['v'] = self.conv_angle(buf[3])
                res['sd'] = self.conv_dist(buf[4])
                res['th'] = self.conv_dist(buf[5])
            return res


class Idex(TotalStation):
    """ Class to import Leica IDEX format
    """

    def __init__(self, fname, separator=r'[,\(\)]'):
        """ Initialize a new instance

            :param fname: input file name (string)
            :param separator: field separator in input (string/regexp)
        """
        super(Idex, self).__init__(fname, separator)
        # block status flags
        self.header = False
        self.units = False
        self.project = False
        self.database = False
        self.points = False
        self.theminfo = False
        self.annotations = False
        self.meteo = False
        self.theodolite = False
        self.instrument = False
        self.configs = False
        self.setup = False
        self.slope = False
        self.angular = "PDEG"
        self.linear = "METRE"
        # process header (units)
        self.open()
        while True:
            buf = self.get_line()
            if buf is None:
                return
            buf = self.buf_strip(buf)
            if len(buf) == 0:
                continue
            if buf[0] == "HEADER":
                self.header = True
            elif buf[0] == "UNITS":
                self.units = True
            elif re.match("ANGULAR", buf[0]) and self.header and self.units:
                w = re.split(r'\W+', buf[0])[-1]
                if w == "DMS":
                    self.angular = "PDEG"
            elif re.match("LINEAR", buf[0]) and self.header and self.units:
                self.linear = re.split(r'\W+', buf[0])[-1]
            elif buf[0] == "END UNITS":
                self.units = False
            elif buf[0] == "END HEADER":
                self.header = False
                break

    @staticmethod
    def buf_strip(buf, keep_empty=False):
        """ Strip list items & remove empty items

            :param buf: input list
            :param keep_empty: whether to retain empty items in the list
            :return: list with stipped items
        """
        return [x.strip(' \t";\'') for x in buf
                if keep_empty or len(x.strip(' \t";\''))]

    def parse_next(self):
        """ Load next observation, station

            :returns: observation data
        """
        res = {}
        if self.fp is None:
            return None
        while True:
            buf = self.get_line()
            if buf is None:
                return None
            buf = self.buf_strip(buf, True)  # keep empty items
            if len(buf) == 0:
                continue
            if buf[0] == "DATABASE":
                self.database = True
            elif buf[0] == "POINTS":
                self.points = True
            elif buf[0] == "THEMINFO":
                self.theminfo = True
            elif buf[0] == "ANNOTATIONS":
                self.annotations = True
            elif buf[0] == "END ANNOTATIONS":
                self.annotations = False
            elif buf[0] == "END THEMINFO":
                self.theminfo = False
            elif buf[0] == "END POINTS":
                self.points = False
            elif buf[0] == "END DATABASE":
                self.database = False
            elif buf[0] == "METEO":
                self.meteo = True
            elif buf[0] == "END METEO":
                self.meteo = False
            elif buf[0] == "THEODOLITE":
                self.theodolite = True
            elif buf[0] == "SETUP":
                self.setup = True
            elif buf[0] == "SLOPE":
                self.slope = True
            elif buf[0] == "END SLOPE":
                self.slope = False
            elif buf[0] == "END SETUP":
                self.setup = False
                return res
            elif buf[0] == "END THEODOLITE":
                self.theodolite = False
            elif buf[0][:6] == "STN_ID":
                if self.setup:
                    res["point_id"] = re.split(r'\W+', buf[0])[-1]
                    res['station'] = 'station'
            elif buf[0][:7] == "INST_HT":
                if self.setup:
                    res["ih"] = float(re.split(r'\W+', buf[0])[-1])
            elif buf[0] == "SLOPE":
                self.slope = True
            elif buf[0] == "END SLOPE":
                self.slope = False
            elif self.database and self.points and not self.theminfo and not self.annotations:
                # point coordinate record
                if buf[1] and ((buf[2] and buf[3]) or buf[4]):
                    res['point_id'] = buf[1]
                    res['e'] = float(buf[2]) if len(buf[2]) else None
                    res['n'] = float(buf[3]) if len(buf[3]) else None
                    res['z'] = float(buf[4]) if len(buf[4]) else None
                    res['pcode'] = buf[5] if len(buf[5]) else None
                    return res
            elif self.theodolite and self.slope:
                res['point_id'] = buf[1]
                res['station'] = ''
                res['hz'] = Angle(float(buf[3]), self.angular).get_angle(ANGLE_UNITS_STORE[config.angle_stored]) \
                    if len(buf[3]) else None
                res['v'] = Angle(float(buf[4]), self.angular).get_angle(ANGLE_UNITS_STORE[config.angle_stored]) \
                    if len(buf[4]) else None
                res['sd'] = float(buf[5]) if len(buf[5]) else None
                res['th'] = float(buf[6]) if len(buf[6]) else None
                return res


class NikonRaw(TotalStation):
    """ Class to read Nikon RAW v2 data. Based almost entirely on TotalOpenStation:
    https://github.com/steko/totalopenstation/blob/master/totalopenstation/formats/nikon_raw_v200.py
    """
    UNITS = {
        "angle": {"DDDMMSS": "PDEG", "MIL": "MIL", "Gons": "GON", "Degrees": "DEG"},
        "distance": {"Feet": "feet", "Metres": "metre", "Feet US": "ussfeet"}
    }

    COORDINATE_ORDER = ('NEZ', 'ENZ')

    def __init__(self, fname):
        """ Initialize a new instance

            :param fname: file name to open (str)
        """
        super(NikonRaw, self).__init__(fname, ',')
        self.coordorder = 'ENZ'
        self.angle_unit = 'deg'
        self.dist_unit = 'metre'
        self.last_station = {}

    @staticmethod
    def check_coordorder(coordorder):
        if any((coordorder == v for v in NikonRaw.COORDINATE_ORDER)):
            return coordorder
        else:
            raise ValueError('Invalid coordinate order')

    def parse_next(self):
        fs = self.get_line()
        if fs is None:
            return None

        res = {}

        # Get angle and distance units
        if fs[0] == 'CO':
            if fs[1].startswith('Coord Order:'):
                self.coordorder = NikonRaw.check_coordorder(fs[1].split(':')[-1].strip())
            if fs[1].startswith('Angle Units:'):
                self.angle_unit = NikonRaw.UNITS["angle"][fs[1].split(':')[1].strip()]
            if fs[1].startswith('Dist Units:'):
                self.dist_unit = NikonRaw.UNITS["distance"][fs[1].split(':')[1].strip()]

        # Look for point coordinates
        elif fs[0] in ('UP', 'MP', 'CC', 'RE', 'MC'):
            res['pt'] = fs[0]
            res['point_id'] = fs[1]
            easting = fs[3]
            northing = fs[4]
            if self.coordorder == "NEZ":
                easting, northing = northing, easting

            res['e'] = float(easting)
            res['n'] = float(northing)
            res['z'] = float(fs[5])
            res['pc'] = fs[6]

        # Look for station coordinates
        elif fs[0] == 'ST':
            self.last_station['pt'] = fs[0]
            self.last_station['point_id'] = fs[1]
            self.last_station['station'] = 'station'

            try:
                self.last_station['ih'] = float(fs[5])
            except ValueError:
                self.last_station['ih'] = 0.0

            # Look for back sight values in station values
            # Treat only one backsight or the last one
            # if fs[3] != '':
            #     b_zero_st = (float(fs[6]) - float(fs[7])) % NikonRaw.UNITS_CIRCLE[self.angle_unit]
            # else:
            #     b_zero_st = 0.0
            # if fs[3] != '':
            #     point_name = fs[3]
            #     azimuth = fs[6]
            #     circle = fs[7]

            # try:
            #     self.last_station['hz'] =
            #         Angle(float(fs[7]), self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
            # except ValueError:
            #     self.last_station['hz'] = 0.0

        # Look for Face 1 and Face 2
        elif fs[0] in ('F1', 'F2'):
            for i in (2, 3, 4, 5):
                if fs[i] == '':
                    fs[i] = 0
            # self.last_station['th'] = float(fs[2])
            # For stations we store the instrument height in the target height field.
            self.last_station['th'] = self.last_station['ih']
            self.last_station['sd'] = float(fs[3])
            self.last_station['hz'] = Angle(float(fs[4]), self.angle_unit).get_angle(
                ANGLE_UNITS_STORE[config.angle_stored])
            self.last_station['v'] = Angle(float(fs[5]), self.angle_unit).get_angle(
                ANGLE_UNITS_STORE[config.angle_stored])

            res = self.last_station

        # Look for Sideshot
        elif fs[0] == 'SS':
            res['pt'] = fs[0]
            res['station'] = None
            for i in (2, 3, 4, 5):
                if fs[i] == '':
                    fs[i] = 0
            res['point_id'] = fs[1]
            res['th'] = float(fs[2])
            res['sd'] = float(fs[3])
            res['hz'] = Angle(float(fs[4]), self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
            res['v'] = Angle(float(fs[5]), self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
            if len(fs) >= 8:
                res['pc'] = fs[7]

        # Look for Stakeout
        elif fs[0] == 'SO':
            res['station'] = None
            res['pt'] = fs[0]
            res['point_id'] = fs[1]
            res['th'] = float(fs[3])
            res['sd'] = float(fs[4])
            res['hz'] = Angle(float(fs[5]), self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
            res['v'] = Angle(float(fs[6]), self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])

        # Look for Control point
        elif fs[0] == 'CP':
            res['station'] = None
            res['pt'] = fs[0]
            res['point_id'] = fs[1]
            res['th'] = float(fs[3])
            res['sd'] = float(fs[4])
            res['hz'] = Angle(float(fs[5]), self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
            res['v'] = Angle(float(fs[6]), self.angle_unit).get_angle(ANGLE_UNITS_STORE[config.angle_stored])
            res['pc'] = fs[8]

        return res
