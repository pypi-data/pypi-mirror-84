"""periodical_requests_recorder - """

__version__ = "0.1.0"
__author__ = "fx-kirin <fx.kirin@gmail.com>"
__all__ = []


import datetime
import logging
import os
from pathlib import Path

import kanilog
import stdlogging
import yaml
from kanirequests import KaniRequests

import crython


class RequestsRecorder:
    def __init__(self, headers=None):
        self.log = logging.getLogger(self.__class__.__name__)
        if headers is None:
            self.headers = {
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:82.0) Gecko/20100101"
                    " Firefox/82.0"
                ),
                "Accept-Language": "ja,en-US;q=0.7,en;q=0.3",
                "Connection": "keep-alive",
                "Accept": (
                    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
                ),
                "Accept-Encoding": "gzip, deflate, br",
                "Cache-Control": "max-age=0",
            }
        else:
            self.headers = headers
        self.session = KaniRequests(headers=self.headers)

    def load_yaml(self, yaml_path):
        now = datetime.datetime.now()
        if isinstance(yaml_path, str):
            yaml_path = Path(yaml_path)

        assert isinstance(yaml_path, Path)

        cron_data = yaml.safe_load(yaml_path.read_text())

        for cron in cron_data:
            assert isinstance(cron, dict)
            for key in ["name", "url", "record_dir", "output_file_format", "cron_expr"]:
                assert key in cron

            def recorder(cron):
                self.record(cron)

            recorder.__name__ = cron["name"]
            crython.job(expr=cron["cron_expr"], cron=cron)(recorder)
            self.log.info(f"cron registered {cron=}")

    def record(self, cron):
        self.log.info(f"Recording {cron=}")
        result = self.session.get(cron["url"])
        if result.status_code == 200:
            now = datetime.datetime.now()
            output_file = cron["output_file_format"].format(**cron)
            output_file = now.strftime(output_file)
            output_file = Path(output_file)
            output_file.parent.mkdir(parents=True, exist_ok=True)
            output_file.write_bytes(result.content)
        else:
            self.log.error(f"Requests failed {cron=} status_code:{result.status_code}")

    def start(self):
        crython.start()
        crython.join()
