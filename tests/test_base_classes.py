# Copyright (c) 2019 GeoSpark
#
# Released under the MIT License (MIT)
# See the LICENSE file, or visit http://opensource.org/licenses/MIT
from base_classes import Point, compare, Angle, Circle, PolarObservation, Distance


def test_base_classes():
    """
        unit test
    """
    ang = Point('1', 100, 200)
    if not compare(ang, ang):
        # fix_print_with_import
        print("Compare function test failed")
    print("Test for Angle class")
    adms = '359-59-59'
    ang = Angle(adms, 'DMS')
    if not compare(ang.get_angle('DMS'), adms):
        print("DMS test failed")
    if not compare(Angle(ang.get_angle('RAD'), 'RAD').get_angle('DMS'), adms):
        print("RAD test failed")
    if not compare(Angle(ang.get_angle('DMS'), 'DMS').get_angle('DMS'), adms):
        print("DMS 2 test failed")
    if not compare(Angle(ang.get_angle('DEG'), 'DEG').get_angle('DMS'), adms):
        print("DEG test failed")
    if not compare(Angle(ang.get_angle('GON'), 'GON').get_angle('DMS'), adms):
        print("GON test failed")
    if not compare(Angle(ang.get_angle('NMEA'), 'NMEA').get_angle('DMS'), adms):
        print("NMEA test failed")
    if not compare(Angle(ang.get_angle('PDEG'), 'PDEG').get_angle('DMS'), adms):
        print("PDEG test failed")
    if not compare(Angle('16-20', 'DMS').get_angle('DMS'), '16-20-00'):
        print("Short DMS test failed")
    if not compare(Angle('16', 'DMS').get_angle('DMS'), '16-00-00'):
        print("Short DMS 2 test failed")
    # new test style to continue from here
    # pnt = [Point('1', 1000, 2000, 50), Point('2', 1500, 2000, 60)]
    obs = [PolarObservation('1', 'station', None, None, None, 1.54),
           PolarObservation('2', None, Angle(60.9345, 'GON'), Angle(89.855615, 'DEG'), Distance(501.105, 'SD'), 1.80)]
    if not compare(obs[1].horiz_dist(), 501.103):
        print("Horizontal distance test failed")
    circ = Circle(Point('3', 100, 200), 100.0)
    if not compare(circ.p.e, 100):
        print("Circle from center and radius test failed by e")
    if not compare(circ.p.n, 200):
        print("Circle from center and radius test failed by n")
    if not compare(circ.r, 100.0):
        print("Circle from center and radius test failed by r")
    circ = Circle(Point('4', 0, 50), Point('5', 50, 100), Point('6', 100, 50))
    if not compare(circ.p.e, 50.0):
        print("Circle from 3 points test failed by e")
    if not compare(circ.p.n, 50.0):
        print("Circle from 3 points test failed by n")
    if not compare(circ.r, 50.0):
        print("Circle from 3 points test failed by r")
    # c = Circle(Point('4', 50, 50), Point('5', 100, 100), Point('6', 200, 200))
    circ = Circle(Point('4', 100, 100), Point('5', 0, 100), Angle(60, 'DEG'))
    if not compare(circ.p.e, 50.0):
        print("Circle from 2 points and angle test failed by e")
    if not compare(circ.p.n, 128.867513459):
        print("Circle from 2 points and angle test failed by n")
    if not compare(circ.r, 57.735026919):
        print("Circle from 2 points and angle test failed by r")
