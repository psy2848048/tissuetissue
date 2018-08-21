from detectLongDist import SearchLongDist
from scoring import Scoring
from termcolor import colored


def analyzer_top5(word):
    candidate_creater = SearchLongDist()
    scorer = Scoring()

    candidates = candidate_creater.getCandidates(word)
    ret = scorer.scoring(candidates)

    if len(ret) > 0:
        return ret

    else:
        return [
                {
                      "score": 1
                    , "candidate": [ 
                          {
                              "cnt": 0
                            , "word": word
                          } 
                        ]
                }
               ]

def analyzer(word):
    cand = analyzer_top5(word)
    if len(cand) > 0:
        ret = [ item['word'] for item in cand[0]['candidate'] ]

    else:
        ret = [ word ]

    return ret


if __name__ == '__main__':
    import csv
    import argparse
    import sys

    parser = argparse.ArgumentParser(description='TissueTissue Compond Noun Analyzer')
    parser.add_argument('-i', '--input', dest='filename', help='Test input file name')
    parser.add_argument('-t', '--test', dest='test', action='store_true', help='Test input file name')
    args = parser.parse_args()

    testcases = []
    if "filename" not in args or args.filename == None or args.filename == "":
        parser.print_help()
        sys.exit(1)

    if args.test == True:
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

    else:
        f = open(args.filename, 'r')
        word_list = f.read().split('\n')
        f.close()

        for word in word_list:
            f2 = open('output.txt', 'a')
            answer = ' '.join( analyzer(word) )
            f2.write( '{}\n'.format(answer) )
            f2.close()

