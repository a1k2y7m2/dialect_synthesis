#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import commands
import sys
import codecs
import copy
import re

txt_path = ""
alignment_path = "/home/akiyama/"
subword_path = ""

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
    sent = sent.replace(u'ャ', u' a')
    sent = sent.replace(u'ュ', u' u')
    sent = sent.replace(u'ョ', u' o')

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

def alignnum2list(alignnum_file):
    alignnum = []
    for text in open(alignnum_file).readlines():
        text = text.rstrip("\n")
        list = text.split(" ")
        contextalign = []
        for l in list:
            char_kat = map(int, l.split("-"))
            contextalign.append(char_kat)

        alignnum.append(contextalign)

    return alignnum

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

#subwordnumber - contextnumber

def subword_context(subwordfile, src):
    src_char_len = []
    for i in range(len(src)):
        src_char_len.append(len(src[i]))

    src_char_num = []
    for i in range(len(src)):
        src_char_num.append(sum(src_char_len[0:i+1]))

    subword = open(subwordfile).read()
    #subword = "私は JASCA に 所属 しています。"
    subword = subword.rstrip()

    subword_list = subword.rsplit(" ")

    # for subword in subword_list:
    #     print subword.decode('utf-8')


    subword_char_len = []
    for i in range(len(subword_list)):
        subword_char_len.append(len(subword_list[i].decode('utf-8')))

    subword_char_num = []
    for i in range(len(subword_list)):
        subword_char_num.append(sum(subword_char_len[0:i+1]))

    src_num = []
    subword_num = []

    if src_char_num[len(src_char_num) - 1] <> subword_char_num[len(subword_char_num) - 1]:
        #print "There is something wrong in subwordtxt in " + args.targetfile.rstrip("_KAN.txt") + "{0:03d}".format(sentencenum)
        return 0, 0, 0

    for j in range(src_char_num[len(src_char_num) - 1]):
        for k in range(len(src_char_num)):

            if j < src_char_num[k] and k == 0:
               src_num.append([0, j])
               break

            elif j < src_char_num[k]:
                src_num.append([k, j-src_char_num[k-1]])
                break

    # for j in range(subword_char_num[len(subword_char_num) - 1]):
    #     for k in range(len(subword_char_num)):
    #
    #         if j < subword_char_num[k] and k == 0:
    #            subword_num.append([0, j])
    #            break
    #
    #         elif j < subword_char_num[k]:
    #             subword_num.append([k, j-subword_char_num[k-1]])
    #             break

    # print src_num
    # print subword_char_num
    # print subword_num

    return src_num, subword_char_num, subword_list

def subword_phoneme(src_num, subword_char_num, alignnum, kat):

    #convert kat into list
    devided_kat = []
    for context_kat in kat:
        devided_kat.append(list(context_kat))

    subword_kat = []

    for i in range(len(subword_char_num)):
        subword_kat_list = []
        if i == 0:
            for j in range(0,subword_char_num[i]):
                char_kat_list = []
                ctxtword = src_num[j][0]
                ctxtwordchar = src_num[j][1]

                for relation in alignnum[ctxtword]:
                    if relation[0] == ctxtwordchar:
                        char_kat_list.append(devided_kat[ctxtword][relation[1]])

                char_kat = "".join(char_kat_list)
                subword_kat_list.append(char_kat)

            subword_kat.append("".join(subword_kat_list))




                #print subword_kat_num
        else:
            for j in range(subword_char_num[i-1],subword_char_num[i]):
                char_kat_list = []
                ctxtword = src_num[j][0]
                ctxtwordchar = src_num[j][1]

                for relation in alignnum[ctxtword]:
                    if relation[0] == ctxtwordchar:
                        char_kat_list.append(devided_kat[ctxtword][relation[1]])

                char_kat = "".join(char_kat_list)
                subword_kat_list.append(char_kat)

            subword_kat.append("".join(subword_kat_list))

    # print text
    # for kat in subword_kat:
    #     print kat.encode('utf-8')

    # get mora boudary
    # i = 0
    # while i < len(subword_kat):
    #     if subword_kat[i] in [u'ャ', u'ュ', u'ョ']:
    #         if i == 0:
    #             subword_kat[i] = subword_kat[i].replace(u'ャ', u'ヤ').replace(u'ュ', u'ユ').replace(u'ョ', u'ヨ')
    #         else:
    #             subword_kat[i - 1] += subword_kat[i]
    #             del subword_kat[i]
    #             i -= 1
    #     i += 1

    connec_subword_phone = []
    subword_phone_list = []

    for s in range(len(subword_kat)):

        subword_phone = []

        phs = list(subword_kat[s])
        prephs = list(subword_kat[max([s - 1, 0])])
        i = 0
        while i < len(phs):
            if phs[i] in [u'ャ', u'ュ', u'ョ']:
                if i == 0:
                    #phs[i] = phs[i].replace(u'ャ', u'ヤ').replace(u'ュ', u'ユ').replace(u'ョ', u'ヨ')
                    # シ ョ -> 'ショ' -> 'sh o' -> 'sh' 'o'
                    if s == 0 or len(prephs) == 0:
                        phs[i] = phs[i].replace(u'ャ', u'ヤ').replace(u'ュ', u'ユ').replace(u'ョ', u'ヨ')
                    else:
                        connec_kat = prephs[-1] + phs[i]
                        phoneme_kat = yomi2voca(connec_kat).strip()
                        phoneme = phoneme_kat.split(" ")
                        phs[i] = phoneme[-1]
                        if not len(yomi2voca(prephs[-1]).strip().split(" ")) == 1:
                            del connec_subword_phone[-1]
                            del subword_phone_list[-1][-1]
                        connec_subword_phone[-1] = phoneme[0]
                        subword_phone_list[-1][-1] = phoneme[0]

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

            #print phs[m].encode('utf-8')
            phs[m] = phs[m].split(" ")

            connec_subword_phone += phs[m]
            subword_phone += phs[m]
        subword_phone_list.append(subword_phone)



        # subword_kat[m] = yomi2voca(subword_kat[m]).strip()
        #
        # if subword_kat[m] == u':':
        #     subword_kat[m] = subword_kat[m - 1][-1]
        #
        # if not re.match(r'[a-zA-Z\: ]+', subword_kat[m]):
        #     subword_kat[m] = 'pau'
        #
        # subword_kat[m] = subword_kat[m].split(" ")
        #
        # connec_subword_phone += subword_kat[m]


    #print subword_phone_list

    return subword_phone_list, connec_subword_phone

def get_connec_phonemes(ctxt):
    connec_phone = []

    for c in ctxt:
        if c[8] is None:
            print c[0]
            raise ValueError("Can't recognize yomi")

        phs = list(c[8])
        #phone.append([])


        #get mora boudary


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

            #print phs[m].encode('utf-8')
            phs[m] = phs[m].split(" ")
            # print phs

            connec_phone += phs[m]

    #print connec_phone
        #print phone[-1]

    return connec_phone
    # print phone
    # exit(0)






if __name__ == "__main__":

    sentencenum = 0
    wrongnum = 0

    for text in open("/home/akiyama/JNAS/JNAS1/OriginalText/KANJI/NP_unlabeled/" + args.targetfile).readlines():
        sentencenum += 1

        alignnumfile = "/home/akiyama/synthesis/fast_align/build/char_kat_align/" + args.targetfile.rstrip("_KAN.txt") + "/" + args.targetfile.rstrip("_KAN.txt") + "{0:03d}".format(sentencenum) + ".alignnum"
        alignnum = alignnum2list(alignnumfile)

        rawscriptfile = "/home/akiyama/JNAS/JNAS_rawscript/" + args.targetfile.rstrip("_KAN.txt") + "/" + args.targetfile.rstrip("_KAN.txt") + "{0:03d}".format(sentencenum) + ".txt"
        text = open(rawscriptfile).read()
        text = text.rstrip("\n")
        #print text
        context = mecab_analysis(text)
        src, kat = get_katakana(context)

        subwordfile = "/home/akiyama/JNAS/JNAS_sentencepiece/subword_txt/" + args.targetfile.rstrip("_KAN.txt") + "/" + args.targetfile.rstrip("_KAN.txt") + "{0:03d}".format(sentencenum) + ".sub"

        src_num, subword_char_num, subword_list = subword_context(subwordfile, src)

        if src_num ==0:
            wrongnum += 1
            # print text
            # print args.targetfile.rstrip("_KAN.txt") + "{0:03d}".format(sentencenum)
            # for sub in subword_list:
            #     print sub.decode('utf-8')
            # #print subword_phone
            continue

        subword_phone, connec_subword_phone = subword_phoneme(src_num, subword_char_num, alignnum, kat)
        connec_ctxt_phone = get_connec_phonemes(context)

        if not connec_subword_phone == connec_ctxt_phone:
            wrongnum += 1
            # print text
            # for sub in subword_list:
            #     print sub.decode('utf-8')
            # print connec_subword_phone
            # print connec_ctxt_phone
            # print "There is something wrong in fast_align in " + args.targetfile.rstrip("_KAN.txt") + "{0:03d}".format(sentencenum)
            continue

        fw = open(
            "/home/akiyama/JNAS/JNAS_splitdata/" + args.targetfile.rstrip("_KAN.txt") + "/" + args.targetfile.rstrip(
                "_KAN.txt") + "{0:03d}".format(sentencenum) + ".txt", "w")

        startnum = 1
        endnum = 0
        if not len(subword_list) == len(subword_phone):
            # print text
            # print args.targetfile.rstrip("_KAN.txt") + "{0:03d}".format(sentencenum)
            # for sub in subword_list:
            #     print sub.decode('utf-8')
            # print subword_phone
            continue

        for m in range(len(subword_list)):
            endnum += len(subword_phone[m])
            fw.write("%i "%startnum)
            fw.write("%i "%endnum)
            fw.write(subword_list[m])
            fw.write("\n")
            startnum += len(subword_phone[m])

        fw.close()

    #print wrongnum

    #     # for text in ['もともとは日本髪を結う時の道具の一つで、かつては$女性＄同様に「男性も」髪を纏めるためにこれを用いた。']:
    #     text = text.rstrip("\n")
    #     context = mecab_analysis(text)
    #     src, kat = get_katakana(context)





