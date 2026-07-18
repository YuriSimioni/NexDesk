# Importing necessary libraries
import os
from pathlib import Path
from dotenv import load_dotenv


# Project root directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# Path to the .env file located at the project root
ENV_FILE = BASE_DIR / ".env"


# Load environment variables from .env file
load_dotenv(
    ENV_FILE
)


class EnvLoader:


    @staticmethod
    def get(key, default=None):
        """
        Get an environment variable value.

        Args:
            key (str): Environment variable name.
            default: Default value if variable does not exist.

        Returns:
            Environment variable value or default.
        """

        return os.getenv(
            key,
            default
        )


    @staticmethod
    def get_int(key, default=0):
        """
        Get an environment variable as an integer.

        Args:
            key (str): Environment variable name.
            default (int): Default value if variable does not exist.

        Returns:
            Integer value or default.
        """

        value = os.getenv(key)

        if value:
            return int(value)

        return default


    @staticmethod
    def get_bool(key, default=False):
        """
        Get an environment variable as a boolean.

        Accepted true values:
            - true
            - 1
            - yes

        Args:
            key (str): Environment variable name.
            default (bool): Default value if variable does not exist.

        Returns:
            Boolean value or default.
        """

        value = os.getenv(
            key,
            ""
        ).lower()


        if value in [
            "true",
            "1",
            "yes"
        ]:
            return True


        return default