# HelaSentiLex (Hela Sentiment Lexicon)
Python API for Sinhala Sentiment Lexicon

### Setup environment
1. Make sure you have Python >= 3.6 by `python --version`
2. Additionally, you’ll need to make sure you have pip available by running `pip --version`
3. To install pip see [install pip](https://pip.pypa.io/en/stable/installing/)
4. Install helasentilex package using the command `pip install helasentilex`

### Getting started
Let's begin with showing how easy it is to find sentiments of Sinhala words using helasentilex
```
>>> import helasentilex
>>> helasentilex.sentiment('යහපත්')
1
>>> helasentilex.sentiment('අමිහිරි')
-1
>>> helasentilex.sentiment('පරිගණකය')
0
```

If the input word does not exist in our sentiment lexicon or the input is invalid then it will return `None`
```
>>> helasentilex.sentiment(23)
None
```

You can enter a sentence as a string and get sentiment scores for available words in the sentiment lexicon
```
>>> helasentilex.sentiments('හොඳින් හෝ නරකින් කරන්න')
{'හොඳින්': 1, 'හෝ': 0, 'නරකින්': -1, 'කරන්න': None}
```

If the input is invalid then it will return an empty dictionary
```
>>> helasentilex.sentiments(23)
{}
```

### Defining labels
```
 1: POSITIVE (ධනාත්මක)
-1: NEGATIVE (ඍණාත්මක)
 0: OBJECTIVE (මධ්‍යස්ථ හෝ උදාසීන)
```


### Contributing
Want to report a bug, contribute some code, or improve documentation? Excellent! fork our repository and start 
contributing.

#### Adding new words to the sentiment lexicon
To add new words along with their sentiment scores 

1. Open `lexicon.csv` file
2. Append `new_word,sentiment_score`
3. Sort words in ascending order
4. Save changes to your forked repo and make a pull request

_Love helasentilex? Give our repo a **star**!_