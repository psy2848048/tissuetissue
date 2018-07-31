import re
import csv


class ExtractNoun(object):
    def __init__(self):
        self.stopwords = []
        self._loadStopwordList("stopwords.csv")

    def _loadStopwordList(self, filename):
        with open(filename, 'r') as f:
            csvReader = csv.reader(f)
            for row in csvReader:
                self.stopwords.append(row[0])

        self.stopwords.sort(key=len, reverse=True)

    def extract(self, chunk):
        regex = r'(.*?){}\Z'
        extracted_word = ""
        for word in self.stopwords:
            extracted_obj = re.search(regex.format(word), chunk)
            if extracted_obj is None:
                continue

            else:
                extracted_word = extracted_obj.group(1)
                break

        return extracted_word

if __name__ == "__main__":
    obj = ExtractNoun()
    word = obj.extract("술렁이는")
    print(word)
