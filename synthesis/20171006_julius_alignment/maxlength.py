#!/usr/bin/env python
# -*- coding: utf-8 -*-

import numpy as np
import re

class maxlength :

    def maxlength(self, scpfile):

        len_cf0 = []

        for r in open(scpfile).readlines():
            fn = r.strip()
            accfile = "/home/akiyama/synthesis/20171006_julius_alignment/accphrase/" + fn[0:3] + "/" + fn + ".txt"
            labfile = "/home/akiyama/synthesis/20171006_julius_alignment/out/" + fn + ".lab"
            splitfile = "/home/akiyama/synthesis/20171006_julius_alignment/split/" + fn + ".lab"

            accstart = []
            accend = []
            accphrase = []
            phonemephrase = []

            acctimestart = []
            acctimeend = []

            #load phoneme-time relation

            phonemestart = []
            phonemeend = []
            for l in open(labfile).readlines():
                data = l.split(' ')
                phonemestart += [float(data[0])]
                phonemeend += [float(data[1])]

            # add silS to list
            acctimestart += [phonemestart[0]]
            acctimeend += [phonemeend[0]]
            accphrase += ["sil\n"]
            phonemephrase += ["sil"]


            #load accent phrase-word relation

            for a in open(accfile).readlines():
                data = a.strip().split(' ')
                accstart += [int(data[0])]
                accend += [int(data[1])]
                accphrase += [data[2] + "\n"]
                phonemephrase += [data[3]]


            #time-accphrase relation

            for i in range(len(accphrase) - 1):
                acctimestart += [phonemestart[accstart[i]]]
                acctimeend += [phonemeend[accend[i]]]


            # add silE to list
            acctimestart += [phonemestart[-1]]
            acctimeend += [phonemeend[-1]]
            accphrase += ["sil"]
            phonemephrase += ["sil"]

            timelength = phonemeend[-1]

            continuousF0file = "/home/akiyama/synthesis/20171006_julius_alignment/continuousF0/NF" + fn + "_DT.txt"
            continuousF0 = np.loadtxt(continuousF0file)

            framelength = len(continuousF0)

            sr = timelength / framelength

            sentence_len_cf0 = []
            for k in range(1, len(accphrase)-1):
                sub_cf0 = continuousF0[int(acctimestart[k] / sr):int(acctimeend[k] / sr)]
                sentence_len_cf0 += [len(sub_cf0)]

            len_cf0 += [max(sentence_len_cf0)]

        max_length = max(len_cf0)
        print("Max length is ", max_length)

        return max_length

    def yomi2voca(self, sent):
        sent = sent.replace(u'ウ゛ァ', u' b a')
        sent = sent.replace(u'ウ゛ィ', u' b i')
        sent = sent.replace(u'ウ゛ェ', u' b e')
        sent = sent.replace(u'ウ゛ォ', u' b o')
        sent = sent.replace(u'ウ゛ュ', u' by u')
        sent = sent.replace(u'ゥ゛', u' b u')
        sent = sent.replace(u'アァ', u' a a')
        sent = sent.replace(u'イィ', u' i i')
        sent = sent.replace(u'イェ', u' i e')
        sent = sent.replace(u'イャ', u' y a')
        sent = sent.replace(u'ウゥ', u' u:')
        sent = sent.replace(u'エェ', u' e e')
        sent = sent.replace(u'オォ', u' o:')
        sent = sent.replace(u'カァ', u' k a:')
        sent = sent.replace(u'キィ', u' k i:')
        sent = sent.replace(u'クゥ', u' k u:')
        sent = sent.replace(u'クャ', u' ky a')
        sent = sent.replace(u'クュ', u' ky u')
        sent = sent.replace(u'クョ', u' ky o')
        sent = sent.replace(u'ケェ', u' k e:')
        sent = sent.replace(u'コォ', u' k o:')
        sent = sent.replace(u'ガァ', u' g a:')
        sent = sent.replace(u'ギィ', u' g i:')
        sent = sent.replace(u'グゥ', u' g u:')
        sent = sent.replace(u'グャ', u' gy a')
        sent = sent.replace(u'グュ', u' gy u')
        sent = sent.replace(u'グョ', u' gy o')
        sent = sent.replace(u'ゲェ', u' g e:')
        sent = sent.replace(u'ゴォ', u' g o:')
        sent = sent.replace(u'サァ', u' s a:')
        sent = sent.replace(u'シィ', u' sh i:')
        sent = sent.replace(u'スゥ', u' s u:')
        sent = sent.replace(u'スャ', u' sh a')
        sent = sent.replace(u'スュ', u' sh u')
        sent = sent.replace(u'スョ', u' sh o')
        sent = sent.replace(u'セェ', u' s e:')
        sent = sent.replace(u'ソォ', u' s o:')
        sent = sent.replace(u'ザァ', u' z a:')
        sent = sent.replace(u'ジィ', u' j i:')
        sent = sent.replace(u'ズゥ', u' z u:')
        sent = sent.replace(u'ズャ', u' zy a')
        sent = sent.replace(u'ズュ', u' zy u')
        sent = sent.replace(u'ズョ', u' zy o')
        sent = sent.replace(u'ゼェ', u' z e:')
        sent = sent.replace(u'ゾォ', u' z o:')
        sent = sent.replace(u'タァ', u' t a:')
        sent = sent.replace(u'チィ', u' ch i:')
        sent = sent.replace(u'ツァ', u' ts a')
        sent = sent.replace(u'ツィ', u' ts i')
        sent = sent.replace(u'ツゥ', u' ts u:')
        sent = sent.replace(u'ツャ', u' ch a')
        sent = sent.replace(u'ツュ', u' ch u')
        sent = sent.replace(u'ツョ', u' ch o')
        sent = sent.replace(u'ツェ', u' ts e')
        sent = sent.replace(u'ツォ', u' ts o')
        sent = sent.replace(u'テェ', u' t e:')
        sent = sent.replace(u'トォ', u' t o:')
        sent = sent.replace(u'ダァ', u' d a:')
        sent = sent.replace(u'ヂィ', u' j i:')
        sent = sent.replace(u'ヅゥ', u' d u:')
        sent = sent.replace(u'ヅャ', u' zy a')
        sent = sent.replace(u'ヅュ', u' zy u')
        sent = sent.replace(u'ヅョ', u' zy o')
        sent = sent.replace(u'デェ', u' d e:')
        sent = sent.replace(u'ドォ', u' d o:')
        sent = sent.replace(u'ナァ', u' n a:')
        sent = sent.replace(u'ニィ', u' n i:')
        sent = sent.replace(u'ヌゥ', u' n u:')
        sent = sent.replace(u'ヌャ', u' ny a')
        sent = sent.replace(u'ヌュ', u' ny u')
        sent = sent.replace(u'ヌョ', u' ny o')
        sent = sent.replace(u'ネェ', u' n e:')
        sent = sent.replace(u'ノォ', u' n o:')
        sent = sent.replace(u'ハァ', u' h a:')
        sent = sent.replace(u'ヒィ', u' h i:')
        sent = sent.replace(u'フゥ', u' f u:')
        sent = sent.replace(u'フャ', u' hy a')
        sent = sent.replace(u'フュ', u' hy u')
        sent = sent.replace(u'フョ', u' hy o')
        sent = sent.replace(u'ヘェ', u' h e:')
        sent = sent.replace(u'ホォ', u' h o:')
        sent = sent.replace(u'バァ', u' b a:')
        sent = sent.replace(u'ビィ', u' b i:')
        sent = sent.replace(u'ブゥ', u' b u:')
        sent = sent.replace(u'フャ', u' hy a')
        sent = sent.replace(u'ブュ', u' by u')
        sent = sent.replace(u'フョ', u' hy o')
        sent = sent.replace(u'ベェ', u' b e:')
        sent = sent.replace(u'ボォ', u' b o:')
        sent = sent.replace(u'パァ', u' p a:')
        sent = sent.replace(u'ピィ', u' p i:')
        sent = sent.replace(u'プゥ', u' p u:')
        sent = sent.replace(u'プャ', u' py a')
        sent = sent.replace(u'プュ', u' py u')
        sent = sent.replace(u'プョ', u' py o')
        sent = sent.replace(u'ペェ', u' p e:')
        sent = sent.replace(u'ポォ', u' p o:')
        sent = sent.replace(u'マァ', u' m a:')
        sent = sent.replace(u'ミィ', u' m i:')
        sent = sent.replace(u'ムゥ', u' m u:')
        sent = sent.replace(u'ムャ', u' my a')
        sent = sent.replace(u'ムュ', u' my u')
        sent = sent.replace(u'ムョ', u' my o')
        sent = sent.replace(u'メェ', u' m e:')
        sent = sent.replace(u'モォ', u' m o:')
        sent = sent.replace(u'ヤァ', u' y a:')
        sent = sent.replace(u'ユゥ', u' y u:')
        sent = sent.replace(u'ユャ', u' y a:')
        sent = sent.replace(u'ユュ', u' y u:')
        sent = sent.replace(u'ユョ', u' y o:')
        sent = sent.replace(u'ヨォ', u' y o:')
        sent = sent.replace(u'ラァ', u' r a:')
        sent = sent.replace(u'リィ', u' r i:')
        sent = sent.replace(u'ルゥ', u' r u:')
        sent = sent.replace(u'ルャ', u' ry a')
        sent = sent.replace(u'ルュ', u' ry u')
        sent = sent.replace(u'ルョ', u' ry o')
        sent = sent.replace(u'レェ', u' r e:')
        sent = sent.replace(u'ロォ', u' r o:')
        sent = sent.replace(u'ワァ', u' w a:')
        sent = sent.replace(u'ヲォ', u' o:')
        sent = sent.replace(u'ウ゛', u' b u')
        sent = sent.replace(u'ディ', u' d i')
        sent = sent.replace(u'デェ', u' d e:')
        sent = sent.replace(u'デャ', u' dy a')
        sent = sent.replace(u'デュ', u' dy u')
        sent = sent.replace(u'デョ', u' dy o')
        sent = sent.replace(u'ティ', u' t i')
        sent = sent.replace(u'テェ', u' t e:')
        sent = sent.replace(u'テャ', u' ty a')
        sent = sent.replace(u'テュ', u' ty u')
        sent = sent.replace(u'テョ', u' ty o')
        sent = sent.replace(u'スィ', u' s i')
        sent = sent.replace(u'ズァ', u' z u a')
        sent = sent.replace(u'ズィ', u' z i')
        sent = sent.replace(u'ズゥ', u' z u')
        sent = sent.replace(u'ズャ', u' zy a')
        sent = sent.replace(u'ズュ', u' zy u')
        sent = sent.replace(u'ズョ', u' zy o')
        sent = sent.replace(u'ズェ', u' z e')
        sent = sent.replace(u'ズォ', u' z o')
        sent = sent.replace(u'キャ', u' ky a')
        sent = sent.replace(u'キュ', u' ky u')
        sent = sent.replace(u'キョ', u' ky o')
        sent = sent.replace(u'シャ', u' sh a')
        sent = sent.replace(u'シュ', u' sh u')
        sent = sent.replace(u'シェ', u' sh e')
        sent = sent.replace(u'ショ', u' sh o')
        sent = sent.replace(u'チャ', u' ch a')
        sent = sent.replace(u'チュ', u' ch u')
        sent = sent.replace(u'チェ', u' ch e')
        sent = sent.replace(u'チョ', u' ch o')
        sent = sent.replace(u'トゥ', u' t u')
        sent = sent.replace(u'トャ', u' ty a')
        sent = sent.replace(u'トュ', u' ty u')
        sent = sent.replace(u'トョ', u' ty o')
        sent = sent.replace(u'ドァ', u' d o a')
        sent = sent.replace(u'ドゥ', u' d u')
        sent = sent.replace(u'ドャ', u' dy a')
        sent = sent.replace(u'ドュ', u' dy u')
        sent = sent.replace(u'ドョ', u' dy o')
        sent = sent.replace(u'ドォ', u' d o:')
        sent = sent.replace(u'ニャ', u' ny a')
        sent = sent.replace(u'ニュ', u' ny u')
        sent = sent.replace(u'ニョ', u' ny o')
        sent = sent.replace(u'ヒャ', u' hy a')
        sent = sent.replace(u'ヒュ', u' hy u')
        sent = sent.replace(u'ヒョ', u' hy o')
        sent = sent.replace(u'ミャ', u' my a')
        sent = sent.replace(u'ミュ', u' my u')
        sent = sent.replace(u'ミョ', u' my o')
        sent = sent.replace(u'リャ', u' ry a')
        sent = sent.replace(u'リュ', u' ry u')
        sent = sent.replace(u'リョ', u' ry o')
        sent = sent.replace(u'ギャ', u' gy a')
        sent = sent.replace(u'ギュ', u' gy u')
        sent = sent.replace(u'ギョ', u' gy o')
        sent = sent.replace(u'ヂェ', u' j e')
        sent = sent.replace(u'ヂャ', u' j a')
        sent = sent.replace(u'ヂュ', u' j u')
        sent = sent.replace(u'ヂョ', u' j o')
        sent = sent.replace(u'ジェ', u' j e')
        sent = sent.replace(u'ジャ', u' j a')
        sent = sent.replace(u'ジュ', u' j u')
        sent = sent.replace(u'ジョ', u' j o')
        sent = sent.replace(u'ビャ', u' by a')
        sent = sent.replace(u'ビュ', u' by u')
        sent = sent.replace(u'ビョ', u' by o')
        sent = sent.replace(u'ピャ', u' py a')
        sent = sent.replace(u'ピュ', u' py u')
        sent = sent.replace(u'ピョ', u' py o')
        sent = sent.replace(u'ウァ', u' u a')
        sent = sent.replace(u'ウィ', u' w i')
        sent = sent.replace(u'ウェ', u' w e')
        sent = sent.replace(u'ウォ', u' w o')
        sent = sent.replace(u'ファ', u' f a')
        sent = sent.replace(u'フィ', u' f i')
        sent = sent.replace(u'フゥ', u' f u')
        sent = sent.replace(u'フャ', u' hy a')
        sent = sent.replace(u'フュ', u' hy u')
        sent = sent.replace(u'フョ', u' hy o')
        sent = sent.replace(u'フェ', u' f e')
        sent = sent.replace(u'フォ', u' f o')
        sent = sent.replace(u'ア', u' a')
        sent = sent.replace(u'イ', u' i')
        sent = sent.replace(u'ウ', u' u')
        sent = sent.replace(u'エ', u' e')
        sent = sent.replace(u'オ', u' o')
        sent = sent.replace(u'カ', u' k a')
        sent = sent.replace(u'キ', u' k i')
        sent = sent.replace(u'ク', u' k u')
        sent = sent.replace(u'ケ', u' k e')
        sent = sent.replace(u'コ', u' k o')
        sent = sent.replace(u'サ', u' s a')
        sent = sent.replace(u'シ', u' sh i')
        sent = sent.replace(u'ス', u' s u')
        sent = sent.replace(u'セ', u' s e')
        sent = sent.replace(u'ソ', u' s o')
        sent = sent.replace(u'タ', u' t a')
        sent = sent.replace(u'チ', u' ch i')
        sent = sent.replace(u'ツ', u' ts u')
        sent = sent.replace(u'テ', u' t e')
        sent = sent.replace(u'ト', u' t o')
        sent = sent.replace(u'ナ', u' n a')
        sent = sent.replace(u'ニ', u' n i')
        sent = sent.replace(u'ヌ', u' n u')
        sent = sent.replace(u'ネ', u' n e')
        sent = sent.replace(u'ノ', u' n o')
        sent = sent.replace(u'ハ', u' h a')
        sent = sent.replace(u'ヒ', u' h i')
        sent = sent.replace(u'フ', u' f u')
        sent = sent.replace(u'ヘ', u' h e')
        sent = sent.replace(u'ホ', u' h o')
        sent = sent.replace(u'マ', u' m a')
        sent = sent.replace(u'ミ', u' m i')
        sent = sent.replace(u'ム', u' m u')
        sent = sent.replace(u'メ', u' m e')
        sent = sent.replace(u'モ', u' m o')
        sent = sent.replace(u'ラ', u' r a')
        sent = sent.replace(u'リ', u' r i')
        sent = sent.replace(u'ル', u' r u')
        sent = sent.replace(u'レ', u' r e')
        sent = sent.replace(u'ロ', u' r o')
        sent = sent.replace(u'ガ', u' g a')
        sent = sent.replace(u'ギ', u' g i')
        sent = sent.replace(u'グ', u' g u')
        sent = sent.replace(u'ゲ', u' g e')
        sent = sent.replace(u'ゴ', u' g o')
        sent = sent.replace(u'ザ', u' z a')
        sent = sent.replace(u'ジ', u' j i')
        sent = sent.replace(u'ズ', u' z u')
        sent = sent.replace(u'ゼ', u' z e')
        sent = sent.replace(u'ゾ', u' z o')
        sent = sent.replace(u'ダ', u' d a')
        sent = sent.replace(u'ヂ', u' j i')
        sent = sent.replace(u'ヅ', u' z u')
        sent = sent.replace(u'デ', u' d e')
        sent = sent.replace(u'ド', u' d o')
        sent = sent.replace(u'バ', u' b a')
        sent = sent.replace(u'ビ', u' b i')
        sent = sent.replace(u'ブ', u' b u')
        sent = sent.replace(u'ベ', u' b e')
        sent = sent.replace(u'ボ', u' b o')
        sent = sent.replace(u'パ', u' p a')
        sent = sent.replace(u'ピ', u' p i')
        sent = sent.replace(u'プ', u' p u')
        sent = sent.replace(u'ペ', u' p e')
        sent = sent.replace(u'ポ', u' p o')
        sent = sent.replace(u'ヤ', u' y a')
        sent = sent.replace(u'ユ', u' y u')
        sent = sent.replace(u'ヨ', u' y o')
        sent = sent.replace(u'ワ', u' w a')
        sent = sent.replace(u'ヰ', u' i')
        sent = sent.replace(u'ヱ', u' e')
        sent = sent.replace(u'ン', u' N')
        sent = sent.replace(u'ッ', u' q')
        sent = sent.replace(u'ー', u':')
        sent = sent.replace(u'ァ', u' a')
        sent = sent.replace(u'ィ', u' i')
        sent = sent.replace(u'ゥ', u' u')
        sent = sent.replace(u'ェ', u' e')
        sent = sent.replace(u'ォ', u' o')
        sent = sent.replace(u'ヮ', u' w a')
        sent = sent.replace(u'ォ', u' o')
        sent = sent.replace(u'ヲ', u' o')
        # sent = sent.replace(u'^ ([a-z])', u'$1')
        sent = sent.replace(u':+', u':')
        sent = sent.replace(u'ャ', u' a')
        sent = sent.replace(u'ュ', u' u')
        sent = sent.replace(u'ョ', u' o')

        # sent = re.sub(r'([a-zA-Z]):', '$1 $1', sent)

        return sent

    def max_mora_length(self, scpfile):
        len_mora = []

        for r in open(scpfile).readlines():
            fn = r.strip()
            accfile = "/home/akiyama/synthesis/20171006_julius_alignment/accphrase/" + fn[0:3] + "/" + fn + ".txt"
            labfile = "/home/akiyama/synthesis/20171006_julius_alignment/out/" + fn + ".lab"
            splitfile = "/home/akiyama/synthesis/20171006_julius_alignment/split/" + fn + ".lab"

            katphrase = []
            sentence_moranum = []

            # load accent phrase-word relation

            for a in open(accfile).readlines():
                data = a.strip().split(' ')
                if len(data) < 4:
                    katphrase += [['pau']]
                else:
                    katphrase += [data[3]]

            for k in range(len(katphrase)):

                phs = list(katphrase[k])

                i = 0
                while i < len(phs):
                    if phs[i] in [u'ャ', u'ュ', u'ョ']:
                        if i == 0:
                            phs[i] = phs[i].replace(u'ャ', u'ヤ').replace(u'ュ', u'ユ').replace(u'ョ', u'ヨ')
                        else:
                            phs[i - 1] += phs[i]
                            del phs[i]
                            i -= 1
                    i += 1

                # katakana to phoneme
                for m in range(len(phs)):
                    phs[m] = self.yomi2voca(phs[m]).strip()

                    # print phs[m]
                    if phs[m] == u':':
                        phs[m] = phs[m - 1][-1]

                    # print phs[m]
                    if not re.match(r'[a-zA-Z\: ]+', phs[m]):
                        phs[m] = 'pau'
                    phs[m] = phs[m].split(" ")

                sentence_moranum += [len(phs)]

            len_mora += [max(sentence_moranum)]

        max_mora = max(len_mora)
        print("Max mora number is ", max_mora)

        return max_mora

    def mora_length(self,subword):
        phs = list(subword)

        i = 0
        while i < len(phs):
            if phs[i] in [u'ャ', u'ュ', u'ョ']:
                if i == 0:
                    phs[i] = phs[i].replace(u'ャ', u'ヤ').replace(u'ュ', u'ユ').replace(u'ョ', u'ヨ')
                else:
                    phs[i - 1] += phs[i]
                    del phs[i]
                    i -= 1
            i += 1

        # katakana to phoneme
        for m in range(len(phs)):
            phs[m] = self.yomi2voca(phs[m]).strip()

            # print phs[m]
            if phs[m] == u':':
                phs[m] = phs[m - 1][-1]

            # print phs[m]
            if not re.match(r'[a-zA-Z\: ]+', phs[m]):
                phs[m] = 'pau'
            phs[m] = phs[m].split(" ")

        return len(phs)
