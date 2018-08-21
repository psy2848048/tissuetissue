import sys
sys.path.append("../noun")
sys.path.append("./noun")
import unittest
from datetime import datetime, timedelta

from compound_noun_analyzer import analyzer
from detectLongDist import SearchLongDist
from scoring import Scoring


class CompoundNounAnalyzerTestCase(unittest.TestCase):

    def test01_getCondidates(self):
        test_words = [
                  "한국전력공사"
                , "세종말뭉치"
                , "언어정보연구원장"
                , "두피케어전문샴푸"
                , "대학생선교회"
                , "투자자귀속유의"
                , "드루킹특검"
                , "한국사물인터넷진흥협회"
                , "바람막이"
                , "올챙이자리"
                , "두물머리"
                , "버르장머리"
                , "대한항공대한항공"
                ]

        searchObj = SearchLongDist()
        for word in test_words:
            ret = searchObj.getCandidates(word)
            print("{} 결과:".format(word))
            for item in ret:
                print(item)

            print()

            self.assertEqual(True, True if len(ret) >= 1 else False)

    def test02_scoring(self):
        candObj = Scoring()
        testset = [
              [{'cnt': 0, 'word': '한국사물인터넷진흥'}, {'cnt': 204, 'word': '협회'}]
            , [{'cnt': 0, 'word': '한국사물인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
            , [{'cnt': 0, 'word': '한국사물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 0, 'word': '진흥협회'}]
            , [{'cnt': 0, 'word': '한국사물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
            , [{'cnt': 0, 'word': '한'}, {'cnt': 19, 'word': '국사'}, {'cnt': 0, 'word': '물인터넷진흥협회'}]
            , [{'cnt': 0, 'word': '한'}, {'cnt': 19, 'word': '국사'}, {'cnt': 0, 'word': '물인터넷진흥'}, {'cnt': 204, 'word': '협회'}]
            , [{'cnt': 0, 'word': '한'}, {'cnt': 19, 'word': '국사'}, {'cnt': 0, 'word': '물인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
            , [{'cnt': 0, 'word': '한'}, {'cnt': 19, 'word': '국사'}, {'cnt': 0, 'word': '물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 0, 'word': '진흥협회'}]
            , [{'cnt': 0, 'word': '한'}, {'cnt': 19, 'word': '국사'}, {'cnt': 0, 'word': '물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
            , [{'cnt': 1779, 'word': '한국'}, {'cnt': 0, 'word': '사물인터넷진흥협회'}]
            , [{'cnt': 1779, 'word': '한국'}, {'cnt': 0, 'word': '사물인터넷진흥'}, {'cnt': 204, 'word': '협회'}]
            , [{'cnt': 1779, 'word': '한국'}, {'cnt': 0, 'word': '사물인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
            , [{'cnt': 1779, 'word': '한국'}, {'cnt': 292, 'word': '사물'}, {'cnt': 0, 'word': '인터넷진흥협회'}]
            , [{'cnt': 1779, 'word': '한국'}, {'cnt': 292, 'word': '사물'}, {'cnt': 0, 'word': '인터넷진흥'}, {'cnt': 204, 'word': '협회'}]
            , [{'cnt': 1779, 'word': '한국'}, {'cnt': 292, 'word': '사물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 0, 'word': '진흥협회'}]
            , [{'cnt': 1779, 'word': '한국'}, {'cnt': 292, 'word': '사물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
            , [{'cnt': 4, 'word': '한국사'}, {'cnt': 0, 'word': '물인터넷진흥협회'}]
            , [{'cnt': 4, 'word': '한국사'}, {'cnt': 0, 'word': '물인터넷진흥'}, {'cnt': 204, 'word': '협회'}]
            , [{'cnt': 4, 'word': '한국사'}, {'cnt': 0, 'word': '물인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
            , [{'cnt': 4, 'word': '한국사'}, {'cnt': 0, 'word': '물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 0, 'word': '진흥협회'}]
            , [{'cnt': 4, 'word': '한국사'}, {'cnt': 0, 'word': '물'}, {'cnt': 2, 'word': '인터넷'}, {'cnt': 57, 'word': '진흥'}, {'cnt': 204, 'word': '협회'}]
            ]

        ret = candObj.scoring(testset)

        for item in ret:
            print(item)

        self.assertEqual(5, len(ret))

    def test03_repeating(self):
        now = datetime.now()
        res = analyzer("대한항공대한항공")
        end = datetime.now()

        self.assertEqual(True, True if end - now < timedelta(seconds=30) else False )
