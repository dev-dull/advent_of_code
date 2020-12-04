def main():
    fin = open('input.list', 'r')
    numbers_str = fin.read()
    fin.close()

    numbers = [int(n) for n in numbers_str.splitlines()]
    numbers.sort(reverse=True)

    # C style looping to avoid checking numbers at the beginning of the list that have already been elimiated
    for i in range(0, len(numbers)):
        look_for = 2020-numbers[i]
        if look_for in numbers[i:]:
            print('%s * %s = %s' % (look_for, numbers[i], look_for*numbers[i]))
            break

if __name__ == '__main__':
    main()
