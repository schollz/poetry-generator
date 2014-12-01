from random import randint
import sys
import datetime
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
		capitalize = True
		isTitle = True
		isParagraph = False
		newPoem = ""
		lines = poem.splitlines()
		lines.append('\n')
		for line in lines:
			line = line.rstrip().lstrip()
			line = line.replace(' ,',',')
			line = line.replace(' ?','?')
			line = line.replace(' !','!')
			line = line.replace(' .','.')
			line = line.replace(' :',':')
			line = line.replace(' \'','\'')
			if capitalize:
				line = line.capitalize()
				capitalize = False
			if isTitle:
				mydate = datetime.datetime.now()
				
				newPoem = newPoem + "<h1>" + line + "</h1>\n<h2>by A Computer, %s</h2>\n"%mydate.strftime("%B %d %Y")
				isTitle = False
			else:
				if len(line) < 1:	
					if isParagraph:
						newPoem = newPoem + "</p>"
					isParagraph = False
				else:
					if not isParagraph:
						newPoem = newPoem + "\n\n<p>"
						line = line.capitalize()
					isParagraph = True
					newPoem = newPoem + line + "<break>"
				if "." in line or "!" in line or "?" in line or "!" in line:
					capitalize = True
		newPoem = newPoem.replace('<break><break>','<break>')
		newPoem = newPoem.replace('<break></p>','</p>')
		newPoem = newPoem.replace('<break>','<br />\n')
		lines = newPoem.splitlines()
		newPoem = ""
		isParagraph = False
		capitalize = False
		for line in lines:
			if capitalize:
				line = line.capitalize()
				capitalize = False
			if "</p>" in line:
				isParagraph = False
				lastChar = line.rsplit('</p>',1)[0][-1]
				if "." in lastChar or "-" in lastChar  or "," in lastChar or "!" in lastChar or "?" in lastChar or "!" in lastChar:
					newPoem = newPoem + line + "\n"
				else:
					newPoem = newPoem + line.replace('</p>','.</p>\n')
			elif "<p>" in line:
				isParagraph = True
				newPoem = newPoem + line + "\n"
			else:
				if isParagraph:
					lastChar = line.rsplit('<br />',1)[0][-1]
					if "." in lastChar or "-" in lastChar or "," in lastChar or "!" in lastChar or "?" in lastChar or "!" in lastChar:
						pass
					else:
						if randint(0,20)<2:
							newPoem = newPoem + line.replace('<br />','?<br />\n')
							capitalize = True
						elif randint(0,20)<2:
							newPoem = newPoem + line.replace('<br />','.<br />\n')
							capitalize = True
						elif randint(0,20)<2:
							newPoem = newPoem + line.replace('<br />','!<br />\n')
							capitalize = True
						elif randint(0,20)<2:
							newPoem = newPoem + line.replace('<br />',',<br />\n')
						else:
							newPoem = newPoem + line + "\n"				
				else:
					newPoem = newPoem + line + "\n"
		newPoem = newPoem.replace('..','.')
		newPoem = newPoem.replace('?.','!')
		newPoem = newPoem.replace('!.','?')
		newPoem = newPoem.replace(' i ',' I ')
		return newPoem
	
bnf = bnfDictionary('poems.bnf')
if "mushy" in sys.argv[1]:
	print(bnf.generatePretty('<mushypoem>'))
else:
	print(bnf.generatePretty('<poem>'))


