###
#
#   Creates the _toc.yml file
#

import logging.config
import yaml
import os
from pathlib import Path

ROOT_DIR = os.getcwd()
BOOK_DIR = os.path.join(ROOT_DIR, "book", "content")
NUMBER_DIGITS = 4


def __create_toc(root_dir: str, current_toc: list) -> str:
    root_path = Path(root_dir)

    entries = [{"name": e.name, "file": e.is_file()} for e in root_path.iterdir()]
    entries.sort(key=lambda e: e["name"])

    logger.debug(f"path: {root_path}")
    logger.debug(f"entries: {entries}")

    for entry in entries:
        if entry["file"]:
            file = entry["name"].split(".")[0]

            current_toc.append(f"- file: {root_dir}/{file}")

        else:
            directory = entry["name"]

            current_toc = __create_toc(os.path.join(root_dir, directory), current_toc)

    logger.debug(f"current_toc: {current_toc}")
    return current_toc


if __name__ == "__main__":
    with open(os.path.join(ROOT_DIR, "logging.yaml"), "r") as config_file:
        config = yaml.safe_load(config_file.read())
        logging.config.dictConfig(config)

    logger = logging.getLogger(__name__)

    logger.info(f"Root dir: {ROOT_DIR}")
    logger.info(f"Book dir: {BOOK_DIR}")

    toc = __create_toc(BOOK_DIR, [])

    output = ""
    output += "format: jb-book\n\n"

    first = True

    for t in toc:
        file_name = t[len(BOOK_DIR) + 1:]

        if first:
            first = False

            output += f"root: {file_name}\n\n"
            output += "chapters:\n"
        else:
            output += f"- file: {t[len(BOOK_DIR) + 1:]}\n"

    logger.debug("Writing:")
    logger.debug(output)

    with open(os.path.join(ROOT_DIR, "book", "_toc.yml"), "w") as toc_file:
        toc_file.write(output)

    logger.info("Finished")
