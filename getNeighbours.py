def getNeighbours(grid, grid_rows, grid_cols, row, column, b):
    openNeighbours = 0
    min_neighbours = 2
    if row > 0:
        if grid[row-1][column] == 1:
            if b:
                if getNeighbours(grid, grid_rows, grid_cols, row-1, column, False) > min_neighbours:
                    openNeighbours += 1
            else:
                openNeighbours += 1
    if row < grid_rows-1:
        if grid[row+1][column] == 1:
            if b:
                if getNeighbours(grid, grid_rows, grid_cols, row+1, column, False) > min_neighbours:
                    openNeighbours += 1
            else:
                openNeighbours += 1
    if column > 0:
        if grid[row][column-1] == 1:
            if b:
                if getNeighbours(grid, grid_rows, grid_cols, row, column-1, False) > min_neighbours:
                    openNeighbours += 1
            else:
                openNeighbours += 1
    if column < grid_cols-1:
        if grid[row][column+1] == 1:
            if b:
                if getNeighbours(grid, grid_rows, grid_cols, row, column+1, False) > min_neighbours:
                    openNeighbours += 1
            else:
                openNeighbours += 1
    return openNeighbours