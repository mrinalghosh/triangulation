import requests
import os
import json
import logging
from dataclasses import dataclass

CURRENCY_FILE = 'currency.json'


class Graph:
    def __init__(self, vertices: dict, edges: list) -> None:
        self.vertices = vertices
        self.edges = edges  # list of (u,v,w)

    def __str__(self) -> str:
        s = 'Graph\n'
        for vert in self.vertices.values():
            for e in self.edges:
                if e.u == vert.code:
                    s += f'{e.u} -> {e.v} [{e.w}]\n'
            s += '----------\n'
        return s


@dataclass
class Vertex:
    code: str
    name: str
    distance: float = float('inf')
    predecessor = None  # Vertex


@dataclass
class Edge:
    u: str
    v: str
    w: float


def bellman_ford(graph: Graph):
    # pick arbitrary source
    source: Vertex = graph.vertices['USD']

    # 1. initialize graph
    # vertex distances already initialized to infinity, predecessor to None
    source.distance = 0

    # 2. relax edges |V|-1 times
    for _ in range(len(graph.vertices)-1):
        for (u, v, w) in graph.edges:
            if graph.vertices[u].distance + w < graph.vertices[v]:
                # relax edge
                graph.vertices[v] = graph.vertices[u].distance + w
                graph.vertices[v].predecessor = graph.vertices[u]

    # 3. check for negative weight cycles - TODO


def download_currencies() -> dict:
    url = 'https://openexchangerates.org/api/currencies.json'
    r = requests.get(url)
    return r.json()


def download(curr) -> dict:
    url = f'https://open.er-api.com/v6/latest/{curr}'
    r = requests.get(url)
    return r.json()['rates']  # NOTE: contains <curr>: 1


def save(data: dict, file):
    with open(file, 'w') as f:
        json.dump(data, f, ensure_ascii=False)
        logging.info(f'wrote data to {file}')


def load(file):
    with open(file, 'r') as f:
        # NOTE: context manager acts as a 'finally' clause before return
        data = json.load(f)
        logging.info(f'loaded data from {file}')
        return data


# clean data?

# process into graph-like structure?


if __name__ == '__main__':
    # setup logging
    logging.basicConfig()
    logging.root.setLevel(level=logging.INFO)

    # (down)load currency names
    if os.path.exists(CURRENCY_FILE):
        currencies = load(CURRENCY_FILE)
    else:
        currencies = download_currencies()
        save(currencies, CURRENCY_FILE)

    vertices = {code: Vertex(code, name) for code, name in currencies.items()}
    # print(vertices)

    # get edge weights

    # TODO: store edge weights to prevent unnecessary calls to API
    edges = []
    for cur in currencies.keys():
        exchange_rates = download(cur)
        for to_cur, rate in exchange_rates.items():
            if to_cur in currencies and to_cur != cur:
                edges.append(Edge(cur, to_cur, rate))
    # print(edges)

    graph = Graph(vertices, edges)

    print(graph)

    # print(currencies)
