from copy import deepcopy


def get_copy(_die):  # creating new variables from another variable of a list still refers to the same list without a copy
    return deepcopy(_die)


class Die:  # represents the die faces, and includes methods to rotate the faces
    def __init__(self):
        self.faces = [
            None,
            [None, None, None, None],
            None
        ]

    def top_face(self):
        return self.faces[1][0]

    def set_top_face(self, _inp):
        self.faces[1][0] = _inp

    def rotate_up(self):
        buffer = get_copy(self.faces)
        buffer[0] = self.faces[1][0]
        buffer[1][0] = self.faces[2]
        buffer[2] = self.faces[1][2]
        buffer[1][2] = self.faces[0]
        self.faces = buffer

    def rotate_down(self):
        buffer = get_copy(self.faces)
        buffer[0] = self.faces[1][2]
        buffer[1][0] = self.faces[0]
        buffer[2] = self.faces[1][0]
        buffer[1][2] = self.faces[2]
        self.faces = buffer

    def rotate_left(self):
        buffer = get_copy(self.faces)
        for i in [0, 1, 2, 3]:
            buffer[1][i - 1] = self.faces[1][i]
        self.faces = buffer

    def rotate_right(self):
        buffer = get_copy(self.faces)
        for i in [0, 1, 2, 3]:
            buffer[1][i] = self.faces[1][i - 1]
        self.faces = buffer


game_grid = [  # index order is y , x
    [57, 33, 132, 268, 492, 732],
    [81, 123, 240, 443, 353, 508],
    [186, 42, 195, 704, 452, 228],
    [-7, 2, 357, 452, 317, 395],
    [5, 23, -4, 592, 445, 620],
    [0, 77, 32, 403, 337, 452]
]


def get_grid_at_pos(_pos: [int, int]):  # takes [x, y] coordinates
    return game_grid[_pos[1]][_pos[0]]


class GameDie:
    def __init__(self):
        self.die = Die()
        self.pos = [0, 5]
        self.score = 0
        self.moves = 0
        self.visited = [[0, 5]]

    def printMe(self):
        print("Die faces: ", self.die.faces)
        print("Die pos: ", self.pos)
        print("Die score: ", self.score)
        print("Die moves: ", self.moves)
        print("Die path: ")
        p_count = 0
        for pos in self.visited:
            print(pos, end=", ")
            p_count += 1
            if p_count >= 10:
                p_count = 0
                print()
        if p_count > 0:
            print()

    def top_face(self):
        return self.die.top_face()

    def set_top_face(self, _inp):
        self.die.set_top_face(_inp)

    def rotate_left(self):
        self.die.rotate_left()
        self.pos[0] -= 1
        self.moves += 1
        return self

    def rotate_right(self):
        self.die.rotate_right()
        self.pos[0] += 1
        self.moves += 1
        return self

    def rotate_up(self):
        self.die.rotate_up()
        self.pos[1] -= 1
        self.moves += 1
        return self

    def rotate_down(self):
        self.die.rotate_down()
        self.pos[1] += 1
        self.moves += 1
        return self


def print_grid(_die: GameDie, printVisited=False):
    for y in [0, 1, 2, 3, 4, 5]:
        for x in [0, 1, 2, 3, 4, 5]:
            num_str = str(get_grid_at_pos([x, y]))
            num_str += " " * (4 - len(num_str))
            if [x, y] in _die.visited:
                if printVisited:
                    print("[{}]".format(num_str), end="")
                else:
                    total_visits = 0
                    for pos in _die.visited:
                        if pos[0] == x and pos[1] == y:
                            total_visits += 1
                    num_str = str(total_visits)
                    num_str += " " * (2 - len(num_str))
                    print("[-{}-]".format(num_str), end="")
            else:
                print(" {} ".format(num_str), end="")
        print()


def get_adjacent_pos(_pos: [int, int]):
    pos_arr = [None, None, None, None]
    if _pos[0] > 0:
        pos_arr[0] = [_pos[0] - 1, _pos[1]]
    if _pos[0] < 5:
        pos_arr[1] = [_pos[0] + 1, _pos[1]]
    if _pos[1] > 0:
        pos_arr[2] = [_pos[0], _pos[1] - 1]
    if _pos[1] < 5:
        pos_arr[3] = [_pos[0], _pos[1] + 1]
    return pos_arr  # left, right, up, down


def valid_pos_filter(_die: GameDie):
    pos_num = get_grid_at_pos(_die.pos.copy())
    if _die.top_face() is not None:  # if the die has a face that was already determined from a prior move...
        expected_num = _die.score + (_die.top_face() * _die.moves)  # the value that the grid SHOULD be if this is a valid move
        if expected_num == pos_num:  # check if it matches the grid value to see if the move is valid
            _die.score = pos_num  # if it's valid, then update the tracked value
            return _die  # return the die object
        else:
            return None  # invalid move, return nothing
    else:  # if die face is yet to be determined, the move is valid no matter what
        top_face = (pos_num - _die.score) / _die.moves  # you can easily work backwards, knowing the die values, to get what the face SHOULD be if this is a valid move
        _die.set_top_face(top_face)
        _die.score = pos_num  # update stored die values, of course
        return _die  # return die object


correct_found = False


def recursing_solve(_die: GameDie, exitDepth=1, currentDepth=0):
    global correct_found
    if correct_found:  # to exit other recursions if solution is found
        return
    _die.visited.append(_die.pos.copy())  # any die entering this function just completed a valid move, add the position to its moves list
    adj_pos_list = get_adjacent_pos(_die.pos.copy())  # returns a list of [x, y] formatted coords of adjacent squares
    future_die_states = []
    succ_count = 0  # succ_count isn't necessary for solution, just used for debug outputs
    for i in [0, 1, 2, 3]:
        if adj_pos_list[i] is None:  # adjacent positions are 'None' if they are off the edge of the board
            continue
        succ_count += 1
        if i == 0:  # python doesn't have switch statements...
            future_die_states.append(valid_pos_filter(deepcopy(_die).rotate_left()))  # each of these appends is a new die object, translated in a direction
        if i == 1:
            future_die_states.append(valid_pos_filter(deepcopy(_die).rotate_right()))  # or 'None' if it doesn't pass the valid_pos_filter
        if i == 2:
            future_die_states.append(valid_pos_filter(deepcopy(_die).rotate_up()))  # which checks the moved die to see if the move was valid
        if i == 3:
            future_die_states.append(valid_pos_filter(deepcopy(_die).rotate_down()))

    if succ_count == 0:  # dead end?
        print()
        print("--------------------", currentDepth)
        _die.printMe()
        print_grid(_die)
    else:
        print('.{}'.format(currentDepth), end="")  # debug printout/progress bar

    if _die.pos[0] == 5 and _die.pos[1] == 0:  # if we have reached the end, we have a valid die
        correct_found = True  # set global value to exit other recursions
        print()
        _die.printMe()
        print("Final grid: ")  # printouts of the valid die's values
        print_grid(_die)
        result = 0
        for x in [0, 1, 2, 3, 4, 5]:
            for y in [0, 1, 2, 3, 4, 5]:
                if [x, y] in _die.visited:  # for all grid positions, we specifically don't want positions the die visited
                    continue
                result += get_grid_at_pos([x, y])  # add unvisited square values to the result
        print("Tally of empty space values: ")
        print(result)
        print()


    currentDepth += 1
    if currentDepth >= exitDepth:  # honestly doesn't do much at this moment, was useful for exiting code early during debug
        print("reached depth limit!")
        return

    for die in future_die_states:
        if die is not None:
            recursing_solve(die, exitDepth, currentDepth)  # continue solving for valid die moves


def find_solution():
    my_die = GameDie()  # initial die object
    recursing_solve(my_die, 55)


find_solution()
