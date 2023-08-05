import param
import panel as pn
import httpx
import json
import eve
from .eve_model import EveModelBase
from .auth import EveAuthBase, AuthSelector
from . import settings


APPS = {}

class EveHttpClient(EveModelBase):
    pass

class EveHttpxClient(EveHttpClient):
    _app_settings = param.Dict(default=None, allow_None=True)
    _self_serve = param.Boolean(False)
    server_url = param.String(default="http://localhost:5000", regex=r"(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:'\".,<>?«»“”‘’]))")
    server_urls = param.List(default=[], class_=str)
    auth = param.ClassSelector(EveAuthBase, default=AuthSelector())
    _log = param.String()
    _messages = param.List(default=[])
    _busy = param.Boolean(False)

    def __init__(self, **params):
        super().__init__(**params)

    @classmethod
    def from_app_settings(cls, settings, urls=None):
        if urls is None:
            urls = settings.get("SERVERS", ["http://localhost:5000"])
        urls = [url.strip("/") + "/".join([settings.get("URL_PREFIX",""), settings.get("API_VERSION", "")]).replace("//","/").replace("///","/") for url in urls]
        instance = cls(server_url=urls[0], server_urls=urls, _app_settings=settings)
        return instance
    
    @property
    def app(self):
        if not self._self_serve:
            return None
        if self.name not in APPS and self._app_settings:
            APPS[self.name] = eve.Eve(self._app_settings)
        return APPS.get(self.name, None)

    def headers(self):
        headers = self.auth.get_headers()
        headers["Accept"] = "application/json"
        headers["Content-Type"] = "application/json"
        return headers
    
    def get(self, url, timeout=10, **params):
        with httpx.Client(app=self.app, base_url=self.server_url) as client:
            self._busy = True
            try:
                resp = client.get(url, params=params, headers=self.headers(), timeout=timeout)
                self._busy = False
                if resp.is_error:
                    self.log_error(resp.text)
                else:
                    self.clear_messages()
                    return resp.json()
            except Exception as e:
                self.log_error(e)
            self._busy = False
        return []

    def post(self, url, data="", json={}, timeout=10):
        with httpx.Client(app=self.app, base_url=self.server_url) as client:
            self._busy = True
            try:
                resp = client.post(url, data=data, json=json, headers=self.headers(), timeout=timeout)
                self._busy = False
                if resp.is_error:
                    self.log_error(resp.text)
                    return False
                else:
                    self.clear_messages()
                    return True
            except Exception as e:
                self.log_error(e)
            self._busy = False

    def put(self, url, data, timeout=10):
        with httpx.Client(app=self.app, base_url=self.server_url) as client:
            self._busy = True
            try:
                resp = client.put(url, data=data, headers=self.headers(), timeout=timeout)
                self._busy = False
                if resp.is_error:
                    self.log_error(resp.text)
                    return False
                else:
                    self.clear_messages()
                    return True
            except Exception as e:
                self.log_error(e)
        self._busy = False

    def patch(self, url, data, timeout=10):
        with httpx.Client(app=self.app, base_url=self.server_url) as client:
            self._busy = True
            try:
                resp = client.patch(url, data=data, headers=self.headers(), timeout=timeout)
                self._busy = False
                if resp.is_error:
                    self.log_error(resp.text)
                    return False
                else:
                    self.clear_messages()
                    return True
            except Exception as e:
                self.log_error(e)
            self._busy = False

    def delete(self, url, etag, timeout=10):
        with httpx.Client(app=self.app, base_url=self.server_url) as client:
            self._busy = True
            headers = self.headers()
            if etag:
                headers["If-Match"] = etag
            try:
                resp = client.post(url,headers=headers, timeout=timeout)
                self._busy = False
                if resp.is_error:
                    self.log_error(resp.text)
                    return False
                else:
                    self.clear_messages()
                    return True
            except Exception as e:
                self.log_error(e)
            self._busy = False

    def log_error(self, e):
        self._log = str(e)
        self._messages = [str(e)]

    def clear_messages(self):
        self._messages = []
    
    def set_token(self, token):
        self.auth.set_token(token)

    @param.depends("_messages")
    def messages(self):
        messages = [pn.pane.Alert(msg, alert_type="danger", width=settings.GUI_WIDTH-20) for msg in self._messages]
        return pn.Column(*messages, width=settings.GUI_WIDTH)

    def make_panel(self):
        settings = pn.Param(self.param, parameters=["_self_serve", "server_url","_log"],
                        width=500, height=150, show_name=False,
                        widgets={"_log": {'type': pn.widgets.TextAreaInput, 'disabled': True, "height":150},
                                "server_url": {'type': pn.widgets.AutocompleteInput, "options": self.server_urls },
                                }
                                )
        return pn.Column(self.auth.panel, settings)
    
    @param.depends("_busy")
    def busy_indicator(self):
        return pn.Param(self.param._busy, width=25,
                    widgets={"_busy": {"type": pn.indicators.LoadingSpinner,"color":"primary", "width":20, "height":20}})

DEFAULT_HTTP_CLIENT = EveHttpxClient

