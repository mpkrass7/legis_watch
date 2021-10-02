from configparser import ConfigParser
import os
import wget

from logzero import logger
import pandas as pd


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
    except Exception as e:
        logger.info(e)
    return senate_path, house_path


def merge_datasets(senate_path, house_path):
    logger.info("Files Downloaded, merging....")
    senate = (
        pd.read_csv(senate_path)
        .drop(columns="comment")
        .rename(columns={"senator": "representative"})
        .assign(legislative_branch="Senate")
    )
    house = (
        pd.read_csv(house_path)
        .drop(columns=["cap_gains_over_200_usd", "disclosure_year", "district"])
        .assign(legislative_branch="House of Representatives", asset_type="Stock")
    )
    full_dataset = pd.concat((senate, house))
    full_dataset.to_csv("data/all_transactions_complete.csv", index=False)


if __name__ == "__main__":
    senate, house = refresh_datasets()
    merge_datasets(senate, house)
