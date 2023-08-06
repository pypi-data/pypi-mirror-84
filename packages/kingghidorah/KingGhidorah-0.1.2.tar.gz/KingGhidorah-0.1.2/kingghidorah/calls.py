import json
import logging
import os

import requests
from requests.auth import HTTPBasicAuth
import attr

import kingghidorah as kd
from kingghidorah.sanitizers import _url_sanitizer
from kingghidorah.exceptions import _UpstreamError, _InvalidURL
from kingghidorah.utils import default_config


def _response(data):
  try:
    if "<h1>Not Found</h1>" in data.decode("utf-8"):
      raise _InvalidURL
  except AttributeError:
    # raise _Error("You forgot to add .content")
    raise Exception("You forgot to add .content")

  try:
    return json.loads(data)
  except:
    if data == b"":
      pass
    else:
      raise Exception(kd.config["domain"], data.decode("utf-8"))


class _APIRequest:

  def __init__(self):

    # If config is not defined, get the default.
    if kd.config is None:
      with open(
        os.path.abspath(
          os.path.join(
            (os.path.dirname(__file__)),
            "../config.json")
          )
      ) as f:
        kd.config = json.load(f)

    # self.config = kd.config
    self.domain = kd.config["domain"]
    self.username = kd.config["username"]
    self.password = kd.config["password"]
    self.proxy = kd.config["proxy"]

    self.auth = requests.auth.HTTPBasicAuth(kd.config["username"], kd.config["password"])
    self.client = requests.session()

  def get(self, url: str):
    url = _url_sanitizer(url)
    if self.proxy is False:
      data = _response(self.client.get(self.domain + url, auth=self.auth).content)
    else:
      data = _response(
        self.client.get(
          self.domain + url,
          auth=self.auth,
          proxies={
            "http": self.proxy,
            "https": self.proxy,
          },
        ).content)

    if self.proxy is False:
      try:
        # Handle Multiple Pages
        while data["next"]:
          next_page = _response(self.client.get(data["next"], auth=self.auth).content)
          data["results"] += next_page["results"]
          data["next"] = next_page["next"]

      except KeyError:
        pass
    else:
      try:
        # Handle Multiple Pages
        while data["next"]:
          next_page = _response(
            self.client.get(
              data["next"],
              auth=self.auth,
              proxies={
                "http": self.proxy,
                "https": self.proxy,
              },
            ).content)
          data["results"] += next_page["results"]
          data["next"] = next_page["next"]

      except KeyError:
        pass

    return data

  def patch(self, url, data=None, json=None):
    """"""
    url = _url_sanitizer(url)
    if self.proxy is False:
      data = self.client.patch(
        url=self.domain + url,
        data=data,
        json=json,
        auth=self.auth,
      )
    else:
      data = self.client.patch(
        url=self.domain + url,
        data=data,
        json=json,
        auth=self.auth,
        proxies={
          "http": self.proxy,
          "https": self.proxy,
        },
      )
    return _response(data.content)

  def post(self, url, data=None, json=None, files=None):
    """
    r = self.client.get(self.domain + "auth/me/", auth=self.auth)
    data = {}
    data["csrfmiddlewaretoken"] = self.client.cookies['csrftoken'] if 'csrftoken' in self.client.cookies else self.client.cookies['csrf']
    """
    url = _url_sanitizer(url)
    # self.client.headers.update({'Content-Type': 'multipart/form-data;'})

    if self.proxy is False:
      data = _response(
        self.client.post(
          self.domain + url, data=data, json=json, files=files, auth=self.auth).content)
    else:
      data = _response(
        self.client.post(
          self.domain + url,
          data=data,
          json=json,
          files=files,
          auth=self.auth,
          proxies={
            "http": self.proxy,
            "https": self.proxy,
          },
        ).content)
    return data

  def delete(self, url):
    """"""
    url = _url_sanitizer(url)
    if self.proxy is False:
      data = _response(self.client.delete(self.domain + url, auth=self.auth).content)
    else:
      data = _response(
        self.client.delete(
          self.domain + url,
          auth=self.auth,
          proxies={
            "http": self.proxy,
            "https": self.proxy,
          },
        ).content)

    return data

  def options(self, url):
    """"""
    url = _url_sanitizer(url)
    return _response(self.client.options(self.domain + url, auth=self.auth).content)
