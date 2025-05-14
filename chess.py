from collections import deque

#Print & Board Creation

def print_board(_board, _type="Default"):
    if _type == "Default":
        for rank in _board:
            print(" ".join(rank))
    elif _type == "BOOL":
        for rank in _board:
            print(" ".join("Q" if cell else "." for cell in rank))
    elif _type == "Tour":
        for rank in _board:
            print(" ".join(f"{cell:2}" for cell in rank))

def Board(_FEN=""):
    if _FEN == "BOOL":
        return [[0 for i in range(8)] for i in range(8)]
    elif _FEN == "Tour":
        return [[-1 for i in range(8)] for i in range(8)]
    elif _FEN:
        try:
            edited_FEN = "".join("." * int(char) if char.isdigit() else char for char in _FEN)
            return list(map(list, edited_FEN.split("/")))
        except:
            return -1
    else:
        edited_FEN = "".join("." * int(char) if char.isdigit() else char for char in "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR")
        return list(map(list, edited_FEN.split("/")))

def is_opponent(_piece_1, _piece_2):
    return _piece_1.isupper() and _piece_2.islower() or _piece_1.islower() and _piece_2.isupper()

def piece_place(_board, _piece, _index=0):
    places = []
    for index, element in enumerate(_board):
        for index_1, element_1 in enumerate(element):
            if element_1 == _piece:
                places.append((_piece, index_1, index))

    try:
        return places[_index]
    except IndexError:
        return -1

def piece_threats(_board, _piece_place):
    threats = 0
    directions = {
        "K": [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)],
        "Q": [(0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1)],
        "R": [(0, 1), (1, 0), (0, -1), (-1, 0)],
        "B": [(1, 1), (1, -1), (-1, -1), (-1, 1)],
        "N": [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)],
        "P": [(-1, -1), (1, -1)],
        "p": [(1, 1), (-1, 1)]
    }
    
    if _piece_place:
        for row in range(8):
            for col in range(8):
                attacker = _board[row][col]
                if attacker != "." and not is_opponent(attacker, _piece_place[0]):
                    continue
                drc = []
                match(attacker.upper()):
                    case "K":
                        drc = directions["K"]
                    case "Q":
                        drc = directions["Q"]
                    case "R":
                        drc = directions["R"]
                    case "B":
                        drc = directions["B"]
                    case "N":
                        drc = directions["N"]
                match(attacker):
                    case "P":
                        drc = directions["P"]
                    case "p":
                        drc = directions["p"]
                        
                if attacker.upper() in ["K", "N", "P"]:
                    for x, y in drc:
                        new_x, new_y = col + x, row + y
                        if 0 <= new_x < 8 and 0 <= new_y < 8 and (new_x, new_y) == _piece_place[1:3]:
                            threats += 1
                            break
                else:
                    for x, y in drc:
                        new_x, new_y = col + x, row + y
                        while 0 <= new_x < 8 and 0 <= new_y < 8:
                            if (new_x, new_y) == _piece_place[1:3]:
                                threats += 1
                                break
                            if _board[new_x][new_y] != ".":
                                break
                            new_x += x
                            new_y += y

    return threats

#Eight Queens Part

def is_safe_q(_board, row, col):
    for i in range(0, col):
        if _board[row][i] == 1:
            return False
    for i, j in zip(range(col, -1, -1), range(row, -1, -1)):
        if _board[j][i] == 1:
            return False
    for i, j in zip(range(col, -1, -1), range(row, 8)):
        if _board[j][i] == 1:
            return False
        
    return True
        
def generator():
    num = 1
    while True:
        yield num
        num += 1

def eight_queens(_board, _gen, _num=0):
    if _num >= 8:
        print(f"\nSolution: {next(_gen)}\n")
        print_board(_board, "BOOL")
        return True
    
    for i in range(8):
        if is_safe_q(_board, i, _num):
            _board[i][_num] = 1
            eight_queens(_board, _gen, _num + 1)
            _board[i][_num] = 0
    
    return False

#Knight Tour

def is_valid(_board, _row, _col):
    return 0 <= _row < 8 and 0 <= _col < 8 and _board[_row][_col] == -1

def num_of_moves(_board, _row, _col):
    knight_moves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
    return sum(1 for x, y in knight_moves if is_valid(_board, y + _row, x + _col))

def knight_tour(_board, _row, _col, _move=1):
    if _move == 64:
        print_board(_board, "Tour")
        return True
    
    knight_moves = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
    moves = []
    for dx, dy in knight_moves:
        new_x, new_y = _col + dx, _row + dy
        if is_valid(_board, new_y, new_x):
            moves.append((num_of_moves(_board, new_y, new_x), new_x, new_y))
            
    moves.sort()
    
    for _, dx, dy in moves:
        _board[dy][dx] = _move
        if knight_tour(_board, dy, dx, _move + 1):
            return True
        _board[dx][dy] = -1
        
    return False
    
#Knight Path

def pos_to_coords(pos):
	return (ord(pos[0]) - ord("a"), int(pos[1]) - 1)

def coords_to_pos(coords):
	return chr(coords[0] + ord("a")) + str(coords[1] + 1)
	
def knight_path(start, end):
	start_coords = pos_to_coords(start)
	end_coords = pos_to_coords(end)
	knight_possibilities = [(1, 2), (1, -2), (-1, 2), (-1, -2), (2, 1), (2, -1), (-2, 1), (-2, -1)]
	
	visited = set()
	queue = deque([start_coords])
	parent = {}
	
	while deque:
		current = queue.popleft()
		if current == end_coords:
			break
			
		if current in visited:
			continue
			
		visited.add(current)
		
		for dc, dr in knight_possibilities:
			new_x, new_y = current[0] + dc, current[1] + dr
			new_pos = (new_x, new_y)
			if 0 <= new_x < 8 and 0 <= new_y < 8 and new_pos not in parent and new_pos:
				parent[new_pos] = current
				queue.append(new_pos)
			
	if end_coords not in parent:
		return -1
		
	path = []
	current = end_coords
	while current != start_coords:
		path.append(coords_to_pos(parent[current]))
		current = parent[current]

	path.reverse()
	path.append(end)
	
	return (len(path) - 1, " => ".join(path))

FEN = "rnbqkbnr/ppp2ppp/8/8/8/8/PPP2PPP/RNBQKBNR"

bool_board = Board("BOOL")
print_board(bool_board, "BOOL")

gen = generator()
eight_queens(bool_board, gen)

tour_board = Board("Tour")
gen = generator()
tour_board[0][0] = 0
knight_tour(tour_board, 0, 0)

print()

board = Board(FEN)

print_board(board)
print(piece_threats(board, piece_place(board, "Q")))

print(knight_path("a1", "h8"))