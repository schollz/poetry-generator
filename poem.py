import datetime
import os
import random
import sys
import uuid
import base64
import yaml
import re

try:
    import en
except:
    print("DOWNLOD NODECUBE")
    print("""wget https://www.nodebox.net/code/data/media/linguistics.zip
unzip linguistics.zip""")

VERSION = "1.1"

THEME_PROB = 0


class bnfDictionary:

    def __init__(self, file):
        self.grammar = yaml.load(open(file,'r'))
        self.poemtype = "<poem>"

    def generate(self, key, num):
        gram = self.grammar[key]
        if len(gram)==1:
            i = 0
        else:
            i = random.randint(0, len(gram) - 1)
        string = ""
        if "<" not in gram[i]:
            string = gram[i]
        else:
            for word in gram[i].split():
                if "<" not in word:
                    string = string + word + " "
                else:
                    if "verb" in word and word != '<adverb>':
                        if "pverb" in word or "mushy" in self.poemtype:
                            v = self.generate("<pverb>", 1).strip()
                        elif "nverb" in word:
                            v = self.generate("<nverb>", 1).strip()
                        # else:
                        #     v = self.generate("<verb>", 1).strip()
                        if random.randint(1, 100) < THEME_PROB:
                            v = self.generate("<theme-verb>", 1).strip()
                        if "verb-inf" in word:
                            string = string + \
                                en.verb.present_participle(v) + " "
                        elif "verb-pr" in word:
                            string = string + \
                                en.verb.present(
                                    v, person=3, negate=False) + " "
                        elif "verb-past" in word:
                            string = string + en.verb.past(v) + " "
                        else:
                            string = string + v + " "
                    elif "noun" in word:
                        if "pnoun" in word or "mushy" in self.poemtype:
                            v = self.generate("<pnoun>", 1).strip()
                        elif "nnoun" in word:
                            v = self.generate("<nnoun>", 1).strip()
                        else:
                            v = self.generate("<noun>", 1).strip()
                        if random.randint(1, 100) < THEME_PROB:
                            v = self.generate("<theme-noun>", 1).strip()
                        if "pl" in word:
                            v = en.noun.plural(v)
                        string = string + v + " "
                    elif "person" in word:
                        v = self.generate("<person>", 1).strip()
                        if "pl" in word:
                            v = en.noun.plural(v)
                        string = string + v + " "
                    elif "adj" in word:
                        if "mushy" in self.poemtype:
                            v = self.generate("<padj>",1)
                        else:
                            if random.randint(1, 100) < THEME_PROB:
                                v = self.generate("<theme-adj>", 1).strip()
                            else:
                                v = self.generate(word, 1).strip()
                        string = string + v + " "
                    elif "fruit" in word:
                        v = self.generate("<fruit>", 1).strip()
                        if "pl" in word:
                            v = en.noun.plural(v)
                        string = string + self.generate(word, 1) + " "
                    elif "person" in word:
                        v = self.generate("<fruit>", 1).strip()
                        if "pl" in word:
                            v = en.noun.plural(v)
                        string = string + self.generate(word, 1) + " "
                    else:
                        if "-pl" in word:
                            v = en.noun.plural(self.generate(word.replace("-pl",""),1))
                        else:
                            v = self.generate(word, 1)
                        string = string + v + " "
        return string

    def generatePretty(self, key, seed_str):
        if seed_str == None:
            seed_str = str(uuid.uuid4()).split("-")[0]

        random.seed(uuid.uuid5(uuid.NAMESPACE_DNS,seed_str).int)
        #tool = language_check.LanguageTool('en-US')
        self.poemtype = key
        if key == "<mushypoem>":
            key = "<poem>"
        poem = self.generate(key, 1)
        poem = poem.replace(" ,", ",")
        puncuation = [".", ".", ".", ".", "!", "?"]
        dontbreaks = ["of", "behind", "the", "when", "what", "why", "who", ",",
                      "your", "by", "like", "to", "you", "your", "a", "are", "become", "newline"]
        capitalize = False
        breaks = 0
        poem2 = []
        foundFirstBreak = False
        for word in poem.replace("\n", "newline").split():
            poem2.append(word.lower())
            if random.randint(1, 100) < 2 and "newline" not in word and foundFirstBreak:
                isgood = True
                for dontbreak in list(dontbreaks + puncuation):
                    if dontbreak == word.lower():
                        isgood = False
                if isgood:
                    poem2.append("newline")
            if "newline" in word:
                foundFirstBreak = True

        poem3 = []
        beforeFirstBreak = True
        for word in poem2:
            if "newline" in word:
                breaks += 1
                beforeFirstBreak = False
            else:
                breaks = 0
            if beforeFirstBreak or word == "i" or "i'" in word:
                word = word.capitalize()
                poem3.append(word)
                capitalize = False
            else:
                if breaks > 1:
                    capitalize = True
                if capitalize == True and "newline" not in word:
                    word = word.capitalize()
                    capitalize = False
                for punc in list(set(puncuation)):
                    if punc in word:
                        capitalize = True
                poem3.append(word)
                if random.randint(1, 100) < 0 and "newline" not in word:
                    isgood = True
                    for dontbreak in list(dontbreaks + puncuation):
                        if dontbreak == word.lower():
                            isgood = False
                    if isgood:
                        poem3.append(random.choice(puncuation))
                        capitalize = True
        # noPunc = True
        # for punc in list(set(puncuation)):
        #     if punc in word:
        #         noPunc = False
        # if noPunc:
        #     poem3.append(random.choice(puncuation))

        newPoem = " ".join(poem3)

        newPoem = newPoem.replace(" a a", " an a")
        newPoem = newPoem.replace("newline .", ". newline")
        newPoem = newPoem.replace("newline ?", "? newline")
        newPoem = newPoem.replace("newline !", "! newline")
        newPoem = newPoem.replace("newline ,", ", newline")
        newPoem = newPoem.replace("newline", "\n")
        newPoem = newPoem.replace(" \n \n", "\n\n")
        newPoem = newPoem.replace("\n \n ", "\n\n")
        newPoem = newPoem.replace(" '", "'")
        for punc in list(set(puncuation)):
            newPoem = newPoem.replace(" " + punc, punc)
        for punc in list(set(puncuation)):
            newPoem = newPoem.replace(" " + punc, punc)
        for punc in list(set(puncuation)):
            newPoem = newPoem.replace(" " + punc, punc)
        newPoem = newPoem.replace(" ,", ",")
        newPoem = newPoem.replace("?.", "?")
        newPoem = newPoem.replace(".?", ".")
        newPoem = newPoem.replace(",.", ",")
        newPoem = newPoem.replace("!.", "!")
        newPoem = newPoem.replace("..", ".")
        newPoem = newPoem.replace("..", ".")
        newPoem = newPoem.replace("..", ".")
        title = newPoem.split("\n")[0]
        newTitle = title.replace(".", "")
        newPoem = newPoem.replace(title, "<h1>" + newTitle + "</h1>")
        newPoem2 = ""
        firstLine = False
        secondLine = False
        for line in newPoem.split("\n"):
            if len(line) > 0:
                if firstLine and not secondLine:
                    newPoem2 = newPoem2 + "<p>\n"
                    secondLine = True
                if firstLine == False:
                    firstLine = True
                    newPoem2 = newPoem2 + line + " \n"
                if firstLine and secondLine:
                    newPoem2 = newPoem2 + line + " <br />\n"
            else:
                newPoem2 = newPoem2 + " <br />\n"
        newPoem2 = newPoem2 + "</p>"
        return newPoem2,seed_str

bnf = bnfDictionary('brain.yaml')


def generate_poem(poemtype, hex_seed=None):
    p,seed_str = bnf.generatePretty('<' + poemtype + '>',hex_seed)
    return p,seed_str

if __name__ == '__main__':
    poemtype = 'poem'
    if 'mushy' in sys.argv[1:]:
        poemtype = 'mushypoem'
    p,seed_str=generate_poem(poemtype)
    print("*"*30 + "\n"*5)
    filtered = []
    for line in re.sub("<.*?>", " ", p).split("\n"):
        if len(line.strip()) > 0:
            filtered.append(line.strip())
        else:
            filtered.append("pause")
    print(p)
