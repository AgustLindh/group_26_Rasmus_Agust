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
from codeapp import models
from codeapp.utils import calculate_statistics, get_data_list, prepare_figure

# define the response type
Response = str | FlaskResponse | WerkzeugResponse

bp = Blueprint("bp", __name__, url_prefix="/")


################################### web page routes ####################################


@bp.get("/")  # root route
def home() -> Response:
    dataset: list[models.AiAndMlJobs] = get_data_list()

    counter: dict[str, int] = calculate_statistics(dataset)

    return render_template("home.html", counter=counter)


@bp.get("/image")
def image() -> Response:

    dataset: list[models.AiAndMlJobs] = get_data_list()

    counter: dict[str, int] = calculate_statistics(dataset)

    unique_locations: list[str] = []
    max_salarys: list[float] = []
    for n in counter:
        unique_locations.append(n)
        max_salarys.append(counter[n])

    max_sal_uni_loc: list[tuple[float, str]] = sorted(
        zip(max_salarys, unique_locations))[::-1]

    max_salarys = [x for x, y in max_sal_uni_loc]
    unique_locations = [y for x, y in max_sal_uni_loc]

    # creating the plot
    fig = Figure()

    fig.gca().bar(unique_locations, max_salarys, width=0.4)

    fig.gca().set_xlabel("Locations")
    fig.gca().set_ylabel("Highest Salary $/year")
    fig.gca().set_xticks(range(len(unique_locations)))
    fig.gca().set_xticklabels(unique_locations, rotation=90)
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

    dataset: list[models.AiAndMlJobs] = get_data_list()

    return jsonify(dataset)


@bp.get("/json-stats")
def get_json_stats() -> Response:

    dataset: list[models.AiAndMlJobs] = get_data_list()

    counter: dict[str, int] = calculate_statistics(dataset)

    return jsonify(counter)
