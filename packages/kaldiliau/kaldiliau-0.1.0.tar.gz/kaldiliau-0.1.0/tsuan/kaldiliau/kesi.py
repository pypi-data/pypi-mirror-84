from contextlib import contextmanager
from http.client import HTTPConnection, HTTPException
from urllib.parse import urlencode


_post_headers = {
    "Content-type": "application/x-www-form-urlencoded",
    "Accept": "text/plain"
}


@contextmanager
def post_liansuann(tsuki, tshamsoo, port=5000):
    lian = HTTPConnection(tsuki, port=port)
    lian.request("POST", '/', urlencode(tshamsoo), _post_headers)
    hueing = lian.getresponse()
    if hueing.status != 200:
        raise HTTPException(
            '連線有問題：{} {}'.format(hueing.status, hueing.reason)
        )
    yield hueing.read()
    lian.close()


@contextmanager
def get_liansuann(tsuki, tmpTonganSootsai, port=5000):
    lian = HTTPConnection(tsuki, port=port)
    lian.request("GET", tmpTonganSootsai)
    hueing = lian.getresponse()
    if hueing.status != 200:
        raise HTTPException(
            '連線有問題：{} {}'.format(hueing.status, hueing.reason)
        )
    yield hueing.read()
    lian.close()


def kaSikan(khaisi, tngte):
    kiatsok_bibio = (
        int(khaisi[:-3]) * 100 + int(khaisi[-2:])
        + int(tngte[:-3]) * 100 + int(tngte[-2:])
    )
    return '{}.{}'.format(kiatsok_bibio // 100, kiatsok_bibio % 100)
