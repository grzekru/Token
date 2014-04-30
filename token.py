# -*- coding: utf-8 -*-

import codecs
import re
#import morfeusz

class token(object):

	def __init__(self):
		self.text = None
		self.settings = []
		self.sep = None
		self.tokens = []
		self.ignore = []
		self.trim = False
		self.white = ['\n','\r','\t',' ']
		self.separator = False
		self.noWhite = False
		self.tokenWithSep = False
		self.minLen = None
		self.maxLen = None
		self.morf = False
		self.input = "raw.txt"
		self.outfile = None
		self.outText = ""
		self.sepexc = []
		#####################################
		self.loadSettings()
		self.applySettings()
		self.loadText()
		self.tokenize()
		if (self.tokenWithSep == True):
			self.conn()
		if (len(self.sepexc)>0):
			self.includeExc()
		self.output()
		if (self.outfile!=None):
			self.saveToFile()

	def loadText(self):
		rawFile = codecs.open(self.input,"r","utf-8")
		self.text = rawFile.read()

	def loadSettings(self):
		settingsFile = codecs.open("settings.txt","r","utf-8")
		self.settings = settingsFile.read().split('\n')

	def applySettings(self):
		for row in self.settings:

			rule = row[0:row.find("=")+1]
			value = row[row.find("=")+1:]

			if (len(value)>0 and (value[-1]=='\n' or value[-1]=='\r')):
				value = value[0:-1]

			if (row.startswith("!token=")):

				if (value=="word"):
					separ = "[^\w\dąęćżźłńóĄĘĆŻŹŁŃÓ—-]"
					if (self.sep == None):
						self.sep = separ
					else:
						self.sep = self.sep + "|" + separ
					#self.ignore.append("")
					#self.ignore.append("—");
				elif (value=="sentence"):
					separ = "[\.|…|?|!]"
					if (self.sep == None):
						self.sep = separ
					else:
						self.sep = self.sep + "|" + separ
					#self.ignore.append("")
					#self.trim = True
					#self.connect = True

			if (row.startswith("!sep=")):
				if (self.sep == None):
					self.sep = value
				else:
					self.sep = self.sep + "|" + value

			if (row.startswith("!ignore=")):
				self.ignore.append(value)

			if (row.startswith("!separator")):
				self.separator = True

			if (row.startswith("!ignWhiteChars")):
				self.noWhite = True

			if (row.startswith("!trim")):
				self.trim = True

			if (row.startswith("!tokenWithSep")):
				self.tokenWithSep = True

			if (row.startswith("!minLen")):
				self.minLen = int(value)

			if (row.startswith("!maxLen")):
				self.maxLen = int(value)

			if (row.startswith("!morf")):
				self.morf = True

			if (row.startswith("!input")):
				self.input = value

			if (row.startswith("!output")):
				self.outfile = value

			if (row.startswith("!sepexc")):
				self.sepexc.append(value)

		if (self.separator == True):
			self.sep = "(" + self.sep + ")"

	def tokenize(self):
		if (self.sep == None):
			self.tokens.append(self.text)
		else:
			tok = re.split(self.sep,self.text)
			for t in tok:
				self.tokens.append(t)

	def output(self):
		id = 0;
		for token in self.tokens:
			if (self.noWhite == True):
				if (self.cut(token)==""):
					continue

			if (self.trim == True):
				token = self.cut(token)

			if (token in self.ignore):
				continue

			if (self.minLen != None):
				if (len(token)<self.minLen):
					continue

			if (self.maxLen != None):
				if (len(token)>self.maxLen):
					continue

			id = id + 1
			wynik = "TOKEN " + str(id) + ": " + token

			#if (self.morf == True):
				#wynik += " MORF:" + str(morfeusz.analyse(token)[0])

			print(wynik + '\n')
			self.outText += wynik + '\n'


			#print "TOKEN " + str(id) + ": " + token# + " " + str(morfeusz.analyse(token)[0])

	def cut(self,stri):
		while (len(stri)>0):
			if (stri[0] in self.white):
				stri = stri[1:]
			else:
				break
		while (len(stri)>0):
			if (stri[-1] in self.white):
				stri = stri[:-1]
			else:
				break
		return stri

	def conn(self):
		wykonuj = True
		start = 0
		while (wykonuj == True):
			wykonuj = False
			for i in range(start,len(self.tokens)):
				m = re.search("([\.|…|?|!])",self.tokens[i])
				if m:
					if (len(self.tokens[i])==len(m.groups()[0])):
						start = i-1
						self.tokens[i-1] = self.tokens[i-1] + self.tokens[i]
						del self.tokens[i]
						wykonuj = True
						break

	def saveToFile(self):
		f = open(self.outfile,'w')
		f.write(self.outText)
		f.close

	def includeExc(self):
		breakFlag = False
		wykonuj = True
		start = 0
		while (wykonuj == True):
			wykonuj = False
			for i in range(start,len(self.tokens)-1):
				for exc in self.sepexc:
					m = re.search(exc,self.tokens[i]+self.tokens[i+1])
					if m:
						if (m.end()>=len(self.tokens[i])):
							start=i
							wykonuj = True
							self.tokens[i] += self.tokens[i+1]
							del self.tokens[i+1]
							breakFlag = True
							breakFlag
				if (breakFlag == True):
					breakFlag = False
					break

if __name__ == '__main__':
	token()
