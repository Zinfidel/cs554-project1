class Production:
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def matches(self, character):
        pass

class Sigma(Production):
    def __init__(self, sigma):
        self.sigma = sigma

    def __str__(self):
        return str(self.sigma)

    def matches(self, character):
        return character == sigma

class Repetition(Production):
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return "* " + str(self.expr)

    def matches(self, string):
        print "matching " + string[0:1]
        if string == []:
            return true
        
        return self.expr.matches(string[0:1]) or self.matches(string[1:])

class Alternative(Production):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '| ' + str(self.left) + ' ' +  str(self.right)

    def matches(self, string):
        return self.left.matches(string) or \
               self.right.matches(string)

class Concatenation(Production):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return '+ ' + str(self.left) + ' ' + str(self.right)

    def matches(self, string):
        return self.left.matches(string[0:1]) and self.right.matches(string[1:])

class NilExpression(Production):
    def __str__(self):
        return ''

    def matches(self, string):
        return string == ''


if __name__ == "__main__":
    sigma = Sigma('a')
    r = Repetition(sigma)
    print r.matches('aaaaa')
    print r
