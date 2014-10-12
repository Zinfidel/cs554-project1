from description_reader import BuildExpression


class LexicalDesc:
    """Encapsulates a complete lexical description."""

    def __init__(self, name, alphabet, classes):
        """
        :param name: The name of this description as a string.
        :param alphabet A list of backquoted symbols as produced by description_reader.py.
        :param classes: A list of parsed classes. Each class is a list of tokens as produced by description_reader.py.
        """
        self.name = name
        self.alphabet = alphabet
        self.classes = [LexicalClass(c[0], c[1], c[2]) for c in classes]

    def scan(self, string_to_scan, tokens=[]):
        '''
        Scans a string and produces a list of Tokens parsed from
        the string. 

        :param string_to_scan the string that will be turned into a list 
               of Token objects. 
        :return a list of Token object recognized by the string. If the
                string cannot be fully recognized (ie, there is part of the
                string left after scanning completely) an empty list will be
                returned.
        '''
        
        
        pass


class LexicalClass:
    """Describes a lexical class using a regular expression."""

    def __init__(self, name, class_tokens, relevance):
        """
        :param name: The name of this class.
        :param class_tokens: The tokens comprising this class regex, in a list.
        :param relevance: The semantic relevance of this class.
        """
        self.name = name
        self.regex = BuildExpression(class_tokens)
        self.relevance = relevance

    def __str__(self):
        return "Name: " + self.name + ", Regex: " + str(self.regex) + ", Relevance: " + self.relevance


class Token:
    '''Essentially a tuple of a String, LexicalClass, and a relevance as
       defined in the lexical desciption of the grammar
    '''

    def __init__(self, string, lex_class, relevance):
        self.string = string
        self.lexical_class = lex_class
        self.relevance = relevance
