from Graph import Graph
import folium
import pathlib
import json
from levenshtein import levenshtein_linear_space
import xyzservices.providers as xyz

LIGNES = pathlib.Path("lignes")


def read_coord(c):
    deg, *q = c.split("°\xa0")
    minu, *q = q[0].split("′\xa0")
    sec = q[0][:-3].split("″")[0]
    sec = 0 if sec == "" else sec
    return float(deg) + float(minu) / 60 + float(sec) / 3600


def parse_lat_lon(loc):
    lat, lon = loc.split(", ")
    return read_coord(lat), read_coord(lon)


def parse_metro_json():
    with open(pathlib.Path("paris_metro_stations.json"), "r") as f:
        d = json.load(f)
        out = {}
        for station in d:
            if "Localisation" in d[station]:
                lat, lon = parse_lat_lon(d[station]["Localisation"])
                out[station.replace(" (Paris Metro)", "")] = {"coord": (lat, lon)}
        with open(pathlib.Path("localisations_stations.json"), "w") as o:
            json.dump(out, o)


def get_closest_name(loc, station: str) -> str:
    stations = list(map(lambda s: (levenshtein_linear_space(s, station), s), list(loc)))
    stations.sort()
    return stations[0]


def create_solution_map(metro_map, route):
    with open(pathlib.Path("localisations_stations.json"), "r") as f:
        loc = json.load(f)
    with open(pathlib.Path("line_colors.json"), "r") as f:
        colors = json.load(f)
    tile_provider = xyz.Stadia.Outdoors
    tile_provider["url"] = (
        tile_provider["url"] + "?api_key=eb79dcc1-ccf0-4c3a-938d-104234e5fbde"
    )
    m = folium.Map(location=(48.85341, 2.3488), zoom_start=12)
    folium.TileLayer(
        tiles=tile_provider.build_url(api_key="eb79dcc1-ccf0-4c3a-938d-104234e5fbde"),
        attr=tile_provider.attribution,
        name=tile_provider.name,
    ).add_to(m)
    _, start_loc = get_closest_name(loc, metro_map.get_station_name(route[0]))
    _, end_loc = get_closest_name(loc, metro_map.get_station_name(route[-1]))
    kw_start = {"prefix": "fa", "color": "green", "icon": "arrow-up"}
    angle_start = 45
    icon_start = folium.Icon(angle=angle_start, **kw_start)
    kw_end = {"prefix": "fa", "color": "red", "icon": "arrow-down"}
    angle_end = 315
    icon_end = folium.Icon(angle=angle_end, **kw_end)
    folium.Marker(
        loc[start_loc]["coord"],
        tooltip=f"Début à {metro_map.get_station_name(route[0])}",
        icon=icon_start,
    ).add_to(m)
    folium.Marker(
        loc[end_loc]["coord"],
        tooltip=f"Fin à {metro_map.get_station_name(route[-1])}",
        icon=icon_end,
    ).add_to(m)
    for u, v in zip(route[:-1], route[1:]):
        _, u_loc = get_closest_name(loc, metro_map.get_station_name(u))
        _, v_loc = get_closest_name(loc, metro_map.get_station_name(v))
        if metro_map._adjacency[u][v]["line"] != "Correspondance":
            color = f"#{colors.get(metro_map.get_line_name(u),"000000").lower()}"
            folium.PolyLine(
                [
                    loc[u_loc]["coord"],
                    loc[v_loc]["coord"],
                ],
                tooltip=f"De {metro_map.get_station_name(u)} à {metro_map.get_station_name(v)}",
                color=color,
                weight=6,
            ).add_to(m)
    vu = set()
    for u in route[1:-1]:
        _, u_loc = get_closest_name(loc, metro_map.get_station_name(u))
        if metro_map.get_line_name(u) == "":
            vu.add(u_loc)
            radius = 10
            folium.CircleMarker(
                location=loc[u_loc]["coord"],
                radius=radius,
                color="#25303b",
                fill=True,
                fill_color="white",
                fill_opacity=1,
                opacity=1,
                tooltip=u_loc,
            ).add_to(m)
        elif u_loc not in vu:
            radius = 5
            folium.CircleMarker(
                location=loc[u_loc]["coord"],
                radius=radius,
                color="#25303b",
                fill=True,
                fill_color="#25303b",
                fill_opacity=1,
                opacity=1,
                tooltip=u_loc,
            ).add_to(m)

    return m


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
