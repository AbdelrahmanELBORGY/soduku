import copy
import random
from collections import deque

ac3_log = []

def get_neighbors(cell):
    r, c = cell
    neighbors = set()
    # Row and Column neighbors
    for i in range(9):
        if i != c: neighbors.add((r, i))
        if i != r: neighbors.add((i, c))
    # 3x3 Box neighbors
    start_r, start_c = (r // 3) * 3, (c // 3) * 3
    for i in range(3):
        for j in range(3):
            if start_r + i != r or start_c + j != c:
                neighbors.add((start_r + i, start_c + j))
    return neighbors

def is_valid(board, row, col, num):
    if num in board[row]: return False
    for i in range(9):
        if board[i][col] == num: return False
    start_r, start_c = (row//3)*3, (col//3)*3
    for i in range(3):
        for j in range(3):
            if board[start_r+i][start_c+j] == num:
                return False
    return True

def find_empty(board):
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0: return r, c
    return None

def solve_random(board):
    empty = find_empty(board)
    if not empty: return True
    r, c = empty
    nums = list(range(1, 10))
    random.shuffle(nums)
    for num in nums:
        if is_valid(board, r, c, num):
            board[r][c] = num
            if solve_random(board): return True
            board[r][c] = 0
    return False

def init_domains(board):
    domains = {}
    for r in range(9):
        for c in range(9):
            if board[r][c] == 0:
                domains[(r, c)] = set(range(1, 10))
            else:
                domains[(r, c)] = {board[r][c]}
    return domains

def revise(domains, xi, xj):
    revised = False
    for x in set(domains[xi]):
        if not any(x != y for y in domains[xj]):
            domains[xi].remove(x)
            revised = True
    return revised

def ac3(domains):
    queue = deque()
    for xi in domains:
        for xj in get_neighbors(xi):
            queue.append((xi, xj))
    step = 0
    ac3_log.clear() 
    while queue:
        xi, xj = queue.popleft()
        snapshot_before = domains[xi].copy()
        changed = revise(domains, xi, xj)
        snapshot_after = domains[xi].copy()
        
        ac3_log.append({
            "step": step, "arc": (xi, xj),
            "before": snapshot_before, "after": snapshot_after, "changed": changed
        })
        
        if changed:
            if len(domains[xi]) == 0: return False, domains
            for xk in get_neighbors(xi):
                queue.append((xk, xi))
        step += 1
    return True, domains

def update_board(board, domains):
    changed = False
    for (r, c), values in domains.items():
        if len(values) == 1:
            val = list(values)[0]
            if board[r][c] == 0:
                board[r][c] = val
                changed = True
    return changed

def find_unassigned(domains):
    for cell in domains:
        if len(domains[cell]) > 1: return cell
    return None

def backtracking_with_domains(domains, board):
    cell = find_unassigned(domains)
    if not cell: return True
    for value in list(domains[cell]):
        if is_valid(board, cell[0], cell[1], value):
            board[cell[0]][cell[1]] = value
            new_domains = copy.deepcopy(domains)
            new_domains[cell] = {value}
            if backtracking_with_domains(new_domains, board): return True
            board[cell[0]][cell[1]] = 0
    return False

def solve_with_ac3(board):
    domains = init_domains(board)
    while True:
        success, domains = ac3(domains)
        if not success: return False
        if not update_board(board, domains): break
    return backtracking_with_domains(domains, board)

def generate_puzzle(remove=40):
    board = [[0]*9 for _ in range(9)]
    solve_random(board)
    full_solution = copy.deepcopy(board) # Save the completed board
    
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)
    for i in range(remove):
        r, c = cells[i]
        board[r][c] = 0
        
    # Return both the puzzle and the answer key
    return board, full_solution