import json
import logging

from kaldiliau.kesi import post_liansuann, get_liansuann, kaSikan
from tuitse._kiamtsa import kiamtsa
from tuitse.boolean import tuitse_boolean


from 臺灣言語工具.解析整理.拆文分析器 import 拆文分析器


logger = logging.getLogger(__name__)


def tuitse(imtong, taibun_tsua):
    kaldi結果 = pooLomaji(imtong, ' '.join(taibun_tsua))
    ko = []
    tsitma = 0
    for tsua in taibun_tsua:
        liong = len(tsua.split())
        su = kaldi結果[tsitma:tsitma + liong]
        kukhaisi = su[0]['khaisi']
        kukiatsok = su[-1]['kiatsok']
        kutngte = '0.00'
        for s in su:
            kutngte = kaSikan(kutngte, s['tngte'])
        ko.append({
            'su': su,
            'khaisi': kukhaisi,
            'kiatsok': kukiatsok,
            'tngte': kutngte,
        })
        tsitma += liong
    return ko


def pooLomaji(wavPath, taibun):
    su = taibun.split()
    ko = []
    for tsua, punte in zip(poo_lian(wavPath, su, tsuanTuitsiau=False), su):
        *_tshun, khaisi, tngte, hunsu = tsua.split()
        if hunsu == '<unk>':
            hunsu = '{0}｜{0}'.format(punte)
        kiatsok = kaSikan(khaisi, tngte)
        ko.append({
            'punte': punte,
            'hunsu': hunsu,
            'khaisi': khaisi,
            'kiatsok': kiatsok,
            'tngte': tngte,
        })
    return ko


def poo_lian(wavPath, taiBun, tsuanTuitsiau):
    ling_tshamsoo = {'wav': wavPath, }
    with post_liansuann('ling_kaldi_format', ling_tshamsoo) as inue:
        tmpPath = json.loads(inue)
        logger.debug('ling %s', tmpPath)
    it_tshamsoo = {
        'tmpTonganSootsai': tmpPath,
        'taibun': json.dumps(taiBun),
        'tsuanTuitsiau': tsuanTuitsiau,
    }
    with post_liansuann('it_poolmj', it_tshamsoo) as inue:
        logger.debug('it %s', json.loads(inue))
    with post_liansuann('ji_fst_decoding_koh_rescoring', {
        'tmpTonganSootsai': tmpPath
    }) as inue:
        logger.debug('ji %s', json.loads(inue))
    with get_liansuann('sam_sikan', tmpPath) as inue:
        sikan = json.loads(inue)
        logger.debug('sam \n%s', ''.join(sikan))
    return sikan


def khuann_kiangi(ko, punte_su):
    # Kiàn-li̍p DP pió
    dp_tin = [[], ]
    loo_tin = [[], ]
    for _ in range(len(punte_su) + 1):
        dp_tin[0].append((0, 0, 0))
        loo_tin[0].append('tah-té')
    for su in ko:
        tsua_dp = [(0, 0, 0), ]
        tsua_loo = ['tah-té', ]

        hanji = 拆文分析器.分詞詞物件(su['hunsu']).看語句()
        for binting, tshu, punte in zip(
            dp_tin[-1][1:], dp_tin[-1], punte_su
        ):
            kam_u = tuitse_boolean(kiamtsa(
                hanji, punte
            ))
            if punte.isnumeric():
                sooji_binting = (binting[0], binting[1] + 1, binting[2])
                sooji_tshu = (tshu[0], tshu[1] + 1, tshu[2])
                if sooji_tshu >= sooji_binting:
                    tsua_dp.append(sooji_tshu)
                    tsua_loo.append('sooji_tshu')
                else:
                    tsua_dp.append(sooji_binting)
                    tsua_loo.append('sooji_binting')
            elif kam_u:
                hah_tshu = (tshu[0] + 1, tshu[1], tshu[2])
                tsua_dp.append(hah_tshu)
                tsua_loo.append('tshu')
            else:
                # Bô tsit jī
                behah_tshu = (tshu[0], tshu[1], tshu[2] + 1)
                tsua_dp.append(behah_tshu)
                tsua_loo.append('behah_tshu')
        dp_tin.append(tsua_dp)
        loo_tin.append(tsua_loo)
    # Se̍h-thâu khuànn siáng ū tuì--tio̍h
    kiat_ko = []
    sin_punte = []
    tit = len(ko)
    huinn = len(punte_su)
    while tit > 0 or huinn > 0:
        hanji = 拆文分析器.分詞詞物件(ko[tit - 1]['hunsu']).看語句()
        punte = punte_su[huinn - 1]
        if loo_tin[tit][huinn] == 'tshu':
            tit -= 1
            huinn -= 1
            kiat_ko.append(punte)
            sin_punte.append(punte)
        elif loo_tin[tit][huinn] == 'sooji_binting':
            tit -= 1
            kiat_ko.append(hanji)
            sin_punte.append(punte)
        elif loo_tin[tit][huinn] == 'sooji_tshu':
            tit -= 1
            huinn -= 1
            kiat_ko.append(hanji)
            sin_punte.append(punte)
        elif loo_tin[tit][huinn] == 'behah_tshu':
            tit -= 1
            huinn -= 1
            kiat_ko.append(punte)
            sin_punte.append(punte)
    sin_punte.reverse()
    kiat_ko.reverse()
    return sin_punte, kiat_ko
