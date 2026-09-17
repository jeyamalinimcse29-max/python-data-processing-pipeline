import logging
import os


base_folder = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

log_folder = os.path.join(base_folder, "logs")

os.makedirs(log_folder, exist_ok=True)

log_file = os.path.join(log_folder, "pipeline.log")


logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


logger = logging.getLogger(__name__)