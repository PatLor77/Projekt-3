from typing import Any, Optional, Dict, List


# Obiekt typu vertex (wierzcholek)
# Przechowuje on dane wierzcholka, oraz jego index
class Vertex:
    # data: Any
    # index: int
    # Konstruktor klasy Vertex, pobiera dane w wierzcholku, oraz index
    def __init__(self, data: Any, index: int):
        self.data = data
        self.index = index


# Obiekt typu Edge (krawedz)
# Przechowuje ona wierzcholek poczatkowy, wierzcholek odcelowy,oraz opcjonalna wage
class Edge:
    # source: Vertex
    # destination: Vertex
    # weight: Optional[float]
    # Konstruktor klasy Edge, pobiera Wierzcholek poczatkowy, Wierzcholek docelowy
    # oraz opcjonalna wage (ustawiona domyslnie na None)
    def __init__(self, source: Vertex, destination: Vertex, weight: Optional[float] = None):
        self.source = source
        self.destination = destination
        self.weight = weight


# Obiekt typu graf
class Graph:
    # adjacencies: Dict[Vertex, List[Edge]]
    # Konstruktor klasy grafu, pobiera ewentualny slownik z wierzcholkami, oraz krawedziami
    # Poczatkowo (domyslnie) ustawiony na pusty slownik
    def __init__(self, adjacencies: Dict[Vertex, List[Edge]] = {}):
        self.adjacencies = adjacencies

    # Metoda tworzaca nowy wierzcholek i dodajaca go do slownika adjacencies
    # jako klucz, a jako wartosc pusta liste
    def create_vertex(self, data: Any) -> Vertex:
        v = Vertex(data, len(self.adjacencies))
        self.adjacencies[v] = []
        # Wierzcholek ktory zostal dodany, jest zwracany
        return v

    # Metoda dodajaca nowa krawedz do adjacencies (czyli pod kluczem source, jest nadawana
    # wartosc destination)
    def add_edge(self, source: Vertex, destination: Vertex, weight: Optional[float] = None) -> None:
        e = Edge(source, destination, weight)
        self.adjacencies[e.source].append(e.destination)

    # Metoda znajdujaca wszystkie najkrotsze sciezki od wierzcholka
    # start, do kazdego innego.
    # Zwracana wartoscia jest slownik ktory jako klucze ma wierzcholki docelowe
    # a jako wartosci wszystkie przejscia od wierzcholka startowego, do docelowego
    def all_shortest_paths(self, start):
        # Wszystkie wierzcholki docelowe (czyli wszystkie wierzcholki poza startowym)
        destinations = list(self.adjacencies.keys())
        destinations.remove(start)
        # Slownik z wynikami
        dictionary_result = {}
        # Dla kazdego wierzcholka docelowego, szukamy sciezke
        for dest in destinations:
            wynik = self.bfs(start, dest)
            wynik = [w.data for w in wynik]  # list comprehension
            dictionary_result[dest.data] = wynik
            print(f"Najkrotsza sciezka od {start.data} do {dest.data} to", wynik)
        return dictionary_result

    def bfs(self, start, dest):
        explored = []
        queue = [[start]]

        while queue:
            path = queue.pop(0)
            node = path[-1]

            if node not in explored:
                neighbours = self.adjacencies[node]

                for neighbour in neighbours:
                    new_path = list(path)
                    new_path.append(neighbour)
                    queue.append(new_path)

                    if neighbour == dest:
                        return new_path
                explored.append(node)

    # Wyswietlanie grafu
    def show(self):
        for key, value in self.adjacencies.items():
            print(key.data, [val.data for val in value])


# Zwracamy wierzcholek ktory posiada nazwe == data
def get_vertex(vertex_list: List[Vertex], data: str) -> Vertex:
    for vertex in vertex_list:
        if vertex.data == data:
            return vertex


# Tworzymy graf startujac od slownika podanego jako parametr
def init_graph(data_dict: Dict[str, List[str]]) -> Graph:
    g = Graph()
    v = []
    for vertex in data_dict.keys():
        v.append(g.create_vertex(vertex))

    for vertex in v:
        for edge in data_dict[vertex.data]:
            g.add_edge(vertex, get_vertex(v, edge))
    return g, v


if __name__ == "__main__":
    # Slownik inicjujacy graf 1
    graph1 = {'A': ['B', 'E', 'C'],
              'B': ['A', 'D', 'E'],
              'C': ['A', 'F', 'G'],
              'D': ['B', 'E'],
              'E': ['A', 'B', 'D'],
              'F': ['C'],
              'G': ['C']}
    # Slownik inicjujacy graf 2
    graph2 = {'A': ['D', 'C'],
              'B': ['D', 'E'],
              'C': ['A'],
              'D': ['A', 'B', 'E'],
              'E': ['B', 'D', 'C', 'F'],
              'F': ['E']}
    # Slownik inicjujacy graf 3
    graph3 = {'A': ['B', 'G'],
              'B': ['A', 'C'],
              'C': ['B', 'D'],
              'D': ['C', 'E'],
              'E': ['D', 'F'],
              'F': ['E', 'G'],
              'G': ['F', 'A']}

    # g, v = init_graph(graph1)
    # g, v = init_graph(graph2)
    g, v = init_graph(graph3)
    print("Wyswietlanie grafu:")
    g.show()
    print("\nWyswietlanie najkrotszych sciezek w czytelny sposob: ")
    wynik_slownik = g.all_shortest_paths(v[0])
    print("\nWyswietlanie najkrotszych sciezek w formie slownika: ")
    print(wynik_slownik)