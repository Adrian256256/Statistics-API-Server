# Le Stats Sportif 🏅

Le Stats Sportif is a Python-based multithreaded web server that serves statistical data insights based on a CSV dataset. It exposes various API endpoints to calculate and retrieve sports-related statistics in a scalable and thread-safe manner.

## 📦 Project Structure

```
.
├── __init__.py             # Initializes logging, job queue, and job counter
├── data_ingestor.py        # Parses CSV and loads Question objects
├── job_counter.py          # Thread-safe job ID counter
├── question.py             # Dataclass for a single CSV entry
├── routes.py               # API endpoints implementation
├── task_runner.py          # ThreadPool for job processing
├── results/                # Folder for storing job results
```

## ⚙️ How It Works

- A **ThreadPool** manages incoming jobs using Python threads.
- Jobs are placed in a **thread-safe queue** and processed asynchronously.
- Each job gets a **unique job ID**, and its status is tracked in a shared dictionary (`job_status`).
- Results are written to disk in the `results/` folder using the job ID as the filename.
- A **graceful shutdown** mechanism ensures no job is lost when shutting down the server.

## 📊 Supported Endpoints

| Endpoint                              | Method | Description |
|---------------------------------------|--------|-------------|
| `/api/get_results/<job_id>`           | GET    | Get the result of a processed job |
| `/api/states_mean`                    | POST   | Compute mean for all states |
| `/api/state_mean`                     | POST   | Compute mean for a specific state |
| `/api/best5`                          | POST   | Top 5 performing entries |
| `/api/worst5`                         | POST   | Worst 5 performing entries |
| `/api/global_mean`                    | POST   | Compute global mean |
| `/api/diff_from_mean`                 | POST   | Difference from global mean |
| `/api/state_diff_from_mean`           | POST   | Difference from mean for a specific state |
| `/api/mean_by_category`              | POST   | Mean grouped by category |
| `/api/state_mean_by_category`        | POST   | Mean by category for a specific state |
| `/api/graceful_shutdown`             | POST   | Gracefully shutdown the server |
| `/api/jobs`                          | GET    | List all job statuses |
| `/api/num_jobs`                      | GET    | Get count of pending jobs |


CSV path should be passed or configured in the `DataIngestor` initialization.

## ✅ Design Highlights

- ✅ **Thread-safe job counter** without global locks
- ✅ **ThreadPool** with clean shutdown handling
- ✅ **Modular and documented** codebase
- ✅ Pylint score > 8
- ✅ Uses `RotatingFileHandler` for logging

## 📁 Results Directory

All job results are stored as files in the `results/` folder using the `job_id` as the filename.

