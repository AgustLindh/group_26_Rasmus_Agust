# built-in imports
# standard library imports
import ast
import csv
import pickle
from urllib.request import urlretrieve

# internal imports
from codeapp import db
from codeapp.models import AiAndMlJobs


def get_data_list() -> list[AiAndMlJobs]:
    """
    Function responsible for downloading the dataset from the source, translating it
    into a list of Python objects, and saving it to a Redis list.
    """
    url = " https://onu1.s2.chalmers.se/datasets/AI_ML_jobs.csv"
    path = "AiAndMlJobs.csv"
    urlretrieve(url, path)

    with open(path, encoding='utf-8') as csvfile:
        csv_data = csv.DictReader(csvfile)

        type_data: list[AiAndMlJobs] = []

        row: list[str]

        for row_raw in csv_data:
            row = list(row_raw.values())

            type_data.append(AiAndMlJobs(
                str(row[0]),
                str(row[1]),
                str(row[2]),
                str(row[3]),
                str(row[4]),
                float(row[5]),
                list(ast.literal_eval(row[6])),
            ))

    db.set("dataset", pickle.dumps(type_data))

    return type_data


def calculate_statistics(dataset: list[AiAndMlJobs]) -> dict[str, int]:
    """
    Receives the dataset in the form of a list of Python objects, and calculates the
    statistics necessary.
    """
    locations = [row.location for row in dataset]

    max_salarys: list[int] = []
    unique_locations: list[str] = []
    location_salarys: list[float] = []
    for location in set(locations):
        location_salarys = []
        for row in dataset:
            if row.location == location:
                location_salarys.append(float(row.salary))
        max_salarys.append(int(max(location_salarys)))
        unique_locations.append(location)

    out_dict: dict[str, int] = dict(zip(unique_locations, max_salarys))

    return out_dict


def prepare_figure(input_figure: str) -> str:
    """
    Method that removes limits to the width and height of the figure. This method must
    not be changed by the students.
    """
    output_figure = input_figure.replace('height="345.6pt"', "").replace(
        'width="460.8pt"', 'width="100%"'
    )
    return output_figure
