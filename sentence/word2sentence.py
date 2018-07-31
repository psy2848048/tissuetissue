import hgtk
import koreanLetter as kl
import re

def charAssembler(raw_sentence):
    # ㄱ ㄴ ㄷ ㄹ ... 모두 어디에 저장
    # 앞 글자가 받침이 없고, 뒷 글자가 외자면: 앞 글자 decompose, 뒷 글자와 결합
    # 외자 스캔 -> 외자가 있을 시 앞자를 보기
    
    organized_sentence = raw_sentence
    for idx, unitLetter in enumerate(organized_sentence):
        if unitLetter in kl.WHOLE_CONSONANT_SET:
            temp_idx = idx - 1 
            while organized_sentence[temp_idx] == ' ':
                temp_idx += -1
                if temp_idx <= 0:
                    print("Cannot find consonant")
                    break

            print('"{}"'.format(organized_sentence[temp_idx]))
            if not hgtk.checker.is_hangul(organized_sentence[temp_idx]):
                continue

            decomposed_letter = list(hgtk.letter.decompose(organized_sentence[temp_idx]))
            replaced_letter = ""
            if decomposed_letter[2] == '': 
                decomposed_letter[2] = unitLetter
                print(decomposed_letter)
                replaced_letter = hgtk.letter.compose(*decomposed_letter)
                organized_sentence = organized_sentence[:temp_idx] + replaced_letter + organized_sentence[temp_idx+1:idx] + ' ' + organized_sentence[idx+1:]

    return organized_sentence

def extractQuote(sentence):
    regx = r'\((.*?)\)|\[(.*?)\]|\{(.*?)\}|\「(.*?)\」|\『(.*?)\』|\<(.*?)\>|\《(.*?)\》|\"(.*?)\"|\'(.*?)\'|\-(.*?)\-'
