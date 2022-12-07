# https://adventofcode.com/2022/day/7

from dataclasses import dataclass, field


class File:
    def __init__(self, name, size):
        self.name: str = name
        self.size: int = size


@dataclass
class Directory(File):
    name: str
    parent: 'Directory' = None
    contents: list = field(default_factory=list)

    @property
    def size(self):
        return sum(item.size for item in self.contents)

    def get_directory(self, directory_name):
        for item in self.contents:
            if isinstance(item, Directory) and item.name == directory_name:
                return item

    def get_directories(self):
        for item in self.contents:
            if isinstance(item, Directory):
                yield item
                yield from item.get_directories()


class FileSystem:
    def __init__(self, total_space):
        self.total_space = total_space
        self.root_directory = Directory('/')
        self.current_directory = None

    @property
    def free_space(self):
        return self.total_space - self.root_directory.size

    def get_all_directories(self):
        return self.root_directory.get_directories()

    def parse_cd(self, directory_name):
        match directory_name:
            case '/':
                self.current_directory = self.root_directory
            case '..':
                self.current_directory = self.current_directory.parent
            case _:
                self.current_directory = self.current_directory.get_directory(directory_name)

    def parse_command(self, command_str):
        command, *args = command_str.split(' ')
        match command:
            case 'cd':
                directory_name = args[0]
                self.parse_cd(directory_name)
            case 'ls':
                # Skip ls command
                pass

    def parse_line(self, line):
        identifier, *other = line.split(' ')
        match identifier:
            case '$':
                command_str = ' '.join(other)
                self.parse_command(command_str)
            case 'dir':
                directory_name = other[0]
                new_directory = Directory(directory_name, parent=self.current_directory)
                self.current_directory.contents.append(new_directory)
            case _:
                file_name = other[0]
                file_size = int(identifier)
                new_file = File(file_name, file_size)
                self.current_directory.contents.append(new_file)


def get_data(total_space, file_name='input.txt'):
    file_system = FileSystem(total_space)
    with open(file_name) as f:
        for line in f.read().splitlines():
            file_system.parse_line(line)
    return file_system


def run_part_1(file_system, at_most_size):
    total_size = sum(directory.size for directory in file_system.get_all_directories() if directory.size <= at_most_size)
    print(f'Part 1 Total Size: {total_size}')


def run_part_2(file_system, update_size):
    required_space = update_size - file_system.free_space
    total_size = min(directory.size for directory in file_system.get_all_directories() if directory.size >= required_space)
    print(f'Part 2 Total Size: {total_size}')


def main():
    file_system = get_data(total_space=70000000)
    run_part_1(file_system, at_most_size=100000)
    run_part_2(file_system, update_size=30000000)


if __name__ == '__main__':
    main()
