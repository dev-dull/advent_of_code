def main():
    fin = open('input.list', 'r')
    numbers_str = fin.read()
    fin.close()

    numbers = [int(n) for n in numbers_str.splitlines()]
    numbers.sort(reverse=True)
    set_breaks = False

    for n in numbers:
        max_adder = 2019 - n
        candidates = filter(lambda i: i < max_adder, numbers)
        for c in candidates:
            look_for = 2020 - (c + n)
            if look_for in numbers:
                print('%s + %s + %s = %s' % (n, c, look_for, n+c+look_for))
                print('%s * %s * %s = %s' % (n, c, look_for, n*c*look_for))
                set_breaks = True
                break
        if set_breaks:
            break

if __name__ == '__main__':
    main()
