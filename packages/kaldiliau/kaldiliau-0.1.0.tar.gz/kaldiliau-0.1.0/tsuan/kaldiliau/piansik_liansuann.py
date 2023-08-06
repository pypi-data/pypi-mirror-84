
import json
import logging

from kaldiliau.kesi import post_liansuann, get_liansuann, kaSikan


logger = logging.getLogger(__name__)


def _piansik_lian(piansik, wavPath):
    tshamsoo = {'wav': wavPath}
    with post_liansuann('ling_kaldi_format', tshamsoo) as inue:
        tmpPath = json.loads(inue)
        logger.debug('ling %s', tmpPath)
    with post_liansuann(piansik, {'tmpTonganSootsai': tmpPath}) as inue:
        logger.debug('ji %s',  json.loads(inue))
    with get_liansuann('sam_sikan', tmpPath) as inue:
        sikan = json.loads(inue)
        logger.debug('sam \n%s', ''.join(sikan))
    return sikan


def piansik(imtong):
    ko = []
    for tsua in _piansik_lian('ji_lm', imtong):
        _mia, *tshun = tsua.split()
        khaisi = tshun[-3]
        tngte = tshun[-2]
        kiatsok = kaSikan(khaisi, tngte)
        ko.append({
            'hunsu': tshun[-1],
            'khaisi': khaisi,
            'kiatsok': kiatsok,
            'tngte': tngte,
        })
    return ko


def freesyllable(imtong):
    ko = []
    for tsua in _piansik_lian('ji_freesyllable', imtong):
        _mia, *tshun = tsua.split()
        khaisi = tshun[-3]
        tngte = tshun[-2]
        kiatsok = kaSikan(khaisi, tngte)
        ko.append({
            'imtsiat': tshun[-1],
            'khaisi': khaisi,
            'kiatsok': kiatsok,
            'tngte': tngte,
        })
    return ko
