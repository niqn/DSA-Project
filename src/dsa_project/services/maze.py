class Graph:
    """Undirected graph represented by an adjacency list."""

    def __init__(self):
        self.adjacency_list = {}

    def add_vertex(self, vertex):
        self.adjacency_list.setdefault(vertex, [])

    def add_edge(self, u, v):
        if u not in self.adjacency_list or v not in self.adjacency_list:
            return False
        if v not in self.adjacency_list[u]:
            self.adjacency_list[u].append(v)
        if u not in self.adjacency_list[v]:
            self.adjacency_list[v].append(u)
        return True

    def get_neighbors(self, vertex):
        return list(self.adjacency_list.get(vertex, []))

    def get_edges(self):
        return [(u, v) for u, neighbors in self.adjacency_list.items()
                for v in neighbors if u < v]

    def to_dict(self):
        return {vertex: list(neighbors)
                for vertex, neighbors in self.adjacency_list.items()}

    @classmethod
    def from_dict(cls, adjacency_list):
        if not isinstance(adjacency_list, dict):
            raise ValueError("Invalid graph adjacency list.")
        graph = cls()
        for vertex, neighbors in adjacency_list.items():
            if not isinstance(vertex, str) or not isinstance(neighbors, list):
                raise ValueError("Invalid graph vertex or neighbor list.")
            if not all(isinstance(n, str) for n in neighbors):
                raise ValueError("Invalid graph neighbor.")
            graph.add_vertex(vertex)
        for vertex, neighbors in adjacency_list.items():
            for neighbor in neighbors:
                if neighbor not in graph.adjacency_list:
                    raise ValueError("Graph contains an unknown vertex.")
                graph.add_edge(vertex, neighbor)
        return graph


class Maze:
    """Grid coordinates for display; all connectivity lives in Graph."""

    def __init__(self, rows, cols):
        if type(rows) is not int or type(cols) is not int or rows < 1 or cols < 1:
            raise ValueError("Rows and columns must be positive integers.")
        self.rows = rows
        self.cols = cols
        self.start = "0-0"
        self.end = f"{rows - 1}-{cols - 1}"
        self.cells = [[{"id": f"{r}-{c}", "row": r, "col": c}
                       for c in range(cols)] for r in range(rows)]
        self.graph = Graph()
        for row in self.cells:
            for cell in row:
                self.graph.add_vertex(cell["id"])

    def get_grid_neighbors(self, vertex):
        """Potential orthogonal neighbors, used only when generating edges."""
        try:
            row, col = (int(part) for part in vertex.split("-"))
        except (AttributeError, ValueError):
            return []
        candidates = ((row - 1, col), (row, col + 1),
                      (row + 1, col), (row, col - 1))
        result = []
        for r, c in candidates:
            if 0 <= r < self.rows and 0 <= c < self.cols:
                result.append(f"{r}-{c}")
        return result

    def add_passage(self, u, v):
        if v not in self.get_grid_neighbors(u):
            return False
        return self.graph.add_edge(u, v)

    def to_dict(self):
        return {
            "rows": self.rows,
            "cols": self.cols,
            "start": self.start,
            "end": self.end,
            "cells": self.cells,
            "graph": self.graph.to_dict(),
            "edges": [{"from": u, "to": v} for u, v in self.graph.get_edges()],
        }

    @classmethod
    def from_dict(cls, data):
        if not isinstance(data, dict):
            raise ValueError("Invalid maze data.")
        rows, cols = data.get("rows"), data.get("cols")
        if type(rows) is not int or type(cols) is not int or not (1 <= rows <= 30 and 1 <= cols <= 30):
            raise ValueError("Invalid maze dimensions.")
        maze = cls(rows, cols)
        graph = Graph.from_dict(data.get("graph"))
        if len(graph.adjacency_list) != rows * cols:
            raise ValueError("Graph does not contain the expected maze vertices.")
        if set(graph.adjacency_list) != set(maze.graph.adjacency_list):
            raise ValueError("Graph vertices do not match the maze grid.")
        start, end = data.get("start"), data.get("end")
        if start not in graph.adjacency_list or end not in graph.adjacency_list:
            raise ValueError("Invalid start or end vertex.")
        for u, neighbors in graph.adjacency_list.items():
            for v in neighbors:
                if v not in maze.get_grid_neighbors(u):
                    raise ValueError("Maze edges must connect adjacent cells.")
                if u not in graph.get_neighbors(v):
                    raise ValueError("Graph edges must be undirected.")
        maze.start, maze.end, maze.graph = start, end, graph
        return maze
