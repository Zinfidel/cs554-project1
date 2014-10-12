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
        return character == self.sigma

class Repetition(Production):
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return "* " + str(self.expr)

    def matches(self, string):

        if string == '':
            return True

        return self.expr.matches(string[0:1]) or self.expr.matches(string[1:])

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


def BuildExpression(tokens):
    """Builds an expression from a list of tokens using a one token look ahead
       strategy.

       tokens: Expected to be a list of string tokens (ie: ['+', 'a', 'a'])
    """
    t = tokens[0]

    # E -> + E E
    if t == '+':
        # TODO: Clean this up
        #        return BuildConcatenation(tokens[1:])a
        # build the appropriate expression for the left argument to the concat
        # operation and return the leftover tokens
        leftSide, leftover = BuildExpression(tokens[1:])

        # Make sure we have tokens to consume, otherwise an error
        if len(leftover) == 0:
            raise Error('''No more tokens found after building the left hand side of
                           a ConcatExpression''')
        # Build the right hand side of the ConcatExpression
        rightSide, leftover = BuildExpression(leftover)
        return Concatenation(leftSide, rightSide), leftover
    # E -> | E E
    elif t == '|':

        leftSide, leftover = BuildExpression(tokens[1:])

        # Make sure we have tokens to consume, otherwise an error
        if len(leftover) == 0:
            raise Error('''No more tokens found after building the left hand side of
                           a ConcatExpression''')

        rightSide, leftover = BuildExpression(leftover)
        return Alternative(leftSide, rightSide), leftover
    # E -> * E
    elif t == '*':
        e, leftover = BuildExpression(tokens[1:])
        return Repetition(e), leftover
    # E -> _ (empty, not underscore)
    elif t == '':
        return NilExpression(), tokens[1:]
    # E -> sigma (where sigma is some symbol that doesn't match the previous
    # values
    else:
        return Sigma(t), tokens[1:]


if __name__ == "__main__":
    a = Sigma('a')
    print a
    print a.matches('a')
    print 

    r = Repetition(a)
    print r
    print r.matches('aaaaa')
    print

    b = Sigma('b')
    a = Alternative(b, r)
    print a
    print a.matches('b')
    print a.matches('aaaa')
    print a.matches('c')
    print 

    c = Concatenation(b, a)
    print c
    print c.matches('ba')
    print c.matches('ab')
    print c.matches('baa')
