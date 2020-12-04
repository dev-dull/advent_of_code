def get_input():
    fin = open('input.list', 'r')
    passwords = fin.read().splitlines()
    fin.close()

    while '' in passwords:
        passwords.remove('')

    retval = []
    for i in passwords:
        rule,password = i.split(':')
        password = password.strip()
        min = int(rule.split('-')[0])
        max = int(rule.split('-')[1].split()[0])
        letter = rule.split()[1]
        retval.append((min, max, letter, password))

    return retval


def part2(passwords):
    validct = 0
    for i,j,letter,password in passwords:
        chars = set([password[i-1], password[j-1]])
        if len(chars)-1 and letter in chars:
            validct += 1
    print(validct)


def part1(passwords):
    validct = 0
    for min,max,letter,password in passwords:
        passct = password.count(letter)
        if passct >= min and passct <= max:
            validct += 1
    print(validct)


def main():
    passwords = get_input()
    #part1(passwords)
    part2(passwords)


if __name__ == '__main__':
    main()
