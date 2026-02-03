from Utils import construct_metro_map


def main():
    metro_map = construct_metro_map()

    source: str = metro_map.get_random_node()
    target: str = metro_map.get_random_node()

    print(f"Trouver l'itinéraire de {source} à {target}")

    dist, pred = metro_map.bfs(source)

    route = metro_map.get_route(target, pred)

    to_print = metro_map.print_route(route)

    print("\n".join(to_print))


if __name__ == "__main__":
    main()
