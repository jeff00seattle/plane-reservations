#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#

import sys
import getopt
import logging


class PlaneReservationsB(object):
    """Plane Reservations class
    Count by available seat sections.
    """
    _PLANE_ROW = [[0, 0, 0], [0, 0, 0, 0], [0, 0, 0]]
    """Plane Row
    Each row has 3 sections separated by aisles:
    + [A][B][C]     -- 3 Seats available
    + [D][E][F][G]  -- 4 Seats available
    + [H][J][K]     -- 3 Seats available
    """

    _PLANE_ROW_SECTION_INDEX = {
        'A': 0,
        'B': 0,
        'C': 0,

        'D': 1,
        'E': 1,
        'F': 1,
        'G': 1,

        'H': 2,
        'J': 2,
        'K': 2,
    }
    """Plane Section in Row.
    Key: Seating Letter
    Value: Section Index in Plane Row.
    """

    _PLANE_ROW_SECTION_SEAT_INDEX = {
        'A': 0,
        'B': 1,
        'C': 2,

        'D': 0,
        'E': 1,
        'F': 2,
        'G': 3,

        'H': 0,
        'J': 1,
        'K': 2,
    }
    """Plane Seat in Row Section.
    Key: Seating Letter
    Value: Seat Index in Plane Row Section.
    """

    @classmethod
    def _generate_plane_sections(cls, N):
        """Generate all plane rows into a single list."""
        plane_sections = []
        for _ in range(N):
            for section in cls._PLANE_ROW:
                plane_sections.append(list(section))
        return plane_sections

    @staticmethod
    def _row_index(res, number_of_rows):
        """Return seat index within Plane row"""
        row = int(res[:-1])
        row_index = row - 1
        # print(row, row_index, number_of_rows)
        assert row_index >= 0
        assert row_index < number_of_rows
        return row_index

    @classmethod
    def _row_section_index(cls, res):
        """Return seat index within Plane row"""
        seat = res[-1:]
        assert isinstance(seat, str)
        assert len(seat) == 1
        row_section_index = cls._PLANE_ROW_SECTION_INDEX.get(seat, None)
        assert row_section_index is not None
        return row_section_index

    @classmethod
    def _row_section_seat_index(cls, res):
        """Return seat index within Plane row"""
        seat = res[-1:]
        assert isinstance(seat, str)
        assert len(seat) == 1
        row_section_seat_index = cls._PLANE_ROW_SECTION_SEAT_INDEX.get(seat, None)
        assert row_section_seat_index is not None
        return row_section_seat_index

    @classmethod
    def _parse_reservations_generator(cls, N, S):
        """Parse reservation string into a generator
        of dictionary { "row": [Row Index], "section": [Row Section Index]}, "Seat": [Row Section Seat Index]}.
        """
        return (
            {
                "row_index": cls._row_index(res, N),
                "section_index": cls._row_section_index(res),
                "seat_index": cls._row_section_seat_index(res),
            } for res in S.split(" ")
        )

    @classmethod
    def _get_row_section_offset(cls, res):
        row_index = res.get("row_index", None)
        assert row_index is not None
        assert isinstance(row_index, int)
        assert row_index >= 0

        row_section_index = res.get("section_index", None)
        assert row_section_index is not None
        assert isinstance(row_section_index, int)
        assert row_section_index >= 0

        row_seat_section_offset = (row_index * len(cls._PLANE_ROW)) + row_section_index
        assert row_seat_section_offset >= 0
        return row_seat_section_offset

    @classmethod
    def _reserve_seat_in_section(cls, N, S):
        """Reserve Plane's Seats using expected number of rows and map which seats should be reserved."""
        unreserved_seats = cls._generate_plane_sections(N)
        reserved_seats = unreserved_seats[:]
        if len(S) > 0:
            for res in cls._parse_reservations_generator(N, S):
                row_seat_section_offset = cls._get_row_section_offset(res)
                row_section_seat_index = res.get("seat_index", None)
                reserved_seats[row_seat_section_offset][row_section_seat_index] = 1
        return reserved_seats

    @classmethod
    def _find_max_number_of_grouping(cls, reserved_seats, k):
        """Find the max number of grouping of seats adjacent of length k
        amoung currently reserved seats.
        """
        n_sections = len(reserved_seats)
        count_groups = 0
        # print('start', n_sections, count_groups)
        i = 0
        while i < n_sections:

            if len(reserved_seats[i]) < k:
                # print('small', i, count_groups)
                i += 1
                continue

            if sum(reserved_seats[i]) >= k:
                # print('full', i, count_groups)
                i += 1
                continue

            if len(reserved_seats[i]) == k:
                count_groups += 1
                # print('found', i, count_groups)
                i += 1
                continue

            j = 0
            count_empty_contigous_seats = 0
            while j < len(reserved_seats[i]):
                # print('check', i, j)
                if reserved_seats[i][j] != 0:
                    # print('continue', i, j)
                    count_empty_contigous_seats = 0
                    j += 1
                    continue

                count_empty_contigous_seats += 1
                # print('empty', i, count_empty_contigous_seats)
                if count_empty_contigous_seats >= k:
                    count_groups += 1
                    # print('found', i, j, count_groups)

                j += 1

            i += 1

        return count_groups

    @classmethod
    def _plane_rows_split(cls, seats):
        """Split list of planes seats by rows.
        """
        seats = ["-" if x == 2 else x for x in seats]
        row_length = len(cls._PLANE_ROW)
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

    @classmethod
    def _pretty_print_plane_rows(cls, reserved_seats):
        """Split list of planes seats by rows.
        """
        rows = [reserved_seats[i:i + 3] for i in range(0, len(reserved_seats), 3)]

        rows_seats = []
        for row in rows:
            rows_seats.append([seat for section in row for seat in section + ["-"]][:-1])

        return rows_seats

    @staticmethod
    def _pretty_print_2d_array(rows):
        """Pretty print plain rows with seat reservations
        """
        s = [[str(e) for e in row] for row in rows]
        lens = [max(map(len, col)) for col in zip(*s)]
        fmt = "\t".join("{{:{}}}".format(x) for x in lens)
        table = [fmt.format(*row) for row in s]
        return "\n" + "\n".join(table)

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
        self.reserved_seats = cls._reserve_seat_in_section(self.number_rows, self.reservations)

        self.logger.info("Plane Rows Reserved: {0}".format(
            cls._pretty_print_2d_array(
                cls._pretty_print_plane_rows(self.reserved_seats)
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

    plane_reservations = PlaneReservationsB(kw)
    plane_reservations.reserve_seats()
    plane_reservations.max_grouping()


if __name__ == "__main__":
    main()