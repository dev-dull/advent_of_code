def get_input():
    fin = open('input.list', 'r')
    #fin = open('testdata', 'r')
    lines = fin.read().splitlines()
    fin.close()

    while '' in lines:
        lines.remove('')

    return lines

def part2(input):
    results=findit(input)
    results.sort()
    for i in range(0,len(results)-1):
        if results[i]+1 != results[i+1]:
            print('occupied:', results[i])
            print('     you:', results[i]+1)
            print('occupied:', results[i+1])
            if results[i]+1 in results:
                print('sanity check failed :-(')


def part1(input):
    results = findit(input)
    print(max(results))

def findit(input):
    seat_ids = []
    for line in input:
        rows = list(range(0,128))
        cols = list(range(0,8))
        for c in line[:7]:
            if c == 'F':
                rows = _F(rows)
            elif c == 'B':
                rows = _B(rows)

        for c in line[7:]:
            if c == 'R':
                cols = _B(cols)
            elif c == 'L':
                cols = _F(cols)

        seat_ids.append(rows[0]*8 + cols[0])
    return seat_ids

def _B(rows):
    return rows[int(len(rows)/2):]

def _F(rows):
    return rows[:int(len(rows)/2)]

def main():
    input = get_input()
    #part1(input)
    part2(input)


if __name__ == '__main__':
    main()
