# This program receives the tagger type and the path to a test file
# as command line parameters and outputs the POS tagged version of that file.

import argparse
from nltk.tag import hmm
from nltk.probability import MLEProbDist, ELEProbDist, LaplaceProbDist, LidstoneProbDist, FreqDist
from nltk.tag.brill import Pos, Word, fntbl37, nltkdemo18, brill24, nltkdemo18plus
from nltk.tag.brill_trainer import BrillTaggerTrainer
from nltk.tag import RegexpTagger
from nltk.tbl.template import Template
import nltk
import os


def main():

    parser = argparse.ArgumentParser()

    # Create positional (mandatory) arguments
    parser.add_argument('--tagger', type=str, required=True)
    parser.add_argument('--train', type=str, required=True)
    parser.add_argument('--test', type=str, required=True)
    parser.add_argument('--output', type=str, required=True)

    # Get the argument list
    args = parser.parse_args()

    train_data = process_data(args.train)

    test_data = process_data(args.test)

    if args.tagger == 'hmm':

        trainer = hmm.HiddenMarkovModelTrainer()

        # test_hmm(trainer, train_data, test_data)

        # best hmm tagger parameters over test.txt, second best over test_ood.txt
        def estimator(fdist, bins): return nltk.LidstoneProbDist(
            fdist, 1e-5, bins)

        tagger = trainer.train_supervised(train_data, estimator=estimator)

        print("\nBest HMM tagger testing result (estimator: Listone, gamma: 1e-5)")

        tagger.test(test_data)

    elif args.tagger == 'brill':
        baseline = RegexpTagger([
            (r'^-?[0-9]+(\.[0-9]+)?$', 'CD'),  # cardinal numbers
            (r'(The|the|A|a|An|an)$', 'AT'),   # articles
            (r'.*able$', 'JJ'),                # adjectives
            (r'.*ness$', 'NN'),                # nouns formed from adjectives
            (r'.*ly$', 'RB'),                  # adverbs
            (r'.*s$', 'NNS'),                  # plural nouns
            (r'.*ing$', 'VBG'),                # gerunds
            (r'.*ed$', 'VBD'),                 # past tense verbs
            (r'.*', 'NN')                      # nouns (default)
        ])

        # test_brill(baseline, train_data, test_data)
        Template._cleartemplates()
        trainer = BrillTaggerTrainer(initial_tagger=baseline,
                                     templates=brill24(), trace=3)
        tagger = trainer.train(train_data, max_rules=200)
        print("\nBest Brill tagger testing result (template: brill24, count: 200)")
        print(tagger.accuracy(test_data))

    output_tags(tagger, args.test, args.output)


def test_hmm(trainer, train_data, test_data):
    """
    Test different HMM tagger parameters
    
    Args:
        trainer (HiddenMarkovModelTrainer): HMM trainer
        train_data (list): training data
        test_data (list): testing data

    Returns:
        None
    """
    print("Testing LidStone")
    # test lidstone
    for i in [1e-2, 1e-3, 1e-4, 1e-5, 1e-6]:

        print("With i: ", i)

        def estimator(fdist, bins): return nltk.LidstoneProbDist(
            fdist, i, bins)

        tagger = trainer.train_supervised(train_data, estimator=estimator)

        tagger.test(test_data)

    # MLE
    print("---"*10)
    print("Testing MLE (Default)")
    tagger = trainer.train_supervised(train_data, estimator=nltk.MLEProbDist)

    tagger.test(test_data)

    # ELE
    print("---"*10)
    print("Testing ELE")

    def estimator(fdist, bins): return nltk.ELEProbDist(
        fdist, bins)

    tagger = trainer.train_supervised(train_data, estimator=estimator)

    tagger.test(test_data)

    # Laplace
    print("---"*10)
    print("Testing Laplace")
    def estimator(fdist, bins): return nltk.LaplaceProbDist(
        fdist, bins)

    tagger = trainer.train_supervised(train_data, estimator=estimator)

    tagger.test(test_data)


def test_brill(baseline, train_data, test_data):
    """
    Test different Brill tagger parameters

    Args:
        baseline (RegexpTagger): baseline tagger
        train_data (list): training data
        test_data (list): testing data
    
    Returns:
        None
    """
    templates_list = {"demo18": nltkdemo18(),
                      "fntb137": fntbl37(),
                      "brill24": brill24()}
    counts = [10, 50, 100, 200]

    for template in templates_list:
        for count in counts:
            Template._cleartemplates()
            trainer = BrillTaggerTrainer(initial_tagger=baseline,
                                         templates=templates_list[template], trace=3)
            tagger = trainer.train(train_data, max_rules=count)
            print("Template: {}, count: {}".format(template, count))
            print(tagger.accuracy(test_data))
            print("---"*10)


def process_data(data_path):
    """
    Process the data from the given path

    Args:
        data_path (str): path to the data file
    
    Returns:
        list: list of tuples (word, tag)
    """
    file = open(data_path, 'r', errors='ignore')
    lines = [l for l in (line.strip() for line in file)
             if l]  # ignoring empty lines

    for ind in range(len(lines)):
        doc = lines[ind].split()
        word, tag = doc[0], doc[1]
        lines[ind] = [(word, tag)]

    return lines


def output_tags(tagger, test_path, output_path):
    """
    Output the POS tagged version of the test file

    Args:
        tagger (TaggerI): POS tagger
        test_path (str): path to the test file
        output_path (str): path to the output file
    
    Returns:
        None
    """
    os.makedirs(output_path.split('/')[0], exist_ok=True)

    file = open(test_path, 'r', errors='ignore')
    lines = file.readlines()

    with open(output_path, 'w') as fp:
        for line in lines:
            if line != '\n':
                doc = line.strip().split(" ")
                pair = tagger.tag([doc[0]])[0]
                # write each item on a new line
                fp.write("{} {}\n".format(pair[0], pair[1]))
            else:

                fp.write("\n")


main()
