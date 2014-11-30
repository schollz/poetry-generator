from random import randint
import sys
#import language_check

class bnfDictionary:

	def __init__(self,file):
		self.grammar = {}
		with open("poems.bnf") as f:
			for line in f:
				lineSplit = line.split('=')
				self.grammar[lineSplit[0]] = []
				for syntax in lineSplit[1].split('|'):
					self.grammar[lineSplit[0]].append(syntax)
				#print(self.grammar[lineSplit[0]])
				
	def generate(self,key,num):
		gram = self.grammar[key]
		i = randint(0,len(gram)-1)
		string = ""
		if "<" not in gram[i]:
			string = gram[i]
		else:
			for word in gram[i].split():
				if "<" not in word:
					string = string + word + " "
				else:
					string = string + self.generate(word,1) + " "
		return string.replace('newline','')
		
	def generatePretty(self,key):
		#tool = language_check.LanguageTool('en-US')
		poem = self.generate(key,1)
		capitalize = False
		newPoem = ""
		firstLine = True
		lastLineWasText = False
		lastLineWasFirst = False
		for line in poem.splitlines():
			line = line.rstrip()
			line = line.replace(' ,',',')
			line = line.replace(' !','!')
			line = line.replace(' ?','?')
			line = line.replace(' i ',' I ')
			line = line.replace(' \'','\'')
			#matches = tool.check(line)
			#print(language_check.correct(line, matches))
			if len(line)>1:
				if " " in line[0]:
					line = line[1:]
				if capitalize:
					capitalize = False
					line = line.capitalize()
				if not firstLine and "." not in line[-1] and "-" not in line[-1] and "!" not in line[-1] and "," not in line[-1] and "?" not in line[-1]:
					if randint(0,9) < 3 and "the" not in line[-3:]:
						line = line + "."
						capitalize = True
				else:
					capitalize = True
				if firstLine:
					line = "<h2>" + line + "</h2>"
					firstLine = False
					lastLineWasFirst = True
					newPoem = newPoem + line
				else:	
					newPoem = newPoem + "<br>" + line
				lastLineWasText = True
			else:
				if lastLineWasText and not lastLineWasFirst and "!" not in newPoem[-1] and "-" not in newPoem[-1] and "." not in newPoem[-1] and "," not in newPoem[-1] and "?" not in newPoem[-1]:
					newPoem = newPoem + ".<br>" + line
					capitalize = True
					lastLineWasText = False
				else:
					if lastLineWasFirst:
						newPoem = newPoem + line
					else:
						newPoem = newPoem + "<br>" + line
					capitalize = True
					lastLineWasFirst = False
		if "!" not in newPoem[-1] and "-" not in newPoem[-1] and "." not in newPoem[-1] and "," not in newPoem[-1] and "?" not in newPoem[-1]:
			return newPoem + "."
		else:
			return newPoem
		
bnf = bnfDictionary('poems.bnf')
if "mushy" in sys.argv[1]:
	print(bnf.generatePretty('<mushypoem>'))
else:
	print(bnf.generatePretty('<poem>'))


