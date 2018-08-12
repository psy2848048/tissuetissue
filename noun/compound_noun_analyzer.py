from detectLongDist import SearchLongDist
from scoring import Scoring
from termcolor import colored


def analyzer_top5(word):
    candidate_creater = SearchLongDist()
    scorer = Scoring()

    candidates = candidate_creater.getCandidates(word)
    ret = scorer.scoring(candidates)

    return ret

def analyzer(word):
    cand = analyzer_top5(word)
    ret = [ item['word'] for item in cand[0]['candidate'] ]

    return ret


if __name__ == "__main__":
    import csv
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='TissueTissue Compond Noun Analyzer')
    parser.add_argument('-f', '--file', dest='filename', help='Test input file name')
    args = parser.parse_args()

    testcases = []
    if "filename" not in args or args.filename == None or args.filename == "":
        parser.print_help()
        sys.exit(1)

    with open(args.filename, 'r') as f:
        reader = csv.reader(f)
        for item in reader:
            case = item[0]
            answer = item[1]
            testcases.append([case, answer.split(",")])

    test_result = []
    for word, answer in testcases:
        ret = analyzer_top5(word)
        for item in ret:
            print(item)

        top_answer = analyzer(word)
        print(colored("Top answer: ", "red"), "{}".format(top_answer))
        print()

        test_result.append([word, ",".join(answer), ",".join(top_answer), "O" if top_answer == answer else "X"])

    with open("result.csv", 'w') as f2:
        writer = csv.writer(f2)
        for item in test_result:
            writer.writerow(item)