# Copyright (c) 2019 GeoSpark
#
# Released under the MIT License (MIT)
# See the LICENSE file, or visit http://opensource.org/licenses/MIT
from groma.base_classes import Point, compare, Angle, Circle, PolarObservation, Distance


def test_compare():
    ang = Point('1', 100, 200)
    assert compare(ang, ang)


def test_angle():
    expected_result = '359-59-59'
    ang = Angle('359-59-59', 'DMS')

    assert compare(ang.get_angle('DMS'), expected_result)
    assert compare(Angle(ang.get_angle('RAD'), 'RAD').get_angle('DMS'), expected_result)
    assert compare(Angle(ang.get_angle('DMS'), 'DMS').get_angle('DMS'), expected_result)
    assert compare(Angle(ang.get_angle('DEG'), 'DEG').get_angle('DMS'), expected_result)
    assert compare(Angle(ang.get_angle('GON'), 'GON').get_angle('DMS'), expected_result)
    assert compare(Angle(ang.get_angle('NMEA'), 'NMEA').get_angle('DMS'), expected_result)
    assert compare(Angle(ang.get_angle('PDEG'), 'PDEG').get_angle('DMS'), expected_result)
    assert compare(Angle('16-20', 'DMS').get_angle('DMS'), '16-20-00')
    assert compare(Angle('16', 'DMS').get_angle('DMS'), '16-00-00')


def test_observation():
    # pnt = [Point('1', 1000, 2000, 50), Point('2', 1500, 2000, 60)]
    obs = [PolarObservation('1', 'station', None, None, None, 1.54),
           PolarObservation('2', None, Angle(60.9345, 'GON'), Angle(89.855615, 'DEG'), Distance(501.105, 'SD'), 1.80)]
    assert compare(obs[1].horiz_dist(), 501.103)


def test_circle_from_center_radius():
    circ = Circle(Point('3', 100, 200), 100.0)
    assert compare(circ.p.e, 100)
    assert compare(circ.p.n, 200)
    assert compare(circ.r, 100.0)


def test_circle_from_three_points():
    circ = Circle(Point('4', 0, 50), Point('5', 50, 100), Point('6', 100, 50))
    assert compare(circ.p.e, 50.0)
    assert compare(circ.p.n, 50.0)
    assert compare(circ.r, 50.0)


def test_circle_from_two_points_and_angle():
    # c = Circle(Point('4', 50, 50), Point('5', 100, 100), Point('6', 200, 200))
    circ = Circle(Point('4', 100, 100), Point('5', 0, 100), Angle(60, 'DEG'))
    assert compare(circ.p.e, 50.0)
    assert compare(circ.p.n, 128.867513459)
    assert compare(circ.r, 57.735026919)
