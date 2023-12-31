# Jack Tokenizer


keyword = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false','null','this','let','do', 'if', 'else', 'while', 'return']
symbol = ['{', '}', '(', ')', '[', ']', '.', ',',';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']


class Tokenizer():
    def __init__(self, inputFile):
        self.inputFile = inputFile
        self.SYMBOL = ['{', '}', '(', ')', '[', ']', '.', ',',';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
        self.KEYWORD = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var', 'int', 'char', 'boolean', 'void', 'true', 'false','null','this','let','do', 'if', 'else', 'while', 'return']
        self.tokens = []
        self.currentToken = ''
        self.charStream = ''
        self.currentCharIdx = 0
        self.result = ['<tokens>']
        #self.currentTokenizedLine = ''

    def _read_input_file(self):
        with open(self.inputFile) as f:
            # process text file
            lines = f.readlines()
            for line in lines:
                line = line.strip()
                # Comments or empty line
                if line[0:2] == "/*" or line[0:2] == "\n" or line[0:2] == '//' or line == '' or line[0:2] == '*/' or line[0] == '*': 
                    pass
                else:
                    line = line.strip('\n')
                    line = line.strip('\t')
                    # inline comment
                    line = line.split("//")[0]
                    # Each character in line
                    for char in line:                        
                        self.charStream += char
    
    def outputting(self, outTokenizedFile):
        with open(outTokenizedFile, 'w') as f:
            for token in self.result:
                f.write(token + '\n')
        
    def hasMoreTokens(self):
        nchar = len(self.charStream)
        if self.currentCharIdx <= nchar - 1:
            return True
        else:
            return False
    
    # get the next token from the input and makes it
    # the current
    def advance(self):
        currentChar = self.charStream[self.currentCharIdx]

        if currentChar in self.SYMBOL:
            self.currentToken = currentChar
            self.tokens.append(currentChar)
            self.currentCharIdx += 1
        else:
            self.currentToken = ''
            # accumulate character until becomes a token
            #while ((currentChar not in self.SYMBOL) and (currentChar != ' ')):
            #while (currentChar != ' '):

            #    if (currentChar in self.SYMBOL) and self.currentToken[0] != '"':
            #        break

            if currentChar == '"':
                while True:
                    self.currentToken += currentChar
                    self.currentCharIdx += 1
                    currentChar = self.charStream[self.currentCharIdx]

                    if currentChar == '"':
                        self.currentToken += currentChar
                        self.currentCharIdx += 1
                        currentChar = self.charStream[self.currentCharIdx]
                        break

            else:

                while ((currentChar not in self.SYMBOL) and (currentChar != ' ')):

                    self.currentToken += currentChar
                    self.currentCharIdx += 1
                    currentChar = self.charStream[self.currentCharIdx]

                    # hit white space while in quotation

                    #if self.currentToken[0] == '"':
                    #    while (currentChar in self.SYMBOL) or currentChar == ' ':
                    #        self.currentToken += currentChar
                    #        self.currentCharIdx += 1
                    #        currentChar = self.charStream[self.currentCharIdx]

                    if self.currentToken[0] == '"' and currentChar == ' ':
                        self.currentToken += currentChar
                        self.currentCharIdx += 1
                        currentChar = self.charStream[self.currentCharIdx]
                    
                    if self.currentToken[0] == '"' and self.currentToken[-1] == '"' and len(self.currentToken) >= 2:
                        break

                    # hit symbol  while in quotation - safe to go
                    #if self.currentToken[0] == '"' and (currentChar in self.SYMBOL):
                    #    self.currentToken += currentChar
                    #    self.currentCharIdx += 1
                    #    currentChar = self.charStream[self.currentCharIdx]

                    #if self.currentToken[0] == '"' and currentChar == ' ':
                    #    self.currentToken += currentChar
                    #    self.currentCharIdx += 1
                    #    currentChar = self.charStream[self.currentCharIdx]

            # no appending since '' + " " shall not be accounted
            if self.currentToken != '':
                self.tokens.append(self.currentToken)

            if currentChar == ' ':
                self.currentCharIdx += 1


    # return the type of the current token
    def tokenType(self):
        if self.currentToken in self.KEYWORD:
            return 'KEYWORD'
        elif self.currentToken in self.SYMBOL:
            return 'SYMBOL'
        else:
            #print(self.currentToken)
            if self.currentToken[0] == '"' and self.currentToken[-1] == '"':
                return 'STRING_CONST'
            elif self.currentToken.isnumeric():
                return 'INT_CONST'
            else:
                return 'IDENTIFIER'

    # return the keyword of the current token call iff current token type is KEYWORD
    def keyWord(self):
        return self.currentToken

    # return the symbol of the current token call iff current token type is SYMBOL
    def symbol(self):
        if self.currentToken == '<':
            return '&lt;'
        elif self.currentToken == '>':
            return '&gt;'
        elif self.currentToken == '"':
            return '&quot;'
        elif self.currentToken == '&':
            return '&amp;'
        else:
            return self.currentToken

    # return the string of the current token call iff current token type is IDENTIFIER
    def identifier(self):

        return self.currentToken
    
    # return the integer value of the current token call iff current token type is INT_CONST
    def intVal(self):

        return int(self.currentToken)

    # return the string value of the current token call iff current token type is STRING_CONST
    def stringVal(self):

        return self.currentToken[1:-1] # strip quotation

    def run(self):

        self._read_input_file()
        while self.hasMoreTokens():
            self.advance()
            if self.currentToken == '':
                pass
            else:
                tokenType = self.tokenType()
                if tokenType == 'KEYWORD':
                    openBracket = '<keyword>'
                    content = self.keyWord()
                    closeBracket ='</keyword>'

                elif tokenType == 'SYMBOL':
                    openBracket = '<symbol>'
                    content = self.symbol()
                    closeBracket ='</symbol>'

                elif tokenType == 'IDENTIFIER':
                    openBracket = '<identifier>'
                    content = self.identifier()
                    closeBracket ='</identifier>'

                elif tokenType == 'INT_CONST':
                    openBracket = '<integerConstant>'
                    content = str(self.intVal())
                    closeBracket ='</integerConstant>'

                elif tokenType == 'STRING_CONST':
                    openBracket = '<stringConstant>'
                    content = self.stringVal()
                    closeBracket ='</stringConstant>'
                
                self.toPrint = openBracket +' ' + content +' '+ closeBracket

                self.result.append(self.toPrint)

                # Feed to compiler engine
                #self.currentTokenizedLine = self.toPrint

        self.result.append('</tokens>')


if __name__ == "__main__":
    import sys
    inputFile =sys.argv[1]

    tkn = Tokenizer(inputFile)
    tkn.run()
    #for token in tkn.result:
    #    print(token)
    with open('./Out.xml', 'w') as f:
        for token in tkn.result:
            f.write(token + '\n')
        