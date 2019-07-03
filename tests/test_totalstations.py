# Copyright (c) 2019 GeoSpark
#
# Released under the MIT License (MIT)
# See the LICENSE file, or visit http://opensource.org/licenses/MIT
from totalstations import Idex, Dump, SurvCE, Stonex, LeicaGsi, JobAre, Sdr


def test_totalstations():
    """
        unit test
    """
    import sys
    import os

    if len(sys.argv) > 1:
        # maps extensions to classes; first item in list is the class
        # and second, if present, is second argument for class
        # constructor
        ext2class = {
            '.idx': [Idex],
            '.dmp': [Dump],
            '.rw5': [SurvCE],
            '.dat': [Stonex],
            '.gsi': [LeicaGsi, ' '],
            '.job': [JobAre, '='],
            '.crd': [Sdr, None]
        }
        # find the class
        try:
            toexec = ext2class[os.path.splitext(sys.argv[1])[1].lower()]
        except KeyError:
            print('Unknown extension for file', sys.argv[1])
            sys.exit(1)

        if len(sys.argv) == 3:
            # the user may provide an argument to pass to the class
            ts = toexec[0](sys.argv[1], sys.argv[2])
        elif len(toexec) == 1:
            # no default for second argument
            ts = toexec[0](sys.argv[1])
        else:
            # there is a default second argument
            ts = toexec[0](sys.argv[1], toexec[1])
    else:
        ts = Idex('samples/test.idx')
        # ts = Dump('samples/xxx.dmp')
        # ts = SurvCE('samples/EBO-1739.rw5')
        # ts = Stonex('samples/PAJE2OB.DAT')
        # ts = LeicaGsi('samples/tata3.gsi', ' ')
        # ts = JobAre('samples/test1.job', '=')
        # ts = Sdr('samples/PAJE04.crd', None)

    if ts.open() != 0:
        print("Open error")
    else:
        while True:
            r = ts.parse_next()
            if r is None:
                break
            if len(r) > 0:
                print(r)
        ts.close()
