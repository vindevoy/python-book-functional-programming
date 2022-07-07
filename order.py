###
#
#   This script creates the numbers in front of the directory and files 
#   in a +10-style like it was in Basic on a Commodore-64.  You typically had:
#       10 x = 1
#       20 print(x)
#       30 ....
#
#   If you wanted to put a command somewhere between 2 other existing lines,
#   you could number it somewhere in between and run the reorder method 
#   to make the numbers using this 10 numbering again
#
#   It is allowed to mix directories and files, as you could have:
#       1 Introduction (from a file)
#       2 Something content (from a directory)
#       2.1 First
#       2.2 Second
#

import logging.config
import yaml
import os
from pathlib import Path

ROOT_DIR = os.getcwd()
BOOK_DIR = os.path.join(ROOT_DIR, "book", "content")
NUMBER_DIGITS = 4


def __order_dir(root_dir: str) -> None:
    root_path = Path(root_dir)

    entries = [{"name": e.name, "dir": e.is_dir()} for e in root_path.iterdir()]
    entries.sort(key=lambda e: e["name"])

    logger.debug(f"path: {root_path}")
    logger.debug(f"entries: {entries}")

    entry_number = 0

    for entry in entries:
        entry_number += 10
        entry_name = entry["name"]
        idx = entry_name.find("_")

        if entry["dir"]:
            __order_dir(os.path.join(root_dir, entry_name))
            # Recursive call before we rename directories

        new_name = f"{str(entry_number).zfill(NUMBER_DIGITS)}_{entry_name[idx + 1:]}"
        new_name = new_name.replace("-", "_")

        __rename(root_dir=root_dir, original_entry=entry_name, new_entry=new_name)


def __rename(root_dir, original_entry, new_entry):
    if original_entry == new_entry:
        logger.debug(f"{original_entry} needs no renaming")
    else:
        logger.info(f"Renaming {original_entry} to {new_entry}")
        os.rename(os.path.join(root_dir, original_entry), os.path.join(root_dir, new_entry))


if __name__ == "__main__":
    with open(os.path.join(ROOT_DIR, "logging.yaml"), "r") as config_file:
        config = yaml.safe_load(config_file.read())
        logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)

    logger.info(f"Root dir: {ROOT_DIR}")
    logger.info(f"Book dir: {BOOK_DIR}")
    logger.debug(f"Number of digits for the counters: {NUMBER_DIGITS}")

    __order_dir(BOOK_DIR)

    logger.info("Finished")
