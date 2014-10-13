class Production:
    '''
    Defines the base class that all Regex inherit from. 
    '''
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def matches(self, string):
        pass

    def consume(self, string):
        i = 0
        while self.matches(string[0:(i+1)]) and i <= len(string):
            i += 1

        if i == 0:
            return '', string
        else:
            return string[0:i], string[i:]


class Sigma(Production):
    def __init__(self, sigma):
        self.sigma = sigma

    def __str__(self):
        return str(self.sigma)

    def matches(self, string):
        return self.sigma == string

    def consume(self, string):
        if len(string) >= 1 and string[0] == self.sigma:
            return string[0:1], string[1:]
        else:
            return '', string

class Repetition(Production):
    def __init__(self, expr):
        self.expr = expr
    
    def __str__(self):
        return "* " + str(self.expr)

    def matches(self, string):
        if string == '':
            return True

        return self.expr.matches(string[0:1]) and self.matches(string[1:])

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
    
    def consume(self, string):
        left_match, leftover = self.left.consume(string)
        right_match, leftover = self.right.consume(leftover)

        if left_match == '' or right_match == '':
            return '', string
 
        left_match += right_match

        return ''.join(left_match), leftover

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
    print a.consume('a')
    print a.consume('b')
    print 

    r = Repetition(a)
    print r
    print r.matches('aaaaa')
    print r.consume('aaaaab')
    print 

    b = Sigma('b')
    a = Alternative(b, r)
    print a
    print a.matches('b')
    print a.matches('aaaa')
    print a.matches('c')
    print a.consume('aaaaabaaa')
    print a.consume('dasdf')
    print 

    c = Concatenation(b, a)
    print c
    print c.matches('ba')
    print c.matches('ab')
    print c.matches('baa')
    print c.consume('baba')
    print c.consume('bsa')

