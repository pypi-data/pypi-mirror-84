import _thread
from typing import Union
from urllib.parse import urljoin

import dtale
import pandas as pd
import requests
from dtale import utils as _utils
from dtale import views as _views

from dtale_desktop.settings import settings

dtale.app.initialize_process_props(host=settings.HOST, port=settings.DTALE_PORT)

DTALE_HOST = dtale.app.ACTIVE_HOST

DTALE_PORT = dtale.app.ACTIVE_PORT

DTALE_URL = _utils.build_url(DTALE_PORT, DTALE_HOST)

app = dtale.app.build_app(DTALE_URL, host=DTALE_HOST, reaper_on=False)


def _start_server():
    app.run(host=DTALE_HOST, port=DTALE_PORT, threaded=True)


def run():
    _thread.start_new_thread(_start_server, ())


def _start_server_if_needed():
    if not _views.is_up(DTALE_URL):
        run()


def get_instance(data_id: Union[str, int]) -> Union[dtale.app.DtaleData, None]:
    return dtale.app.get_instance(data_id)


def launch_instance(
    data: pd.DataFrame, data_id: Union[str, int]
) -> dtale.app.DtaleData:
    instance = dtale.app.startup(
        DTALE_URL, data=data, data_id=data_id, ignore_duplicate=True
    )
    _start_server_if_needed()
    return instance


if settings.DTALE_EXTERNAL_HOST_NAME is not None:
    _BASE_URL = f"http://{settings.DTALE_EXTERNAL_HOST_NAME}"
else:
    _BASE_URL = f"http://{settings.HOST_NAME}:{settings.DTALE_PORT}"


def get_main_url(data_id: Union[str, int]) -> str:
    return urljoin(_BASE_URL, f"/dtale/main/{data_id}")


def get_charts_url(data_id: Union[str, int]) -> str:
    return urljoin(_BASE_URL, f"/charts/{data_id}")


def get_describe_url(data_id: Union[str, int]) -> str:
    return urljoin(_BASE_URL, f"/dtale/popup/describe/{data_id}")


def get_correlations_url(data_id: Union[str, int]) -> str:
    return urljoin(_BASE_URL, f"/dtale/popup/correlations/{data_id}")


def kill_instance(data_id: Union[str, int]) -> None:
    requests.get(urljoin(_BASE_URL, f"/dtale/cleanup/{data_id}"))
