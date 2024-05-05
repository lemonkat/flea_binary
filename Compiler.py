from dataclasses import dataclass, field
from typing import Any, Callable, ClassVar
from Board import Board
from Util import rule_code
import time
from tqdm import tqdm
# import pygame
# pygame.init()


@dataclass
class Line:
    powerline: str
    align_left: str
    main: str
    align_right: str

    def add_aligns(self, left: int, right: int) -> "Line":
        return Line(
            powerline=self.powerline,
            align_left=self.align_left,
            main=(self.align_left * left) + self.main + (self.align_right * right),
            align_right=self.align_right,
        )

    def __len__(self) -> int:
        return 2 + len(self.main)

    def __str__(self) -> str:
        return (
            self.powerline
            + "|"
            + self.align_left
            + "|"
            + self.main
            + "|"
            + self.align_right
        )


correction = 1


@dataclass
class Blueprint:
    name: str
    num_inputs: int
    copy_inputs: bool
    wires: list[str]
    lines: list[Line]
    library: ClassVar[dict[str, "Blueprint"]] = {}

    # def __init__(self, name:str, num_inputs:int, copy_inputs:bool = True):
    def init_old(self, name: str, num_inputs: int, copy_inputs: bool = True):
        self.lines = []
        self.name = name
        self.num_inputs = num_inputs
        self.copy_inputs = copy_inputs

    def num_wires(self) -> int:
        return len(self.wires)

    @classmethod
    def add_line(cls, obj, line: Line) -> None:
        obj.lines.insert(0, line)

    @classmethod
    def add_lines(cls, obj, lines: list[Line]) -> None:
        for line in lines:
            Blueprint.add_line(obj, line)

    @classmethod
    def add_blueprint(cls, obj, blueprint: "Blueprint", shift: int = 0) -> None:
        for line in blueprint.lines[::-1]:
            if blueprint.name == "GAP":
                Blueprint.add_line(
                    obj,
                    line.add_aligns(
                        shift, obj.num_wires() - shift - blueprint.num_inputs
                    ),
                )
            else:
                Blueprint.add_line(
                    obj,
                    line.add_aligns(
                        shift,
                        obj.num_wires() - shift - blueprint.num_inputs + correction,
                    ),
                )

    # def __str__(self) -> str:
    # result = self.name + " " + str(self.num_inputs) + " " + str(self.num_wires())
    # if self.copy_inputs:
    # result += " 1"
    # else:
    # result += " 0"
    # for line in self.lines:
    # result += "\n" + line.powerline + line.align_left + line.main + line.align_right
    # return result

    @classmethod
    def from_str(cls, s: str) -> "Blueprint":
        lines = s.split("\n")
        removed = []
        for line in lines:
            if len(line) <= 1 or "//" in line:
                removed.append(line)
        for line in removed:
            lines.remove(line)
        first = lines[0].split(" ")
        result = Blueprint(first[0], first[1], copy_inputs=first[3] == "1")
        for line in lines[:0:-1]:
            line = Line(
                powerline=line[0:2],
                align_left=line[2:4],
                main=line[4:-2],
                align_right=line[-2:],
            )
            Blueprint.add_line(result, line)
        return result

    def is_shiftable(self) -> bool:
        return self.power() == 0

    def power(self) -> int:
        count = 0
        for line in self.lines:
            if line.powerline == "37":
                count += 1
        return count

    def time(self) -> int:
        count = self.power() * 2 + len(self.lines)
        for line in self.lines:
            if line.powerline == "38":
                count += 2
        return count

    def __len__(self) -> int:
        return len(self.lines)

    def width(self) -> int:
        if self.lines == []:
            return 0
        max_len = 0
        for line in self.lines:
            max_len = max(max_len, len(line))
        return max_len

    # @dataclass
    # class BlueprintLvl2(Blueprint):
    # wires:list[str]
    # library:dict[str,"Blueprint"]

    def __init__(self, name: str, wires: list[str], copy_inputs: bool = False):
        self.wires = wires
        # super().__init__(name, len(wires))
        self.init_old(name, len(wires), copy_inputs=copy_inputs)

    @classmethod
    def order(cls, obj: "Blueprint", order: list[str], shift: int = 0) -> None:
        for wire_num in range(len(order)):
            Blueprint.move(obj, order[wire_num], wire_num + shift)

    @classmethod
    def move(cls, obj: "Blueprint", wire_name: str, position: int) -> None:
        current_pos = obj.wires.index(wire_name)
        if current_pos == position:
            return
        elif current_pos > position:
            Blueprint.add_blueprint(
                obj, Blueprint.library["SWAP"], shift=current_pos - 1
            )
            obj.wires[current_pos], obj.wires[current_pos - 1] = (
                obj.wires[current_pos - 1],
                obj.wires[current_pos],
            )
        else:
            Blueprint.add_blueprint(obj, Blueprint.library["SWAP"], shift=current_pos)
            obj.wires[current_pos], obj.wires[current_pos + 1] = (
                obj.wires[current_pos + 1],
                obj.wires[current_pos],
            )
        Blueprint.move(obj, wire_name, position)

    @classmethod
    def call(
        cls, obj: "Blueprint", inputs: list[str], outputs: list[str], gate: "Blueprint"
    ) -> None:
        for input_num in range(len(inputs)):
            inp = inputs[input_num]
            if gate.copy_inputs and not inp in outputs:
                Blueprint.move(obj, inp, 0)
                Blueprint.add_blueprint(obj, Blueprint.library["SPLIT"], 0)
                obj.wires.insert(0, obj.wires[0] + "_SYS_INPUT")
            else:
                obj.wires[obj.wires.index(inp)] += "_SYS_INPUT"
            inputs[input_num] += "_SYS_INPUT"

        Blueprint.delete_wires(obj, outputs)

        # if gate.is_shiftable() and len(inputs) != 0:
        # pos = 0
        # for inp in inputs:
        # pos += obj.wires.index(inp)
        # Blueprint.order(obj, inputs, shift = pos // len(inputs))
        # print(obj.wires)
        # Blueprint.add_blueprint(obj, gate, shift = pos // len(inputs))
        # obj.wires = obj.wires[:pos // len(inputs)] + outputs + obj.wires[pos // len(inputs):]
        # else:
        if True:
            Blueprint.order(obj, inputs)
            Blueprint.add_blueprint(obj, gate)
            obj.wires = outputs + obj.wires[len(inputs) :]

    @classmethod
    def delete(cls, obj: "Blueprint", wire_name: str) -> None:
        if wire_name in obj.wires:
            Blueprint.add_blueprint(
                obj, Blueprint.library["DEL"], shift=obj.wires.index(wire_name)
            )
            obj.wires.remove(wire_name)

    @classmethod
    def delete_wires(cls, obj: "Blueprint", wire_names: list[str]) -> None:
        for wire in wire_names:
            Blueprint.delete(obj, wire)

    @classmethod
    def if_statement(
        cls,
        obj: "Blueprint",
        condition: str,
        inputs: list[str],
        outputs: list[str],
        gate: "Blueprint",
    ) -> None:
        Blueprint.call(obj, [condition], ["SYS_IF"], Blueprint.library["COPY"])
        Blueprint.call(
            obj,
            [wire + "_SYS_BRANCH" for wire in inputs],
            [wire + "_SYSBRANCH" for wire in outputs],
            gate,
        )
        for wire in outputs:
            if wire in obj.wires:
                Blueprint.call(
                    obj,
                    ["SYS_IF", wire, wire + "_SYS_BRANCH"],
                    [wire],
                    Blueprint.library["IF"],
                )
                Blueprint.delete_wire(obj, "SYS_IF")
            else:
                Blueprint.call(
                    obj,
                    ["SYS_IF", wire + "_SYS_BRANCH"],
                    [wire],
                    Blueprint.library["AND"],
                )

    @classmethod
    def empty_row(cls, obj: "Blueprint"):
        Blueprint.add_blueprint(obj, Blueprint.library["DEL_ALL"], shift=0)


Cmd = tuple[Callable[[*list[Any]], None], list[Any]]


@dataclass
class Compiler:
    current_board: ClassVar[Board] = None

    def __init__(self):
        pass

    @classmethod
    def store_blueprint(cls, bp: Blueprint) -> None:
        Blueprint.library[bp.name] = bp

    @classmethod
    def define(cls, name: str, args: list[str], cmds: list[Cmd]) -> None:
        # result = BlueprintLvl2(name, args, self.library)
        result = Blueprint(name, args, Blueprint.library)
        for cmd in cmds:
            # BlueprintLvl2.cmd[0](*cmd[1])
            fun, args = cmd
            fun(result, *args)

        cls.store_blueprint(result)

    @classmethod
    def compile(cls, program: str) -> None:
        program = program.split("\n")
        index = 0
        while index < len(program):
            line = program[index].split(" ")
            if (not len(line) <= 1) and not "//" in "".join(line):
                if line[0] == "IMPORT":
                    cls.load_file(line[1])
                elif line[0] == "DEFINE":
                    name = line[1]
                    args = line[2:]
                    cmds = []
                    while line[0] != "END":
                        index += 1
                        line = program[index].split(" ")
                        if line[0] == "ORDER":
                            cmds.append((Blueprint.order, [line[1:]]))
                        elif line[0] == "SET":
                            to_pos = line.index("TO")
                            cmds.append(
                                (
                                    Blueprint.call,
                                    [
                                        line[to_pos + 2 :],
                                        line[1:to_pos],
                                        Blueprint.library[line[to_pos + 1]],
                                    ],
                                )
                            )
                        elif line[0] == "IF":
                            to_pos = line.index("TO")
                            cmds.append(
                                (
                                    Blueprint.if_statement,
                                    [
                                        line[to_pos + 2 :],
                                        line[2:to_pos],
                                        Blueprint.library[line[to_pos + 1]],
                                    ],
                                )
                            )
                        elif line[0] == "DEL":
                            cmds.append((Blueprint.delete_wires, [line[1:]]))
                        elif line[0] == "GAP":
                            cmds.append(
                                (Blueprint.call, [[], [], Blueprint.library["GAP"]])
                            )
                        elif line[0] == "CLEAR":
                            cmds.append((Blueprint.empty_row, []))
                    cls.define(name, args, cmds)
            index += 1

    @classmethod
    def load_file(cls, filename: str) -> None:
        file = open(filename + ".txt", "r")
        blueprints = file.read().split("\n\n")
        file.close()
        for blueprint in blueprints:
            cls.store_blueprint(Blueprint.from_str(blueprint))

    @classmethod
    def load_program(cls, filename: str) -> None:
        file = open(filename + ".txt", "r")
        program = file.read().split("\n\n")
        file.close()
        cls.compile(program)

    @classmethod
    def run(
        cls,
        args: list[bool],
        cell_size: int,
        color_profile: dict,
        flea_color: str,
        wait: float = 0,
        jump: int = 10000,
    ) -> list[bool]:
        start_time = time.time()
        main = Blueprint.library["MAIN"]
        board = Compiler.get_board(cell_size, color_profile)
        ruleset = rule_code("110 223 331 452 540 6 0 780 882 ")
        power_to_run = main.power()
        board.reload()
        for i in range(power_to_run):
            board.add_flea(ruleset, 0, -1, 3, flea_color)

        for input_num in range(main.num_inputs):
            if args[input_num]:
                board.add_flea(ruleset, input_num * 2 + 2, -1, 3, flea_color)

        for i in tqdm(range(main.time() + 1)):
            board.step(times=jump)
            board.update()
            # if wait != 0:
            # 	clock.tick(int(1 / wait))
            time.sleep(max(start_time + i * wait - time.time(), 0))

        return [
            board.is_flea_at(pos, 0) for pos in range(2, (main.num_wires() * 2 + 2), 2)
        ]

    @classmethod
    def show(cls, cell_size: int, color_profile: dict, y_mult=1):
        Compiler.get_board(cell_size, color_profile, y_mult=y_mult).root.mainloop()

    @classmethod
    def get_board(cls, cell_size, color_profile, y_mult=1) -> Board:
        if cls.current_board != None:
            cls.current_board.root.destroy()
        main = Blueprint.library["MAIN"]
        width = main.width() + 30
        board = Board(width, len(main), cell_size, color_profile, y_mult=y_mult)
        board.board = [
            [*(line.powerline + line.main + " " * (width - len(line)))]
            for line in main.lines
        ]
        board.reload()
        board.update()
        cls.current_board = board
        return board

    @classmethod
    def get_board_image(cls, cell_size, color_profile, filename: str, y_mult=0):
        board = Compiler.get_board(cell_size, color_profile)
        board.save(filename)
