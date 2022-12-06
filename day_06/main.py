# https://adventofcode.com/2022/day/6

from more_itertools import windowed


class Device:
    @staticmethod
    def is_marker_valid(marker):
        return len(marker) == len(set(marker))

    def subroutine(self, datastream, marker_length=4):
        for i, marker in enumerate(windowed(datastream, marker_length)):
            if self.is_marker_valid(marker):
                return i + marker_length


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        return f.read()


def run(device, datastream):
    print(f'Packet Character: {device.subroutine(datastream)}')
    print(f'Message Character: {device.subroutine(datastream, marker_length=14)}')


def main():
    device = Device()
    datastream = get_data()
    run(device, datastream)


if __name__ == '__main__':
    main()
