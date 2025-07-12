"""
This module implements ThreadPool and TaskRunner classes.
"""

import json
import os
from queue import Queue
from threading import Thread, Event
from app.data_ingestor import DataIngestor

class ThreadPool:
    """
    This class implements a thread pool that will process jobs from the queue.
    """

    def __init__(self, given_queue: Queue, given_job_status: dict,
                data_ingestor: DataIngestor):
        # You must implement a ThreadPool of TaskRunners
        # Your ThreadPool should check if an environment variable TP_NUM_OF_THREADS is defined
        # If the env var is defined, that is the number of threads to be used by the thread pool
        # Otherwise, you are to use what the hardware concurrency allows
        # You are free to write your implementation as you see fit, but
        # You must NOT:
        #   * create more threads than the hardware concurrency allows
        #   * recreate threads for each task
        # Note: the TP_NUM_OF_THREADS env var will be defined by the checker

        self.queue = given_queue
        self.shutdown_event = Event()
        self.job_status = given_job_status

        max_threads = os.cpu_count()
        if 'TP_NUM_OF_THREADS' in os.environ:
            max_threads = int(os.environ['TP_NUM_OF_THREADS'])
        self.threads = []

        # Create threads
        for i in range(max_threads):
            self.threads.append(TaskRunner(self.queue, self.job_status,
                                           self.shutdown_event, data_ingestor, i))

    def start(self):
        """
        Starts the threads in the thread pool.
        """

        # Start threads
        for thread in self.threads:
            thread.start()

    def stop(self):
        """
        Waits for all threads to finish.
        """

        self.shutdown_event.set()
        for thread in self.threads:
            thread.join()

class TaskRunner(Thread):
    """
    This class implements a thread that will process jobs from the queue.
    """

    def __init__(self, given_queue: Queue, given_job_status: dict,
                 shutdown_event: Event, data_ingestor: DataIngestor, thread_id: int):
        super().__init__()
        self.queue = given_queue
        self.shutdown_event = shutdown_event
        self.data_ingestor = data_ingestor
        self.thread_id = thread_id
        self.job_status = given_job_status

    def calculate_worst5(self, job):
        """
        Calculates the 5 worst-performing states for a given question.
        """

        question = job.data['question']
        sums = {}
        counts = {}
        for q in self.data_ingestor.questions:
            if q.question == question:
                if q.location not in sums:
                    sums[q.location] = 0.0
                    counts[q.location] = 0
                sums[q.location] += q.data_value
                counts[q.location] += 1
        for state in sums:
            if counts[state] > 0:
                sums[state] = sums[state] / counts[state]
        result = dict(sorted(sums.items(), key=lambda item: item[1], reverse=False))
        # search in best_is_min or best_is_max
        if not question in self.data_ingestor.questions_best_is_min:
            result = dict(list(result.items())[:5])
        else:
            result = dict(list(result.items())[-5:])
        return result

    def calculate_best5(self, job):
        """
        Calculates the 5 best-performing states for a given question."
        """

        question = job.data['question']
        sums = {}
        counts = {}
        for q in self.data_ingestor.questions:
            if q.question == question:
                if q.location not in sums:
                    sums[q.location] = 0.0
                    counts[q.location] = 0
                sums[q.location] += q.data_value
                counts[q.location] += 1
        for state in sums:
            if counts[state] > 0:
                sums[state] = sums[state] / counts[state]
        result = dict(sorted(sums.items(), key=lambda item: item[1]))
        # search in best_is_min or best_is_max
        if question in self.data_ingestor.questions_best_is_min:
            result = dict(list(result.items())[:5])
        else:
            result = dict(list(result.items())[-5:])
        return result

    def calculate_state_mean(self, job):
        """
        Calculates the mean for a given question and state.
        """

        question = job.data['question']
        state = job.data['state']
        float_result = 0.0
        count = 0
        # access questions from data_ingestor
        for q in self.data_ingestor.questions:
            if q.question == question and q.location == state:
                float_result += q.data_value
                count += 1
        if count > 0:
            float_result = float_result / count
        result = {state: float_result}
        return result

    def calculate_states_mean(self, job):
        """
        Calculates the mean for a given question and all states.
        """

        question = job.data['question']
        result = {}
        count = {}
        for q in self.data_ingestor.questions:
            if q.question == question:
                if q.location not in result:
                    result[q.location] = 0.0
                    count[q.location] = 0
                result[q.location] += q.data_value
                count[q.location] += 1
        for state in result:
            if count[state] > 0:
                result[state] = result[state] / count[state]
        result = dict(sorted(result.items(), key=lambda item: item[1]))
        return result

    def calculate_global_mean(self, job):
        """
        Calculates the global mean for a given question.
        """

        question = job.data['question']
        float_result = 0.0
        count = 0
        for q in self.data_ingestor.questions:
            if q.question == question:
                float_result += q.data_value
                count += 1
        if count > 0:
            float_result = float_result / count
        result = {"global_mean": float_result}
        return result

    def calculate_diff_from_mean(self, job):
        """
        Calculates the difference from the mean for a given question and all states.
        """

        question = job.data['question']
        result = {}
        count = {}
        for q in self.data_ingestor.questions:
            if q.question == question:
                if q.location not in result:
                    result[q.location] = 0.0
                    count[q.location] = 0
                result[q.location] += q.data_value
                count[q.location] += 1
        for state in result:
            if count[state] > 0:
                result[state] = result[state] / count[state]
        result = dict(sorted(result.items(), key=lambda item: item[1]))
        global_mean = 0.0
        global_count = 0
        for q in self.data_ingestor.questions:
            if q.question == question:
                global_mean += q.data_value
                global_count += 1
        if global_count > 0:
            global_mean = global_mean / global_count
        for state in result:
            result[state] = - result[state] + global_mean
        return result

    def calculate_state_diff_from_mean(self, job):
        """
        Calculates the difference from the mean for a given question and state.
        """

        question = job.data['question']
        state = job.data['state']
        float_result = 0.0
        count = 0
        # access questions from data_ingestor
        for q in self.data_ingestor.questions:
            if q.question == question and q.location == state:
                float_result += q.data_value
                count += 1
        if count > 0:
            float_result = float_result / count
        global_mean = 0.0
        global_count = 0
        for q in self.data_ingestor.questions:
            if q.question == question:
                global_mean += q.data_value
                global_count += 1
        if global_count > 0:
            global_mean = global_mean / global_count
        float_result = - float_result + global_mean
        result = {state: float_result}
        return result

    def calculate_state_mean_by_category(self, job):
        """
        Calculates the mean for a given question and state, stratified by category.
        """

        question = job.data['question']
        state = job.data['state']
        result = {}
        count = {}
        for q in self.data_ingestor.questions:
            if q.question == question and q.location == state:
                # concat StratificationCategory1,Stratification1
                concat = f"('{q.stratification_category1}', '{q.stratification1}')"
                if concat not in result:
                    result[concat] = 0.0
                    count[concat] = 0
                result[concat] += q.data_value
                count[concat] += 1
        for strat in result:
            if count[strat] > 0:
                result[strat] = result[strat] / count[strat]
        # sort alphabetically the result
        result = dict(sorted(result.items(), key=lambda item: item[0]))
        # put the state : result
        result = {state: result}
        return result

    def calculate_mean_by_category(self, job):
        """
        Calculates the mean for a given question, stratified by category.
        """

        question = job.data['question']
        result = {}
        count = {}
        for q in self.data_ingestor.questions:
            if q.question == question:
                # concat State, StratificationCategory1, Stratification1
                # for json entry
                # if one of the values is None or empty, skip
                if q.location == "" or q.stratification_category1 == "" or q.stratification1 == "":
                    continue
                location = q.location
                strat_category1 = q.stratification_category1
                strat1 = q.stratification1
                concat =f"('{location}', '{strat_category1}', '{strat1}')"
                if concat not in result:
                    result[concat] = 0.0
                    count[concat] = 0
                result[concat] += q.data_value
                count[concat] += 1
        for strat in result:
            if count[strat] > 0:
                result[strat] = result[strat] / count[strat]
        return result

    def find_job(self):
        """
        When there is a job in the queue, it is processed.
        """

        job = self.queue.get()
        # process the job, write in the result folder
        result = None

        if job.type == "worst5":
            result = self.calculate_worst5(job)

        if job.type == "best5":
            result = self.calculate_best5(job)

        if job.type == "state_mean":
            result = self.calculate_state_mean(job)

        if job.type == "states_mean":
            result = self.calculate_states_mean(job)

        if job.type == "global_mean":
            result = self.calculate_global_mean(job)

        if job.type == "diff_from_mean":
            result = self.calculate_diff_from_mean(job)

        if job.type == "state_diff_from_mean":
            result = self.calculate_state_diff_from_mean(job)

        if job.type == "state_mean_by_category":
            result = self.calculate_state_mean_by_category(job)

        if job.type == "mean_by_category":
            result = self.calculate_mean_by_category(job)

        if job.type == "shutdown":
            # shutdown the thread
            self.shutdown_event.set()
            # erase the job status
            del self.job_status[int(job.job_id)]
            return

        # write the result to disk (file with job_id name)
        with open(f"results/{job.job_id}", 'w', encoding='utf-8') as file:
            # clear the file, if it exists
            file.write('')
            file.write(json.dumps(result))
        # set the job status to done
        self.job_status[int(job.job_id)] = "done"


    def run(self):
        """
        Starts the thread and processes jobs from the queue.
        """

        while not self.shutdown_event.is_set():
            # Get job from queue
            self.find_job()
