#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
.. module: calculation
    :platform: Linux, Windows
    :synopsis: pure calculation class

.. moduleauthor::Zoltan Siki <siki@agt.bme.hu>

"""
# noinspection PyUnresolvedReferences
from qgis.core import QgsMessageLog, Qgis

from . import config
from .base_classes import *
from .resultlog import *


class Calculation(object):
    """ Container class for calculations. Pure static class.
    """

    def __init__(self):
        pass

    @staticmethod
    def orientation(st, ref_list):
        """ Orientation calculation for a station

            :param st: station (Station)
            :param ref_list: list of [Point, PolarObservation] lists
            :returns: average orientation angle (Angle) None if no reference direction at all or in case of error
        """
        try:
            sz = 0
            cz = 0
            sd = 0
            for ref in ref_list:
                pt = ref[0]
                obs = ref[1]
                b = bearing(st.p, pt).get_angle()
                r = obs.hz.get_angle()
                z = b - r
                if z < 0:
                    z = z + math.pi * 2
                d = distance2d(st.p, pt).d
                sd = sd + d
                sz = sz + math.sin(z) * d
                cz = cz + math.cos(z) * d
                ref.append(d)
                ref.append(Angle(z))
                ref.append(Angle(r))
                ref.append(Angle(b))

            if sd == 0:
                raise ValueError('Total distance is 0')

            sz = sz / sd
            cz = cz / sd
            # Calculate average orient angle.
            za = math.atan2(sz, cz)
            while za < 0:
                za = za + math.pi * 2
        except (ValueError, TypeError, AttributeError) as e:
            raise e

        ret = []

        for ref in ref_list:
            e = ref[3].get_angle('SEC') - Angle(za).get_angle('SEC')
            if e > PISEC:
                e = e - 2 * PISEC
            if e < -PISEC:
                e = e + 2 * PISEC
            E = e / RO * ref[2]

            if ANGLE_UNITS_DISP[config.angle_displayed] in ('DEG', 'DMS'):
                pass
            elif ANGLE_UNITS_DISP[config.angle_displayed] == 'GON':
                e = Angle(e, 'SEC').get_angle('GON')
                e *= 10000.0
            elif ANGLE_UNITS_DISP[config.angle_displayed] == 'RAD':
                e = Angle(e, 'SEC').get_angle('RAD')

            ret.append((ref[1].point_id, (ref[1].pc if ref[1].pc is not None else "-"),
                        ref[4].get_angle(ANGLE_UNITS_DISP[config.angle_displayed]),
                        ref[5].get_angle(ANGLE_UNITS_DISP[config.angle_displayed]),
                        ref[3].get_angle(ANGLE_UNITS_DISP[config.angle_displayed]), ref[2], e, E))
        return Angle(za), ret

    @staticmethod
    def polarpoint(st, obs):
        """ Calculate coordinates of a point measured by an independent radial measurement

            :param st: station (Station)
            :param obs: observation from station to the unknown point (PolarObservation)
            :returns: the polar point with new coordinates (Point)
        """
        try:
            # Calculate the bearing angle between the station and new point.
            b = st.o.hz.get_angle() + obs.hz.get_angle()
            # Calculate the coordinates of the new point.
            e = st.p.e + obs.horiz_dist() * math.sin(b)
            n = st.p.n + obs.horiz_dist() * math.cos(b)
            if st.p.z is not None and st.o.th is not None and obs.v is not None:
                z = st.p.z + st.o.th + obs.d.d * math.cos(obs.v.get_angle())
                if obs.th is not None:
                    z = z - obs.th
            else:
                z = None

            p = Point(obs.point_id, e, n, z, obs.pc, obs.pt)
            ret = (p.id, (p.pc if p.pc is not None else "-"), p.e, p.n, p.z,
                   Angle(b).get_angle(ANGLE_UNITS_DISP[config.angle_displayed]), obs.horiz_dist())

            return p, ret
        except (ValueError, TypeError, AttributeError) as e:
            raise e

    @staticmethod
    def intersection(s1, obs1, s2, obs2):
        """ Calculate intersection

            :param s1: station 1 (Station)
            :param obs1: observation from station 1 (PolarObservation)
            :param s2: station 2 (Station)
            :param obs2: observation from station 2 (PolarObservation)
            :returns: intersection point (Point)
        """
        # If the two observation are the same.
        if obs1.point_id != obs2.point_id:
            return None, None
        # Calculate the two bearing angles of two observations.
        b1 = s1.o.hz.get_angle() + obs1.hz.get_angle()
        b2 = s2.o.hz.get_angle() + obs2.hz.get_angle()
        # Calculate an intersection point of two lines. If the two lines are parallels the function returns None object
        pp = intersecLL(s1.p, s2.p, b1, b2)
        if pp is None:
            return None, None

        if obs1.pc is None:
            pc = obs2.pc
        else:
            pc = obs1.pc
        pp.id = obs1.point_id
        pp.pc = pc

        return pp, (pp.id, (pp.pc if pp.pc is not None else "-"), pp.e, pp.n,
                    Angle(b1).get_angle(ANGLE_UNITS_DISP[config.angle_displayed]),
                    Angle(b2).get_angle(ANGLE_UNITS_DISP[config.angle_displayed]))

    @staticmethod
    def resection(st, p1, p2, p3, obs1, obs2, obs3):
        """ Calculate resection

            :param st: station (Station)
            :param p1: first control point (Point)
            :param p2: second control point (Point)
            :param p3: third control point (Point)
            :param obs1: observation from st to p1 (PolarObservation)
            :param obs2: observation from st to p2 (PolarObservation)
            :param obs3: observation from st to p3 (PolarObservation)
            :returns: coordinates of the resection point (Point) if it can be calculated; otherwise None
        """
        try:
            # Calculate angle between obs1 and obs2 and between obs2 and obs3.
            alpha = Angle(obs2.hz.get_angle() - obs1.hz.get_angle())
            beta = Angle(obs3.hz.get_angle() - obs2.hz.get_angle())

            # Create a circle on points p1 and p2 and alpha.
            circ1 = Circle(p1, p2, alpha)
            # Create a circle on points p2 and p3 and beta.
            circ2 = Circle(p2, p3, beta)
            # Calculate the intersection of two circles.
            try:
                points = intersecCC(circ1, circ2)
            except AttributeError as e:
                raise e

            # IntersectCC functions can return with zero or two intersection points.
            # If the number of intersection point is zero the resection method return None object.
            if len(points) == 2:
                #  Select the right one from the two intersection points.
                if math.fabs(p2.e - points[0].e) < 0.1 and math.fabs(p2.n - points[0].n) < 0.1:
                    p = Point(st.p.id, points[1].e, points[1].n, st.p.z, st.p.pc, st.p.pt)
                else:
                    p = Point(st.p.id, points[0].e, points[0].n, st.p.z, st.p.pc, st.p.pt)

                rows = list()

                rows.append((obs1.point_id, (obs1.pc if obs1.pc is not None else "-"), p1.e, p1.n,
                             obs1.hz.get_angle(ANGLE_UNITS_DISP[config.angle_displayed]),
                             alpha.get_angle(ANGLE_UNITS_DISP[config.angle_displayed])))
                rows.append((obs2.point_id, (obs2.pc if obs2.pc is not None else "-"), p2.e, p2.n,
                             obs2.hz.get_angle(ANGLE_UNITS_DISP[config.angle_displayed]),
                             beta.get_angle(ANGLE_UNITS_DISP[config.angle_displayed])))
                rows.append((obs3.point_id, (obs3.pc if obs3.pc is not None else "-"), p3.e, p3.n,
                             obs3.hz.get_angle(ANGLE_UNITS_DISP[config.angle_displayed]), ''))
                rows.append((p.id, (p.pc if p.pc is not None else "-"), p.e, p.n, '', ''))
                return p, rows
            else:
                raise IndexError('There must be exactly two points')
        except (ValueError, TypeError) as e:
            raise e

    @staticmethod
    def traverse(trav_obs, forceFree=False):
        """ Calculate traverse line. This method can compute the following types of travesres

            1. open traverse (free): originates at a known position with known bearings and ends at an unknown position
            2. closed traverse at both ends and the start point has known bearings
            3. closed traverse at both ends and both endpoints has known bearings
            4. inserted traverse: closed at both ends but no bearings

            :param trav_obs: a list of sublists consists of a Point and two PolarObservations, If the station member is
             not None the point is a station. Start point must have coordinates in case of type 1-4 and end points must
             have coordinates in case of type 2-4.  Two observations are needed at the angle points. At the start point
             the second observation is required in case of type 1-3. At the end point the first observation is required
             in case of type 3.
            :param forceFree: force free traverse calculation (Boole)
            :returns: a list of points which's coordinates has been computed.
        """
        ResultLog.resultlog_message = ""
        n = len(trav_obs)
        # at least 3 points must be
        if n < 3:
            ResultLog.resultlog_message += \
                tr("Error: At least 3 points must be added to traverse line!") + "\n"
            return None
        # start point and end point
        startp = trav_obs[0][0]
        endp = trav_obs[n - 1][0]
        # no coord for startpoint
        if startp is None or startp.p is None or startp.p.e is None or startp.p.n is None:
            ResultLog.resultlog_message += \
                tr("Error: No coordinates on start point!") + "\n"
            return None

        free = False
        if forceFree is True:
            # force to calculate free traverse (for node)
            free = True
            endp.p.e = None
            endp.p.n = None
        elif endp is None or endp.p is None or endp.p.e is None or endp.p.n is None:
            # no coordinate for endpoint
            ResultLog.resultlog_message += \
                tr("Warning: No coordinates for end point -> Free traverse.") + "\n"
            free = True  # free traverse

        # collect measurements in traverse
        beta = [None] * n
        t = [None] * n
        t1 = [None] * n
        t2 = [None] * n

        for i in range(0, n):
            st = trav_obs[i][0]
            obsprev = trav_obs[i][1]
            obsnext = trav_obs[i][2]
            if i == 0:
                beta[0] = st.o.hz
                if beta[0] is None:
                    # no orientation on start
                    if free is True:
                        ResultLog.resultlog_message += \
                            tr("Error: No orientation on start point and no coordinates on end point!") + "\n"
                        return None
                    else:
                        ResultLog.resultlog_message += \
                            tr("Warning: No orientation on start point - inserted traverse.") + "\n"

            if i == n - 1:
                beta[i] = st.o.hz
                if beta[i] is None:
                    # no orientation on end
                    ResultLog.resultlog_message += \
                        tr("Warning: No orientation on end point.") + "\n"

            if i != 0 and i != n - 1 and (
                    obsprev is None or obsnext is None or obsprev.hz is None or obsnext.hz is None):
                # no angle at angle point
                ResultLog.resultlog_message += \
                    tr("Error: No angle at point %s!") % trav_obs[i][0].p.id + "\n"
                return None

            if i == 0:
                # there was orientation on first
                if beta[0] is not None and obsnext is not None and obsnext.hz is not None:
                    beta[0].set_angle(beta[0].get_angle() + obsnext.hz.get_angle())
                else:
                    beta[0] = None
            elif i == n - 1:
                if beta[i] is not None and beta[0] is not None and obsprev is not None and obsprev.hz is not None:
                    # there was orientation on last and first
                    beta[i].set_angle(math.pi * 2 - (beta[i].get_angle() + obsprev.hz.get_angle()))
                else:
                    beta[i] = None
            else:
                beta[i] = Angle(obsnext.hz.get_angle() - obsprev.hz.get_angle())

            if beta[i] is not None:
                while beta[i].get_angle() > math.pi * 2:
                    beta[i].set_angle(beta[i].get_angle() - math.pi * 2)
                while beta[i].get_angle() < 0:
                    beta[i].set_angle(beta[i].get_angle() + math.pi * 2)

            if obsprev is not None and obsprev.d is not None:
                if t[i] is not None:
                    # save distance for output
                    t1[i] = Distance(obsprev.horiz_dist(), "HD")
                    t2[i] = t[i]
                    t[i] = Distance((t[i].d + obsprev.horiz_dist()) / 2.0, "HD")
                else:
                    t[i] = Distance(obsprev.horiz_dist(), "HD")
            elif i > 0 and t[i] is None:
                # no distance between points
                ResultLog.resultlog_message += \
                    tr("Error: No distance between points %s and %s!") % \
                    (trav_obs[i - 1][0].p.id, trav_obs[i][0].p.id) + "\n"
                return None

            if obsnext is not None and obsnext.d is not None:
                t[i + 1] = Distance(obsnext.horiz_dist(), "HD")

        if forceFree is True:
            beta[n - 1] = None

        # calculate sum of betas if we have both orientation
        if beta[0] is not None and beta[n - 1] is not None:
            sumbeta = 0.0  # in radians
            for i in range(0, n):
                sumbeta = sumbeta + beta[i].get_angle()
            # calculate angle error
            dbeta = (n - 1) * math.pi - sumbeta  # in radians
            while dbeta > math.pi:
                dbeta = dbeta - 2 * math.pi
            while dbeta < -math.pi:
                dbeta = dbeta + 2 * math.pi
        else:
            sumbeta = 0.0
            dbeta = 0.0

        # angle corrections
        w = 0.0  # in seconds
        vbeta = [0.0] * n  # in seconds
        for i in range(0, n):
            vbeta[i] = dbeta / n
            w = w + vbeta[i]

        #    calculate bearings and de & dn for sides
        delta = [0.0] * n  # in radians
        sumde = 0.0
        sumdn = 0.0
        sumt = 0.0
        de = [0.0] * n
        dn = [0.0] * n
        for i in range(1, n):
            j = i - 1
            if j == 0:
                if beta[j] is not None:
                    d = delta[j] + beta[j].get_angle() + vbeta[j]
                else:
                    # find orientation for first side "beillesztett"
                    d = 0
                    sumde = 0
                    sumdn = 0
                    for k in range(1, n):
                        de[k] = t[k].d * math.sin(d)
                        dn[k] = t[k].d * math.cos(d)
                        sumde = sumde + de[k]
                        sumdn = sumdn + dn[k]
                        if k < n - 1:
                            d = d + beta[k].get_angle() - math.pi

                    d = bearing(Point("@", endp.p.e, endp.p.n), Point("@", startp.p.e, startp.p.n)).get_angle() - \
                        bearing(Point("@", sumde, sumdn), Point("@", 0, 0)).get_angle()
                    sumde = 0
                    sumdn = 0
            else:
                d = delta[j] + beta[j].get_angle() + vbeta[j] - math.pi

            while d < 0:
                d = d + math.pi * 2
            while d > math.pi * 2:
                d = d - math.pi * 2
            delta[i] = d
            de[i] = t[i].d * math.sin(d)
            dn[i] = t[i].d * math.cos(d)
            sumde = sumde + de[i]
            sumdn = sumdn + dn[i]
            sumt = sumt + t[i].d

        #    calculate de & dn error
        if free is True:
            dde = 0  # free traverse
            ddn = 0
            ddist = 0
        else:
            dde = endp.p.e - startp.p.e - sumde
            ddn = endp.p.n - startp.p.n - sumdn
            ddist = math.hypot(dde, ddn)  # linear error

        #    calculate final coords
        ve = [0.0] * n
        vn = [0.0] * n
        ee = [0.0] * n
        nn = [0.0] * n
        we = dde / sumt
        wn = ddn / sumt
        ee[0] = startp.p.e
        nn[0] = startp.p.n
        for i in range(1, n):
            ve[i] = t[i].d * we
            vn[i] = t[i].d * wn
            ee[i] = ee[i - 1] + de[i] + ve[i]
            nn[i] = nn[i - 1] + dn[i] + vn[i]

        for i in range(0, n):
            pcode = (trav_obs[i][0].p.pc if trav_obs[i][0].p is not None and trav_obs[i][0].p.pc is not None else "-")
            t_1 = "%8.3f" % t1[i].d if t1[i] is not None else "-"
            t_2 = "%8.3f" % t2[i].d if t2[i] is not None else "-"
            ResultLog.resultlog_message += "           %10.4f %8s\n" % (delta[i] * 200 / math.pi, t_1)

            if i > 0:
                if beta[i] is None:
                    ResultLog.resultlog_message += u"%-10s %10s %8.3f %8.3f %8.3f %10.3f %10.3f\n" % \
                                                   ((trav_obs[i][0].p.id if trav_obs[i][0].p is not None else "-"), "",
                                                    t[i].d,
                                                    de[i], dn[i], de[i] + ve[i], dn[i] + vn[i])
                else:
                    ResultLog.resultlog_message += u"%-10s %-14s %8.3f %8.3f %8.3f %10.3f %10.3f\n" % \
                                                   ((trav_obs[i][0].p.id if trav_obs[i][0].p is not None else "-"),
                                                    beta[i].get_angle(ANGLE_UNITS_DISP[config.angle_displayed]), t[i].d,
                                                    de[i], dn[i], de[i] + ve[i], dn[i] + vn[i])
            else:
                if beta[i] is None:
                    ResultLog.resultlog_message += u"%-10s %10s\n" % \
                                                   (trav_obs[i][0].p.id, "")
                else:
                    ResultLog.resultlog_message += u"%-10s %-14s\n" % \
                                                   (trav_obs[i][0].p.id,
                                                    beta[i].get_angle(ANGLE_UNITS_DISP[config.angle_displayed]))

            if i > 0:
                if free is True:
                    w1 = "-"
                    w2 = "-"
                else:
                    w1 = "%8.3f" % ve[i]
                    w2 = "%8.3f" % vn[i]
                if beta[0] is None or beta[n - 1] is None:
                    ResultLog.resultlog_message += u"%-10s %10s %8s %8s %8s %10.3f %10.3f\n" % \
                                                   (pcode, "", t_2, w1, w2, ee[i], nn[i])
                else:
                    ResultLog.resultlog_message += u"%-10s %10.4f %8s %8.3f %8.3f %10.3f %10.3f\n" % \
                                                   (pcode, vbeta[i] * 200 / math.pi, t_2, ve[i], vn[i], ee[i], nn[i])
            else:
                if beta[0] is None or beta[n - 1] is None:
                    ResultLog.resultlog_message += u"%-10s %10s                            %10.3f %10.3f\n" % \
                                                   (pcode, "", ee[i], nn[i])
                else:
                    ResultLog.resultlog_message += u"%-10s %10.4f                            %10.3f %10.3f\n" % \
                                                   (pcode, vbeta[i] * 200 / math.pi, ee[i], nn[i])
            pass

        ResultLog.resultlog_message += "\n"
        if beta[0] is None or beta[n - 1] is None:
            ResultLog.resultlog_message += "           %10s                            %10.3f %10.3f\n" % \
                                           ("", ee[n - 1] - ee[0], nn[n - 1] - nn[0])
            ResultLog.resultlog_message += "           %10s %8.3f %8.3f %8.3f\n\n" % \
                                           ("", sumt, sumde, sumdn)
            if not free:
                ResultLog.resultlog_message += "           %10s          %8.3f %8.3f\n" % ("", dde, ddn)
        else:
            ResultLog.resultlog_message += "           %-14s                            %10.3f %10.3f\n" % \
                                           (Angle(0).get_angle(ANGLE_UNITS_DISP[config.angle_displayed]),
                                            ee[n - 1] - ee[0], nn[n - 1] - nn[0])
            ResultLog.resultlog_message += "           %10.4f %8.3f %8.3f %8.3f\n" % \
                                           (sumbeta * 200.0 / math.pi, sumt, sumde, sumdn)
            ResultLog.resultlog_message += "           %10.4f\n" % \
                                           ((n - 1) * 200)
            ResultLog.resultlog_message += "           %10.4f          %8.3f %8.3f\n" % \
                                           (dbeta * 200 / math.pi, dde, ddn)
        if not free:
            ResultLog.resultlog_message += "                                   %8.3f\n" % ddist

        if free is True:
            last = n
        else:
            last = n - 1
        plist = []  # list of calculated points
        for i in range(1, last):

            if trav_obs[i][0] is not None and trav_obs[i][0].p is not None:
                plist.append(trav_obs[i][0].p)
            else:
                plist.append(Point(trav_obs[i][0].o.point_id))
            plist[-1].e = ee[i]
            plist[-1].n = nn[i]

        return plist

    @staticmethod
    def gauss_elimination(a, b):
        """ Solve a linear equation system::
                a * x = b

            :param a: coefficients of the equation system (list of lists)
            :param b: list of pure term of equations
            :returns: (unknowns, inverse_matrix)
        """
        size = len(b)
        for i in range(0, size):
            q = 1.0 / a[i][i]
            for k in range(0, size):
                if i != k:
                    a[i][k] = q * a[i][k]
                else:
                    a[i][k] = q

            b[i] = q * b[i]
            for j in range(0, size):
                if j != i:
                    t = a[j][i]
                    for k in range(0, size):
                        if i != k:
                            a[j][k] = a[j][k] - t * a[i][k]
                        else:
                            a[j][k] = -t * q
                    b[j] = b[j] - t * b[i]
        return b, a

    @staticmethod
    def orthogonal_transformation(plist):
        """ Calculate parameters of orthogonal transformation. Four parameters scale, rotation and offset.::
            E = E0 + c * e - d * n
            N = N0 + d * e + c * n

            :param plist: a list of common points used in the transormation plist[i]==[srci,desti]
            :returns: the list of transformation parameters {E0 N0 c d}
        """
        es = 0.0  # sum of source coordinates
        ns = 0.0
        Es = 0.0  # sum of destination coordinates
        Ns = 0.0
        for p in plist:
            es = es + p[0].e
            ns = ns + p[0].n
            Es = Es + p[1].e
            Ns = Ns + p[1].n

        ew = es / float(len(plist))
        nw = ns / float(len(plist))
        Ew = Es / float(len(plist))
        Nw = Ns / float(len(plist))

        s1 = 0.0  # sum of ei*Ei+ni*Ni
        s2 = 0.0  # sum of ei*Ni-ni*Ei
        s3 = 0.0  # sum of ei*ei+ni*ni

        for p in plist:
            e = p[0].e - ew
            n = p[0].n - nw
            E = p[1].e - Ew
            N = p[1].n - Nw
            s1 = s1 + e * E + n * N
            s2 = s2 + e * N - n * E
            s3 = s3 + e * e + n * n

        c = s1 / s3
        d = s2 / s3
        E0 = (Es - c * es + d * ns) / float(len(plist))
        N0 = (Ns - c * ns - d * es) / float(len(plist))
        return [E0, N0, c, d]

    @staticmethod
    def orthogonal3tr(plist):
        """ Calculate parameters of orthogonal transformation. Three parameters::
            E = E0 + cos(alpha) * e - sin(alpha) * n
            N = N0 + sin(alpha) * e + cos(alpha) * n

            :param plist: a list of common points used in the transormation plist[i]==[srci,desti]
            :returns: the list of transformation parameters {E0 N0 alpha}
        """
        # approximate values from Helmert4
        appr = Calculation.orthogonal_transformation(plist)
        E0 = appr[0]
        N0 = appr[1]
        alpha = math.atan2(appr[3], appr[2])

        # calculate sums
        s1 = 0.0  # -ei*sin(alpha) - ni*cos(alpha)
        s2 = 0.0  # ei*cos(alpha) - ni*sin(alpha)
        s3 = 0.0  # (-ei*sin(alpha) - ni*cos(alpha))^2 + \
        # ( ei*cos(alpha) - ni*sin(alpha))^2
        s4 = 0.0  # Ei - Eei
        s5 = 0.0  # Ni - Nei
        s6 = 0.0  # (-ei*sin(alpha) - ni*cos(alpha)) * (Ei-Eei) +
        # ( ei*cos(alpha) - ni*sin(alpha)) * (Ni-Nei)

        for p in plist:
            e = p[0].e
            n = p[0].n
            E = p[1].e
            N = p[1].n
            w1 = -e * math.sin(alpha) - n * math.cos(alpha)
            w2 = e * math.cos(alpha) - n * math.sin(alpha)
            s1 = s1 + w1
            s2 = s2 + w2
            s3 = s3 + w1 * w1 + w2 * w2

            w3 = E - (E0 + e * math.cos(alpha) - n * math.sin(alpha))
            w4 = N - (N0 + e * math.sin(alpha) + n * math.cos(alpha))
            s4 = s4 + w3
            s5 = s5 + w4
            s6 = s6 + w1 * w3 + w2 * w4

        # set matrix of normal equation
        ata = []
        ata[0][0] = len(plist)
        ata[0][1] = 0.0
        ata[0][2] = s1
        ata[1][0] = 0.0
        ata[1][1] = len(plist)
        ata[1][2] = s2
        ata[2][0] = s1
        ata[2][1] = s2
        ata[2][2] = s3
        # set A*l
        al = []
        al[0] = s4
        al[1] = s5
        al[2] = s6
        # solve the normal equation
        Calculation.gauss_elimination(ata, al)

        return [E0 + al[0], N0 + al[1], alpha + al[2]]

    @staticmethod
    def affine_transformation(plist):
        """ Calculate parameters of affine transformation. Six parameters::
            E = E0 + a * e + b * n
            N = N0 + c * e + d * n

            :param plist: a list of common points used in the transormation plist[i]==[srci,desti]
            :returns: the list of transformation parameters {E0 N0 a b c d}
        """
        # calculate weight point in point list
        es = 0.0  # sum of source coordinates
        ns = 0.0
        Es = 0.0  # sum of destination coordinates
        Ns = 0.0
        for p in plist:
            es = es + p[0].e
            ns = ns + p[0].n
            Es = Es + p[1].e
            Ns = Ns + p[1].n

        ew = es / float(len(plist))
        nw = ns / float(len(plist))
        Ew = Es / float(len(plist))
        Nw = Ns / float(len(plist))

        s1 = 0.0  # sum of ei*ei
        s2 = 0.0  # sum of ni*ni
        s3 = 0.0  # sum of ei*ni
        s4 = 0.0  # sum of ei*Ei
        s5 = 0.0  # sum of ni*Ei
        s6 = 0.0  # sum of ei*Ni
        s7 = 0.0  # sum of ni*Ni
        for p in plist:
            e = p[0].e - ew
            n = p[0].n - nw
            E = p[1].e - Ew
            N = p[1].n - Nw
            s1 = s1 + e * e
            s2 = s2 + n * n
            s3 = s3 + e * n
            s4 = s4 + e * E
            s5 = s5 + n * E
            s6 = s6 + e * N
            s7 = s7 + n * N

        w = float(s1 * s2 - s3 * s3)
        a = -(s5 * s3 - s4 * s2) / w
        b = -(s4 * s3 - s1 * s5) / w
        c = -(s7 * s3 - s6 * s2) / w
        d = -(s6 * s3 - s7 * s1) / w
        E0 = (Es - a * es - b * ns) / float(len(plist))
        N0 = (Ns - c * es - d * ns) / float(len(plist))
        return [E0, N0, a, b, c, d]

    @staticmethod
    def polynomial_transformation(plist, degree=3):
        """ Calculate parameters of polynomial (rubber sheet) transformation.::
            X = X0 + a1 * x + a2 * y + a3 * xy + a4 * x^2 + a5 * y^2 + ...
            Y = Y0 + b1 * x + b2 * y + b3 * xy + b4 * x^2 + b5 * y^2 + ...

            :param plist: a list of common points used in the transformation plist[i]==[srci,desti]
            :param degree: degree of transformation 3/4/5
            :returns: the list of parameters X0 Y0 a1 b1 a2 b2 a3 b3 ... and the weight point coordinates in source
             and target system
        """
        # set up A matrix (a1 for e, a2 for n)
        np = len(plist)  # number of points
        m = (degree + 1) * (degree + 2) // 2  # number of unknowns
        # calculate average x and y to reduce rounding errors
        s1 = 0.0
        s2 = 0.0
        S1 = 0.0
        S2 = 0.0
        for p in plist:
            e = p[0].e
            n = p[0].n
            s1 = s1 + e
            s2 = s2 + n
            E = p[1].e
            N = p[1].n
            S1 = S1 + E
            S2 = S2 + N
        avge = s1 / np
        avgn = s2 / np
        avgE = S1 / np
        avgN = S2 / np
        i = 0
        a1 = [[0.0] * m] * np
        a2 = [[0.0] * m] * np
        l1 = [0.0] * np
        l2 = [0.0] * np
        for p in plist:
            e = p[0].e - avge
            n = p[0].n - avgn
            E = p[1].e - avgE
            N = p[1].n - avgN
            ll = 0
            for j in range(0, degree + 1):
                for k in range(0, degree + 1):
                    if j + k <= degree:
                        a1[i][ll] = math.pow(e, k) * math.pow(n, j)
                        a2[i][ll] = math.pow(e, k) * math.pow(n, j)
                        ll += 1
            l1[i] = E
            l2[i] = N
            i += 1

        # set matrix of normal equation
        # N1 = a1T*a1, N2 = a2T * a2, n1 = a1T * l1, n2 = a2T * l2
        N1 = [[0.0] * m] * m
        N2 = [[0.0] * m] * m
        n1 = [0.0] * m
        n2 = [0.0] * m
        for i in range(0, m):
            for j in range(i, m):
                s1 = 0.0
                s2 = 0.0
                for k in range(0, np):
                    s1 = s1 + a1[k][i] * a1[k][j]
                    s2 = s2 + a2[k][i] * a2[k][j]
                N1[i][j] = s1
                N1[j][i] = s1
                N2[i][j] = s2
                N2[j][i] = s2
        for i in range(0, m):
            s1 = 0.0
            s2 = 0.0
            for k in range(0, np):
                s1 = s1 + a1[k][i] * l1[k]
                s2 = s2 + a2[k][i] * l2[k]
            n1[i] = s1
            n2[i] = s2

        # solve the normal equation
        (x1, inv1) = Calculation.gauss_elimination(N1, n1)
        (x2, inv2) = Calculation.gauss_elimination(N2, n2)
        return x1, x2, [avge, avgn, avgE, avgN]
