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
    elfs = ElegantLogicalFileSystem()
    for command in data:
        if command:  # Toss out blank lines from ingestion
            elfs.run_cmd(command)

    space_used = elfs.refresh_size_on_disk()
    space_needed = 30000000 - (70000000 - space_used)
    # print(space_used, space_needed)
    elfs.dirs_gte(space_needed)


def part1(data):
    elfs = ElegantLogicalFileSystem()
    for command in data:
        if command:  # Toss out blank lines from ingestion
            elfs.run_cmd(command)

    elfs.sum_dirs()


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

    def refresh_size_on_disk(self):
        sumdirs = 0
        for k, v in self.elfs.items():
            sumdirs += v.refresh_size_on_disk()
        sumdirs += sum([f[0] for f in self.elfs.files])  # It took me way, WAY too long to spot that I was missing this.
        self.elfs.size_on_disk = sumdirs  # As noted elsewhere, I should've just tracked this from the start
        return sumdirs

    def sum_dirs(self):
        diskuse = []
        for k, v in self.elfs.items():
            v.sum_dirs(k, diskuse)
        print(sum(diskuse), diskuse)

    def dirs_gte(self, space_needed):
        diskuse = [70000000]  # pass-by-ref-lazy-mode: activate!
        for k, v in self.elfs.items():
            v.dirs_gte(diskuse, space_needed)
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
                    file_size, filename = dir_item.split()
                    file_size = int(file_size)
                    self.files.append((file_size, filename))

    def refresh_size_on_disk(self):
        # Would've been better to track this as files are added, but this is easier to groc.
        sumdirs = 0
        for k, v in self.items():
            sumdirs += v.refresh_size_on_disk()
        sumdirs += sum([f[0] for f in self.files])
        self.size_on_disk = sumdirs
        return sumdirs

    def sum_dirs(self, parent_key, diskuse, max_size=100000):
        # Bah. `max_size` should've been an optional param at the ElegantLogicalFileSystem.sum_dirs()
        dirsum = 0
        for k, v in self.items():
            dirsum += v.sum_dirs(k, diskuse)

        dirsum += sum([f[0] for f in self.files])
        if dirsum <= max_size:
            print(parent_key, dirsum)
            diskuse.append(dirsum)
        return dirsum

    def dirs_gte(self, diskuse, space_needed):
        if self.size_on_disk >= space_needed and self.size_on_disk < diskuse[0]:
            diskuse[0] = self.size_on_disk
        for k, v in self.items():
            v.dirs_gte(diskuse, space_needed)
        return diskuse


def main():
    parser = argparse.ArgumentParser(description='Advent of code 2022 solutions by Alastair')
    parser.add_argument('-t', '--test', dest='test', action='store_true', default=False, help='Use the file testdata instead of input.list')
    args = parser.parse_args()
    data = get_input(args.test)
    # part1(data)
    part2(data)


if __name__ == '__main__':
    main()
