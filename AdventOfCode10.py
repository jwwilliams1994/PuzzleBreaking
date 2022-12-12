

data = []
with open("advent10data.txt", "r") as f:
    out_arr = []
    for line in f.readlines():
        out_arr.append(line.strip("\n"))
    print(out_arr)
    data = out_arr


op_arr = []


class Operation:
    def __init__(self, _cycles_required: int, _val: int):
        self.cycles = _cycles_required
        self.val = _val


for d in data:
    if d.startswith("addx"):
        d2 = d.split(" ")
        num = int(d2[1])  # the data is formatted well, this will not throw an exception :^)
        op_arr.append(Operation(2, num))
    else:  # else it is a noop...
        op_arr.append(Operation(1, 0))

# part 1 solution commented out
# reg_x = 1
# cycles = 0
# cycles_i_want_signals_from = [20, 60, 100, 140, 180, 220]
# signal_arr = []
#
# for op in op_arr:
#     for c in range(op.cycles):
#         cycles += 1
#         # 'during' the cycle is right here
#         if cycles in cycles_i_want_signals_from:
#             # signal strength is reg_x times cycle num...
#             signal_str = reg_x * cycles
#             signal_arr.append(signal_str)
#             print("SIGNAL AT {}: ".format(cycles), signal_str)
#
#     reg_x += op.val
#
# print("TOTAL: ", sum(signal_arr))

screen = []

for y in range(6):  # creating the 2d screen array...
    sub_arr = []
    for x in range(40):
        sub_arr.append("_")
    screen.append(sub_arr)


reg_x = 1
cycles = 0
y = 0
for op in op_arr:
    for c in range(op.cycles):
        cycles += 1
        y = cycles // 40
        x = cycles % 40
        if reg_x <= x <= reg_x + 2:
            screen[y][x] = "#"
        # 'during' the cycle is here
    reg_x += op.val


print(cycles)
# print(screen)
for y in range(6):
    for x in range(40):
        print(screen[y][x], end="")
    print()

