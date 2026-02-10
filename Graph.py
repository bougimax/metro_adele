from pile import File
from random import choice
import heapq
from math import inf


class Graph:

    def __init__(self):
        self._adjacency = {}
        self._canon_station = []

    def add_node(self, node: str) -> None:
        if node not in self._adjacency:
            self._adjacency[node] = {}
        if self.get_station_name(node) not in self._adjacency:
            self._canon_station.append(self.get_station_name(node))
            self._adjacency[self.get_station_name(node)] = {}

    def add_directed_edge(self, u: str, v: str, attributes=None) -> None:
        self.add_node(u)
        self._adjacency[u][v] = {} if attributes is None else attributes

    def add_undirected_edge(self, u: str, v: str, attributes=None) -> None:
        self.add_directed_edge(u, v, attributes)
        self.add_directed_edge(v, u, attributes)

    def get_station_name(self, u: str) -> str:
        return u.split("_")[0]

    def get_line_name(self, u: str) -> str:
        s = u.split("_")
        if len(s) <= 1:
            return ""
        else:
            return s[1].replace("_", " ").lower()

    def get_neighbours(self, u: str):
        return self._adjacency[u]

    def get_stations(self):
        return self._canon_station

    def connect_correspondance(self, u: str) -> None:
        self.add_undirected_edge(
            self.get_station_name(u), u, {"line": "Correspondance", "weight": 3}
        )

    def bfs(self, s: str):
        f = File()
        f.enfiler(s)
        pred, dist = {}, {}
        vu = set()
        pred[s] = s
        dist[s] = 0
        while not f.est_vide():
            act = f.defiler()
            if act not in vu:
                vu.add(act)
                for neigh in self.get_neighbours(act):
                    if neigh not in vu:
                        f.enfiler(neigh)
                        pred[neigh] = act
                        dist[neigh] = dist[act] + 1
        return dist, pred

    def dijkstra(self, s: str, key=lambda d: d.get("weight", 1)):
        q = []
        heapq.heappush(q, (0, s))
        pred, dist = {}, {}
        vu = set()
        pred[s] = s
        dist[s] = 0
        while q:
            _, act = heapq.heappop(q)
            if act not in vu:
                vu.add(act)
                for neigh in self.get_neighbours(act):
                    if neigh not in vu:
                        updated_d = dist[act] + key(self._adjacency[act][neigh])
                        if updated_d < dist.get(neigh, inf):
                            heapq.heappush(q, (updated_d, neigh))
                            pred[neigh] = act
                            dist[neigh] = updated_d
        return dist, pred

    def get_random_node(self) -> str:
        return choice(self.get_stations())

    def get_route(self, target: str, pred):
        route = [target]
        act = target
        while pred[act] != act:
            route.append(pred[act])
            act = pred[act]
        return route[::-1]

    def print_route(self, route) -> str:
        current_start = None
        current_line = None
        to_print = []
        for u, v in zip(route[:-1], route[1:]):
            if current_line is None:
                current_start = u
                current_line = self._adjacency[u][v]["line"]
            elif self._adjacency[u][v]["line"] != current_line:
                if current_line != "Correspondance":
                    to_print.append(
                        f"Prendre la {current_line} de {self.get_station_name(current_start)} à {self.get_station_name(u)}"
                    )
                current_line = self._adjacency[u][v]["line"]
                current_start = u
        return to_print
