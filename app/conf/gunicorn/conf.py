import multiprocessing
import os

from dotenv import load_dotenv

load_dotenv()

# The number of worker processes for handling requests
workers = multiprocessing.cpu_count() * 2 + 1

# Worker class
worker_class = "app.conf.gunicorn.worker.UvicornWorker"

# The socket to bind
bind = f"{os.getenv('SERVER_HOST')}:{os.getenv('SERVER_PORT')}"
