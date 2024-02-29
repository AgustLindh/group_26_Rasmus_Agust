# built-in imports
# standard library imports
import pickle
import csv

# external imports
from flask import current_app

# internal imports
from codeapp import db
from codeapp.models import AI_and_ML_jobs

from urllib.request import urlretrieve

def get_data_list() -> list[AI_and_ML_jobs]:
    """
    Function responsible for downloading the dataset from the source, translating it
    into a list of Python objects, and saving it to a Redis list.
    """
    url = " https://onu1.s2.chalmers.se/datasets/AI_ML_jobs.csv"
    path = "AI_and_ML_jobs.csv"
    urlretrieve(url, path)

    with open(path,  encoding='utf-8') as csvfile:
        csv_data = csv.DictReader(csvfile)
   
        rows = [AI_and_ML_jobs(*row.values()) for row in csv_data]
    
    db.set("dataset", pickle.dumps(rows))

    return rows


def calculate_statistics(dataset: list[AI_and_ML_jobs]) -> dict[int | str, int]:
    """
    Receives the dataset in the form of a list of Python objects, and calculates the
    statistics necessary.
    """
    locations = [row.location for row in dataset]

    max_Salarys: list[float] = []
    unique_locations: list[str] = []
    location_Salarys: list[float] = []
    for location in set(locations):
        location_Salarys = []
        for row in dataset:
            if row.location == location:
                location_Salarys.append(float(row.salary))
        max_Salarys.append(max(location_Salarys))
        unique_locations.append(location)

    out_dict: dict[int | str, int] = dict(zip(unique_locations, max_Salarys))

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
