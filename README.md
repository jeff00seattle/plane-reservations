# plane_reservations
FLEXE coding challenge on Codilify: Plane Reservations

**Version Thursday, 2018 May 17, 19:30 PST**

Jeff Tanner
206 849 8808
jeff00seattle@gmail.com

 * [Plane Reservation problem](#plane-reservation-problem)
    + [Plane seating layout](#plane-seating-layout)
    + [Plane Reservations](#plane-reservations)
    + [Problem Definition](#problem-definition)
  * [Example Solution](#example-solution)
      - [Usage](#usage)
      - [4 rows, No Reservations and Grouping of 3: 12 available](#4-rows--no-reservations-and-grouping-of-3--12-available)
      - [4 rows, Reservations "1A 3B 4J 4K 2A 2B" and Grouping of 3: 8 available](#4-rows--reservations--1a-3b-4j-4k-2a-2b--and-grouping-of-3--8-available)
      - [2 rows, Reservations "1A 1B 1C 2H 2J 2K" and Grouping of 3: 4 available](#2-rows--reservations--1a-1b-1c-2h-2j-2k--and-grouping-of-3--4-available)
      - [10 rows, Reservations "1A 1B 1C 2H 2J 2K 5C 7G 4F 9D 9E 9F 9G 10H 10K" and Grouping of 3: 24 available](#10-rows--reservations--1a-1b-1c-2h-2j-2k-5c-7g-4f-9d-9e-9f-9g-10h-10k--and-grouping-of-3--24-available)


## Plane Reservation problem

Given a plane with reserved seats, find the maximum number of seat groupings so that family of 3 can sit together.

### Plane seating layout

+ 1 to N rows
+ 10 seats per row are identified by A, B, C, D, E, F, G, H, J, K (no I)

```
	A       B       C               D       E       F       G               H       J       K
	-----------------------------------------------------------------------------------------
1	0	0	0	-	0	0	0	0	-	0	0	0
2	0	0	0	-	0	0	0	0	-	0	0	0
3	0	0	0	-	0	0	0	0	-	0	0	0
4	0	0	0	-	0	0	0	0	-	0	0	0

***

N	0	0	0	-	0	0	0	0	-	0	0	0
```

### Plane Reservations

+ Unordered listing of Seats identified by ```[ROW NUMBER][SEAT LETTER]```.
+ Space delimited.

Example:
```
1F 2A 1G 2E 3D 3F
```

### Problem Definition

Provided a plane with **`N`** rows of 10 seats across and knowing which seats have been reserved provided by **`S`**,
find the maximum number of contiguous seat groups of length **`k`**.

For example, how many family of 3 can sit together after determining available seating that are not yet reserved.

## Example Solution

#### Usage

```bash
$ python3 plane_reservation.py --help

Usage: plane_reservation.py
        [-v | --verbose]
        [-h | --help]
        --number-rows int
        --reservations string
    --number-rows: Number of Rows [Required]
    --reservations: Seat reservations, example '1F 2A 1G 2E 3D 3F', default ''.
```

#### 4 rows, No Reservations and Grouping of 3: 12 available
```bash
$ python3 plane_reservation.py \
  --number-rows 4 \
  --grouping 3

2018-05-17 19:01:18,850 Plane Reservation INFO     Plane Rows Reserved:
0	0	0	-	0	0	0	0	-	0	0	0
0	0	0	-	0	0	0	0	-	0	0	0
0	0	0	-	0	0	0	0	-	0	0	0
0	0	0	-	0	0	0	0	-	0	0	0
2018-05-17 19:01:18,850 Plane Reservation INFO     Seat Grouping By 3: Max Number = 12
```

#### 4 rows, Reservations "1A 3B 4J 4K 2A 2B" and Grouping of 3: 8 available
```bash
python3 plane_reservation.py \
  --number-rows 4 \
  --grouping 3 \
  --reservations "1A 3B 4J 4K 2A 2B"

2018-05-17 19:02:46,187 Plane Reservation INFO     Plane Rows Reserved:
1	0	0	-	0	0	0	0	-	0	0	0
1	1	0	-	0	0	0	0	-	0	0	0
0	1	0	-	0	0	0	0	-	0	0	0
0	0	0	-	0	0	0	0	-	0	1	1
2018-05-17 19:02:46,187 Plane Reservation INFO     Seat Grouping By 3: Max Number = 8
```

#### 2 rows, Reservations "1A 1B 1C 2H 2J 2K" and Grouping of 3: 4 available
```bash
python3 plane_reservation.py \
  --number-rows 2 \
  --grouping 3 \
  --reservations "1A 1B 1C 2H 2J 2K"

2018-05-17 19:18:17,872 Plane Reservation INFO     Plane Rows Reserved:
1	1	1	-	0	0	0	0	-	0	0	0
0	0	0	-	0	0	0	0	-	1	1	1
2018-05-17 19:18:17,872 Plane Reservation INFO     Seat Grouping By 3: Max Number = 4
```

#### 10 rows, Reservations "1A 1B 1C 2H 2J 2K 5C 7G 4F 9D 9E 9F 9G 10H 10K" and Grouping of 3: 24 available
```bash
python3 plane_reservation.py \
  --number-rows 10 \
  --grouping 3 \
  --reservations "1A 1B 1C 2H 2J 2K 5C 7G 4F 9D 9E 9F 9G 10H 10K"
2018-05-17 19:33:02,022 Plane Reservation INFO     Plane Rows Reserved:
1	1	1	-	0	0	0	0	-	0	0	0
0	0	0	-	0	0	0	0	-	1	1	1
0	0	0	-	0	0	0	0	-	0	0	0
0	0	0	-	0	0	1	0	-	0	0	0
0	0	1	-	0	0	0	0	-	0	0	0
0	0	0	-	0	0	0	0	-	0	0	0
0	0	0	-	0	0	0	1	-	0	0	0
0	0	0	-	0	0	0	0	-	0	0	0
0	0	0	-	1	1	1	1	-	0	0	0
0	0	0	-	0	0	0	0	-	1	0	1
2018-05-17 19:33:02,022 Plane Reservation INFO     Seat Grouping By 3: Max Number = 24
```
