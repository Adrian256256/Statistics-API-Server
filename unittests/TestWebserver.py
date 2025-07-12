import unittest
from app.data_ingestor import DataIngestor
from app.task_runner import TaskRunner
from app.routes import Job

class TestWebserver(unittest.TestCase):
    def setUp(self):
        # instance of class DataIngestor with path "data_subset.csv"
        self.data_ingestor = DataIngestor("./unittests/data_subset.csv")
        # instance of class TaskRunner with the data_ingestor
        self.task_runner = TaskRunner(None, None, None, self.data_ingestor, 1)

    def test_calculate_worst5(self):
        """ Test the worst5 function """

        expected_results = [
            {'South Dakota': 34.5, 'Montana': 35.85, 'North Dakota': 36.6, 'Utah': 36.7, 'Connecticut': 42.3},
            {'Nebraska': 36.800000000000004, 'Arkansas': 38.6, 'Wyoming': 39.15, 'Tennessee': 41.6, 'Iowa': 43.55},
            {'Ohio': 31.6, 'Oklahoma': 35.85, 'Maryland': 38.4, 'North Carolina': 42.7, 'Delaware': 51.0},
            {'Arkansas': 42.5, 'Louisiana': 47.2},
            {'Michigan': 17.45, 'Kentucky': 23.2, 'California': 29.7, 'Indiana': 35.4, 'Guam': 36.3},
            {'Puerto Rico': 26.6, 'Arkansas': 38.5, 'Virginia': 44.9, 'Kansas': 45.5, 'Missouri': 45.5},
            {'North Dakota': 15.5, 'Oklahoma': 15.7, 'Maryland': 16.9, 'Missouri': 20.0, 'Washington': 20.15},
            {'Connecticut': 24.9, 'Illinois': 26.3, 'Guam': 26.6, 'North Carolina': 28.1, 'West Virginia': 31.1},
            {'Rhode Island': 19.7, 'Pennsylvania': 20.1, 'Missouri': 23.5, 'Louisiana': 23.9, 'Tennessee': 24.2}
        ]
        index = 0
        # question in self.data_ingestor.questions_best_is_min and self.data_ingestor.questions_best_is_max
        for question in self.data_ingestor.questions_best_is_min + self.data_ingestor.questions_best_is_max:
            job = Job(job_id=1, data={"question": question}, type="worst5", status="running")
            result = self.task_runner.calculate_worst5(job)
            # check if the result is equal to the expected result
            self.assertEqual(result, expected_results[index])
            index += 1

    def test_calculate_best5(self):
        """ Test the best5 function """

        expected_results = [
            {'Wisconsin': 28.4, 'Vermont': 29.6, 'Michigan': 31.0, 'North Carolina': 31.0, 'Pennsylvania': 32.4},
            {'Minnesota': 15.6, 'Arizona': 21.55, 'North Carolina': 24.1, 'Rhode Island': 24.1, 'New York': 24.2},
            {'Montana': 14.7, 'North Dakota': 17.8, 'Maine': 18.0, 'New Hampshire': 18.85, 'Alabama': 20.6},
            {'Arkansas': 42.5, 'Louisiana': 47.2},
            {'New York': 17.2, 'Michigan': 17.45, 'Kentucky': 23.2, 'California': 29.7, 'Indiana': 35.4},
            {'Virginia': 44.9, 'Kansas': 45.5, 'Missouri': 45.5, 'Idaho': 51.46666666666667, 'Connecticut': 55.2},
            {'Maryland': 16.9, 'Missouri': 20.0, 'Washington': 20.15, 'Arizona': 20.2, 'Hawaii': 23.1},
            {'Maine': 35.1, 'Florida': 38.3, 'Indiana': 38.9, 'Tennessee': 39.0, 'Idaho': 43.7},
            {'Michigan': 33.1, 'New Hampshire': 35.3, 'Vermont': 37.9, 'National': 38.7, 'Washington': 40.3}
        ]
        index = 0
        # question in self.data_ingestor.questions_best_is_min and self.data_ingestor.questions_best_is_max
        for question in self.data_ingestor.questions_best_is_min + self.data_ingestor.questions_best_is_max:
            job = Job(job_id=1, data={"question": question}, type="best5", status="running")
            result = self.task_runner.calculate_best5(job)
            # check if the result is equal to the expected result
            self.assertEqual(result, expected_results[index])
            index += 1

    def test_calculate_state_mean(self):
        """ Test the state_mean function """

        expected_results = [
            {'Louisiana': 34.5},
            {'Louisiana': 0.0},
            {'Louisiana': 24.9},
            {'Louisiana': 47.2},
            {'Louisiana': 0.0},
            {'Louisiana': 0.0},
            {'Louisiana': 0.0},
            {'Louisiana': 0.0},
            {'Louisiana': 23.9}
        ]
        index = 0
        # question0in self.data_ingestor.questions_best_is_min and self.data_ingestor.questions_best_is_max
        for question in self.data_ingestor.questions_best_is_min + self.data_ingestor.questions_best_is_max:
            job = Job(job_id=1, data={"question": question, "state": "Louisiana"}, type="state_mean", status="running")
            result = self.task_runner.calculate_state_mean(job)
            # check if the result is equal to the expected result
            self.assertEqual(result, expected_results[index])
            index += 1

    def test_calculate_states_mean(self):
        """ Test the states_mean function """

        expected_results = [
            {'Wisconsin': 28.4, 'Vermont': 29.6, 'Michigan': 31.0, 'North Carolina': 31.0, 'Pennsylvania': 32.4, 
             'Alaska': 32.8, 'Oklahoma': 33.75, 'Florida': 33.95, 'Illinois': 34.45, 
             'Maryland': 34.46666666666667, 'Louisiana': 34.5, 'Puerto Rico': 34.5, 'South Dakota': 34.5, 
             'Montana': 35.85, 'North Dakota': 36.6, 'Utah': 36.7, 'Connecticut': 42.3},
            {'Minnesota': 15.6, 'Arizona': 21.55, 'North Carolina': 24.1, 'Rhode Island': 24.1, 
             'New York': 24.2, 'Utah': 24.9, 'Montana': 26.2, 'New Mexico': 29.35, 'District of Columbia': 29.4, 
             'Ohio': 29.4, 'New Hampshire': 29.5, 'Missouri': 31.0, 'North Dakota': 31.0, 'Maine': 31.8, 
             'Michigan': 32.4, 'Pennsylvania': 32.7, 'Indiana': 33.1, 'Mississippi': 34.43333333333333, 
             'Georgia': 35.0, 'California': 36.7, 'Nebraska': 36.800000000000004, 'Arkansas': 38.6, 
             'Wyoming': 39.15, 'Tennessee': 41.6, 'Iowa': 43.55},
            {'Montana': 14.7, 'North Dakota': 17.8, 'Maine': 18.0, 'New Hampshire': 18.85, 'Alabama': 20.6, 
             'Kentucky': 22.9, 'Michigan': 23.0, 'Nebraska': 23.0, 'Iowa': 23.03333333333333, 'Wisconsin': 24.0, 
             'Oregon': 24.1, 'Missouri': 24.3, 'Louisiana': 24.9, 'Utah': 25.0, 'Arizona': 25.6, 
             'District of Columbia': 25.6, 'South Dakota': 25.6, 'Virgin Islands': 25.6, 'Massachusetts': 26.5, 
             'New York': 26.5, 'Georgia': 27.1, 'South Carolina': 28.3, 'Kansas': 28.7, 'Arkansas': 29.549999999999997, 
             'Ohio': 31.6, 'Oklahoma': 35.85, 'Maryland': 38.4, 'North Carolina': 42.7, 'Delaware': 51.0},
            {'Arkansas': 42.5, 'Louisiana': 47.2},
            {'New York': 17.2, 'Michigan': 17.45, 'Kentucky': 23.2, 'California': 29.7, 'Indiana': 35.4, 'Guam': 36.3},
            {'Puerto Rico': 26.6, 'Arkansas': 38.5, 'Virginia': 44.9, 'Kansas': 45.5, 'Missouri': 45.5, 'Idaho': 51.46666666666667, 'Connecticut': 55.2},
            {'North Dakota': 15.5, 'Oklahoma': 15.7, 'Maryland': 16.9, 'Missouri': 20.0, 'Washington': 20.15, 'Arizona': 20.2, 'Hawaii': 23.1},
            {'Connecticut': 24.9, 'Illinois': 26.3, 'Guam': 26.6, 'North Carolina': 28.1, 'West Virginia': 31.1, 'Wisconsin': 31.1, 'Kentucky': 31.7, 'National': 32.9, 'Arizona': 33.8, 'Maine': 35.1, 'Florida': 38.3, 'Indiana': 38.9, 'Tennessee': 39.0, 'Idaho': 43.7},
            {'Rhode Island': 19.7, 'Pennsylvania': 20.1, 'Missouri': 23.5, 'Louisiana': 23.9, 'Tennessee': 24.2, 'North Dakota': 24.7, 'Alaska': 26.6, 'South Dakota': 28.700000000000003, 'Connecticut': 29.3, 'Oregon': 30.9, 'Massachusetts': 31.4, 'Michigan': 33.1, 'New Hampshire': 35.3, 'Vermont': 37.9, 'National': 38.7, 'Washington': 40.3},
        ]
        index = 0
        # question in self.data_ingestor.questions_best_is_min and self.data_ingestor.questions_best_is_max
        for question in self.data_ingestor.questions_best_is_min + self.data_ingestor.questions_best_is_max:
            job = Job(job_id=1, data={"question": question}, type="states_mean", status="running")
            result = self.task_runner.calculate_states_mean(job)
            # check if the result is equal to the expected result
            self.assertEqual(result, expected_results[index])
            index += 1

    def test_calculate_global_mean(self):
        """ Test the global_mean function """

        expected_results = [
            {'global_mean': 33.9076923076923},
            {'global_mean': 32.23783783783785},
            {'global_mean': 25.91351351351351},
            {'global_mean': 44.85},
            {'global_mean': 25.24285714285714},
            {'global_mean': 45.62222222222223},
            {'global_mean': 18.9625},
            {'global_mean': 32.96428571428572},
            {'global_mean': 29.0578947368421}
        ]
        index = 0
        # question in self.data_ingestor.questions_best_is_min and self.data_ingestor.questions_best_is_max
        for question in self.data_ingestor.questions_best_is_min + self.data_ingestor.questions_best_is_max:
            job = Job(job_id=1, data={"question": question}, type="global_mean", status="running")
            result = self.task_runner.calculate_global_mean(job)
            # check if the result is equal to the expected result
            self.assertEqual(result, expected_results[index])
            index += 1

    def test_calculate_diff_from_mean(self):
        """ Test the diff_from_mean function """

        expected_results = [
            {'Wisconsin': 5.507692307692302, 'Vermont': 4.3076923076922995, 'Michigan': 2.907692307692301,
             'North Carolina': 2.907692307692301, 'Pennsylvania': 1.5076923076923023, 
             'Alaska': 1.1076923076923038, 'Oklahoma': 0.15769230769230091, 'Florida': -0.04230769230770193, 
             'Illinois': -0.5423076923077019, 'Maryland': -0.5589743589743676, 'Louisiana': -0.5923076923076991, 
             'Puerto Rico': -0.5923076923076991, 'South Dakota': -0.5923076923076991, 
             'Montana': -1.9423076923077005, 'North Dakota': -2.6923076923077005, 'Utah': -2.792307692307702, 
             'Connecticut': -8.392307692307696},
            {'Minnesota': 16.63783783783785, 'Arizona': 10.68783783783785, 'North Carolina': 8.13783783783785, 
             'Rhode Island': 8.13783783783785, 'New York': 8.037837837837852, 'Utah': 7.337837837837853, 
             'Montana': 6.037837837837852, 'New Mexico': 2.88783783783785, 'District of Columbia': 2.837837837837853, 
             'Ohio': 2.837837837837853, 'New Hampshire': 2.7378378378378514, 'Missouri': 1.2378378378378514, 
             'North Dakota': 1.2378378378378514, 'Maine': 0.4378378378378507, 'Michigan': -0.16216216216214718, 
             'Pennsylvania': -0.46216216216215145, 'Indiana': -0.86216216216215, 'Mississippi': -2.1954954954954786, 
             'Georgia': -2.7621621621621486, 'California': -4.4621621621621514, 'Nebraska': -4.562162162162153, 
             'Arkansas': -6.36216216216215, 'Wyoming': -6.912162162162147, 'Tennessee': -9.36216216216215, 
             'Iowa': -11.312162162162146},
            {'Montana': 11.213513513513512, 'North Dakota': 8.11351351351351, 'Maine': 7.913513513513511, 
             'New Hampshire': 7.063513513513509, 'Alabama': 5.313513513513509, 'Kentucky': 3.0135135135135123, 
             'Michigan': 2.913513513513511, 'Nebraska': 2.913513513513511, 'Iowa': 2.8801801801801794, 
             'Wisconsin': 1.9135135135135108, 'Oregon': 1.8135135135135094, 'Missouri': 1.6135135135135101, 
             'Louisiana': 1.0135135135135123, 'Utah': 0.9135135135135108, 'Arizona': 0.3135135135135094, 
             'District of Columbia': 0.3135135135135094, 'South Dakota': 0.3135135135135094, 
             'Virgin Islands': 0.3135135135135094, 'Massachusetts': -0.5864864864864892, 
             'New York': -0.5864864864864892, 'Georgia': -1.1864864864864906, 'South Carolina': -2.38648648648649, 
             'Kansas': -2.7864864864864884, 'Arkansas': -3.6364864864864863, 'Ohio': -5.686486486486491, 
             'Oklahoma': -9.93648648648649, 'Maryland': -12.486486486486488, 'North Carolina': -16.786486486486492, 
             'Delaware': -25.08648648648649}
        ]
        index = 0
        # question in self.data_ingestor.questions_best_is_min and self.data_ingestor.questions_best_is_max
        for question in self.data_ingestor.questions_best_is_min + self.data_ingestor.questions_best_is_max:
            if index == 3:
                break
            job = Job(job_id=1, data={"question": question}, type="diff_from_mean", status="running")
            result = self.task_runner.calculate_diff_from_mean(job)
            # check if the result is equal to the expected result
            self.assertEqual(result, expected_results[index])
            index += 1

    def test_calculate_state_diff_from_mean(self):
        """ Test the state_diff_from_mean function """

        expected_results = [
            {'Louisiana': -0.5923076923076991},
            {'Louisiana': 32.23783783783785},
            {'Louisiana': 1.0135135135135123},
            {'Louisiana': -2.3500000000000014},
            {'Louisiana': 25.24285714285714},
            {'Louisiana': 45.62222222222223},
            {'Louisiana': 18.9625},
            {'Louisiana': 32.96428571428572},
            {'Louisiana': 5.157894736842103}
        ]
        index = 0
        # question in self.data_ingestor.questions_best_is_min and self.data_ingestor.questions_best_is_max
        for question in self.data_ingestor.questions_best_is_min + self.data_ingestor.questions_best_is_max:
            job = Job(job_id=1, data={"question": question, "state": "Louisiana"}, type="state_diff_from_mean", status="running")
            result = self.task_runner.calculate_state_diff_from_mean(job)
            # check if the result is equal to the expected result
            self.assertEqual(result, expected_results[index])
            index += 1

    def test_calculate_mean_by_category(self):
        """ Test the mean_by_category function """

        expected_results = [
            {"('Alaska', 'Income', '$35,000 - $49,999')": 33.1, "('Alaska', 'Income', '$15,000 - $24,999')": 32.5, 
             "('Connecticut', 'Race/Ethnicity', '2 or more races')": 42.3, "('Florida', 'Gender', 'Female')": 32.5, 
             "('Florida', 'Race/Ethnicity', 'Non-Hispanic Black')": 35.4, 
             "('Illinois', 'Education', 'High school graduate')": 32.2, 
             "('Illinois', 'Race/Ethnicity', 'Hispanic')": 36.7, 
             "('Louisiana', 'Race/Ethnicity', 'Hawaiian/Pacific Islander')": 34.5, 
             "('Maryland', 'Education', 'Some college or technical school')": 35.3, 
             "('Maryland', 'Race/Ethnicity', '2 or more races')": 27.1, 
             "('Maryland', 'Age (years)', '65 or older')": 41.0, "('Michigan', 'Race/Ethnicity', 'Non-Hispanic Black')": 31.0, 
             "('Montana', 'Race/Ethnicity', 'Non-Hispanic White')": 37.2, "('Montana', 'Age (years)', '35 - 44')": 34.5,
             "('North Carolina', 'Income', '$25,000 - $34,999')": 31.0, "('North Dakota', 'Total', 'Total')": 36.6, 
             "('Oklahoma', 'Race/Ethnicity', 'Non-Hispanic White')": 35.1, "('Oklahoma', 'Age (years)', '45 - 54')": 32.4, 
             "('Pennsylvania', 'Race/Ethnicity', 'Hispanic')": 32.4, 
             "('Puerto Rico', 'Race/Ethnicity', 'American Indian/Alaska Native')": 34.5, 
             "('South Dakota', 'Income', '$25,000 - $34,999')": 34.5, "('Utah', 'Race/Ethnicity', 'Hispanic')": 38.9, 
             "('Utah', 'Race/Ethnicity', 'Other')": 34.5, "('Vermont', 'Race/Ethnicity', 'Other')": 29.6, "('Wisconsin', 'Age (years)', '35 - 44')": 30.3, 
             "('Wisconsin', 'Age (years)', '18 - 24')": 26.5},
        ]
        index = 0
        # question in self.data_ingestor.questions_best_is_min and self.data_ingestor.questions_best_is_max
        for question in self.data_ingestor.questions_best_is_min + self.data_ingestor.questions_best_is_max:
            if index == 1:
                break
            job = Job(job_id=1, data={"question": question}, type="mean_by_category", status="running")
            result = self.task_runner.calculate_mean_by_category(job)
            # check if the result is equal to the expected result
            self.assertEqual(result, expected_results[index])
            index += 1
    
    def test_calculate_state_mean_by_category(self):
        """ Test the state_mean_by_category function """

        expected_results = [
            {'Utah': {"('Race/Ethnicity', 'Hispanic')": 38.9, "('Race/Ethnicity', 'Other')": 34.5}},
            {'Utah': {"('Gender', 'Male')": 24.9}}
        ]
        index = 0
        # question in self.data_ingestor.questions_best_is_min and self.data_ingestor.questions_best_is_max
        for question in self.data_ingestor.questions_best_is_min + self.data_ingestor.questions_best_is_max:
            if index == 2:
                break
            job = Job(job_id=1, data={"question": question, "state": "Utah"}, type="state_mean_by_category", status="running")
            result = self.task_runner.calculate_state_mean_by_category(job)
            # check if the result is equal to the expected result
            self.assertEqual(result, expected_results[index])
            index += 1