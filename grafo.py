def crearGrafo(nodos, grid, grid_rows, grid_cols):
    grafo = {}
    cont = 0
    for i in range(0,grid_rows):
        for j in range(0, grid_cols):
            if i > 0:
                nodos[i][j].agregarConexion(nodos[i-1][j], max(grid[i][j],grid[i-1][j]))
            if j > 0:
                nodos[i][j].agregarConexion(nodos[i][j-1], max(grid[i][j],grid[i][j-1]))
            if i < grid_rows-1:                
                nodos[i][j].agregarConexion(nodos[i+1][j], max(grid[i][j],grid[i+1][j]))
            if j < grid_cols-1:                
                nodos[i][j].agregarConexion(nodos[i][j+1], max(grid[i][j],grid[i][j+1]))
            grafo[cont] = nodos[i][j]
            cont+=1
    return grafo