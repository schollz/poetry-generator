import datetime
import os
import random
import sys
import uuid
import binascii
import re

try:
    import en
except:
    print("DOWNLOD NODECUBE")
    print("""wget https://www.nodebox.net/code/data/media/linguistics.zip
unzip linguistics.zip""")

VERSION = "1.1"

class bnfDictionary:

    def __init__(self, file):
        self.grammar = {}
        numFeatures = 0
        with open("poems.bnf") as f:
            for line in f:
                lineSplit = line.split('=')
                self.grammar[lineSplit[0]] = []
                for syntax in lineSplit[1].split('|'):
                    self.grammar[lineSplit[0]].append(syntax)
                self.grammar[lineSplit[0]] = list(set(self.grammar[lineSplit[0]]))
                numFeatures += len(self.grammar[lineSplit[0]])
                # print(self.grammar[lineSplit[0]])
        print("Loaded " + str(numFeatures) + " features.")

    def generate(self, key, num):
        gram = self.grammar[key]
        i = random.randint(0, len(gram) - 1)
        string = ""
        if "<" not in gram[i]:
            string = gram[i]
        else:
            for word in gram[i].split():
                if "<" not in word:
                    string = string + word + " "
                else:
                    if "verb" in word:
                        if "pverb" in word:
                            v = self.generate("<pverb>", 1).strip()
                        else:
                            v = self.generate("<nverb>", 1).strip()
                        if random.randint(1,100) < 11:
                            v = self.generate("<theme-verb>",1).strip()
                        if "verb-inf" in word:
                            string = string + en.verb.present_participle(v) + " "
                        elif "verb-pr" in word:
                            string = string + en.verb.present(v, person=3, negate=False) + " "
                        elif "verb-past" in word:
                            string = string + en.verb.past(v) + " "
                        else:
                            string = string + v + " "
                    elif "noun" in word:
                        if "pnoun" in word:
                            v = self.generate("<pnoun>",1).strip()
                        else:
                            v = self.generate("<nnoun>",1).strip()
                        if random.randint(1,100) < 11:
                            v = self.generate("<theme-noun>",1).strip()
                        if "pl" in word:
                            v = en.noun.plural(v)
                        string = string + v + " "
                    elif "person" in word:
                        v = self.generate("<person>",1).strip()
                        if "pl" in word:
                            v = en.noun.plural(v)
                        string = string + v + " "
                    elif "adj" in word:
                        if random.randint(1,100) < 11:
                            v = self.generate("<theme-adj>",1).strip()
                        else:
                            v = self.generate(word,1).strip()
                        string = string + v + " "
                    elif "fruit" in word:
                        v = self.generate("<fruit>",1).strip()
                        if "pl" in word:
                            v = en.noun.plural(v)
                        string = string + self.generate(word, 1) + " "
                    else:
                        string = string + self.generate(word, 1) + " "
        return string.replace('newline', '')

    def generatePretty(self, key):
        #tool = language_check.LanguageTool('en-US')
        poem = self.generate(key, 1)
        poem = poem.replace(" ,",",")
        puncuation = [".",".",".",".","!","?"]
        dontbreaks = ["of","behind","the","when","what","why","who",",","your","by","like","to","you","your","a","are","become"]
        capitalize = False
        breaks = 0
        poem2 = []
        foundFirstBreak = False
        for word in poem.replace("\n","zbreak").split():
            poem2.append(word.lower())
            if random.randint(1,100) < 7 and "zbreak" not in word and foundFirstBreak:
                poem2.append("zbreak")
            if "zbreak" in word:
                foundFirstBreak = True

        poem3 = []
        beforeFirstBreak = True
        for word in poem2:
            if "zbreak" in word:
                breaks +=1
                beforeFirstBreak = False
            else:
                breaks = 0
            if beforeFirstBreak or word=="i" or "i'" in word:
                word = word.capitalize()
                poem3.append(word)
                capitalize = False
            else:
                if breaks > 1:
                    capitalize = True
                if capitalize == True and "zbreak" not in word:
                    word = word.capitalize()
                    capitalize = False
                for punc in list(set(puncuation)):
                    if punc in word:
                        capitalize = True
                poem3.append(word)
                if random.randint(1,100) < 0 and "zbreak" not in word:
                    isgood = True
                    for dontbreak in list(dontbreaks+puncuation):
                        if dontbreak == word.lower():
                            isgood = False
                    if isgood:
                        poem3.append(random.choice(puncuation))
                        capitalize = True
        noPunc = True
        for punc in list(set(puncuation)):
            if punc in word:
                noPunc = False
        if noPunc:
            poem3.append(random.choice(puncuation))

        newPoem = " ".join(poem3)
        newPoem = newPoem.replace(" a a"," an a")
        newPoem = newPoem.replace("zbreak","\n")
        newPoem = newPoem.replace(" \n \n","\n\n")
        newPoem = newPoem.replace("\n \n ","\n\n")
        newPoem = newPoem.replace("\n\n",".\n\n")
        newPoem = newPoem.replace(" '","'")
        for punc in list(set(puncuation)):
            newPoem = newPoem.replace(" " + punc,punc)
        for punc in list(set(puncuation)):
            newPoem = newPoem.replace(" " + punc,punc)
        for punc in list(set(puncuation)):
            newPoem = newPoem.replace(" " + punc,punc)
        newPoem = newPoem.replace(" ,",",")
        newPoem = newPoem.replace("?.","?")
        newPoem = newPoem.replace(".?",".")
        newPoem = newPoem.replace(",.",",")
        newPoem = newPoem.replace("!.","!")
        newPoem = newPoem.replace("..",".")
        newPoem = newPoem.replace("..",".")
        newPoem = newPoem.replace("..",".")
        title = newPoem.split("\n")[0]
        newTitle = title.replace(".","")
        newPoem = newPoem.replace(title,newTitle)
        #
        # capitalize = True
        # isTitle = True
        # isParagraph = False
        # newPoem = ""
        # lines = poem.splitlines()
        # lines.append('\n')
        # for line in lines:
        #     line = line.rstrip().lstrip()
        #     line = line.replace(' ,', ',')
        #     line = line.replace(' ?', '?')
        #     line = line.replace(' !', '!')
        #     line = line.replace(' .', '.')
        #     line = line.replace(' :', ':')
        #     line = line.replace(' \'', '\'')
        #     if capitalize:
        #         line = line.capitalize()
        #         capitalize = False
        #     if isTitle:
        #         mydate = datetime.datetime.fromtimestamp(0)
        #
        #         newPoem = newPoem + "<h1>" + line + \
        #             "</h1>\n<h2>by A Computer, %s</h2>\n" % mydate.strftime(
        #                 "%B %d %Y")
        #         isTitle = False
        #     else:
        #         if len(line) < 1:
        #             if isParagraph:
        #                 newPoem = newPoem + "</p>"
        #             isParagraph = False
        #         else:
        #             if not isParagraph:
        #                 newPoem = newPoem + "\n\n<p>"
        #                 line = line.capitalize()
        #             isParagraph = True
        #             newPoem = newPoem + line + "<break>"
        #         if "." in line or "!" in line or "?" in line or "!" in line:
        #             capitalize = True
        # newPoem = newPoem.replace('<break><break>', '<break>')
        # newPoem = newPoem.replace('<break></p>', '</p>')
        # newPoem = newPoem.replace('<break>', '<br />\n')
        # lines = newPoem.splitlines()
        # newPoem = ""
        # isParagraph = False
        # capitalize = False
        # for line in lines:
        #     if capitalize:
        #         line = line.capitalize()
        #         capitalize = False
        #     if "</p>" in line:
        #         isParagraph = False
        #         lastChar = line.rsplit('</p>', 1)[0][-1]
        #         if "." in lastChar or "-" in lastChar or "," in lastChar or "!" in lastChar or "?" in lastChar or "!" in lastChar:
        #             newPoem = newPoem + line + "\n"
        #         else:
        #             newPoem = newPoem + line.replace('</p>', '.</p>\n')
        #     elif "<p>" in line:
        #         isParagraph = True
        #         newPoem = newPoem + line + "\n"
        #     else:
        #         if isParagraph:
        #             lastChar = line.rsplit('<br />', 1)[0][-1]
        #             if "." in lastChar or "-" in lastChar or "," in lastChar or "!" in lastChar or "?" in lastChar or "!" in lastChar:
        #                 pass
        #             else:
        #                 if random.randint(0, 20) < 2:
        #                     newPoem = newPoem + \
        #                         line.replace('<br />', '?<br />\n')
        #                     capitalize = True
        #                 elif random.randint(0, 20) < 14:
        #                     newPoem = newPoem + \
        #                         line.replace('<br />', '.<br />\n')
        #                     capitalize = True
        #                 elif random.randint(0, 20) < 2:
        #                     newPoem = newPoem + \
        #                         line.replace('<br />', '!<br />\n')
        #                     capitalize = True
        #                 elif random.randint(0, 20) < 2:
        #                     newPoem = newPoem + \
        #                         line.replace('<br />', ',<br />\n')
        #                 else:
        #                     newPoem = newPoem + line + "\n"
        #         else:
        #             newPoem = newPoem + line + "\n"
        # newPoem = newPoem.replace('..', '.')
        # newPoem = newPoem.replace('?.', '!')
        # newPoem = newPoem.replace('!.', '?')
        # newPoem = newPoem.replace(' i ', ' I ')
        return newPoem

bnf = bnfDictionary('poems.bnf')


def generate_poem(poemtype, hex_seed=None):
    if hex_seed == None:
        hex_seed = str(uuid.uuid4()).split("-")[0]

    random.seed(int(binascii.hexlify(hex_seed.encode()), 16))

    return (
        bnf.generatePretty('<' + poemtype + '>')
        + '\n<h2>/' + poemtype + '/' + hex_seed + '</h2>'
    )

if __name__ == '__main__':
    poemtype = 'poem'
    if 'mushy' in sys.argv[1:]:
        poemtype = 'mushypoem'
    print(re.sub("<.*?>", " ",generate_poem(poemtype)))
