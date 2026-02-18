import logging
from config.settings import config
from pathlib import Path

def setup_logger():
	Path("logs").mkdir(exist_ok=True)

	logging.basicConfig(
	  filename=config.log_file,
	  level=logging.DEBUG if config.debug else logging.INFO,
	  format="%(asctime)s [%(levelname)s] %(message)s",
	)
	return logging.getLogger("creed")

