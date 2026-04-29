from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List
import copy
import time
from solver import solve_with_ac3, generate_puzzle, is_valid, ac3_log

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Board(BaseModel):
    grid: List[List[int]]

class Move(BaseModel):
    grid: List[List[int]]
    row: int
    col: int
    num: int

@app.post("/solve")
async def solve_puzzle(board: Board):
    grid_to_solve = copy.deepcopy(board.grid)
    
    start_time = time.time()
    success = solve_with_ac3(grid_to_solve)
    end_time = time.time()
    
    if success:
        # Calculate details for the UI
        details = {
            "algorithm": "AC-3 Constraint Propagation + Backtracking",
            "time_ms": round((end_time - start_time) * 1000, 2),
            "ac3_steps": len(ac3_log)
        }
        return {"status": "success", "grid": grid_to_solve, "details": details}
    else:
        raise HTTPException(status_code=400, detail="No solution exists for this board.")

@app.post("/generate")
async def generate_new_puzzle():
    puzzle, solution = generate_puzzle(remove=45)
    return {"status": "success", "grid": puzzle, "solution": solution}

@app.post("/validate")
async def validate_user_move(move: Move):
    temp_val = move.grid[move.row][move.col]
    move.grid[move.row][move.col] = 0
    valid = is_valid(move.grid, move.row, move.col, move.num)
    move.grid[move.row][move.col] = temp_val
    return {"valid": valid}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)