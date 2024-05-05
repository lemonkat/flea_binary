from Board import Board


# def rule_code(s:str) -> dict:
#   result = {}
#   tokens = s.split(" ")
#   for token in tokens:
#     if token != "":
#       name_dat = token.split(":")
#       dat = name_dat[1].split(",")
#       assembled_dat = {}
#       for d in dat:
#         if d != "":
#           assembled_dat[d[0]] = d[1:]
#         else:
#           assembled_dat[d[0]] = " "
#       result[name_dat[0]] = assembled_dat
#   return result
def rule_code(s: str) -> dict:
    result = {}
    for i in range(len(s) // 4):
        result[s[i * 4]] = {"s": s[i * 4 + 1], "r": s[i * 4 + 2]}
    return result


def parse_board(b: str):
    result = []
    b_all = b.split("\n")
    for line in b_all:
        if line != "" and (not "//" in line):
            l = []
            for i in range(len(b_all[0])):
                l.append(line[i])
            result.append(l)
    return result


def board_setup(b: str, cell_size: int, color_profile: dict):
    b_all = parse_board(b)
    board = Board(len(b_all[0]), len(b_all), cell_size, color_profile, " ")
    board.board = b_all
    board.update()
    return board
