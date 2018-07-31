import pymysql
import copy

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

        heads = [ self._unitDivide(original_word, rightMost=fromRight) ]
        idx = 0

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

        return heads



if __name__ == "__main__":
    searchObj = SearchLongDist()
    test_words = ["한국전력공사", "세종말뭉치", "언어정보연구원장", "두피케어전문샴푸", "대학생선교회"]
    for word in test_words:
        ret = searchObj.nounPartioning(word)
        print("{} 결과:".format(word))
        print("Left")
        for item in ret:
            print(item)

        ret = searchObj.nounPartioning(word, fromRight=True)
        print("Right")
        for item in ret:
            print(item)

        print()

