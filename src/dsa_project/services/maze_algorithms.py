import random
from collections import deque


def generate_maze(maze):
    """Build a spanning tree using randomized DFS and explicit graph edges."""
    steps = []
    start = maze.start
    visited = {start}
    stack = [start]
    steps.append({"type": "visit", "vertex": start, "message": f"Starting at vertex {start}"})
    steps.append({"type": "current", "vertex": start, "message": "Starting randomized DFS maze generation"})

    while stack:
        current = stack[-1]
        candidates = [v for v in maze.get_grid_neighbors(current) if v not in visited]
        random.shuffle(candidates)
        if candidates:
            neighbor = candidates[0]
            maze.add_passage(current, neighbor)
            visited.add(neighbor)
            steps.append({"type": "add_edge", "u": current, "v": neighbor,
                          "message": f"Adding edge {current} — {neighbor}"})
            steps.append({"type": "visit", "vertex": neighbor,
                          "message": f"Discovering vertex {neighbor}"})
            steps.append({"type": "current", "vertex": neighbor,
                          "message": f"Moving to vertex {neighbor}"})
            stack.append(neighbor)
        else:
            stack.pop()
            if stack:
                steps.append({"type": "backtrack", "vertex": stack[-1],
                              "message": f"Backtracking to vertex {stack[-1]}"})

    steps.append({"type": "complete", "message": "Maze generation complete. The graph is a spanning tree."})
    return steps


def _reconstruct_path(parent, start, end):
    if end != start and end not in parent:
        return []
    path, current = [], end
    while current is not None:
        path.append(current)
        current = parent.get(current)
    path.reverse()
    return path if path and path[0] == start else []


def breadth_first_search(maze):
    """BFS over the graph adjacency list; finds a shortest unweighted path."""
    start, end = maze.start, maze.end
    queue, visited, parent = deque([start]), {start}, {start: None}
    steps = [{"type": "visit", "vertex": start,
              "message": f"Discovered start vertex {start}"}]
    while queue:
        current = queue.popleft()
        steps.append({"type": "current", "vertex": current,
                      "message": f"Dequeuing vertex {current}"})
        if current == end:
            break
        for neighbor in maze.graph.get_neighbors(current):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            parent[neighbor] = current
            queue.append(neighbor)
            steps.append({"type": "visit", "vertex": neighbor,
                          "message": f"Discovered {neighbor} from {current}"})
    path = _reconstruct_path(parent, start, end)
    if not path:
        steps.append({"type": "complete", "message": "No path exists between the start and end vertices."})
        return steps
    steps.append({"type": "path", "vertices": path,
                  "message": f"BFS found a shortest path with {len(path) - 1} edges."})
    steps.append({"type": "complete", "message": "BFS complete."})
    return steps


def depth_first_search(maze):
    """Iterative DFS over the graph adjacency list; does not ensure shortest path."""
    start, end = maze.start, maze.end
    stack, visited, parent = [start], {start}, {start: None}
    steps = [{"type": "visit", "vertex": start,
              "message": f"Discovered start vertex {start}"}]
    while stack:
        current = stack.pop()
        steps.append({"type": "current", "vertex": current,
                      "message": f"Visiting vertex {current} from the DFS stack"})
        if current == end:
            break
        for neighbor in reversed(maze.graph.get_neighbors(current)):
            if neighbor in visited:
                continue
            visited.add(neighbor)
            parent[neighbor] = current
            stack.append(neighbor)
            steps.append({"type": "visit", "vertex": neighbor,
                          "message": f"Discovering {neighbor} from {current}"})
    path = _reconstruct_path(parent, start, end)
    if not path:
        steps.append({"type": "complete", "message": "No path exists between the start and end vertices."})
        return steps
    steps.append({"type": "path", "vertices": path,
                  "message": (f"DFS found a path with {len(path) - 1} edges. "
                              "DFS does not guarantee the shortest path.")})
    steps.append({"type": "complete", "message": "DFS complete."})
    return steps
