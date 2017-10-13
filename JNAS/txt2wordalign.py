#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands
import sys
import codecs
import copy
import re
import argparse

sys.stdin = codecs.getreader('utf-8')(sys.stdin)
sys.stdout = codecs.getwriter('utf-8')(sys.stdout)

mecab = "mecab -d /usr/lib/mecab/dic/mecab-ipadic-neologd"

parser = argparse.ArgumentParser()
parser.add_argument('targetfile', type=str, help='target file(e.g.001_KAN.txt)')

args = parser.parse_args()


def yomi2voca(sent):
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

    # sent = re.sub(r'([a-zA-Z]):', '$1 $1', sent)

    return sent


def mecab_analysis(txt):
    res = commands.getoutput("echo %s | %s" % (txt, mecab)).rstrip("\n").decode('utf-8').split("\n")[:-1]
    res = [r.replace(u"\t", u",").split(u",") + [None for i in range(max(0, 10 - len(r.split(u","))))] for r in res]

    katakana = u"ァアィイゥウェエォオカガキギクグケゲコゴサザシジスズセゼソゾタダチヂッツヅテデトドナニヌネノハバパヒビピフブプヘベペホボポマミムメモャヤュユョヨラリルレロヮワヰヱヲンヴー"

    for r in range(len(res)):
        if r < len(res):
            # katakana
            if res[r][8] == None and (all([ch in katakana for ch in res[r][0]]) == True):
                res[r][8] = res[r][0]

            # remove unreadable marks
            if res[r][1] == u'記号' and res[r][8] == None:
                del res[r]

    return res


def get_acc_boundary(ctxt):
    res = [True for x in range(len(ctxt))]

    for c in range(len(ctxt)):
        if c < len(ctxt) - 1:
            # rule 2
            if ctxt[c][1] == u'名詞' and ctxt[c + 1][1] == u'名詞':
                res[c] = True
            # rule 3
            if ctxt[c][1] == u'形容詞' and ctxt[c + 1][1] == u'名詞':
                res[c] = False
            # rule 4
            if ctxt[c][1] == u'形容詞' and ctxt[c][2] == u'形容動詞語幹' and ctxt[c + 1][1] == u'名詞':
                res[c] = False
            # rule 5
            if (ctxt[c][1] == u'動詞') and (ctxt[c + 1][1] == u'形容詞' or ctxt[c + 1][1] == u'名詞'):
                res[c] = False

        # rule 6
        if ctxt[c][1] in [u'副詞', u'接続詞', u'連体詞']:
            res[c] = False
            # rule 7
        if ctxt[c][1] == u'名詞' and ctxt[c][2] == u'副詞可能':
            res[c] = False
        # rule 8
        if ctxt[c][1] in [u'助詞', u'助動詞']:
            res[c] = True

        if c < len(ctxt) - 1:
            # rule 9
            if ctxt[c][1] in [u'助詞', u'助動詞'] and ctxt[c + 1][1] not in [u'助詞', u'助動詞']:
                res[c] = False
            # rule 10
            if ctxt[c][2] == u'接尾' and ctxt[c + 1][1] == u'名詞':
                res[c] = False

        if c > 0:
            # rule 11
            if (ctxt[c - 1][1] == u'形容詞' and ctxt[c - 1][2] == u'非自立') and ( \
                            (ctxt[c][1] == u'動詞' and ctxt[c][2][:2] == u'連用') or \
                                (ctxt[c][1] == u'形容詞' and ctxt[c][2][:2] == u'連用') or \
                            (ctxt[c][1] == u'助詞' and ctxt[c][2] == u'接続助詞' and ctxt[c][7] in [u'で', u'て'])):
                res[c] = True
            # rule 12
            if (ctxt[c - 1][1] == u'動詞' and ctxt[c - 1][2] == u'非自立') and ( \
                            (ctxt[c][1] == u'動詞' and ctxt[c][2][:2] == u'連用') or \
                                (ctxt[c][1] == u'名詞' and ctxt[c][2] == u'サ変接続') or \
                            (ctxt[c][1] == u'助詞' and ctxt[c][2] == u'接続助詞' and ctxt[c][7] in [u'で', u'て'])):
                res[c] = True

                # rule 13
        if ctxt[c][1] == u'記号':
            res[c] = False

    return res


def get_phonemes(ctxt):
    phone = []

    for c in ctxt:
        if c[8] is None:
            print c[0]
            raise ValueError("Can't recognize yomi")

        phs = list(c[8])
        phone.append([])

        # get mora boudary
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
            phs[m] = yomi2voca(phs[m]).strip()

            # print phs[m]
            if phs[m] == u':':
                phs[m] = phs[m - 1][-1]

            # print phs[m]
            if not re.match(r'[a-zA-Z\: ]+', phs[m]):
                phs[m] = 'pau'
            phs[m] = phs[m].split(" ")
            # print phs

        phone[-1] = phs
        # print phone[-1]

    return phone
    # print phone
    # exit(0)

def get_katakana(ctxt):
    src = []
    kat = []
    for c in ctxt:
        if c[8] is None:
            print c[0]
            raise ValueError("Can't Recognize yomi")
        src.append(c[0])
        kat.append(c[8])

    return src, kat



if __name__ == '__main__':
    # text = "あらゆる現実を，全て自分の方へねじ曲げたのだ．"

    sentencenum = 0

    for text in open("/home/akiyama/JNAS/JNAS1/OriginalText/KANJI/NP_unlabeled/" + args.targetfile).readlines():
        sentencenum += 1
        # for text in ['もともとは日本髪を結う時の道具の一つで、かつては$女性＄同様に「男性も」髪を纏めるためにこれを用いた。']:
        text = text.rstrip("\n")
        context = mecab_analysis(text)
        accbound = get_acc_boundary(context)
        try:
            phoneme = get_phonemes(context)
        except ValueError:
            print args.targetfile, sentencenum

        src, kat = get_katakana(context)


        # print sentence segmented by accent phrase boundary, mora, and phoneme
        # sent = ""
        # for (c, a, p) in zip(context, accbound, phoneme):
        #     #sent += c[0] + "("
        #     for m in p:
        #         for n in m:
        #             sent += n
        #             sent += " "
                #sent += "-".join(m)  # phoneme
                #sent += "_"  # mora boundary
            #sent += ")"
            # if a is False:  # accent phrase boundary
            #     sent += "\n"
                # print c[0], c[1], a

        #print text.decode('utf-8'), "->\n", sent
        #print sent

        fw = open("/home/akiyama/JNAS/align_data/" + args.targetfile.rstrip("_KAN.txt") + "/" + args.targetfile.rstrip("_KAN.txt") + "{0:03d}".format(sentencenum) + ".align", "w")

        for s in range(len(src)):
            srcsplit = " ".join(src[s])
            katsplit = " ".join(kat[s])
            fw.write(srcsplit.encode('utf-8'))
            fw.write(" ||| ")
            fw.write(katsplit.encode('utf-8'))
            fw.write("\n")

        fw.close()

    print args.targetfile + ",Completed!"


        # fw.write("%s\n"%text)
        #sent = sent.rstrip()
        #fw.write(sent.encode('utf-8'))
        #fw.close()