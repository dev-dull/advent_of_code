import re

lines = '''.....#......#...#...#...#....##.....#.....#.....###....#...#......#..####....##....###.##.....#.
......#...#....##.#....##...###....####..###.#.#.#...........###...#..#..#.##..#..#.............
#......###.............#.#.##.##..##.##.##....#.......#.....#....#.........#...#..#..#...##.....'''.splitlines()

monster_head = re.compile('..................#.')
monster_middle = re.compile('#....##....##....###')
monster_bottom = re.compile('.#..#..#..#..#..#...')

# for m in monster_middle.finditer(lines[1]):
m = monster_middle.search(lines[1][24:44])
print(m.start(), m.end())

# m = monster_head.search(lines[0][18:38])
# print(m.start(), m.end())
#
# m = monster_bottom.search(lines[2])
# print(m.start(), m.end())
