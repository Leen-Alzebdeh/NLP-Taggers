# NLP-Taggers
compare, and contrast two part-of-speech taggers’ (HMM and Brill) performance on in-domain and out-of-domain text samples.

## Data
Input data: sentences with POS tags
  The input is a tsv (tab-separated values) file like the sample:
  |id|label|sentence|pos|
  | -|-----|--------|---|
  |73|0|Many thanks in advance for your cooperation .| JJ NNS IN NN IN PRP$ NN .| 74| 1| At that moment we saw the bus to come .|IN DT NN PRP VBD DT NN TO VB .|
  <br>
The id column is the unique id for each sentence. The label column indicates whether a sentence contains grammar errors (1 means having errors and 0 means error-free). The pos column contains the POS tags for each token in the sentence, also separated by a single space.

The POS tags follow the Penn Treebank (PTB) tagging scheme, described [here](https://www.ling.upenn.edu/courses/Fall_2003/ling001/penn_treebank_pos.html)
## Tasks
### Task 1: Building a toy grammar
  - We wrote a toy CFG for English in NLTK’s .cfg format.

### Task 2: Constituency parsing
  - We used the chart parser from NLTK to parse each of the POS sequences in the dataset with the toy grammar we wrote in task 1. We stored results in a TSV file with three columns:

|Column name|Description|
| --------- | --------- |
|id|The id of the input sentence.|ground_truth|The ground truth label of the input sentence, copied from the dataset. |
|prediction|1 if the sentence has grammar errors, 0 if not. In other words, whether the POS sequence can be parsed successfully with your grammar and parser.|

### Task 3: Evaluation and error analysis
- We evaluate the performance of our grammar checker by calculating its precision and recall on the data available to us. To do that, we compared the prediction of our system on a given sentence and its corresponding label in the dataset. 

# Report and Results
Further details and results can be found [here](https://github.com/Leen-Alzebdeh/NLP-Taggers/blob/main/REPORT.md)

# Contributors

Leen Alzebdeh  @Leen-Alzebdeh

Sukhnoor Khehra @Sukhnoor-K

# Resources Consulted

- https://gist.github.com/blumonkey/007955ec2f67119e0909
 - https://stats.stackexchange.com/questions/366552/nlp-various-probabilities-estimators-in-nltk
 - https://www.nltk.org/_modules/nltk/tag/hmm.html
 - https://gist.github.com/h-alg/4ec991f90a682c6d0a0b
 - https://www.nltk.org/_modules/nltk/tag/brill.html
 - https://www.nltk.org/api/nltk.tag.brill_trainer.html
 - Github Copilot

## Libraries

* `main.py L:4, 13` used `argparse` for extracting command line args.
* `main.py L:8, 104` used `os` for creating directory of output.
  
# Instructions to execute code

1. Ensure Python is installed, as well as the Python Standard Library. To download Python if it is not already installed, follow the instructions on the following website: [https://www.python.org/downloads/](https://www.python.org/downloads/).

Example usage: use the following commands in the current directory.

For using the HMM tagger on in-domain data:
`python3 src/main.py --tagger hmm --train data/train.txt --test data/test.txt --output output/test_hmm.txt`

For using the HMM tagger in out-of-domain data:
`python3 src/main.py --tagger hmm --train data/train.txt --test data/test_ood.txt --output output/test_ood_hmm.txt`

For using the Brill tagger on in-domain data:
`python3 src/main.py --tagger brill --train data/train.txt --test data/test.txt --output output/test_brill.txt`

For using the Brill tagger on out-of-domain data:
`python3 src/main.py --tagger brill --train data/train.txt --test data/test_ood.txt --output output/test_ood_brill.txt`

