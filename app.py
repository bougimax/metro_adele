from flask import Flask, request, render_template, render_template_string
from Utils import construct_metro_map, create_solution_map

app = Flask(__name__)

metro_map = construct_metro_map()


@app.route("/")
def home():
    return render_template("index.html")


SOURCE = ""
TARGET = ""
ROUTE = None
TEXT_ROUTE = ""


@app.route("/play", methods=["GET", "POST"])
def play():
    global TEXT_ROUTE, SOURCE, TARGET, ROUTE
    if request.method == "POST":
        list_route = "\n".join([f"<li>{l}</li>" for l in TEXT_ROUTE])
        m = create_solution_map(metro_map, ROUTE)
        m.get_root().width = "800px"
        m.get_root().height = "600px"
        iframe = m.get_root()._repr_html_()
        return render_template_string(
            f"""
            <!DOCTYPE html>
            <html>
                <head></head>
                <body>
                   <p>Une de(s) meilleure(s) route(s) possible de {SOURCE} à {TARGET} était de:</p>
                   <ul>
                        {list_route}
                   </ul>
                    {"{{ iframe|safe }}"}
                   <a href="play"><h1>Play again</h1></a>
                </body>
            </html>
        """,
            iframe=iframe,
        )
    else:
        SOURCE = metro_map.get_random_node()
        TARGET = metro_map.get_random_node()

        dist, pred = metro_map.bfs(SOURCE)

        ROUTE = metro_map.get_route(TARGET, pred)
        TEXT_ROUTE = metro_map.print_route(ROUTE)

        return f"""<p>Trouver l'itinéraire de {SOURCE} à {TARGET}</p>
                    <p>Press button to show solution</p>
                    <form method="post">
                        <input type="submit" value="Solution">
                    </form>
                """


if __name__ == "__main__":
    app.run()
