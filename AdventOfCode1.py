class Elf:
    def __init__(self):
        self.calorie_arr = []

    def add_calories(self, _calories):
        self.calorie_arr.append(_calories)

    def get_total(self):
        return sum(self.calorie_arr)


elf_arr = []

with open("advent1data.txt", "r") as f:
    data = f.readlines()
    current_elf = Elf()
    for d in data:
        d = d.strip("\n")
        if len(d) == 0:
            elf_arr.append(current_elf)
            current_elf = Elf()
        else:
            current_elf.add_calories(int(d))


total_arr = [elf.get_total() for elf in elf_arr]

total_arr.sort()
print("HIGHEST: ", total_arr[-1])

top_three_arr = total_arr[-3:]
print("SUM OF TOP THREE: ", sum(top_three_arr))
