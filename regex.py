# -*- coding: utf-8 -*-

class Production:
    '''
    Defines the base class that all Regex inherit from. 
    '''
    def __init__(self, alphabet):
        self.alphabet = alphabet

    def matches(self, string):
        pass

    def consume(self, string):
        pass


class Sigma(Production):
    def __init__(self, sigma):
        self.sigma = sigma

    def __str__(self):
        return str(self.sigma)

    def __repr__(self):
        return str(self.sigma)

    def __eq__(self, other):
        return isinstance(other, Sigma) and (self.sigma == other.sigma)

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

    def __eq__(self, other):
        return isinstance(other, Repetition) and (self.expr == other.expr)

    def matches(self, string):
        if string == '':
            return True

        return self.expr.matches(string[0:1]) and self.matches(string[1:])
        
    def consume(self, string):
        consumed = 'default'
        total_consumed = ''
        leftover = string

        while consumed != '':
            consumed, leftover = self.expr.consume(leftover)
            total_consumed += consumed

        return total_consumed, leftover
        

class Alternative(Production):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '| ' + str(self.left) + ' ' +  str(self.right)

    def __eq__(self, other):
        return isinstance(other, Alternative) and (self.left == other.left) \
                                              and (self.right == other.right)
                                                   
    def matches(self, string):
        return self.left.matches(string) or \
               self.right.matches(string)

    def consume(self, string):
        left_consume, leftover = self.left.consume(string)
        # he he he. rightover.... I crack myself up.
        right_consume, rightover = self.right.consume(string)

        # This could be a potential problem due to there
        # being multiple parses include the left or right
        # side... We'll go with the longer parse for now
        if len(left_consume) >= len(right_consume):
            return left_consume, leftover
        else:
            return right_consume, rightover
            

class Concatenation(Production):
    def __init__(self, left, right):
        self.left = left
        self.right = right
    
    def __str__(self):
        return '+ ' + str(self.left) + ' ' + str(self.right)

    def __eq__(self, other):
        return isinstance(other, Concatenation) and (self.left == other.left)\
                                                and (self.right == other.right)

    def matches(self, string):
        return self.left.matches(string[0:1]) and self.right.matches(string[1:])
    
    def consume(self, string):
        left_match, leftover = self.left.consume(string)
        right_match, leftover = self.right.consume(leftover)

        if left_match == '':
            return '', string
 
        left_match += right_match

        return ''.join(left_match), leftover

class NilExpression(Production):
    def __str__(self):
        # return ''
        return 'ε'

    def __repr__(self):
        return 'ε'

    def __eq__(self, other):
        return isinstance(other, NilExpression)

    def matches(self, string):
        return string == ''

    def consume(self, string):
        return '', string


class Empty(Production):
    def __str__(self):
        return '∅'

    def __repr__(self):
        return '∅'

    def __eq__(self, other):
        return isinstance(other, Empty)

    def matches(self, string):
        return False

    def consume(self, string):
        return None, string


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
        #these value are quoted so we must remove the quote
        return Sigma(t[1:]), tokens[1:]


def __simplify(re):
    """ Runs one pass through a regex tree and simplifies it.

        :param Production re: The regex tree to simplify (once).
        :rtype: Production
    """
    # ALTERNATIVE
    if isinstance(re, Alternative):
        # Union (e, f) when e = f -> e
        if re.left == re.right:
            return re.left

        # Union (Union (e, f), g) -> simple (Union (e, Union (f, g)))
        elif isinstance(re.left, Alternative):
            e, f, g = re.left.left, re.left.right, re.right
            return __simplify(Alternative(e, Alternative(f, g)))

        # Union (Empty, e) -> e
        elif isinstance(re.left, Empty):
            return re.right

        # Union (e, Empty) -> e
        elif isinstance(re.right, Empty):
            return re.left

        # Union (e, f) -> Union (e, f)
        else:
            return Alternative(__simplify(re.left), __simplify(re.right))

    # CONCATENATION
    elif isinstance(re, Concatenation):
        # Concat (Concat (e, f), g) -> simple (Concat (e, Concat (f, g)))
        if isinstance(re.left, Concatenation):
            e, f, g = re.left.left, re.left.right, re.right
            return __simplify(Concatenation(e, Concatenation(f, g)))

        # Concat (Epsilon, e) -> simple e
        elif isinstance(re.left, NilExpression):
            return __simplify(re.right)

        # Concat (e, Epsilon) -> simple e
        elif isinstance(re.right, NilExpression):
            return __simplify(re.left)

        # Concat (Empty, e) | Concat(e, Empty) -> Empty
        elif isinstance(re.left, Empty) or isinstance(re.right, Empty):
            return Empty([])

        # Concat (e, f) -> Concat (e, f)
        else:
            return Concatenation(__simplify(re.left), __simplify(re.right))

    # REPETITION
    elif isinstance(re, Repetition):
        # Star Empty -> Epsilon
        if isinstance(re.expr, Empty):
            return NilExpression([])

        # Star Epsilon -> Epsilon
        elif isinstance(re.expr, NilExpression):
            return NilExpression([])

        # Star e -> Star e
        else:
            return Repetition(__simplify(re.expr))

    # SYMBOL
    else:
        return re


def simplify(regex):
    """ This function repeatedly simplifes a regex and checks that it is
        minimal via idempotence.

        :param Production regex: The regex to simplify
        :rtype: Production
    """
    simplifiedRegex = __simplify(regex)
    while str(regex) != str(simplifiedRegex):
        regex = simplifiedRegex
        simplifiedRegex = __simplify(simplifiedRegex)

    return simplifiedRegex
