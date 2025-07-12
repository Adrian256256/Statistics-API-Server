"""
This module defines the routes for the webserver.
"""

import json
from dataclasses import dataclass
from app import webserver
from flask import request, jsonify

@dataclass
class Job:
    """ Dataclass for a job in the queue. """
    job_id: int
    # save the json data from the request
    data: dict
    type: str
    status: str

# Example endpoint definition
@webserver.route('/api/post_endpoint', methods=['POST'])
def post_endpoint():
    if request.method == 'POST':
        # Assuming the request contains JSON data
        data = request.json
        webserver.logger.info("Entering /api/post_endpoint with: %s", data)

        # Process the received data
        # For demonstration purposes, just echoing back the received data
        response = {"message": "Received data successfully", "data": data}

        # Sending back a JSON response
        webserver.logger.info("Exiting /api/post_endpoint with: %s", response)
        return jsonify(response)
    else:
        # Method Not Allowed
        return jsonify({"error": "Method not allowed"}), 405

@webserver.route('/api/get_results/<job_id>', methods=['GET'])
def get_response(job_id):
    # log the request
    webserver.logger.info("Entering /api/get_results with: %s", job_id)
    # Check if job_id is valid
    num_job = webserver.job_counter.get_value()
    if int(job_id) < 1 or int(job_id) > int(num_job):
        # log the error
        webserver.logger.error("[ERROR] Invalid job_id: %s,"
        "smaller than 1 or greater than %s", job_id, webserver.job_counter)
        return jsonify({"status": "error", "reason": "Invalid job_id"})

    # check if job_id is done in the job_status map
    if webserver.job_status[int(job_id)] == "done":
        with open(f"results/{job_id}", 'r', encoding='utf-8') as file:
            data = json.load(file)
            # log the exit
            webserver.logger.info("Exiting /api/get_results with data for job_id %s",
                                   job_id)
            return jsonify({"status": "done", "data": data})
    # log the exit
    webserver.logger.info("Exiting /api/get_results with status %s for job_id %s",
                          "running" , job_id)
    # If not, return running
    return jsonify({"status": "running"})

def check_server_status():
    """ Function to check if the server is running """
    if webserver.shutdown:
        # log the error
        webserver.logger.error("[ERROR] Server is shutting down")
        return True
    return False

def put_job_in_queue(type, data):
    """ Function that puts a job in the queue and returns the job_id """
    if check_server_status():
        return jsonify({"status": "error", "reason": "shutting down"})
    # log the request
    webserver.logger.info("Entering /api/%s with: %s", type, data)
    # Increment job_id counter in a thread-safe manner and get the new value
    job_id = webserver.job_counter.increment_and_get()
    # Get request data
    data = request.json

    # Register job. Don't wait for task to finish
    job = Job(job_id=job_id, data=data, type=type, status="running")
    # add job to job_status map
    webserver.job_status[int(job.job_id)] = "running"
    # add job to job_queue
    webserver.job_queue.put(job)
    # log exiting the function
    webserver.logger.info("Exiting /api/%s with: %s", type, job)
    # Return associated job_id
    return jsonify({"job_id": job.job_id})

@webserver.route('/api/states_mean', methods=['POST'])
def states_mean_request():
    """ Function to handle the /api/states_mean endpoint """
    return put_job_in_queue("states_mean", request.json)

@webserver.route('/api/state_mean', methods=['POST'])
def state_mean_request():
    """ Function to handle the /api/state_mean endpoint """
    return put_job_in_queue("state_mean", request.json)

@webserver.route('/api/best5', methods=['POST'])
def best5_request():
    """ Function to handle the /api/best5 endpoint """
    return put_job_in_queue("best5", request.json)

@webserver.route('/api/worst5', methods=['POST'])
def worst5_request():
    """ Function to handle the /api/worst5 endpoint """
    return put_job_in_queue("worst5", request.json)

@webserver.route('/api/global_mean', methods=['POST'])
def global_mean_request():
    """ Function to handle the /api/global_mean endpoint """
    return put_job_in_queue("global_mean", request.json)

@webserver.route('/api/diff_from_mean', methods=['POST'])
def diff_from_mean_request():
    """ Function to handle the /api/diff_from_mean endpoint """
    return put_job_in_queue("diff_from_mean", request.json)

@webserver.route('/api/state_diff_from_mean', methods=['POST'])
def state_diff_from_mean_request():
    """ Function to handle the /api/state_diff_from_mean endpoint """
    return put_job_in_queue("state_diff_from_mean", request.json)

@webserver.route('/api/mean_by_category', methods=['POST'])
def mean_by_category_request():
    """ Function to handle the /api/mean_by_category endpoint """
    return put_job_in_queue("mean_by_category", request.json)

@webserver.route('/api/state_mean_by_category', methods=['POST'])
def state_mean_by_category_request():
    """ Function to handle the /api/state_mean_by_category endpoint """
    return put_job_in_queue("state_mean_by_category", request.json)

@webserver.route('/api/graceful_shutdown', methods=['GET'])
def graceful_shutdown():
    """ Function to handle the /api/graceful_shutdown endpoint """
    # log the request
    webserver.logger.info("Entering /api/graceful_shutdown")
    webserver.shutdown = True
    # put in queue a job with shutdown type
    job = Job(job_id=0, data={}, type="shutdown", status="running")
    # add job to job_status map
    webserver.job_status[int(job.job_id)] = "running"
    # add job to job_queue
    webserver.job_queue.put(job)
    # check if there are jobs in the queue, apart from the shutdown job
    if webserver.job_queue.qsize() == 1 or webserver.job_queue.empty():
        # log the exit
        webserver.logger.info("Exiting /api/graceful_shutdown with status done")
        return jsonify({"status": "done"})
    else:
        # log the exit
        webserver.logger.info("Exiting /api/graceful_shutdown with status running")
        return jsonify({"status": "running"})

@webserver.route('/api/jobs', methods=['GET'])
def get_jobs():
    """ Function to handle the /api/jobs endpoint """
    # log the request
    webserver.logger.info("Entering /api/jobs")

    # get all jobs from job_status map
    jobs = []
    for job_id, status in webserver.job_status.items():
        jobs.append({job_id: status})

    # log the exit
    webserver.logger.info("Exiting /api/jobs with status done")
    return jsonify({"status": "done", "data": jobs})

@webserver.route('/api/num_jobs', methods=['GET'])
def num_jobs():
    """ Function to handle the /api/num_jobs endpoint """
    # log the request
    webserver.logger.info("Entering /api/num_jobs")

    # get the number of jobs in the queue, that are not done
    num_jobs = 0
    for job_id, status in webserver.job_status.items():
        if status != "done":
            num_jobs += 1

    # log the exit
    webserver.logger.info("Exiting /api/num_jobs with status done")
    return jsonify({"status": "done", "data": num_jobs})

# You can check localhost in your browser to see what this displays
@webserver.route('/')
@webserver.route('/index')
def index():
    routes = get_defined_routes()
    msg = f"Hello, World!\n Interact with the webserver using one of the defined routes:\n"

    # Display each route as a separate HTML <p> tag
    paragraphs = ""
    for route in routes:
        paragraphs += f"<p>{route}</p>"

    msg += paragraphs
    return msg

def get_defined_routes():
    routes = []
    for rule in webserver.url_map.iter_rules():
        methods = ', '.join(rule.methods)
        routes.append(f"Endpoint: \"{rule}\" Methods: \"{methods}\"")
    return routes
