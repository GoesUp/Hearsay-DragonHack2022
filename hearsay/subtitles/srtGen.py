# pip install pyenchant
import enchant

from hearsay.assembly.manager import TranscriptionResult

import json
import srt
from datetime import timedelta


# usage:
#	transcription to srt 		-> fja srt_from_transcription(transcription)
#	transciption + text to srt  -> fja srt_from_transcription_and_text(transcription, real_text)
#   transcription + srt to srt  -> fja srt_from_transcription_and_srt(transcription, srt_str)
#	Vse te fje vrnem srt_str, ki ga lahko sharnis v file z :
#		write_to_file(filename, srt)	
#
#	Za testiranje je se uporabno json_file_to_transcription(json_filename)

def srt_from_transcription(transcription: TranscriptionResult):
    return srt_from_words(transcription.words)


def srt_from_transcription_and_text(transcription: TranscriptionResult, real_text: str):
    return srt_from_text_and_words(real_text, transcription.words)


def srt_from_transcription_and_srt(transcription: TranscriptionResult, srt_str: str):
    text = ""
    subs = list(srt.parse(srt_str))
    for s in subs:
        text += s.content
        text += " "

    text = text.replace("\n", " ").replace("  ", " ")
    # print(text)
    return srt_from_transcription_and_text(transcription, text)


def write_to_file(filename, text):
    with open(filename, "w") as file:
        file.write(text)


def json_file_to_transcription(json_filename):
    with open(json_filename) as file:
        transcription_json = json.loads(file.read())
        return TranscriptionResult(**transcription_json)


# tole se mal bolj internal fje

def srt_from_words(words):
    subs = []
    stavek = []

    for word in words:
        if (len(word.text) < 1):
            continue

        prva_beseda = 0 == len(stavek)
        zadnja_beseda = word.text[-1] == '.' or len(stavek) > 10
        stavek.append(word)

        if (not zadnja_beseda):
            continue

        stavek_str = ""
        for b in stavek:
            stavek_str += b.text + " "

        dolzina_napisa = len(stavek_str)
        for x in range(dolzina_napisa // 2, dolzina_napisa):
            if (stavek_str[x] == ' '):
                stavek_str = stavek_str[:x] + "\n" + stavek_str[x + 1:]
                break

        # stavek_str = stavek_str.replace("\n ", "\n")

        subs.append(srt.Subtitle(index=1 + len(subs), start=timedelta(milliseconds=stavek[0].start),
                                 end=timedelta(milliseconds=stavek[-1].end + 500),
                                 content=stavek_str))  # +500 podaljsa dolzino podnapisa za max 500ms

        if (len(subs) > 1):  # popravimo mozna prekrivanja
            if (subs[-2].end > subs[-1].start):
                subs[-2].end = subs[-1].start

        stavek = []
        dolzina_vrstice = 0

    result = srt.compose(subs)
    # print(result)
    return result


def cmp_beseda(value, target):  # uporabmo Levenstain iz pyenchant
    value = value.replace(",", "").replace(".", "")
    target = target.replace(",", "").replace(".", "")
    levenstain = enchant.utils.levenshtein(value.lower(), target.lower())
    return 1 - levenstain / len(target)


def find_next_match(target, str_words, search_depth):
    best_match = 0
    best_index = 0
    for d in range(min(search_depth, len(str_words))):
        cmp_str = str_words[d]

        curr_match = cmp_beseda(cmp_str, target)
        if (curr_match == 1):  # najdena beseda
            return d

        if (curr_match > best_match):
            best_match = curr_match
            best_index = d

    if (best_match) > 0.5:  # najdena priblizno podobna beseda
        return best_index

    return -1  # ni blo najdene podobne besede


def srt_from_text_and_words(real_text, words):
    output_words = []  # tipa Word

    r_words = real_text.split(' ')
    t_words = [x.text for x in words]

    print(t_words)

    r_index = 0
    t_index = 0

    ##naceloma, ce najdemo match, moremo vedno izbrat besedo iz real_text
    # za vsak match, ko najdem bom dodal besedo iz trans result, ki popravim z textom iz real texta
    # v output_trans_result

    while (r_index < len(r_words) and t_index < len(t_words)):
        r_target = r_words[r_index]
        t_target = t_words[t_index]

        foundat = find_next_match(r_target, t_words[t_index:], 5)

        if (foundat < 0):  # ni blo najdenega matcha.
            # probamo se obratno.
            foundat = find_next_match(t_target, r_words[r_index:], 5)
            if (foundat < 0):  # ni blo nobenega matcha v obeh smereh. -> preskocimo to besedo.
                r_index += 1
                t_index += 1
                continue

            r_index += foundat + 1
            t_index += 1

            # print("match: {}, {}".format(t_target, r_words[r_index]))
            output_words.append(words[t_index - 1])
            output_words[-1].text = r_words[r_index - 1]
            continue

        # print("match: {}, {}".format(r_target, t_words[t_index + foundat]))
        r_index += 1
        t_index += foundat + 1

        output_words.append(words[t_index - 1])
        output_words[-1].text = r_words[r_index - 1]

    # print(output_words)
    # print(r_words)
    # print(t_words)
    return srt_from_words(output_words)
