from requests import Response, Request
import requests as _requests
import subprocess
import json

_BASE_URL = "https://api.tradologics.com/beta"
_TOKEN = None
_DEFAULT_TIMEOUT = 5
_IS_BACKTEST = False
_CURRENT_BAR_INFO = None
_BACKTEST_START = None
_BACKTEST_END = None


def set_token(token):
    global _TOKEN
    global _TOKEN
    _TOKEN = token


def _set_backtest_mode(start, end):
    global _IS_BACKTEST
    global _BACKTEST_START
    global _BACKTEST_END

    # cmd = [
    #     "./eroc",
    #     "db",
    # ]
    # cmd = " ".join(cmd)
    # subprocess.run(cmd, shell=True)
    _IS_BACKTEST = True
    _BACKTEST_START = start
    _BACKTEST_END = end


def _callErocMethod(method, endpoint, **kwargs):
    global _CURRENT_BAR_INFO
    global _BACKTEST_START
    global _BACKTEST_END

    headers = json.dumps({
        'start': _BACKTEST_START,
        'end': _BACKTEST_END,
        'datetime': _CURRENT_BAR_INFO.get('datetime'),
        'resolution': _CURRENT_BAR_INFO.get('resolution')
    })

    print(headers)
    cmd = [
        "./eroc",
        "api",
        f"-m '{method}'",
        f"-u '{endpoint}'",
        f"-h '{headers}'"
    ]

    if 'json' in kwargs:
        data = json.dumps(kwargs["json"])
        cmd.append(f"-d '{data}'")
    cmd = " ".join(cmd)
    res = subprocess.run(cmd, stdout=subprocess.PIPE, shell=True)

    parsed = json.loads(res.stdout.decode('utf-8'))
    status = parsed.get('status')
    del parsed['status']
    response = Response()

    state = {
        '_content': json.dumps(parsed).encode('utf-8'),
        'status_code': status,
        'encoding': 'utf-8'
    }
    response.__setstate__(state)

    return response


def _set_current_bar_info(info):
    global _CURRENT_BAR_INFO
    _CURRENT_BAR_INFO = info


def _process_request(method, url, **kwargs):
    global _IS_BACKTEST
    global _TIMESTAMP

    if "://" in url:
        return _requests.request(method, url, **kwargs)

    if "timeout" not in kwargs:
        kwargs["timeout"] = _DEFAULT_TIMEOUT

    if "headers" not in kwargs:
        if not _TOKEN:
            raise Exception("Please use `set_token(...)` first.")
        kwargs["headers"] = {
            "Authorization": "Bearer {token}".format(token=_TOKEN)
        }

    if _IS_BACKTEST:
        return _callErocMethod(method, url, **kwargs)
    else:
        url = f"{_BASE_URL}/{url.strip('/')}"
        return _requests.request(method, url, **kwargs)


def get(url, **kwargs):
    return _process_request('GET', url, **kwargs)


def post(url, **kwargs):
    return _process_request('POST', url, **kwargs)


def patch(url, **kwargs):
    return _process_request('PATCH', url, **kwargs)


def put(url, **kwargs):
    return _process_request('PUT', url, **kwargs)


def delete(url, **kwargs):
    return _process_request('DELETE', url, **kwargs)


def options(url, **kwargs):
    return _process_request('OPTIONS', url, **kwargs)


def head(url, **kwargs):
    return _process_request('HEAD', url, **kwargs)


class Session(_requests.Session):
    def _process_request(self, method, url, **kwargs):
        return _process_request(self, method, url, **kwargs)

    def get(self, url, **kwargs):
        return self._process_request('GET', url, **kwargs)

    def post(self, url, **kwargs):
        return self._process_request('POST', url, **kwargs)

    def patch(self, url, **kwargs):
        return self._process_request('PATCH', url, **kwargs)

    def put(self, url, **kwargs):
        return self._process_request('PUT', url, **kwargs)

    def delete(self, url, **kwargs):
        return self._process_request('DELETE', url, **kwargs)

    def options(self, url, **kwargs):
        return self._process_request('OPTIONS', url, **kwargs)

    def head(self, url, **kwargs):
        return self._process_request('HEAD', url, **kwargs)
