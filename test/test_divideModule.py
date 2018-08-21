import sys
sys.path.append("../noun")
sys.path.append("./noun")
sys.path.append("./")
import unittest
from datetime import datetime, timedelta
from module_every_decomp import generate_whole_candidates, get_lemma_list_of_dictionary_A, scoring_candidates

class DevideModuleTestCase(unittest.TestCase):

    def test01_getCondidates(self):
        compound_noun = "흙먼지털이기"
        whole_candidates = generate_whole_candidates(compound_noun)
        lemma_list_of_dict_A = get_lemma_list_of_dictionary_A()
        list_with_score = scoring_candidates(whole_candidates, lemma_list_of_dict_A, compound_noun)
        threshold = 0
        for i in list_with_score:
            if i[1] > threshold: #복합명사 별로 출력되는 점수대가 다름. 적당히 조절해가면서 보세여
                print(i)

