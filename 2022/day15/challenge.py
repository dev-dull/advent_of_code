import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().splitlines()

    lines = [l.replace(':', '').replace(',', '') for l in lines]
    retval = {}
    for line in lines:
        if line:
            words = line.split()
            # Ew.
            sx = int(words[2].replace('x=', ''))
            sy = int(words[3].replace('y=', ''))
            bx = int(words[8].replace('x=', ''))
            by = int(words[9].replace('y=', ''))
            #      col, row    col, row
            retval[(sx, sy)] = (bx, by)

    return retval


def part2(data):
    pass


def part1(data, test):
    # too low: 5086760
    #          5086760

    sensor_array = SensorArray(data)
    print(str(sensor_array))

    row = 10 if test else 2000000
    no_beacon_count = sensor_array.check_row(row)
    print('This might be right:', no_beacon_count)


class SensorArray(dict):
    class __SBItem(object):
        def __init__(self, partner_object, partner_distance):
            # I don't yet know if these values are going to be useful within the object.
            # Also, multiple sensors report back to the same beacon, so that'll need to change if I need to use this info
            self.partner = partner_object
            self.distance = partner_distance

    class _Sensor(__SBItem):
        def __str__(self):
            return 'S'

    class _Beacon(__SBItem):
        def __str__(self):
            return 'B'

    def __init__(self, sensor_pairs):
        self.top = float('inf')
        self.bottom = float('-inf')
        self.left = float('inf')
        self.right = float('-inf')
        self.max_distance = float('-inf')

        for sensor, beacon in sensor_pairs.items():
            # Find the edges so I can write a __str__ function
            if min([sensor[1], beacon[1]]) < self.top:
                self.top = min([sensor[1], beacon[1]])
            if max([sensor[1], beacon[1]]) > self.bottom:
                self.bottom = max([sensor[1], beacon[1]])
            if min([sensor[0], beacon[0]]) < self.left:
                self.left = min([sensor[0], beacon[0]])
            if max([sensor[0], beacon[0]]) > self.right:
                self.right = max([sensor[0], beacon[0]])

            city_distance = self.city_distance(sensor, beacon)
            if city_distance > self.max_distance:
                self.max_distance = city_distance

            self[sensor] = self._Sensor(beacon, city_distance)
            self[beacon] = self._Beacon(sensor, city_distance)
        print(self.left, self.right, self.top, self.bottom)

        # self.mark_beaconless()  # The real dataset uses numbers too large for this to do the job, but helps debugging.

    def __str__(self):
        if self.right > 100:
            return 'inf'

        retval = '             11111111112222222222\n'
        retval += '   012345678901234567890123456789\n'
        for ri in range(self.top, self.bottom + 1):
            retval += f'{ri:02} '
            for ci in range(self.left, self.right+1):
                retval += str(self[(ci, ri)]) if (ci, ri) in self else '.'
            retval += '\n'
        return retval

    def city_distance(self, pos1, pos2):
        return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])

    def check_row(self, row_num):
        # In my first several attempts, I had failed to consider looking beyond the edges of the initial input.
        # I added `self.max_distance` to fix it.
        in_range_ct = 0
        for ci in range(self.left-self.max_distance, self.right+self.max_distance+1):
            if not ci % 10000:
                print(' ', (ci, row_num), '      ', end='\r')

            if self.check_position((ci, row_num)):
                in_range_ct += 1
        print('')
        return in_range_ct

    def check_position(self, position):
        # If I had to do this over again, __SBItem would know its own point and
        # sensor[position] would return True if they were within range of each other.
        if position not in self:
            for item_position, sb_item in self.items():
                if isinstance(sb_item, self._Sensor):
                    point_distance = self.city_distance(position, item_position)
                    if point_distance <= sb_item.distance:
                        return True

        return False

    def mark_beaconless(self):
        # Works, but is too slow for the large numbers of the input.
        # leaving this here since it was tricky.
        marked = {}
        for position, sb_item in self.items():
            if isinstance(sb_item, self._Sensor):
                print('distance:', sb_item.distance)
                marked.update(self._mark_beaconless(position, sb_item.distance))
                # break
        self.update(marked)

    def _mark_beaconless(self, position, distance, marked={}):
        if distance+1:
            for h_offset in range(distance+1):
                # vertical is position[1]
                for v_offset in range(distance+1-h_offset):
                    if (position[0]+h_offset, position[1]+v_offset) not in self:
                        marked[(position[0]+h_offset, position[1]+v_offset)] = '#'
                    if (position[0]+h_offset, position[1]-v_offset) not in self:
                        marked[(position[0]+h_offset, position[1]-v_offset)] = '#'
                    if (position[0]-h_offset, position[1]+v_offset) not in self:
                        marked[(position[0]-h_offset, position[1]+v_offset)] = '#'
                    if (position[0]-h_offset, position[1]-v_offset) not in self:
                        marked[(position[0]-h_offset, position[1]-v_offset)] = '#'

        return marked

    def placeholder(self):
        # I expect that in part 2, they'll want me to count ALL the places where there can't be a beacon
        # In the below, 9 in the 'city distance' for the sensor to the beacon.
        # It took me a while to realize I was looking at two triangles and NOT a square that got elongated by ASCII-art.
        9 * 2 * 9 + 9 * 2


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    part1(data, args.test)
    #part2(data)


if __name__ == '__main__':
    main()
