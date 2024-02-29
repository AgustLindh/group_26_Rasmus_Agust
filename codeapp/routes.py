# pylint: disable=cyclic-import
"""
File that contains all the routes of the application.
This is equivalent to the "controller" part in a model-view-controller architecture.
In the final project, you will need to modify this file to implement your project.
"""
# built-in imports
import io

# external imports
from flask import Blueprint, jsonify, render_template
from flask.wrappers import Response as FlaskResponse
from matplotlib.figure import Figure
from werkzeug.wrappers.response import Response as WerkzeugResponse

# internal imports
import codeapp.models as models
from codeapp.utils import calculate_statistics, get_data_list, prepare_figure

# define the response type
Response = str | FlaskResponse | WerkzeugResponse

bp = Blueprint("bp", __name__, url_prefix="/")


################################### web page routes ####################################


@bp.get("/")  # root route
def home() -> Response:

    dataset: list[models.AI_and_ML_jobs] = get_data_list()

    counter: dict[int, int] = calculate_statistics(dataset)

    return render_template("home.html", counter=counter)

@bp.get("/image")
def image() -> Response:

    dataset: list[models.AI_and_ML_jobs] = get_data_list()

    counter: dict[str, int] = calculate_statistics(dataset)

        
    unique_locations: list[str] = []
    max_Salarys: list[float] = []
    for n in counter:
        unique_locations.append(n)
        max_Salarys.append(counter[n])

    max_Sal_uni_loc = zip(max_Salarys, unique_locations)

    max_Sal_uni_loc = sorted(max_Sal_uni_loc)[::-1]

    max_Salarys = [y for x, y in max_Sal_uni_loc]
    unique_locations = [x for x, y in max_Sal_uni_loc]

    # print(len(unique_locations))

    # creating the plot
    fig = Figure()

    fig.gca().bar(max_Salarys, unique_locations, width = 0.4)

    fig.gca().set_xlabel("Locations")
    fig.gca().set_ylabel("Highest Salary $/year")
    fig.gca().set_xticklabels(max_Salarys, rotation = 90)
    fig.tight_layout()


    ################ START -  THIS PART MUST NOT BE CHANGED BY STUDENTS ################
    # create a string buffer to hold the final code for the plot
    output = io.StringIO()
    fig.savefig(output, format="svg")
    # output.seek(0)
    final_figure = prepare_figure(output.getvalue())
    return FlaskResponse(final_figure, mimetype="image/svg+xml")


@bp.get("/about")
def about() -> Response:
    return render_template("about.html")


################################## web service routes ##################################


@bp.get("/json-dataset")
def get_json_dataset() -> Response:

    dataset: list[models.AI_and_ML_jobs] = get_data_list()

    return jsonify(dataset)



@bp.get("/json-stats")
def get_json_stats() -> Response:

    dataset: list[models.AI_and_ML_jobs] = get_data_list()

    counter: dict[int, int] = calculate_statistics(dataset)

    return jsonify(counter)
