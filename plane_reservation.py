#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import sys
import getopt
import logging


class PlaneReservations(object):
    """Plane Reservations class
    """
    PLANE_ROW = [0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0]
    """Plane Row unreserved
    0: Unreserved
    1: Reserved
    2: Aisle
    """

    PLANE_SEAT = {
        'A': 0,
        'B': 1,
        'C': 2,

        'D': 4,
        'E': 5,
        'F': 6,
        'G': 7,

        'H': 9,
        'J': 10,
        'K': 11,
    }

    PLANE_SEAT_INVERSE = {
        0: 'A',
        1: 'B',
        2: 'C',

        4: 'D',
        5: 'E',
        6: 'F',
        7: 'G',

        9:  'H',
        10: 'J',
        11: 'K'
    }

    """Plane Seating in Row.
    Key: Seating Letter
    Value: Index in Plane Row.
    """

    @staticmethod
    def _plane_seats(N):
        """Generate all plane rows into a single list."""
        return PlaneReservations.PLANE_ROW * N

    @staticmethod
    def _seat_index(reservation):
        """Return seat index within Plane row"""
        seat = reservation[-1:]
        assert isinstance(seat, str)
        assert len(seat) == 1
        seat_index = PlaneReservations.PLANE_SEAT.get(seat, None)
        assert seat_index is not None
        return seat_index

    @staticmethod
    def _row_index(reservation, number_of_rows):
        """Return seat index within Plane row"""
        row_index = int(reservation[:-1]) - 1
        assert row_index >= 0
        assert row_index < number_of_rows
        return row_index

    @staticmethod
    def _parse_reservations(N, S):
        """Parse reservation string in list of [Row Index, Seat Index]"""
        return [[PlaneReservations._row_index(res, N), PlaneReservations._seat_index(res)] for res in S.split(" ")]

    @staticmethod
    def _reserve_seats(N, S):
        """Reserve Plane's Seats using expected number of rows and map which seats should be reserved."""
        unreserved_seats = PlaneReservations._plane_seats(N)
        reserved_seats = unreserved_seats[:]
        if len(S) > 0:
            for row, seat in PlaneReservations._parse_reservations(N, S):
                assert isinstance(row, int)
                assert isinstance(seat, int)
                seat_offset = (row * len(PlaneReservations.PLANE_ROW)) + seat
                assert seat_offset < len(reserved_seats)
                reserved_seats[seat_offset] = 1

        return reserved_seats

    @staticmethod
    def _find_max_number_of_grouping(reserved_seats, k):
        """Find the max number of grouping of seats adjacent of length k
        amoung currently reserved seats.
        """
        n = len(reserved_seats)
        count_groups = 0
        i = -1
        while i < n:
            i += 1
            if (i + k) > n:
                break

            if reserved_seats[i] != 0:
                continue

            found = True
            kp = i + k - 1
            while i < kp:
                i += 1
                if reserved_seats[i] != 0:
                    found = False
                    break

            if found:
                count_groups += 1

        return count_groups

    @staticmethod
    def _plane_rows_split(seats):
        """Split list of planes seats by rows.
        """
        seats = ["-" if x == 2 else x for x in seats]
        row_length = len(PlaneReservations.PLANE_ROW)
        return [seats[i:i + row_length] for i in range(0, len(seats), row_length)]

    @staticmethod
    def _plane_rows_pretty_print(rows):
        """Pretty print plain rows with seat reservations
        """
        s = [[str(e) for e in row] for row in rows]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = "\t".join("{{:{}}}".format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return "\n" + "\n".join(table)

    @property
    def number_rows(self):
        return self.__number_rows
    @number_rows.setter
    def number_rows(self, value):
        self.__number_rows = value


    @property
    def verbose(self):
        return self.__verbose
    @verbose.setter
    def verbose(self, value):
        self.__verbose = value

    @property
    def reservations(self):
        return self.__reservations
    @reservations.setter
    def reservations(self, value):
        self.__reservations = value

    @property
    def grouping(self):
        return self.__grouping
    @grouping.setter
    def grouping(self, value):
        self.__grouping = value

    @property
    def logger(self):
        return self.__logger
    @logger.setter
    def logger(self, value):
        self.__logger = value

    def _logger_config(self):
        """Logger config"""
        self.logger = logging.getLogger("Plane Reservation")

        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            '%(asctime)s %(name)-12s %(levelname)-8s %(message)s')

        handler.setFormatter(formatter)
        self.logger.addHandler(handler)

        self.logger.setLevel(logging.INFO)
        if self.verbose:
            self.logger.setLevel(logging.DEBUG)

    #
    # Initialize
    #
    def __init__(self, kw):
        """Initialize
        """
        self.number_rows = kw.get("number-rows")
        self.reservations = kw.get("reservations", "")
        self.grouping = kw.get("grouping", "")
        self.verbose = kw.get("verbose", False)

        self._logger_config()

    def reserve_seats(self):
        """Reserve Seats"""
        self.reserved_seats = PlaneReservations._reserve_seats(self.number_rows, self.reservations)
        self.logger.info("Plane Rows Reserved: {0}".format(
            PlaneReservations._plane_rows_pretty_print(
                PlaneReservations._plane_rows_split(self.reserved_seats)
            )
        )
    )

    def max_grouping(self):
        """Group"""
        max_grouping_count = PlaneReservations._find_max_number_of_grouping(self.reserved_seats , self.grouping)
        self.logger.info("Seat Grouping By {0}: Max Number = {1}".format(self.grouping, max_grouping_count))


def main():
    reservations = ""
    grouping = 1
    usage = ("""Usage: {0} 
        [-v | --verbose] 
        [-h | --help] 
        --number-rows int
        --reservations string 
        --grouping number int 
    --number-rows: Number of Rows [Required]
    --reservations: Seat reservations, example '1F 2A 1G 2E 3D 3F', default '{1}'
    --grouping: Seat grouping, default '{2}'
    """).format(sys.argv[0], reservations, grouping)

    try:
        opts, args = getopt.getopt(
            sys.argv[1:],
            "hv",
            ["help", "verbose", "number-rows=", "reservations=", "grouping="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print(err) # will print something like "option -a not recognized"
        print(usage)
        sys.exit(1)

    kw = {}

    for opt, val in opts:
        if opt in ("-v", "--verbose"):
            kw["verbose"] = True
        elif opt in ("-h", "--help"):
            print(usage)
            sys.exit(0)
        elif opt in ("--number-rows"):
            kw["number-rows"] = int(val)
        elif opt in ("--reservations"):
            kw["reservations"] = str(val)
        elif opt in ("--grouping"):
            kw["grouping"] = int(val)

    if "number-rows" not in kw:
        print("%s: Provide --number-rows" % sys.argv[0])
        print(usage)
        sys.exit(2)
    elif "number-rows" in kw and kw["number-rows"] <= 0:
        print("%s: Provide valid --number-rows" % sys.argv[0])
        print(usage)
        sys.exit(2)

    if "reservations" not in kw:
        kw["reservations"] = reservations
    elif "reservations" in kw and len(kw["reservations"]) == 0:
        print("%s: Provide valid --reservations" % sys.argv[0])
        print(usage)
        sys.exit(2)

    if "grouping" not in kw:
        kw["grouping"] = grouping
    elif "grouping" in kw and kw["grouping"] <= 0:
        print("%s: Provide valid --grouping" % sys.argv[0])
        print(usage)
        sys.exit(2)

    assert "number-rows" in kw
    assert "reservations" in kw
    assert "grouping" in kw
    assert kw["number-rows"] > 0

    plane_reservations = PlaneReservations(kw)
    plane_reservations.reserve_seats()
    plane_reservations.max_grouping()


if __name__ == "__main__":
    main()