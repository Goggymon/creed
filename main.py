from core.engine import CreedEngine
from config.settings import config
from utils.logger import setup_logger

def boot():
	logger = setup_logger()

	print (f"==={config.assistant_name} v{config.version} ===")
	logger.info("Boot Seqeunce Started")

	creed = CreedEngine()
	creed.auto_load_modules()
	creed.run()

	logger.info("Boot Complete")

if __name__ == "__main__":
	boot()

