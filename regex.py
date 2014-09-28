class Production:
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def matches(self, character):
        return character in alphabet
        

class Alphabet(Regex):
    def __init__(self, sigma):
        
    def __repr__(
        

class Alternative(Regex):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '| ' + str(self.left) + ' ' +  str(self.right)

    def matches(self, string):
        return self.left.matches(string) or \
               self.right.matches(string)

class Concatenation(Regex):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return '+ ' + str(self.left) + ' ' + str(self.right)

    def matches(self, string):
        return 

class NilExpression(Regex):
    def __str__(self):
        return ''

    def matches(self, string):
        return string == ''


if __name__ == "__main__":
    print '' == ''
