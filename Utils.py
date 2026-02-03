from Graph import Graph
import pathlib

LIGNES = pathlib.Path("lignes")


def construct_metro_map():
    g = Graph()

    for file in LIGNES.iterdir():
        with open(file, "r") as f:
            filepath = str(file.stem)
            line_name = (
                filepath.split(".md")[0]
                .split("_branche")[0]
                .split("_direction")[0]
                .replace("_", " ")
                .title()
            )
            line_number = line_name.split("Ligne ")[1]
            add_undirected = True
            if str(file).count("direction") > 0:
                add_undirected = False
            lines = list(map(str.strip, f.readlines()))
            for u, v in zip(lines[:-1], lines[1:]):
                if add_undirected:
                    g.add_undirected_edge(
                        f"{u}_{line_number}", f"{v}_{line_number}", {"line": line_name}
                    )
                else:
                    g.add_directed_edge(
                        f"{u}_{line_number}", f"{v}_{line_number}", {"line": line_name}
                    )
                g.connect_correspondance(f"{u}_{line_number}")
                g.connect_correspondance(f"{v}_{line_number}")

    return g
