from module_every_decomp import generate_whole_candidates

import pymysql
import copy

SUFFIX = [
            "자리"
          , "머리"
          , "몰이"
          , "쟁이"
          , "탱이"
          , "막이"
          , "거리"
          , "살이"
          , "치기"
          , "덩어리"
          , "받이"
        ]

class SearchLongDist(object):
    def __init__(self):
        self.conn = pymysql.connect(
                host="hotelchat.ce2zgalnsfar.ap-northeast-2.rds.amazonaws.com",
                db="tissue",
                user="translator", 
                password="noSecret01!",
                charset='utf8',
                cursorclass=pymysql.cursors.DictCursor
                )

    def _unitDivide(self, partial_word, rightMost=False):
        cursor = self.conn.cursor()
        res = []

        if len(partial_word) <= 1:
            if rightMost == False:
                return [{"cnt": 0, "word": partial_word}]
            else:
                return [{"cnt": 0, "word": partial_word[::-1]}]

        for idx in range(1, len(partial_word) + 1):
            if idx <= 1:
                continue

            particle = partial_word[:idx]
            if rightMost == True:
                particle = particle[::-1]

            length = len(particle)
            query = """
                SELECT cnt, word
                FROM sejongUnitDic
                WHERE length = %s AND word = %s
            """
            cursor.execute(query, (length, particle, ))
            ret = cursor.fetchone()

            if ret is None or len(ret) < 1:
                continue

            res.append({"cnt": ret['cnt'], "word": ret['word']})

        if len(res) >= 1:
            return res

        else:
            if rightMost == False:
                return [{"cnt": 0, "word": partial_word}]
            else:
                return [{"cnt": 0, "word": partial_word[::-1]}]


    def nounPartioning(self, word, fromRight=False):
        original_word = word
        if fromRight == True:
            original_word = original_word[::-1]

        heads = [ [item] for item in self._unitDivide(original_word, rightMost=fromRight) ]
        idx = 0

        loop = 0
        while True:
            # Checking more loop is needed
            total_length = 0
            for part in heads[idx]:
                total_length += len(part['word'])

            if idx == len(heads) - 1 and total_length == len(word):
                break

            elif idx < len(heads) - 1 and total_length == len(word):
                idx += 1
                continue

            # Divide another
            analyzed_head = ""
            for part in heads[idx]:
                analyzed_head += part['word']

            if fromRight == True:
                original_word = original_word[::-1]

            partial_word = original_word.replace(analyzed_head, "")

            if fromRight == True:
                original_word = original_word[::-1]
                partial_word = partial_word[::-1]

            mid_heads = self._unitDivide(partial_word, rightMost=fromRight)

            # Input result
            if len(mid_heads) == 1 and fromRight==False:
                heads[idx].append(mid_heads[0])

            elif len(mid_heads) == 1 and fromRight==True:
                heads[idx].insert(0, mid_heads[0])

            else:
                for idx_head, mid_head in enumerate(mid_heads):
                    stem = copy.deepcopy(heads[idx])
                    if idx_head < len(mid_heads) - 1 and fromRight==False:
                        stem.append(mid_head)
                        heads.append(stem)

                    elif idx_head < len(mid_heads) - 1 and fromRight==True:
                        stem.insert(0, mid_head)
                        heads.append(stem)

                    else:
                        if fromRight == False:
                            heads[idx].append(mid_head)

                        else:
                            heads[idx].insert(0, mid_head)


            # Prepare another loop
            if idx == len(heads) - 1:
                idx = 0

            if loop > 30:
                break

            loop += 1

        return heads

    def forcedPartition(self, word):
        cursor = self.conn.cursor()

        # use Hyonsu's function
        partitioned_candidates = generate_whole_candidates(word)

        mid_partitioned_list = []
        for item in partitioned_candidates:
            mid_partitioned_list.extend(item)

        mid_partitioned_list = list(set([ "'{}'".format(unit_word) for unit_word in mid_partitioned_list if len(unit_word) > 1 ]))
        inlined_string = ', '.join(mid_partitioned_list)

        query = """
            SELECT cnt, word
            FROM sejongUnitDic
            WHERE word IN ( {} )
        """.format(inlined_string)
        cursor.execute(query)
        words_in_db_list = cursor.fetchall()
        words_in_db_list_words_only = [ item['word'] for item in words_in_db_list ]

        res = []
        for candidate in partitioned_candidates:
            is_exist = False
            temp_res = []

            for idx, unit_word in enumerate(candidate):
                if unit_word in words_in_db_list_words_only:
                    is_exist = True
                    for db_item in words_in_db_list:
                        if db_item['word'] == unit_word:
                            temp_res.append(dict(db_item))
                            break

                else:
                    if idx == 0:
                        temp_res.append({"cnt":0, "word":unit_word})
                    else:
                        if temp_res[-1]['cnt'] > 0:
                            temp_res.append({"cnt":0, "word":unit_word})
                        else:
                            temp_res[-1]['word'] = "{}{}".format(temp_res[-1]['word'], unit_word)

            if is_exist == True:
                for item in res:
                    if temp_res == item:
                        break
                    
                    if len(temp_res) != len(item):
                        continue

                    # Word check
                    cnt_new = 0
                    cnt_old = 0
                    for word_new, word_old in zip(temp_res, item):
                        if word_new['word'] != word_old['word']:
                            break

                        cnt_new += word_new['cnt']
                        cnt_old += word_old['cnt']

                    else:
                        if cnt_new >= cnt_old:
                            res.remove(item)
                            res.append(temp_res)

                        break

                else:
                    res.append(temp_res)

        return res

    def weightRedistribution(self, candidates):
        dup_candidates = copy.deepcopy(candidates)
        ret = []
        for unit_cand in dup_candidates:

            is_exist = False
            for idx, word in enumerate(unit_cand):
                if idx == 0 and len(word['word']) == 1:
                    #어두에 1음절
                    print("Front: ", unit_cand)
                    is_exist = True
                    re_cnt = unit_cand[1]['cnt']
                    re_word = word['word'] + unit_cand[1]['word']
                    for anot_cand in dup_candidates:
                        for anot_word in anot_cand:
                            if re_word == anot_word['word']:
                                anot_word['cnt'] += re_cnt

                elif idx < len(unit_cand) - 1 and len(word['word']) == 1:
                    # 중간 1음절
                    print("Middle: ", unit_cand)
                    is_exist = True

                    re_cnt_front = unit_cand[idx-1]['cnt']
                    re_word_front = unit_cand[idx-1]['word'] + word['word']
                    re_cnt_back = unit_cand[idx+1]['cnt']
                    re_word_back = word['word'] + unit_cand[idx+1]['word']
                    for anot_cand in dup_candidates:
                        for anot_word in anot_cand:
                            if re_word_front == anot_word['word']:
                                anot_word['cnt'] += re_cnt_front

                            elif re_word_back == anot_word['word']:
                                anot_word['cnt'] += re_cnt_back

                elif idx == len(unit_cand) - 1 and len(word['word']) == 1:
                    # 어말에 1음절
                    print("End: ", unit_cand)
                    is_exist = True
                    re_cnt = unit_cand[idx-1]['cnt']
                    re_word = unit_cand[idx-1]['word'] + word['word']
                    for anot_cand in dup_candidates:
                        for anot_word in anot_cand:
                            if re_word == anot_word['word']:
                                anot_word['cnt'] += re_cnt

                else:
                    # 음슴
                    pass

        for unit_cand in dup_candidates:
            need_break = False
            for word in unit_cand:
                if len(word['word']) < 2:
                    need_break = True
                    break
            else:
                ret.append(unit_cand)

        return ret

    def suffixForceAttach(self, candidates):
        ret = []
        for unit_cand in candidates:
            if unit_cand[-1]['word'] in SUFFIX and len(unit_cand) > 1:
                new_cand = copy.deepcopy(unit_cand)

                new_cand[-2]['word'] += unit_cand[-1]['word']
                new_cand.remove(new_cand[-1])

                ret.append(new_cand)

            else:
                ret.append(unit_cand)

        return ret

    def getCandidates(self, word):
        ret_left = self.nounPartioning(word)
        ret_right = self.nounPartioning(word, fromRight=True)
        ret_forced = self.forcedPartition(word)

        ret = ret_left
        for item in ret_right:
            if item not in ret:
                ret.append(item)

        for item in ret_forced:
            if item not in ret:
                ret.append(item)

        ret = self.weightRedistribution(ret)
        ret = self.suffixForceAttach(ret)

        return ret


if __name__ == "__main__":
    searchObj = SearchLongDist()
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
            ]
    for word in test_words:
        try:
            ret = searchObj.getCandidates(word)
            print("{} 결과:".format(word))
            for item in ret:
                print(item)

            print()

        except:
            print("인터넷 연결을 확인해주세요!")
