rps_values = [1, 2, 3]

rps_matrix = [
    [3, 6, 0],
    [0, 3, 6],
    [6, 0, 3]
]

rps_a = ["A", "B", "C"]
rps_y = ["X", "Y", "Z"]

ldw_values = [0, 3, 6]

# score_arr = []
#
# with open("advent2data.txt", "r") as f:
#     data = f.readlines()
#     for d in data:
#         d = d.strip("\n")
#         lr = d.split(" ")
#         l = rps_a.index(lr[0])
#         r = rps_y.index(lr[1])
#         move_score = rps_values[r]
#         result_score = rps_matrix[l][r]
#         score_arr.append(move_score + result_score)
#
# print(sum(score_arr))

score_arr = []

with open("advent2data.txt", "r") as f:
    data = f.readlines()
    for d in data:
        d = d.strip("\n")
        lr = d.split(" ")
        l = rps_a.index(lr[0])
        r = rps_y.index(lr[1])
        move_score = rps_values[rps_matrix[l].index(ldw_values[r])]
        result_score = ldw_values[r]
        score_arr.append(move_score + result_score)

print(sum(score_arr))

