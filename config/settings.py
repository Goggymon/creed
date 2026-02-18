import os
from dataclasses import dataclass
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()


@dataclass
class CreedConfig:
    assistant_name: str = "Creed"
    version: str = "0.1-alpha"
    debug: bool = True
    log_file: str = "logs/creed.log"


config = CreedConfig()

