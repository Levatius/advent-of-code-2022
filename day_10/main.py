# https://adventofcode.com/2022/day/10

from dataclasses import dataclass


@dataclass
class Process:
    WORK_COST_MAP = {'noop': 1, 'addx': 2}
    command: str
    args: list
    work_remaining: int

    @classmethod
    def from_instruction(cls, instruction):
        command, *args = instruction.split(' ')
        return cls(command, args, work_remaining=cls.WORK_COST_MAP[command])

    def do_work(self):
        self.work_remaining -= 1


class Device:
    register_x: int = 1
    queue: list = []
    signal_strength_log: list = []
    crt_display: list[list[chr]] = [['▯' for _ in range(40)] for _ in range(6)]

    @property
    def current_process(self):
        if len(self.queue) > 0:
            return self.queue[0]

    def execute_current_process(self):
        match self.current_process.command:
            case 'noop':
                # Do nothing
                pass
            case 'addx':
                self.register_x += int(self.current_process.args[0])
        self.queue.remove(self.current_process)

    def update_crt_display(self, position):
        if self.register_x - 1 <= position[0] <= self.register_x + 1:
            self.crt_display[position[1]][position[0]] = '▮'

    def execute(self, instructions, max_cycles=240):
        for cycle in range(1, max_cycles + 1):
            # End of previous cycle, execute the current process if no work is remaining
            if self.current_process and self.current_process.work_remaining == 0:
                self.execute_current_process()

            # Start of this cycle, enqueue process from next instruction if the queue is empty
            if not self.current_process:
                new_process = Process.from_instruction(instructions.pop(0))
                self.queue.append(new_process)

            # During this cycle, do work on the current process and update the CRT
            if self.current_process:
                self.current_process.do_work()
            position = (cycle - 1) % 40, (cycle - 1) // 40
            self.update_crt_display(position)

            # End of this cycle, do signal strength logging every 40 cycles starting at cycle 20
            if (cycle - 20) % 40 == 0:
                self.signal_strength_log.append(cycle * self.register_x)

    def draw(self):
        print('\n'.join(''.join(crt_display_row) for crt_display_row in self.crt_display))


def get_data(file_name='input.txt'):
    with open(file_name) as f:
        return f.read().splitlines()


def run(device, instructions):
    device.execute(instructions)
    print(f'Total Signal Strength: {sum(device.signal_strength_log)}')
    device.draw()


def main():
    device = Device()
    instructions = get_data()
    run(device, instructions)


if __name__ == '__main__':
    main()
