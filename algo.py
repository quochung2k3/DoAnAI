import heapq
def bfs_search(maze, start, end):
    def is_valid_move(maze, row, col):
        if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and (maze[row][col] == '0' or maze[row][col] == 'x' or maze[row][col] == 'y'):
            return True
        return False
    def find_path_bfs(maze, start, end):
        queue = [(start, [])]
        visited = []
        while queue:
            (row, col), path = queue.pop(0)
            if (row, col) == end:
                return path + [(row, col)], visited
            if (row, col) not in visited:
                visited.append((row, col))
                for (r, c) in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
                    if is_valid_move(maze, r, c):
                        queue.append(((r, c), path + [(row, col)]))
        return None, visited
    path, visited = find_path_bfs(maze, start, end)
    return path, visited

def dfs_search(maze, start, end):
    def is_valid_move(maze, row, col):
        if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and (maze[row][col] == '0' or maze[row][col] == 'x' or maze[row][col] == 'y'):
            return True
        return False
    def find_path_dfs(maze, current, end, visited, path):
        visited.append(current)
        if current == end:
            return path + [current], visited
        for (r, c) in [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
                       (current[0], current[1] - 1), (current[0], current[1] + 1)]:
            if is_valid_move(maze, r, c) and (r, c) not in visited:
                result, visited = find_path_dfs(maze, (r, c), end, visited, path + [current])
                if result:
                    return result, visited
        return None, visited
    path, visited = find_path_dfs(maze, start, end, [], [])
    return path, visited

def ucs_search(maze, start, end):
    def is_valid_move(maze, row, col):
        if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and (maze[row][col] == '0' or maze[row][col] == 'x' or maze[row][col] == 'y'):
            return True
        return False
    def find_path_ucs(maze, start, end):
        priority_queue = [(0, start, [])]
        visited = []
        while priority_queue:
            cost, (row, col), path = heapq.heappop(priority_queue)
            if (row, col) == end:
                return path + [(row, col)], visited
            if (row, col) not in visited:
                visited.append((row, col))
                for (r, c) in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
                    if is_valid_move(maze, r, c):
                        new_cost = cost + 1
                        heapq.heappush(priority_queue, (new_cost, (r, c), path + [(row, col)]))
        return None, visited
    path, visited = find_path_ucs(maze, start, end)
    return path, visited

def a_star_search(maze, start, end):
    def heuristic(node, goal):
        return abs(node[0] - goal[0]) + abs(node[1] - goal[1])
    def is_valid_move(maze, row, col):
        if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and (maze[row][col] == '0' or maze[row][col] == 'x' or maze[row][col] == 'y'):
            return True
        return False
    def find_path_a_star(maze, start, end):
        heap = [(0, start, [])]
        visited = []
        while heap:
            _, (row, col), path = heapq.heappop(heap)
            if (row, col) == end:
                return path + [(row, col)], visited
            if (row, col) not in visited:
                visited.append((row, col))
                for (r, c) in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
                    if is_valid_move(maze, r, c):
                        next_cost = len(path) + 1 + heuristic((r, c), end)
                        heapq.heappush(heap, (next_cost, (r, c), path + [(row, col)]))
        return None, visited
    path, visited = find_path_a_star(maze, start, end)
    return path, visited

def gbfs_search(maze, start, end):
    def heuristic(node, goal):
        return ((node[0] - goal[0]) ** 2 + (node[1] - goal[1]) ** 2) ** 0.5
    def is_valid_move(maze, row, col):
        if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and (maze[row][col] == '0' or maze[row][col] == 'x' or maze[row][col] == 'y'):
            return True
        return False
    def find_path_gbfs(maze, start, end):
        queue = [(start, [])]
        visited = []
        while queue:
            queue.sort(key=lambda x: heuristic(x[0], end))
            (row, col), path = queue.pop(0)
            if (row, col) == end:
                return path + [(row, col)], visited
            if (row, col) not in visited:
                visited.append((row, col))
                for (r, c) in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
                    if is_valid_move(maze, r, c):
                        queue.append(((r, c), path + [(row, col)]))
        return None, visited
    path, visited = find_path_gbfs(maze, start, end)
    return path, visited

def greedy_search(maze, start, end):
    def heuristic(node, end):
        return abs(node[0] - end[0]) + abs(node[1] - end[1])
    def is_valid_move(maze, row, col):
        if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and (maze[row][col] == '0' or maze[row][col] == 'x' or maze[row][col] == 'y'):
            return True
        return False
    def find_path_greedy(maze, start, end):
        heap = [(heuristic(start, end), start, [])]
        visited = []
        while heap:
            _, (row, col), path = heapq.heappop(heap)
            if (row, col) == end:
                return path + [(row, col)], visited
            if (row, col) not in visited:
                visited.append((row, col))
                for (r, c) in [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]:
                    if is_valid_move(maze, r, c) and (r, c) not in visited:
                        heapq.heappush(heap, (heuristic((r, c), end), (r, c), path + [(row, col)]))
        return None, visited
    path, visited = find_path_greedy(maze, start, end)
    return path, visited


def ids_search(maze, start, end, max_depth):
    def is_valid_move(maze, row, col):
        if 0 <= row < len(maze) and 0 <= col < len(maze[0]) and (maze[row][col] == '0' or maze[row][col] == 'x' or maze[row][col] == 'y'):
            return True
        return False

    def dls(maze, current, end, visited, path, depth, max_depth):
        visited.append(current)
        if current == end:
            return path + [current], visited
        if depth == max_depth:
            return None, visited
        for (r, c) in [(current[0] - 1, current[1]), (current[0] + 1, current[1]),
                       (current[0], current[1] - 1), (current[0], current[1] + 1)]:
            if is_valid_move(maze, r, c) and (r, c) not in visited:
                result, visited = dls(maze, (r, c), end, visited, path + [current], depth + 1, max_depth)
                if result:
                    return result, visited
        return None, visited

    for depth in range(max_depth + 1):
        path, visited = dls(maze, start, end, [], [], 0, depth)
        if path:
            return path, visited

    return None, visited