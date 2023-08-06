import os

from utils.Validator import UrlValidator
from utils.exceptions import PipUrlException


class ProxySetter(object):
    SET_COMMANDS = {
        "linux": "export",
        "windows": "set"
    }

    def __init__(self, os):
        self.set_command = ProxySetter.SET_COMMANDS[os.lower()]

    def set(self, proxies):
        http = proxies["http"]
        https = proxies["https"]
        url_validator = UrlValidator()
        err = ""
        if not url_validator.valid(http) and http:
            err += f"The http url is invalid: {http}"

        if not url_validator.valid(https) and https:
            if err:
                err += "\n"
            err += f"The https url is invalid: {https}"

        if err:
            raise PipUrlException(err)

        if http:
            os.environ["http_proxy"] = http
        if https:
            os.environ["https_proxy"] = https
