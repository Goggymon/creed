from core.engine import CreedEngine
from config.settings import config
from utils.logger import setup_logger
from version import VERSION

def boot():
	logger = setup_logger()

	print (f"CREED v{VERSION} initialized")
	logger.info("Boot Seqeunce Started")

	creed = CreedEngine()
	creed.auto_load_modules()
	creed.run()

	logger.info("Boot Complete")

if __name__ == "__main__":
	boot()

