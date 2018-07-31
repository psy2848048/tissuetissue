import re
import csv

class ParseDic(object):
    def __init__(self):
        self.fileString = ""
        self.organized = []
        pass

    def readFile(self, filename):
        with open(filename, 'r') as f:
            temp = f.read()
            self.fileString = temp.split('\n')

    def parseString(self):
        unit_dic = {}
        for idx, line in enumerate(self.fileString):
            if idx % 2 == 0 and idx != len(self.fileString) - 1:
                category_obj = re.search(r'\<(.*?)\>', line)
                if category_obj == None:
                    print(idx, line)

                category = category_obj.group(1)
                unit_dic['category'] = category

                unit_dic['words'] = [ item.strip() for item in re.sub(r'\<.*?\>', '', line).split(',') ]

            elif idx % 2 == 0 and idx == len(self.fileString) - 1:
                continue

            else:
                unit_dic['answer'] = line

                self.organized.append(unit_dic)

                unit_dic = {}

    def organizeUnitDic(self):
        res = {}
        for item in self.organized:
            if item['category'] == '용례':
                continue

            for word in item['words']:
                if word not in res:
                    res[word] = len(word)

        with open('unitDicData.csv', 'w') as f:
            writer = csv.writer(f)
            for word, length in res.items():
                writer.writerow([str(length), word])

    def organizeProbModelData(self):
        res = {}
        for item in self.organized:
            if item['category'] == '용례':
                continue

            stem = item['words'][0]
            child = item['words'][1:]

            if stem not in res:
                res[stem] = child

            else:
                res[stem].extend(child)

        with open('probModelData.csv', 'w') as f:
            writer = csv.writer(f)
            for stem, child in res.items():
                writer.writerow([stem, ','.join(child)])


if __name__ == "__main__":
    parsing = ParseDic()
    parsing.readFile('combined_noun.txt')

    parsing.parseString()
    parsing.organizeUnitDic()
    parsing.organizeProbModelData()

