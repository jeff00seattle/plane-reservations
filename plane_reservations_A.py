#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import sys
import getopt
import logging


class PlaneReservationsA(object):
    """Plane Reservations class
    Brute force empty seats counting.
    """

    _PLANE_ROW = [0, 0, 0, 2, 0, 0, 0, 0, 2, 0, 0, 0]
    """Plane Row unreserved.
    0: Unreserved
    1: Reserved
    2: Aisle
    """

    _ROW_SEAT_INDEX = {

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
    """Plane Seat index based only layout of _PLANE_ROW.
    Key: Seating Letter
    Value: Seat Index in Plane Row.
    """

    @classmethod
    def _generate_plane_seats(cls, N):
        """Generate all plane rows into a single list."""
        return cls._PLANE_ROW * N

    @staticmethod
    def _row_index(res, number_of_rows):
        """Return seat index within Plane row"""
        row_index = int(res[:-1]) - 1
        assert row_index >= 0
        assert row_index < number_of_rows
        return row_index

    @classmethod
    def _row_seat_index(cls, res):
        """Return seat index within Plane row"""
        seat = res[-1:]
        assert isinstance(seat, str)
        assert len(seat) == 1
        row_seat_index = cls._ROW_SEAT_INDEX.get(seat, None)
        assert row_seat_index is not None
        return row_seat_index

    @classmethod
    def _parse_reservations_generator(cls, N, S):
        """Parse reservation string into a generator
        of dictionary { "row": [Row Index], "seat": [Row Seat Index]}.
        """
        return (
            {
                "row_index": cls._row_index(res, N),
                "seat_index": cls._row_seat_index(res)
            } for res in S.split(" ")
        )

    @classmethod
    def _get_row_seat_offset(cls, res):
        row_index = res.get("row_index", None)
        assert row_index is not None
        assert isinstance(row_index, int)
        assert row_index >= 0

        row_seat_index = res.get("seat_index", None)
        assert row_seat_index is not None
        assert isinstance(row_seat_index, int)
        assert row_seat_index >= 0

        row_seat_offset = (row_index * len(cls._PLANE_ROW)) + row_seat_index
        assert row_seat_offset >= 0
        return row_seat_offset

    @classmethod
    def _reserve_seats(cls, N, S):
        """Reserve Plane's Seats using expected number of rows and map which seats should be reserved."""
        unreserved_seats = cls._generate_plane_seats(N)
        reserved_seats = unreserved_seats[:]
        if len(S) > 0:
            for res in cls._parse_reservations_generator(N, S):
                row_seat_offset = cls._get_row_seat_offset(res)
                assert row_seat_offset < len(reserved_seats)
                reserved_seats[row_seat_offset] = 1

        return reserved_seats

    @classmethod
    def _find_max_number_of_grouping(cls, reserved_seats, k):
        """Find the max number of grouping of seats adjacent of length k
        amoung currently reserved seats.
        """
        # print(reserved_seats)
        n = len(reserved_seats)
        count_groups = 0
        count_empty_contigous_seats = 0
        i = 0
        while i < n:
            if reserved_seats[i] != 0:
                # print('continue', i)
                count_empty_contigous_seats = 0
                i += 1
                continue

            count_empty_contigous_seats += 1
            # print('empty', i, count_empty_contigous_seats)
            if count_empty_contigous_seats >= k:
                count_groups += 1
                # print('found', i, count_groups)

            if ((i + 1) % len(cls._PLANE_ROW)) == 0:
                # print('new row', i)
                count_empty_contigous_seats = 0

            i += 1

        return count_groups

    @classmethod
    def _pretty_print_plane_seats(cls, seats):
        """Split list of planes seats by rows.
        """
        seats = ["-" if x == 2 else x for x in seats]
        row_length = len(cls._PLANE_ROW)
        return [seats[i:i + row_length] for i in range(0, len(seats), row_length)]

    @staticmethod
    def _pretty_print_2d_array(rows):
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
        cls = self.__class__
        self.reserved_seats = cls._reserve_seats(self.number_rows, self.reservations)
        self.logger.info("Plane Rows Reserved: {0}".format(
            cls._pretty_print_2d_array(
                cls._pretty_print_plane_seats(self.reserved_seats)
            )
        )
    )

    def max_grouping(self):
        """Group"""
        cls = self.__class__
        max_grouping_count = cls._find_max_number_of_grouping(self.reserved_seats , self.grouping)
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

    plane_reservations = PlaneReservationsA(kw)
    plane_reservations.reserve_seats()
    plane_reservations.max_grouping()


if __name__ == "__main__":
    main()