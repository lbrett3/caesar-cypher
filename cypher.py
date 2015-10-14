import string
import random

WORDLIST_FILENAME = "words.txt"


def loadWords():
    """
    Returns a list of valid words. Words are strings of lowercase letters.
    
    Depending on the size of the word list, this function may
    take a while to finish.
    """
    print "Loading word list from file..."
    inFile = open(WORDLIST_FILENAME, 'r')
    wordList = inFile.read().split()
    print "  ", len(wordList), "words loaded."
    return wordList

def isWord(wordList, word):
    """
    Determines if word is a valid word.
    returns True if word is in wordList.
    """
    word = word.lower()
    word = word.strip(" !@#$%^&*()-_+={}[]|\\:;'<>?,./\"")
    return word in wordList

def randomWord(wordList):
    """
    Returns a random word.
    """
    return random.choice(wordList)

def randomString(wordList, n):
    """
    Returns a string containing n random words from wordList
    """
    return " ".join([randomWord(wordList) for _ in range(n)])

def randomScrambled(wordList, n):
    """
    Generates a test string by generating an n-word random string
    and encrypting it with a sequence of random shifts.

    n: number of random words to generate and scamble
    """
    s = randomString(wordList, n) + " "
    shifts = [(i, random.randint(0, 25)) for i in range(len(s)) if s[i-1] == ' ']
    return applyShifts(s, shifts)[:-1]

def getStoryString():
    """
    Returns a story in encrypted text.
    """
    return open("story.txt", "r").read()

#Encryption

def buildCoder(shift):
    """
    Returns a dict that can apply a Caesar cipher to a letter.
    The cipher is defined by the shift value. Ignores non-letter characters
    like punctuation, numbers and spaces.

    shift: 0 <= int < 26
    returns: dict
    """
    lower = string.ascii_lowercase
    upper = string.ascii_uppercase
    lower2= ''
    upper2 = ''
    shifted = {}
    
    for letter in lower:        
        letter = lower[(lower.index(letter) + shift) % len(lower)]
        lower2 += letter
    for letter in upper:
        letter = upper[(upper.index(letter) + shift) % len(upper)]
        upper2 += letter
        
    for letter in upper:
        shifted[letter] = upper2[upper.index(letter)]
    for letter in lower:
        shifted[letter] = lower2[lower.index(letter)]

    return shifted


def applyCoder(text, coder):
    """
    Applies the coder to the text. Returns the encoded text.

    text: string
    coder: dict with mappings of characters to shifted characters
    returns: text after mapping coder chars to original text
    """
    text2 = ''

    for letter in text:
        if letter in string.ascii_letters:
            letter = coder[letter]
            text2 += letter
        else:
            text2 += letter
    return text2


def applyShift(text, shift):
    """
    Given a text, returns a new text Caesar shifted by the given shift
    offset. Lower case letters should remain lower case, upper case
    letters should remain upper case, and all other punctuation should
    stay as it is.

    text: string to apply the shift to
    shift: amount to shift the text (0 <= int < 26)
    returns: text after being shifted by specified amount.
    """
    return applyCoder(text, buildCoder(shift))
    

#Decryption

def findBestShift(wordList, text):
    """
    Finds a shift key that can decrypt the encoded text.

    text: string
    returns: 0 <= int < 26
    """
    wordsFound = 0
    bestShift = 0

    for shift in range(0, 26):
        shifted = applyShift(text, shift).split(' ')
        for word in shifted:
            validWords = 0
            if isWord(wordList, word):
                validWords += 1
                if validWords >= wordsFound:
                    wordsFound = validWords
                    bestShift = shift
    return bestShift

def decryptStory():
    """
    returns: string - story in plain text
    """
    story = getStoryString()
    wordList = loadWords()
    bestShift = findBestShift(wordList, story)
    return applyShift(story, bestShift)
