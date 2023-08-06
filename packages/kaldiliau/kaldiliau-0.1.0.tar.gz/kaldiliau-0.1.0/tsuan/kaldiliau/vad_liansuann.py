import json
import logging

from kaldiliau.kesi import get_liansuann, post_liansuann, kaSikan


logger = logging.getLogger(__name__)


def vad(wavPath, vad_hard_max_length=15):
    tshamsoo = {
        'wav': wavPath,
        'tsuliaugiap': 'guân',
    }
    with post_liansuann('ling_kaldi_format', tshamsoo) as inue:
        tmpPath = json.loads(inue)
        logger.debug('ling %s', tmpPath)
    it_tshamsoo = {
        'tmpTonganSootsai': tmpPath,
        'hard-max-length': vad_hard_max_length,
    }
    with post_liansuann('it_vad', it_tshamsoo) as inue:
        logger.debug('it %s', json.loads(inue))
    with get_liansuann('sam_segment', tmpPath) as inue:
        segment = json.loads(inue)
        logger.debug('sam \n%s', ''.join(segment))
    kiatko = []
    for tsua in segment:
        _kumia, _tong, 開始時間, 結束時間 = tsua.split()
        khaisi = float(開始時間)
        kiatsok = float(結束時間)
        kiatko.append({
            'khaisi': khaisi,
            'kiatsok': kiatsok,
            'tngte': kiatsok - khaisi,
        })

    return kiatko


def vad_decoding(wavPath, vad_hard_max_length=15):
    ling_tshamsoo = {
        'wav': wavPath,
        'tsuliaugiap': 'guân',
    }
    with post_liansuann('ling_kaldi_format', ling_tshamsoo) as inue:
        tmpPath = json.loads(inue)
        logger.debug('ling %s', tmpPath)
    it_tshamsoo = {
        'tmpTonganSootsai': tmpPath,
        'hard-max-length': vad_hard_max_length,
    }
    with post_liansuann('it_vad', it_tshamsoo) as inue:
        logger.debug('it %s', json.loads(inue))
    with post_liansuann('ji_lm', {
        'tmpTonganSootsai': tmpPath
    }) as inue:
        logger.debug('ji %s',  json.loads(inue))
    with get_liansuann('sam_segment', tmpPath) as inue:
        segment = json.loads(inue)
        logger.debug('sam \n%s', ''.join(segment))
    with get_liansuann('sam_sikan', tmpPath) as inue:
        sikan = json.loads(inue)
        logger.debug('sam \n%s', ''.join(sikan))

    kiatko = {}
    for tsua in segment:
        kumia, _tong, 開始時間, 結束時間 = tsua.split()
        khaisi = float(開始時間)
        kiatsok = float(結束時間)
        kiatko[kumia] = {
            'khaisi': khaisi,
            'kiatsok': kiatsok,
            'tngte': kiatsok - khaisi,
            'su': []
        }

    for tsua in sikan:
        kumia, *tshun = tsua.split()
        khaisi = tshun[-3]
        tngte = tshun[-2]
        kiatsok = kaSikan(khaisi, tngte)
        kiatko[kumia]['su'].append({
            'hunsu': tshun[-1],
            'khaisi': khaisi,
            'kiatsok': kiatsok,
            'tngte': tngte,
        })
    return sorted(kiatko.values(), key=lambda ko: ko['khaisi'])
