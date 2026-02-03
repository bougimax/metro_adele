from flask import Flask, request, render_template
from Utils import construct_metro_map

app = Flask(__name__)

metro_map = construct_metro_map()


@app.route("/")
def home():
    return render_template("index.html")


SOURCE = ""
TARGET = ""
TEXT_ROUTE = ""


@app.route("/play", methods=["GET", "POST"])
def play():
    global TEXT_ROUTE, SOURCE, TARGET
    if request.method == "POST":
        list_route = "\n".join([f"<li>{l}</li>" for l in TEXT_ROUTE])
        return f"""<p>La meilleure route de {SOURCE} à {TARGET} était de:</p>
                   <ul>
                        {list_route}
                   </ul>
                   <a href="play"><h1>Play again</h1></a>
                """
    else:
        SOURCE = metro_map.get_random_node()
        TARGET = metro_map.get_random_node()

        dist, pred = metro_map.bfs(SOURCE)

        TEXT_ROUTE = metro_map.print_route(metro_map.get_route(TARGET, pred))

        return f"""<p>Trouver l'itinéraire de {SOURCE} à {TARGET}</p>
                    <p>Press button to show solution</p>
                    <form method="post">
                        <input type="submit" value="Solution">
                    </form>
                """


if __name__ == "__main__":
    app.run()
