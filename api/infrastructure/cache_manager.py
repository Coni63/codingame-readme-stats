from __future__ import annotations

import datetime
import pickle
import glob
from pathlib import Path
from typing import Generator

from domain import IDataDto
from config import constants


def load_data(codingamer: str, expiration_seconds=86400) -> IDataDto | None:
    outfile = constants.CACHE_PATH.format(codingamer=codingamer)
    seconds = _get_seconds_since_last_modified(outfile)  # if the file does not exist, the time is 1e8

    if seconds > expiration_seconds:
        return None

    with open(outfile, "rb") as f:
        return pickle.load(f)


def save_data(codingamer: str, user_datas: IDataDto):
    with open(constants.CACHE_PATH.format(codingamer=codingamer), "wb") as f:
        pickle.dump(user_datas, f)


def list_cache() -> Generator[str]:
    for file in glob.iglob(constants.CACHE_PATH.format(codingamer="*")):
        p = Path(file)
        yield p.stem


def _get_seconds_since_last_modified(path: str) -> int:
    f = Path(path)

    if not f.is_file():
        return 1e8

    # get modification time
    last_modified_timestamp = f.stat().st_mtime  # float with unix timestamp including ms & us

    # get current time
    presentDate = datetime.datetime.now()
    current_timestamp = datetime.datetime.timestamp(presentDate)

    return round(current_timestamp - last_modified_timestamp)

