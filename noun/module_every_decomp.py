from itertools import combinations
import re

def get_lemma_list_of_dictionary_A():
    dic_file = open("./dic_A")
    lines = dic_file.readlines()
    lemma_list = []
    for line in lines:
        lemma_list.append(line.split('\t')[1])
    #print(lemma_list)
    return lemma_list

def generate_whole_candidates(input_string):

    preprocessed_input = ""
    every_candidates_final = []

    # 예를 들면 "대학생선교회"를 "대1학2생3선4교5회"로 만드는 과정. 분절 경계 위치를 나타내는 마커는 $(숫자)& 포맷을 따름.
    # preprocessed_input = "대$1&학$2&생$3&선$4&교$5&회"로 변환됨.
    for i in range(len(input_string)):
        if not len(input_string) == i+1:
            preprocessed_input = preprocessed_input + input_string[i] + "$" + str(i+1) + "&"
        else:
            preprocessed_input = preprocessed_input + input_string[i]

    # 조합의 모든 경우 생성.
    split_range = range(1, len(input_string))
    split_combination = []

    for i in range(1, len(split_range)):
        split_combination = split_combination + list(combinations(split_range, i))

    # 조합 목록을 참고하여 해당하는 분절 경계에 구분자를 삽입. 여기서는 콤마(,)를 사용.
    for tuple in split_combination:
        current_sequence = preprocessed_input
        for position in tuple:
            current_sequence = current_sequence.replace("$"+str(position)+"&", ',')
        #사용되지 않은 분절 경계 마커는 모두 삭제 처리.
        parsed_string = re.sub("\$\d+&", "", current_sequence)
        every_candidates_final.append(parsed_string.split(","))

    every_candidates_final.sort()   #심심해서 소팅 한 번

    # 콘솔 출력
    print("Sorted list of whole candidates has been generated: length "+ str(len(every_candidates_final)))
    #print(every_candidates_final)

    return every_candidates_final

def scoring_candidates(whole_candidates, lemma_list_of_dict_A, compound_noun):
    list_with_score = []

    for candidate in whole_candidates:

        matched_constituents_positive = 0 # 사전에서 매칭된 단어의 개수마다 +1점
        single_syllable_negative = 0 # 1음절짜리로 쪼개진 경우마다 -1점
        simplicity_score_positive = len(compound_noun) - len(candidate) #콤마 개수가 적을수록 높은 점수

        for constituent in candidate:
            if lemma_list_of_dict_A.__contains__(constituent):
                matched_constituents_positive = matched_constituents_positive + 1
            if len(constituent) == 1:
                single_syllable_negative = single_syllable_negative + 1

        weight = (matched_constituents_positive * 3) - (single_syllable_negative * 1.2) + (simplicity_score_positive * 1.2)

        list_with_score.append([candidate, weight])

    list_with_score.sort(key=lambda list_with_score: list_with_score[1], reverse=True)

    return list_with_score


### 여기부터 메인 코드 시작
if __name__ == "__main__":
    compound_noun = "흙먼지털이기"
    
    whole_candidates = generate_whole_candidates(compound_noun)
    
    lemma_list_of_dict_A = get_lemma_list_of_dictionary_A()
    
    list_with_score = scoring_candidates(whole_candidates, lemma_list_of_dict_A, compound_noun)
    
    threshold = 0
    for i in list_with_score:
        if i[1] > threshold: #복합명사 별로 출력되는 점수대가 다름. 적당히 조절해가면서 보세여
            print(i)
