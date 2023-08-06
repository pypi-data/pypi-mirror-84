import logging

from kaldiliau.kesi import kaSikan
from kaldiliau.poo_lomaji_liansuann import poo_lian, khuann_kiangi


logger = logging.getLogger(__name__)


def pooLomaji_kah_sooji(wavPath, taibun):
    su = taibun.split()
    ko = []
    for tsua in poo_lian(wavPath, su, tsuanTuitsiau=True):
        *_tshun, khaisi, tngte, hunsu = tsua.split()
        if hunsu == '<unk>':
            hunsu = '{0}｜{0}'.format('UNK')
        kiatsok = kaSikan(khaisi, tngte)
        ko.append({
            'hunsu': hunsu,
            'khaisi': khaisi,
            'kiatsok': kiatsok,
            'tngte': tngte,
        })
    punte, kiangi = khuann_kiangi(ko, su)
    for su, punte, kiangi in zip(ko, punte, kiangi):
        *_tshun, khaisi, tngte, hunsu = tsua.split()
        kiatsok = kaSikan(khaisi, tngte)
        su.update({
            'punte': punte,
            'kiangi': kiangi,
        })
    return ko
    return ko
