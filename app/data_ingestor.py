"""
This module defines the DataIngestor class, which is responsible for reading and processing
data from a CSV file. Each line of the CSV file is converted into a Question object.
The module also defines two lists:
- questions_best_is_min: Questions where lower values are better.
- questions_best_is_max: Questions where higher values are better.
"""

import csv
from app.question import Question

class DataIngestor:
    """
    This class is responsible for reading a CSV file.
    """

    def __init__(self, csv_path: str):
        # use Question dataclass to create the array of information of each line of the csv file
        self.questions = []
        # open with sopecified encoding
        with open(csv_path, encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for line in reader:
                location = line[4]
                year_start = int(line[1])
                year_end = int(line[2])
                question = line[8]
                data_value = float(line[11])
                # second and third last columns are the stratification category and stratification
                stratification_category1 = line[-4]
                stratification1 = line[-3]
                new_question = Question(location, year_start, year_end, question,
                                        data_value, stratification_category1, stratification1)
                self.questions.append(new_question)
        #sort the array by state in alphabetical order
        self.questions = sorted(self.questions, key=lambda x: x.location)

        self.questions_best_is_min = [
            'Percent of adults aged 18 years and older who have an overweight '
            'classification',
            'Percent of adults aged 18 years and older who have obesity',
            'Percent of adults who engage in no leisure-time physical activity',
            'Percent of adults who report consuming fruit less than one time daily',
            'Percent of adults who report consuming vegetables less than one time '
            'daily'
        ]

        self.questions_best_is_max = [
            (
                'Percent of adults who achieve at least 150 minutes a week of '
                'moderate-intensity aerobic physical activity or 75 minutes a week of '
                'vigorous-intensity aerobic activity (or an equivalent combination)'
            ),
            (
                'Percent of adults who achieve at least 150 minutes a week of '
                'moderate-intensity aerobic physical activity or 75 minutes a week of '
                'vigorous-intensity aerobic physical activity and engage in '
                'muscle-strengthening activities on 2 or more days a week'
            ),
            (
                'Percent of adults who achieve at least 300 minutes a week of '
                'moderate-intensity aerobic physical activity or 150 minutes a week of '
                'vigorous-intensity aerobic activity (or an equivalent combination)'
            ),
            'Percent of adults who engage in muscle-strengthening activities on 2 or '
            'more days a week',
        ]
