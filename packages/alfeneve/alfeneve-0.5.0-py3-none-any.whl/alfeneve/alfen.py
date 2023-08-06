# Copyright (c) 2019 Nick Douma <n.douma@nekoconeko.nl>
#
# This file is part of alfeneve .
#
# Licensed under the terms of the MIT license, see the
# LICENSE file in the root of the project.

from urllib.parse import urljoin
import json
import requests
import iso8601


class Alfen:
    def __init__(self, url, credentials, session=None, proxy=None):
        self.session = requests.Session()
        self.base_url = url
        self.credentials = credentials

        if session:
            self.session.cookies["session"] = session
        else:
            self._login()

    def _build_url(self, endpoint):
        return urljoin(self.base_url, endpoint)

    def _post(self, endpoint, payload):
        resp = self.session.post(
            self._build_url(endpoint),
            json=payload,
            headers={"Content-Type": "application/lolo3-v1+json"})
        resp.raise_for_status()
        return resp.json()

    def _get(self, endpoint, params=None, decode_json=True, try_login=True):
        resp = self.session.get(
            self._build_url(endpoint),
            params=params)
        if resp.status_code == 403 and try_login:
            self._login()
            return self._get(endpoint, params, decode_json, try_login=False)
        resp.raise_for_status()
        resp = resp.text
        if decode_json:
            try:
                return json.loads(resp)
            except json.JSONDecodeError:
                # Try to work around misspelled NaN values
                resp = resp.replace(":nan,", ":NaN,")
                return json.loads(resp)
        return resp

    def _login(self):
        del self.session.cookies["session"]
        self._post(
            "/api/login",
            {"username": self.credentials[0],
             "password": self.credentials[1],
             "displayname": "python-alfeneve"})

    def categories(self):
        return [cat
                for cat in self._get("/api/categories")['categories']
                if cat]

    def properties(self, category=None, ids=None):
        if ids:
            params = {"ids": ids}
        else:
            params = {"cat": category}
        props = self._get("/api/prop", params=params)
        del props['count']
        del props['version']

        ap = [AlfenProperty.from_response(name, r)
              for name, r in props.items()]
        return ap

    def whitelist(self, index):
        return self._get("/api/whitelist",
                         params={"index": index})['whitelist']

    def transactions(self):
        offset = 0
        while True:
            resp = self._get("/api/transactions",
                             params={"offset": offset},
                             decode_json=False)
            for line in resp.splitlines():
                yield line

                try:
                    tid = line.split(" ", 2)[0]
                    ttype = tid.split("_", 2)[1][:-1]
                    tid = tid.split("_", 2)[0]
                except IndexError:
                    break

            offset = int(tid)

            if ttype == "txstop":
                break

    def logs(self, since=None):
        offset = 0
        stop = False
        while not stop:
            resp = self._get("/api/log",
                             params={"offset": offset},
                             decode_json=False)
            for line in reversed(resp.splitlines()):
                try:
                    lid = int(line.split("_", 1)[0])
                    rest = line.split("_", 1)[1]
                    timestamp = iso8601.parse_date(rest[:24])
                    rest = rest[25:]
                    level, filename, linenum, line = rest.split(":", 3)

                    if since and lid <= since:
                        stop = True
                        break
                    yield (lid, timestamp, level, filename, linenum, line)
                except IndexError:
                    stop = True
                    break

            if stop or lid == 0:
                break

            offset += 32


class AlfenProperty:
    def __init__(self, name, id, value, **kwargs):
        self.name = name
        self.id = id
        self.value = value
        self.properties = ["name", "value", "id", "cat"]
        self.all_properties = ["name", "value", "id", "cat"]
        if kwargs:
            for k, v in kwargs.items():
                self.all_properties.append(k)
                setattr(self, k, v)
            self.all_properties = set(self.all_properties)

    @classmethod
    def from_response(cls, name, body):
        return cls(name=name, **body)

    def to_dict(self, all=False):
        if all:
            return {k: getattr(self, k) for k in self.all_properties}
        return {k: getattr(self, k) for k in self.properties}

    def __str__(self):
        return "<{}({})>".format(
            self.__class__.__name__,
            ", ".join(["{}={}".format(k, getattr(self, k))
                       for k in self.properties]))

    __repr__ = __str__


ALFEN_PROPERTY_TYPES = {
    2: int,
    # 3: minutes?
    5: int,  # or bool?
    8: float,
    9: str,
    # 27: unixtime in milliseconds ?
}
