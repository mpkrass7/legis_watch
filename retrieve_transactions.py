from configparser import ConfigParser
import os
import wget

from logzero import logger


def refresh_datasets():
    config = ConfigParser()
    config.read("conf.ini")
    senate_url = config["senate"]["data_url"]
    senate_path = config["senate"]["save_path"]
    house_data_url = config["house"]["data_url"]
    house_path = config["house"]["save_path"]
    try:
        logger.info("Downloading Senate Data...")
        senate_file = wget.download(senate_url, out=str("data"), bar=None)
        os.rename(senate_file, senate_path)

        logger.info("Downloading House Data...")
        house_file = wget.download(house_data_url, out=str("data"), bar=None)
        os.rename(house_file, house_path)
        logger.info("Success!")
    except Exception as e:
        logger.info(e)


if __name__ == "__main__":
    refresh_datasets()
