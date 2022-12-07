import argparse


def get_input(test):
    fname = 'input.list'
    if test:
        fname = 'testdata'
        print('USING TESTING DATA')

    with open(fname, 'r') as fin:
        lines = fin.read().split('$ ')

    return lines


def part2(data):
    pass


def part1(data):
    elfs = ElegantLogicalFileSystem()
    for command in data:
        if command:  # Toss out blank lines from ingestion
            elfs.run_cmd(command)

    # import json
    # print(json.dumps(elfs.elfs))
    elfs.sum_dirs()


# If I had just done this all in a regular 'ol dictionary, I would've made life a lot better for myself.
# Also, if I had added things recursively, I could've kept a running FS size total as I added stuff.
class ElegantLogicalFileSystem(object):
    # ELFS header node
    def __init__(self):
        self.elfs = None
        self.cwd = None

    def run_cmd(self, command_data):
        if command_data.startswith('cd'):
            _, dirname = command_data.split()
            if dirname == '/':
                self.elfs = _ELFS(None)
                self.cwd = self.elfs
            else:
                self.cwd = self.cwd.cd(dirname)
        elif command_data.startswith('ls'):
            files = command_data.splitlines()
            self.cwd.ls(files[1:])

    def sum_dirs(self):
        diskuse = []
        for k, v in self.elfs.items():
            v.sum_dirs(k, diskuse)
        print(sum(diskuse), diskuse)


class _ELFS(dict):
    def __init__(self, parent):
        self.parent = parent
        self.files = []
        self.size_on_disk = 0

    def cd(self, dirname):
        if dirname == '..':
            return self.parent
        return self[dirname]

    def ls(self, dir_contents):
        for dir_item in dir_contents:
            if dir_item:
                if dir_item.startswith('dir'):
                    _, dirname = dir_item.split()
                    self[dirname] = _ELFS(self)
                if dir_item[0].isnumeric():
                    size, filename = dir_item.split()
                    self.files.append((int(size), filename))

    def sum_dirs(self, parent_key, diskuse, max_size=100000):
        dirsum = 0
        for k, v in self.items():
            dirsum += v.sum_dirs(k, diskuse)

        dirsum += sum([f[0] for f in self.files])
        if dirsum <= max_size:
            print(parent_key, dirsum)
            diskuse.append(dirsum)
        return dirsum


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    part1(data)
    #part2(data)


if __name__ == '__main__':
    main()
