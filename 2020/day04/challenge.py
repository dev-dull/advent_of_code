import re

class passport(dict):
    def __init__(self):
        self.recolor = re.compile('^#[0-9a-f]{6}$')
        self.repid = re.compile('^[0-9]{9}$')

        self.required = ('byr', 'iyr', 'eyr', 'hgt', 'hcl', 'ecl', 'pid')
        self.valid_eyes = ('amb', 'blu', 'brn', 'gry', 'grn', 'hzl', 'oth')

    def is_valid(self):
        for r in self.required:
            if r not in self:
                return False

        self['byr'] = int(self['byr'])
        if self['byr'] < 1920 or self['byr'] > 2002:
            return False

        self['iyr'] = int(self['iyr'])
        if self['iyr'] < 2010 or self['iyr'] > 2020:
            return False

        self['eyr'] = int(self['eyr'])
        if self['eyr'] < 2020 or self['eyr'] > 2030:
            return False

        height = int(self['hgt'][:-2])
        if self['hgt'].endswith('cm'):
            if height < 150 or height > 193:
                return False
        elif self['hgt'].endswith('in'):
            if height < 59 or height > 76:
                return False
        else:
            return False

        if not self.recolor.match(self['hcl']):
            return False

        if self['ecl'] not in self.valid_eyes:
            return False

        if not self.repid.match(self['pid']):
            return False

        return True

def get_input():
    fin = open('input.list', 'r')
    records = fin.read().split('\n\n')
    fin.close()

    retval = []
    for raw_record in records:
        record = raw_record.replace(' ', '\n')
        normalized_record = passport()
        for r in record.splitlines():
            k,v = r.split(':')
            normalized_record[k] = v
        retval.append(normalized_record)
    return retval

def part2(input):
    pass


def part1(input):
    validct = 0
    for record in input:
        if record.is_valid():
            validct += 1
    print(validct, len(input))


def main():
    input = get_input()
    part1(input)
    #part2(input)


if __name__ == '__main__':
    main()
