# Sequence Transfer

The sequence transfer library developed by [Pangeanic](https://www.pangeanic.com/) is part of the MAPA anonymisation project, funded by the European Commission.
The main goal of the library is to make it easy to transfer annotations between different representations of the same text, for example by tokenizing it.




## Sequences & transfers 
Transfering annotations between BERT and Moses tokens or between BERT tokens and the text source requires a kind of "mapping". Thoses "mappings" are called transfers in the this library.

A transfer operates over sequences: sequences of chars or sequences of tokens. 

To clarify the main ideas, here is an example:

First, we create some sequences:

```python
from sequence_transfer.sequence import CharSequence, TokenSequence
from sequence_transfer.magic_transfer import MagicTransfer
from sequence_transfer.plugin.entity_annotation_transfer_plugin import EntityAnnotationTransferPlugin \
    , EntityAnnotationSequence

text = CharSequence.new("  J'adore  Zoé!  ")  # Sequence of chars
bert_tokens = TokenSequence.new(['j', "'", 'ado', '##re', 'zo', '##e', '!'])  # Sequence of tokens
moses_tokens = TokenSequence.new(['J&apos;', 'adore', 'Zoé', '!'])   # Sequence of tokens
moses_detokenized = CharSequence.new("J'adore Zoé !")  # Sequence of chars

```

Now we can create a transfer function between any pair of thoses sequences. For example, suppose we want to know wich charchaters of the text source correspond to the 5th and 6th BERT tokens 'zo' and '##e' in the source text:

```python
 # We select the 5th and 6th BERT tokens
s = bert_tokens[4:6] 

# We create a transfer function
transfer1 = MagicTransfer(bert_tokens, text)  

# We apply the transfer function to our sequence
transferred = transfer1.apply(s)
print(f"Text: {transferred.text}")
# --> Text: Zoé
print(f"Offsets: {transferred.start}, {transferred.stop}")
# --> Offsets: 11, 14
```

What we did between BERT tokens and the source text can be achieved between any pair of sequences. For example between BERT tokens and Moses Tokens:

```python
transfer2 = MagicTransfer(bert_tokens, moses_tokens) 
transferred = transfer2.apply(s)
print(f"Offsets: {transferred.start}, {transferred.stop}")
# --> Offsets: 2, 3
```

To see a representation of the "mapping" created by the transfer function:

```python
transfer2.debug()

# |Src slice|Index src|Text src|    |Text tgt|Index tgt|Tgt slice|
# |:-------:|:-------:|:------:|:--:|:------:|:-------:|:-------:|
# |  [0:2]  |    0    |   j    |--->|J&apos; |    0    |  [0:1]  |
# |         |    1    |   '    |    |        |         |         |
# |         |         |        |    |        |         |         |
# |  [2:4]  |    2    |  ado   |--->| adore  |    1    |  [1:2]  |
# |         |    3    |  ##re  |    |        |         |         |
# |         |         |        |    |        |         |         |
# |  [4:6]  |    4    |   zo   |--->|  Zoé   |    2    |  [2:3]  |
# |         |    5    |  ##e   |    |        |         |         |
# |         |         |        |    |        |         |         |
# |  [6:7]  |    6    |   !    |--->|   !    |    3    |  [3:4]  |

```

## Annotation transfers
Now we can transfer annotations:
```python
annotations = EntityAnnotationSequence.new([
    "O",
    "O",
    "O",
    "O",
    "B-PER",
    "L-PER",
    "O",
], "biluo")

transferred_annotations = transfer1.apply(annotations, plugin=EntityAnnotationTransferPlugin())
print(transferred_annotations.convert("biluo"))
# ---> ['O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'O', 'B-PER', 'I-PER', 'L-PER', 'O', 'O', 'O'] 
```

## The magic transfer architecture
The MagicTransfer is one of the transfer functions available on the library (all transfer functions are composable and reversible). The "Magic" transfer is still in BETA and requires further testing. Nevertheless, because of its architecture we think that it should be quite strong very soon.

The Magic transfer is based on a supervised renormalization of both texts: the source and its tokenized form. Supervised means that each renormalization function returns a transfer function which tracks the changes it made.

After the renormalization process, both texts tend to be very similar so we use what git usse to detect changes in code (the LCS algorithm) and detect the most longest common subsequence of these two texts and convert that result to another transfer function.

Then it is mathematics:
- if f1, f2, .., fn are the transfer functions for the normalization of the source
- if g1, g2, .., gn are  the transfer functions for the renormalization of the tokenized text
- if h is the LCS transfer
- Then MagicTransfer = Compose(Compose(f1, f2, ...fn), h , Inverse(Compose(g1, g2, ..., gn)))

At this moment, the MagicTransfer function uses only 4 normalizers but we will add more in a near future.

Note for developers: The transfer functions are not letter to letter functions but slice to slice functions. Just observe, in the debug table, that the slice [3:4] is transferred to the slice [3:7]. Slices are sequences and "sequence" is the term used in the source code of the library. My preferred notation for a slice or a sequence is [n p[ reflecting the antisymmetry between the status of both numbers. [n n[ starts with n, but ends before n. It is empty, but positioned!

## Installation

### Requirements
python 3.7

### Test the library
Clone the repository from Github
```BASH
git clone https://github.com/Pangeamt/sequence_transfer.git test_sequence_transfer
cd test_sequence_transfer
```

Create a virtualenv

```BASH
virtualenv -p python3.7 venv
source venv/bin/activate
```

Install requirements
```BASH
pip install -r requirements.txt
```

Install sequence_transfer
```BASH
python setup.py install
```
