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
        head = """
                    <head>
                      <title>Iti</title>
                      <style>
                        @font-face {
                            font-family: 'Parisine';
                            src: url('../fonts/Parisine_Regular.otf') format('otf');
                        }
                        body {
                            background-color: rgb(255,255,255);
                        }
                        html {
                            font-family: "Parisine", "Courier New";
                        }
                        .play-button{
                            position: absolute;
                            top: 90%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                            background-color: rgb(5,13,158);
                            color: rgb(255,255,255);
                            text-decoration: none;
                            font-weight: bold;
                            padding: 10px;
                        }
                        .reponse {
                            position: absolute;
                            top: 50%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                            display: flex;
                        }
                      </style>
                    </head>
                """
        return render_template_string(
            f"""
            <!DOCTYPE html>
            <html>
                {head}
                <body>
                    <div class="reponse">
                        <div class="texte-reponse">
                           <p>Une de(s) meilleure(s) route(s) possible de {SOURCE} à {TARGET} était de:</p>
                           <ul>
                                {list_route}
                           </ul>
                       </div>
                        {"{{ iframe|safe }}"}
                    </div>
                   <a href="play" class="play-button">Play again</a>
                </body>
            </html>
        """,
            iframe=iframe,
        )
    else:
        SOURCE = metro_map.get_random_node()
        TARGET = metro_map.get_random_node()

        dist, pred = metro_map.dijkstra(SOURCE)

        ROUTE = metro_map.get_route(TARGET, pred)
        TEXT_ROUTE = metro_map.print_route(ROUTE)
        head = """
                    <head>
                      <title>Iti</title>
                      <style>
                        @font-face {
                            font-family: 'Parisine';
                            src: url('../fonts/Parisine_Regular.otf') format('otf');
                        }
                        body {
                            background-color: rgb(255,255,255);
                        }
                        html {
                            font-family: "Parisine", "Courier New";
                        }
                        .play-button{
                            background-color: rgb(5,13,158);
                            color: rgb(255,255,255);
                            text-decoration: none;
                            font-weight: bold;
                            padding: 10px;
                            width: fit-content;
                        }
                        .reponse {
                            position: absolute;
                            top: 50%;
                            left: 50%;
                            transform: translate(-50%, -50%);
                            display: flex;
                        }
                        input{
                            text-decoration: none;
                            background-color: rgb(5,13,158);
                            color: rgb(255,255,255);
                            font-family: "Parisine", "Courier New";
                            text-decoration: none;
                            font-weight: bold;
                            border: none;
                            cursor: pointer;
                        }
                      </style>
                    </head>
                """
        return render_template_string(
            f"""
            <!DOCTYPE html>
            <html>
                {head}
                <body>
                    <div class="reponse">
                        <div class="texte-reponse">
                            <p>Trouver l'itinéraire de {SOURCE} à {TARGET}</p>
                            <form method="post" class="play-button">
                                <input type="submit" value="Solution">
                            </form>
                       </div>
                    </div>
                </body>
            </html>
        """,
        )


if __name__ == "__main__":
    app.run()
