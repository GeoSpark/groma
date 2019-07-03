# Copyright (c) 2019 GeoSpark
#
# Released under the MIT License (MIT)
# See the LICENSE file, or visit http://opensource.org/licenses/MIT
from base_classes import Point, compare, Distance, Angle, PolarObservation, Station
from calculation import Calculation, distance2d, distance3d, bearing


def test_calculation():
    """
        modul test
    """
    p1 = Point("1", 100, 200, 20)
    p2 = Point("2", 150, 250, 30)
    d = distance2d(p1, p2)
    if not compare(d.d, 70.7107):
        print("Distance2d test failed")
    d = distance3d(p1, p2)
    if not compare(d.d, 71.4143):
        print("Distance3d test failed")
    b = bearing(p1, p2)
    if not compare(b.get_angle('DMS'), '45-00-00'):
        print("Bearing p1-p2 test failed")
    b = bearing(p2, p1)
    if not compare(b.get_angle('DMS'), '225-00-00'):
        print("Bearing p2-p1 test failed")
    b = bearing(p1, p1)
    if not compare(b.get_angle('DMS'), '0-00-00'):
        print("Bearing p1-p1 test failed")

    # intersection test
    s1o = PolarObservation('1', 'station', Angle(0))
    s2o = PolarObservation('2', 'station', Angle(0))
    s1 = Station(p1, s1o)
    s2 = Station(p2, s2o)
    o1 = PolarObservation("p", None, Angle(25, "DEG"))
    o2 = PolarObservation("p", None, Angle(310, "DEG"))
    p3 = Calculation.intersection(s1, o1, s2, o2)
    if not compare(p3, Point('p', 130.8201, 266.0939)):
        print("Simple-1 intersection test failed")
    A1 = Point("A1", -150, -120)
    A2 = Point("A2", 130, 75)
    sA1o = PolarObservation('A1', 'station', Angle("76-13-23", "DMS"))
    sA2o = PolarObservation('A2', 'station', Angle("324-10-58", "DMS"))
    sA1 = Station(A1, sA1o)
    sA2 = Station(A2, sA2o)
    oA1 = PolarObservation("p3", None, Angle("308-46-36", "DMS"))
    oA2 = PolarObservation("p3", None, Angle("345-49-02", "DMS"))
    P3 = Calculation.intersection(sA1, oA1, sA2, oA2)
    if not compare(P3, Point('p3', -5.8979, 189.0319)):
        print("Simple-2 intersection test failed")
    sA1o = PolarObservation('A1', 'station', Angle("0", "DMS"))
    sA2o = PolarObservation('A2', 'station', Angle("0", "DMS"))
    sA1 = Station(A1, sA1o)
    sA2 = Station(A2, sA2o)
    oA1 = PolarObservation("p4", None, Angle("225", "DMS"))
    oA2 = PolarObservation("p4", None, Angle("45", "DMS"))
    P4 = Calculation.intersection(sA1, oA1, sA2, oA2)

    print("Result for impossible intersection:")

    print(P4.id, P4.e, P4.n)
    A3 = Point("A3", 0, 0)
    A4 = Point("A4", 100, 100)
    sA3o = PolarObservation('A3', 'station', Angle("0", "DMS"))
    sA4o = PolarObservation('A4', 'station', Angle("0", "DMS"))
    sA3 = Station(A3, sA3o)
    sA4 = Station(A4, sA4o)
    oA3 = PolarObservation("p5", None, Angle("45", "DMS"))
    oA4 = PolarObservation("p5", None, Angle("225", "DMS"))
    P5 = Calculation.intersection(sA3, oA3, sA4, oA4)

    print("Result for observe each other:")

    print(P5.id, P5.e, P5.n)  # p5 100.0 100.0
    A3 = Point("A3", 0, 0)
    A4 = Point("A4", 100, 100)
    sA3o = PolarObservation('A3', 'station', Angle("0", "DMS"))
    sA4o = PolarObservation('A4', 'station', Angle("0", "DMS"))
    sA3 = Station(A3, sA3o)
    sA4 = Station(A4, sA4o)
    oA3 = PolarObservation("p5", None, Angle("45", "DMS"))
    oA4 = PolarObservation("p5", None, Angle("45", "DMS"))
    P5 = Calculation.intersection(sA3, oA3, sA4, oA4)
    if not compare(P5, None):
        print("Intersection test for parallel observation failed")

    # resection test
    p1res = Point("3")
    o1res = PolarObservation('3', None, "station", Angle(0))
    s1res = Station(p1res, o1res)
    p101res = Point("101", 658031.813, 247985.580)
    p102res = Point("102", 657638.800, 247759.380)
    p103res = Point("103", 658077.700, 247431.381)
    o101res = PolarObservation("101", None, Angle("22-45-56", "DMS"))
    o102res = PolarObservation("102", None, Angle("164-38-59", "DMS"))
    o103res = PolarObservation("103", None, Angle("96-23-12", "DMS"))
    p1res = Calculation.resection(s1res, p101res, p102res, p103res, o101res, o102res, o103res)
    if not compare(p1res, Point("3", 657871.9494, 247973.2414)):
        print("Simple-1 resection test failed")
    P4res = Point("P4")
    oP4res = PolarObservation('P4', "station", Angle(0))
    sP4res = Station(P4res, oP4res)
    o101res = PolarObservation("101", None, Angle("202-45-56", "DMS"))
    o102res = PolarObservation("102", None, Angle("344-38-59", "DMS"))
    o103res = PolarObservation("103", None, Angle("276-23-12", "DMS"))
    P4res = Calculation.resection(sP4res, p101res, p102res, p103res, o101res, o102res, o103res)
    if not compare(P4res, Point("P4", 657871.9494, 247973.2414)):
        print("Simple-2 resection test failed")
    P5res = Point("P5")
    oP5res = PolarObservation('P5', "station", Angle(0))
    sP5res = Station(P5res, oP5res)
    o101res = PolarObservation("101", None, Angle("88-41-35.8669", "DMS"))
    o102res = PolarObservation("102", None, Angle("40-11-52.9394", "DMS"))
    o103res = PolarObservation("103", None, Angle("155-23-15.1567", "DMS"))
    P5res = Calculation.resection(sP5res, p101res, p102res, p103res, o101res, o102res, o103res)
    if not compare(P5res, None):
        print("Resection test for dangerous circle failed")
    P6res = Point("P6")
    oP6res = PolarObservation('P6', "station", Angle(0))
    sP6res = Station(P6res, oP6res)
    p101res = Point("101", -50, 80)
    p102res = Point("102", 0, 80)
    p103res = Point("103", 50, 80)
    o101res = PolarObservation("101", None, Angle("140-32-24", "DMS"))
    o102res = PolarObservation("102", None, Angle("97-13-15", "DMS"))
    o103res = PolarObservation("103", None, Angle("70-43-22", "DMS"))
    P6res = Calculation.resection(sP6res, p101res, p102res, p103res, o101res, o102res, o103res)
    if not compare(P6res, Point("P6", -29.6182, 142.6576)):
        print("Resection test for reference points on a line failed")
    P7res = Point("P7")
    oP7res = PolarObservation('P7', "station", Angle(0))
    sP7res = Station(P7res, oP7res)
    p101res = Point("101", -50, 80)
    p102res = Point("102", 0, 80)
    p103res = Point("103", 50, 80)
    o101res = PolarObservation("101", None, Angle("225", "DMS"))
    o102res = PolarObservation("102", None, Angle("45", "DMS"))
    o103res = PolarObservation("103", None, Angle("45", "DMS"))
    P7res = Calculation.resection(sP7res, p101res, p102res, p103res, o101res, o102res, o103res)
    if not compare(P7res, None):
        print("Resection test for reference points and station point on a line failed")

    # orientation
    p101ori = Point("101", 5693.45, 328.81)
    p102ori = Point("102", 6002.13, 1001.13)
    p103ori = Point("103", 5511.25, -253.16)
    p104ori = Point("104", 5033.45, -396.15)
    p201ori = Point("201", -4396.15, -561.13)
    p202ori = Point("202", -4000.55, 496.14)
    p203ori = Point("203", -5115.33, 366.11)
    p204ori = Point("204", -3863.96, -268.15)
    p205ori = Point("205", -3455.37, -959.36)
    p206ori = Point("206", -5500.08, -724.69)
    p301ori = Point("301", 4512.35, -496.29)
    p302ori = Point("302", 4073.16, -986.32)
    p303ori = Point("303", 3952.25, 818.66)
    p401ori = Point("401", -3516.22, 156.25)
    p402ori = Point("402", -3986.35, 460.18)
    p403ori = Point("403", -4019.28, 510.54)
    p501ori = Point("501", -116.94, 150.86)
    p502ori = Point("502", 127.03, 337.43)
    p503ori = Point("503", 887.64, -1068.99)
    p504ori = Point("504", -999.53, -896.77)
    p505ori = Point("505", -1150.22, 150.86)
    o101ori = PolarObservation('101', "station")
    s101ori = Station(p101ori, o101ori)
    o102ori = PolarObservation("102", None, Angle("268-14-13", "DMS"))
    o103ori = PolarObservation("103", None, Angle("80-57-34", "DMS"))
    o104ori = PolarObservation("104", None, Angle("105-53-19", "DMS"))
    z101ori = Calculation.orientation(s101ori, [[p102ori, o102ori], [p103ori, o103ori], [p104ori, o104ori]])
    if not compare(z101ori.get_angle('DMS'), '116-25-30'):
        print("Simple-1 orientation test failed")
    o201ori = PolarObservation('201', "station")
    s201ori = Station(p201ori, o201ori)
    o202ori = PolarObservation("202", None, Angle("316-40-57", "DMS"))
    o203ori = PolarObservation("203", None, Angle("258-22-09", "DMS"))
    o204ori = PolarObservation("204", None, Angle("357-19-49", "DMS"))
    o205ori = PolarObservation("205", None, Angle("49-6-32", "DMS"))
    o206ori = PolarObservation("206", None, Angle("197-44-22", "DMS"))
    z201ori = Calculation.orientation(s201ori,
                                      [[p202ori, o202ori], [p203ori, o203ori], [p204ori, o204ori], [p205ori, o205ori],
                                       [p206ori, o206ori]])
    if not compare(z201ori.get_angle('DMS'), '63-50-00'):
        print("Simple-2 orientation test failed")
    o201ori = PolarObservation('201', "station")
    s201ori = Station(p201ori, o201ori)
    o202ori = PolarObservation("202", None, Angle(351.86944, "GON"))
    o203ori = PolarObservation("203", None, Angle(287.07685, "GON"))
    o204ori = PolarObservation("204", None, Angle(397.03364, "GON"))
    o205ori = PolarObservation("205", None, Angle(54.56543, "GON"))
    o206ori = PolarObservation("206", None, Angle(219.71049, "GON"))
    z201ori = Calculation.orientation(s201ori,
                                      [[p202ori, o202ori], [p203ori, o203ori], [p204ori, o204ori], [p205ori, o205ori],
                                       [p206ori, o206ori]])
    if not compare(z201ori.get_angle('DMS'), '63-50-00'):
        print("Simple-3 orientation test failed")
    o301ori = PolarObservation('301', "station")
    s301ori = Station(p301ori, o301ori)
    o302ori = PolarObservation("302", None, Angle("166-10-30", "DMS"))
    o303ori = PolarObservation("303", None, Angle("281-13-55", "DMS"))
    z301ori = Calculation.orientation(s301ori, [[p302ori, o302ori], [p303ori, o303ori]])
    if not compare(z301ori.get_angle('DMS'), '55-41-44'):
        print("Simple-4 orientation test failed")
    o401ori = PolarObservation('401', "station")
    s401ori = Station(p401ori, o401ori)
    o402ori = PolarObservation("402", None, Angle("101-37-23", "DMS"))
    o403ori = PolarObservation("403", None, Angle("103-53-37", "DMS"))
    z401ori = Calculation.orientation(s401ori, [[p402ori, o402ori], [p403ori, o403ori]])
    if not compare(z401ori.get_angle('DMS'), '201-15-38'):
        print("Simple-5 orientation test failed")
    o401ori = PolarObservation('401', "station")
    s401ori = Station(p401ori, o401ori)
    o402ori = PolarObservation("402", None, Angle("101-37-23", "DMS"))
    z401ori = Calculation.orientation(s401ori, [[p402ori, o402ori]])
    if not compare(z401ori.get_angle('DMS'), '201-15-32'):
        print("Simple-6 orientation test failed")
    o501ori = PolarObservation('501', "station")
    s501ori = Station(p501ori, o501ori)
    o502ori = PolarObservation("502", None, Angle("170-50-59", "DMS"))
    o503ori = PolarObservation("503", None, Angle("258-46-56", "DMS"))
    o504ori = PolarObservation("504", None, Angle("338-22-5", "DMS"))
    o505ori = PolarObservation("505", None, Angle("28-15-23", "DMS"))
    z501ori = Calculation.orientation(s501ori,
                                      [[p502ori, o502ori], [p503ori, o503ori], [p504ori, o504ori], [p505ori, o505ori]])
    if not compare(z501ori.get_angle('DMS'), '241-44-41'):
        print("Simple-6 orientation test failed")

    # polar points
    p101pol = Point("101", 13456.25, 12569.75)
    p201pol = Point("201", 13102.13, 11990.13)
    p202pol = Point("202", 13569.11, 12788.66)
    p203pol = Point("203", 13861.23, 12001.54)
    o101pol = PolarObservation('101', "station")
    s101pol = Station(p101pol, o101pol)
    o201pol = PolarObservation("201", None, Angle("112-15-15", "DMS"))
    o202pol = PolarObservation("202", None, Angle("288-06-30", "DMS"))
    o203pol = PolarObservation("203", None, Angle("45-21-12", "DMS"))
    o9pol = PolarObservation("9", None, Angle("145-10-16", "DMS"), None, Distance(206.17, "HD"))
    o10pol = PolarObservation("10", None, Angle("201-30-47", "DMS"), None, Distance(219.38, "HD"))
    z101pol = Calculation.orientation(s101pol, [[p201pol, o201pol], [p202pol, o202pol], [p203pol, o203pol]])
    if not compare(z101pol.get_angle('DMS'), '99-10-05'):
        print("Simple-1 polar points test failed by orientation")
    s101pol.o.hz = z101pol
    p9pol = Calculation.polarpoint(s101pol, o9pol)
    p10pol = Calculation.polarpoint(s101pol, o10pol)
    if not compare(p9pol, Point("9", 13270.4141, 12480.4691)):
        print("Simple-1 polar points test failed by P9")
    if not compare(p10pol, Point("10", 13267.5785, 12681.6903)):
        print("Simple-1 polar points test failed by P10")
    pA1pol = Point("A1", 153.867, 456.430)
    pT1pol = Point("T1", -237.865, -297.772)
    pT2pol = Point("T2", -1549.927, 669.6126)
    pT3pol = Point("T3", 1203.064, -220.0314)
    oA1pol = PolarObservation('A1', "station")
    sA1pol = Station(pA1pol, oA1pol)
    oT1pol = PolarObservation("T1", None, Angle("73-02-35", "DMS"))
    oT2pol = PolarObservation("T2", None, Angle("142-43-39", "DMS"))
    oT3pol = PolarObservation("T3", None, Angle("348-24-26", "DMS"))
    oP1pol = PolarObservation("P1", None, Angle("112-43-47", "DMS"), None, Distance(673.699, "HD"))
    oP2pol = PolarObservation("P2", None, Angle("84-0-44", "DMS"), None, Distance(788.105, "HD"))
    zA1pol = Calculation.orientation(sA1pol, [[pT1pol, oT1pol], [pT2pol, oT2pol], [pT3pol, oT3pol]])
    if not compare(zA1pol.get_angle('DMS'), '134-24-16'):
        print("Simple-2 polar points test failed by orientation")
    sA1pol.o.hz = zA1pol
    pP1pol = Calculation.polarpoint(sA1pol, oP1pol)
    pP2pol = Calculation.polarpoint(sA1pol, oP2pol)
    if not compare(pP1pol, Point("P1", -466.8905, 194.6468)):
        print("Simple-2 polar points test failed by P1")
    if not compare(pP2pol, Point("P2", -335.8415, -161.0610)):
        print("Simple-2 polar points test failed by P2")

    # traverse1
    # closed at one end and known bearings at one end (free traverse)
    p5241otra = Point("5241", 646414.44, 211712.77)
    p5245otra = Point("5245", 646938.71, 212635.92)
    p5246otra = Point("5246", 646380.61, 212793.97)
    p5247otra = Point("5247", 646381.14, 212476.49)
    o5247otra = PolarObservation('5247', "station")
    s5247otra = Station(p5247otra, o5247otra)
    o5241otra = PolarObservation("5241", None, Angle("245-23-41", "DMS"))
    o5245otra = PolarObservation("5245", None, Angle("141-56-11", "DMS"))
    o5246otra = PolarObservation("5246", None, Angle("67-47-14", "DMS"))
    s5247otra.o.hz = Calculation.orientation(s5247otra,
                                             [[p5241otra, o5241otra], [p5245otra, o5245otra], [p5246otra, o5246otra]])
    if not compare(s5247otra.o.hz.get_angle('DMS'), '292-06-34'):
        print("Traverse test for free traverse failed by orientation")

    o5247_111otra = PolarObservation("111", None, Angle("241-26-57", "DMS"), None, Distance(123.42, "HD"))
    s111otra = Station(None, PolarObservation('111', "station"))
    o111_5247otra = PolarObservation("5247", None, Angle("225-39-00", "DMS"))
    o111_112otra = PolarObservation("112", None, Angle("92-38-43", "DMS"), None, Distance(142.81, "HD"))
    s112otra = Station(None, PolarObservation('112', "station"))
    o112_111otra = PolarObservation("111", None, Angle("227-16-34", "DMS"))
    o112_113otra = PolarObservation("113", None, Angle("69-16-28", "DMS"), None, Distance(253.25, "HD"))
    s113otra = Station(None, PolarObservation('113', "station"))
    o113_112otra = PolarObservation("112", None, Angle("102-56-44", "DMS"))
    o113_114otra = PolarObservation("114", None, Angle("205-46-21", "DMS"), None, Distance(214.53, "HD"))
    s114otra = Station(None, PolarObservation('114', "station"))
    o114_113otra = PolarObservation("113", None, Angle("104-23-11", "DMS"))
    o114_115otra = PolarObservation("115", None, Angle("305-54-29", "DMS"), None, Distance(234.23, "HD"))
    s115otra = Station(None, PolarObservation("115", 'station'))
    plist = Calculation.traverse([[s5247otra, None, o5247_111otra], [s111otra, o111_5247otra, o111_112otra],
                                  [s112otra, o112_111otra, o112_113otra], [s113otra, o113_112otra, o113_114otra],
                                  [s114otra, o114_113otra, o114_115otra], [s115otra, None, None]])
    if not compare(plist[0], Point('111', 646394.9860, 212353.8491)):
        print("Traverse test for free traverse failed by point 111")
    if not compare(plist[1], Point('112', 646302.1362, 212245.3429)):
        print("Traverse test for free traverse failed by point 112")
    if not compare(plist[2], Point('113', 646077.3941, 212128.60997)):
        print("Traverse test for free traverse failed by point 113")
    if not compare(plist[3], Point('114', 646131.5459, 211921.02697)):
        print("Traverse test for free traverse failed by point 114")
    if not compare(plist[4], Point('115', 646103.4028, 211688.4938)):
        print("Traverse test for free traverse failed by point 115")

    # traverse2
    # closed at both ends and known bearings at both ends
    pKtra = Point("K", 599767.21, 148946.70)
    pVtra = Point("V", 599733.75, 149831.76)
    p1015tra = Point("1015", 598642.17, 148436.26)
    p1016tra = Point("1016", 600136.60, 148588.85)
    p1017tra = Point("1017", 600264.30, 149325.79)
    p1018tra = Point("1018", 598258.90, 149496.78)
    p1019tra = Point("1019", 600092.33, 150676.80)

    oKtra = PolarObservation('K', "station")
    sKtra = Station(pKtra, oKtra)
    oK_1017tra = PolarObservation("1017", None, Angle("61-28-18", "DMS"))
    oK_1016tra = PolarObservation("1016", None, Angle("142-53-28", "DMS"))
    oK_1015tra = PolarObservation("1015", None, Angle("254-23-32", "DMS"))
    oK_1tra = PolarObservation("1", None, Angle("17-14-18", "DMS"), None, Distance(139.82, "HD"))
    sKtra.o.hz = Calculation.orientation(sKtra,
                                         [[p1017tra, oK_1017tra], [p1016tra, oK_1016tra], [p1015tra, oK_1015tra]])
    if not compare(sKtra.o.hz.get_angle('DMS'), '351-12-05'):
        print("Test traverse closed at both ends and known bearings at both ends failed by orientation1")

    s1tra = Station(None, PolarObservation('1', "station"))
    o1_Ktra = PolarObservation("K", None, Angle("79-28-20", "DMS"), None, Distance(139.85, "HD"))
    o1_2tra = PolarObservation("2", None, Angle("236-13-46", "DMS"), None, Distance(269.32, "HD"))
    # o1_501tra = PolarObservation("501", None, Angle("204-58-10", "DMS"), None, Distance(59.12, "HD"))
    s2tra = Station(None, PolarObservation('2', "station"))
    o2_3tra = PolarObservation("3", None, Angle("82-18-45", "DMS"), None, Distance(169.40, "HD"))
    o2_1tra = PolarObservation("1", None, Angle("217-58-34", "DMS"), None, Distance(269.36, "HD"))
    s3tra = Station(None, PolarObservation('3', "station"))
    o3_2tra = PolarObservation("2", None, Angle("262-18-44", "DMS"), None, Distance(169.45, "HD"))
    o3_Vtra = PolarObservation("V", None, Angle("41-18-10", "DMS"), None, Distance(345.90, "HD"))
    # o3_502tra = PolarObservation("502", None, Angle("344-28-25", "DMS"), None, Distance(55.46, "HD"))

    oVtra = PolarObservation('V', "station")
    sVtra = Station(pVtra, oVtra)
    oV_3tra = PolarObservation("3", None, Angle("257-44-08", "DMS"), None, Distance(345.94, "HD"))
    oV_1018tra = PolarObservation("1018", None, Angle("346-24-11", "DMS"))
    oV_1019tra = PolarObservation("1019", None, Angle("112-12-06", "DMS"))
    oV_1017tra = PolarObservation("1017", None, Angle("222-50-58", "DMS"))
    sVtra.o.hz = Calculation.orientation(sVtra,
                                         [[p1018tra, oV_1018tra], [p1019tra, oV_1019tra], [p1017tra, oV_1017tra]])
    if not compare(sVtra.o.hz.get_angle('DMS'), '270-47-46'):
        print("Test traverse closed at both ends and known bearings at both ends failed by orientation2")

    plist = Calculation.traverse([[sKtra, None, oK_1tra], [s1tra, o1_Ktra, o1_2tra], [s2tra, o2_1tra, o2_3tra],
                                  [s3tra, o3_2tra, o3_Vtra], [sVtra, oV_3tra, None]])
    if not compare(plist[0], Point('1', 599787.74865, 149085.0079)):
        print("Test traverse closed at both ends and known bearings at both ends failed by point 1")
    if not compare(plist[1], Point('2', 599718.9691, 149345.3886)):
        print("Test traverse closed at both ends and known bearings at both ends failed by point 2")
    if not compare(plist[2], Point('3', 599802.5094, 149492.7786)):
        print("Test traverse closed at both ends and known bearings at both ends failed by point 3")

    # traverse3
    # closed at both ends and known bearing at one end
    pA5tra = Point("A5", 646333.5695, 276616.4171)
    pA11tra = Point("A11", 646502.8710, 276361.2386)
    pA4tra = Point("A4", 646284.6886, 276659.2165)

    oA5tra = PolarObservation('A5', "station")
    sA5tra = Station(pA5tra, oA5tra)
    oA5_A4tra = PolarObservation("A4", None, Angle("311-12-21", "DMS"))
    oA5_A6tra = PolarObservation("A6", None, Angle("136-36-49", "DMS"), Angle("100-13-22", "DMS"),
                                 Distance(58.405, "SD"))
    sA5tra.o.hz = Calculation.orientation(sA5tra, [[pA4tra, oA5_A4tra]])
    if not compare(sA5tra.o.hz.get_angle('DMS'), '359-59-57'):
        print("Test traverse closed at both ends and known bearing at one end failed by orientation")

    sA6tra = Station(None, PolarObservation('A6', "station"))
    oA6_A5tra = PolarObservation("A5", None, Angle("316-36-49", "DMS"), Angle("79-56-53", "DMS"),
                                 Distance(58.378, "SD"))
    oA6_A7tra = PolarObservation("A7", None, Angle("136-43-52", "DMS"), Angle("101-55-08", "DMS"),
                                 Distance(43.917, "SD"))
    sA7tra = Station(None, PolarObservation('A7', "station"))
    oA7_A6tra = PolarObservation("A6", None, Angle("316-43-52", "DMS"), Angle("78-21-53", "DMS"),
                                 Distance(43.878, "SD"))
    oA7_A8tra = PolarObservation("A8", None, Angle("141-48-30", "DMS"), Angle("102-29-18", "DMS"),
                                 Distance(48.459, "SD"))
    sA8tra = Station(None, PolarObservation('A8', "station"))
    oA8_A7tra = PolarObservation("A7", None, Angle("321-48-30", "DMS"), Angle("77-49-44", "DMS"),
                                 Distance(48.401, "SD"))
    oA8_A9tra = PolarObservation("A9", None, Angle("153-25-18", "DMS"), Angle("100-01-16", "DMS"),
                                 Distance(47.098, "SD"))
    sA9tra = Station(None, PolarObservation('A9', "station"))
    oA9_A8tra = PolarObservation("A8", None, Angle("333-25-18", "DMS"), Angle("80-17-11", "DMS"),
                                 Distance(47.040, "SD"))
    oA9_A10tra = PolarObservation("A10", None, Angle("153-59-32", "DMS"), Angle("97-46-19", "DMS"),
                                  Distance(58.077, "SD"))
    sA10tra = Station(None, PolarObservation('A10', "station"))
    oA10_A9tra = PolarObservation("A9", None, Angle("333-59-32", "DMS"), Angle("82-27-53", "DMS"),
                                  Distance(58.045, "SD"))
    oA10_A11tra = PolarObservation("A11", None, Angle("154-05-41", "DMS"), Angle("97-06-32", "DMS"),
                                   Distance(58.188, "SD"))

    sA11tra = Station(pA11tra, PolarObservation('A11', "station"))
    oA11_A10tra = PolarObservation("A10", None, Angle("334-05-41", "DMS"), Angle("83-09-29", "DMS"),
                                   Distance(58.151, "SD"))

    plist = Calculation.traverse(
        [[sA5tra, None, oA5_A6tra], [sA6tra, oA6_A5tra, oA6_A7tra], [sA7tra, oA7_A6tra, oA7_A8tra],
         [sA8tra, oA8_A7tra, oA8_A9tra], [sA9tra, oA9_A8tra, oA9_A10tra], [sA10tra, oA10_A9tra, oA10_A11tra],
         [sA11tra, oA11_A10tra, None]])
    if not compare(plist[0], Point('A6', 646373.0353, 276574.6808)):
        print("Test traverse closed at both ends and known bearing at one end failed by point A6")
    if not compare(plist[1], Point('A7', 646402.4768, 276543.4174)):
        print("Test traverse closed at both ends and known bearing at one end failed by point A7")
    if not compare(plist[2], Point('A8', 646431.7153, 276506.2621)):
        print("Test traverse closed at both ends and known bearing at one end failed by point A8")
    if not compare(plist[3], Point('A9', 646452.4490, 276464.8193)):
        print("Test traverse closed at both ends and known bearing at one end failed by point A9")
    if not compare(plist[4], Point('A10', 646477.6637, 276413.1392)):
        print("Test traverse closed at both ends and known bearing at one end failed by point A10")

    # traverse4
    # loop traverse
    pA5tra = Point("A5", 646333.5695, 276616.4171)
    pA4tra = Point("A4", 646284.6886, 276659.2165)

    oA5tra = PolarObservation('A5', "station")
    sA5tra = Station(pA5tra, oA5tra)
    oA5_A4tra = PolarObservation("A4", None, Angle("311-12-21", "DMS"))
    oA5_A6tra = PolarObservation("A6", None, Angle("136-36-49", "DMS"), Angle("100-13-22", "DMS"),
                                 Distance(58.405, "SD"))
    # oA5_A11tra = PolarObservation("A11", None, Angle("146-26-58", "DMS"), Angle("90-00-00", "DMS"),
    #                               Distance(306.234, "SD"))
    sA5tra.o.hz = Calculation.orientation(sA5tra, [[pA4tra, oA5_A4tra]])
    if not compare(sA5tra.o.hz.get_angle('DMS'), '359-59-57'):
        print("Test traverse closed at both ends and known bearing at one end failed by orientation")

    sA6tra = Station(None, PolarObservation('A6', "station"))
    oA6_A5tra = PolarObservation("A5", None, Angle("316-36-49", "DMS"), Angle("79-56-53", "DMS"),
                                 Distance(58.378, "SD"))
    oA6_A7tra = PolarObservation("A7", None, Angle("136-43-52", "DMS"), Angle("101-55-08", "DMS"),
                                 Distance(43.917, "SD"))
    sA7tra = Station(None, PolarObservation('A7', "station"))
    oA7_A6tra = PolarObservation("A6", None, Angle("316-43-52", "DMS"), Angle("78-21-53", "DMS"),
                                 Distance(43.878, "SD"))
    oA7_A8tra = PolarObservation("A8", None, Angle("141-48-30", "DMS"), Angle("102-29-18", "DMS"),
                                 Distance(48.459, "SD"))
    sA8tra = Station(None, PolarObservation('A8', "station"))
    oA8_A7tra = PolarObservation("A7", None, Angle("321-48-30", "DMS"), Angle("77-49-44", "DMS"),
                                 Distance(48.401, "SD"))
    oA8_A9tra = PolarObservation("A9", None, Angle("153-25-18", "DMS"), Angle("100-01-16", "DMS"),
                                 Distance(47.098, "SD"))
    sA9tra = Station(None, PolarObservation('A9', "station"))
    oA9_A8tra = PolarObservation("A8", None, Angle("333-25-18", "DMS"), Angle("80-17-11", "DMS"),
                                 Distance(47.040, "SD"))
    oA9_A10tra = PolarObservation("A10", None, Angle("153-59-32", "DMS"), Angle("97-46-19", "DMS"),
                                  Distance(58.077, "SD"))
    sA10tra = Station(None, PolarObservation('A10', "station"))
    oA10_A9tra = PolarObservation("A9", None, Angle("333-59-32", "DMS"), Angle("82-27-53", "DMS"),
                                  Distance(58.045, "SD"))
    oA10_A11tra = PolarObservation("A11", None, Angle("154-05-41", "DMS"), Angle("97-06-32", "DMS"),
                                   Distance(58.188, "SD"))
    sA11tra = Station(None, PolarObservation('A11', "station"))
    oA11_A10tra = PolarObservation("A10", None, Angle("334-05-41", "DMS"), Angle("83-09-29", "DMS"),
                                   Distance(58.151, "SD"))
    # oA11_A5tra = PolarObservation("A5", None, Angle("326-26-13", "DMS"), Angle("90-00-00", "DMS"),
    #                               Distance(306.233, "SD"))

    plist = Calculation.traverse(
        [[sA5tra, None, oA5_A6tra], [sA6tra, oA6_A5tra, oA6_A7tra], [sA7tra, oA7_A6tra, oA7_A8tra],
         [sA8tra, oA8_A7tra, oA8_A9tra], [sA9tra, oA9_A8tra, oA9_A10tra], [sA10tra, oA10_A9tra, oA10_A11tra],
         [sA11tra, oA11_A10tra, None]])
    if not compare(plist[0], Point('A6', 646373.0539, 276574.6449)):
        print("Test traverse closed at both ends and known bearing at one end failed by point A6")
    if not compare(plist[1], Point('A7', 646402.5093, 276543.3546)):
        print("Test traverse closed at both ends and known bearing at one end failed by point A7")
    if not compare(plist[2], Point('A8', 646431.7631, 276506.1698)):
        print("Test traverse closed at both ends and known bearing at one end failed by point A8")
    if not compare(plist[3], Point('A9', 646452.5118, 276464.6981)):
        print("Test traverse closed at both ends and known bearing at one end failed by point A9")
    if not compare(plist[4], Point('A10', 646477.7451, 276412.9820)):
        print("Test traverse closed at both ends and known bearing at one end failed by point A10")
    if not compare(plist[5], Point('A11', 646502.9712, 276361.0454)):
        print("Test traverse closed at both ends and known bearing at one end failed by point A11")

    # test for polarpoint 3d
    ppp = Point("1", 10, 20, 30)
    ooo = PolarObservation("1", "station", Angle("0", "DMS"), None, None, 1.0)
    sss = Station(ppp, ooo)
    oo2 = PolarObservation("2", None, Angle("90", "DMS"), Angle("45", "DMS"), Distance(20, "SD"), 3.5)
    pp2 = Calculation.polarpoint(sss, oo2)
    if not compare(pp2, Point('2', 24.1421, 20.00000, 41.6421)):
        print("Simple-1 polarpoint 3D test failed")

    ppp = Point("1", 10, 20, 30)
    ooo = PolarObservation("1", "station", Angle("0", "DMS"), None, None, -1.0)
    sss = Station(ppp, ooo)
    oo2 = PolarObservation("2", None, Angle("90", "DMS"), Angle("45", "DMS"), Distance(20, "SD"), 3.5)
    pp2 = Calculation.polarpoint(sss, oo2)
    if not compare(pp2, Point('2', 24.1421, 20.00000, 39.6421)):
        print("Simple-2 polarpoint 3D test failed")

    ppp = Point("1", 10, 20, 30)
    ooo = PolarObservation("1", "station", Angle("0", "DMS"), None, None, 1.0)
    sss = Station(ppp, ooo)
    oo2 = PolarObservation("2", None, Angle("90", "DMS"), Angle("90", "DMS"), Distance(20, "SD"), 3.5)
    pp2 = Calculation.polarpoint(sss, oo2)
    if not compare(pp2, Point('2', 30.0000, 20.0000, 27.5)):
        print("Simple-3 polarpoint 3D test failed")
