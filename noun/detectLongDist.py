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

    def _unitDivide(self, partial_word):
        cursor = self.conn.cursor()
        res = []

        if len(partial_word) <= 1:
            return [{"cnt": 0, "word": partial_word}]

        for idx in range(1, len(partial_word) + 1):
            if idx <= 1:
                continue

            particle = partial_word[:idx]
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
            return [{"cnt": 0, "word": partial_word}]


    def leftMost(self, word):
        heads = [ self._unitDivide(word) ]
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

            partial_word = word.replace(analyzed_head, "")
            mid_heads = self._unitDivide(partial_word)

            # Input result
            if len(mid_heads) == 1:
                heads[idx].append(mid_heads[0])

            else:
                for idx_head, mid_head in enumerate(mid_heads):
                    stem = copy.deepcopy(heads[idx])
                    if idx_head < len(mid_heads) - 1:
                        stem.append(mid_head)
                        heads.append(stem)

                    else:
                        heads[idx].append(mid_head)


            # Prepare another loop
            if idx == len(heads) - 1:
                idx = 0


        return heads


if __name__ == "__main__":
    searchObj = SearchLongDist()
    test_words = ["한국전력공사", "세종말뭉치", "언어정보연구원장", "두피케어전문샴푸", "대학생선교회"]
    for word in test_words:
        ret = searchObj.leftMost(word)
        print("{} 결과:".format(word))
        for item in ret:
            print(item)

        print()

