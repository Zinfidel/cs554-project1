from regex import BuildExpression
import description_reader

class LexicalDesc:
    """Encapsulates a complete lexical description."""

    def __init__(self, name, alphabet, classes):
        """
        :param name: The name of this description as a string.
        :param alphabet A list of backquoted symbols as produced by description_reader.py.
        :param classes: A list of parsed classes. Each class is a list of tokens
                        as produced by description_reader.py.
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
        if string_to_scan == '':
            return tokens

        '''
           Represents the leftmost parse of the parse tree.
        '''
        for c in self.classes:
            matched, leftover = c.regex.consume(string_to_scan)

            #if we do get a match using the regex
            if matched != '':
                if c.relevance != 'discard':
                    new_tokens = tokens + [Token(matched, c.name, c.relevance)]
                else:
                    new_tokens = tokens
                try:
                    return self.scan(leftover, new_tokens)
                except Exception as e:
                    continue

        ''' 
            If we get here, that means there was no logical parse
            using the regexes we were given. We should return an error
            at this point. 
        '''
        raise Exception(string_to_scan)


class LexicalClass:
    """Describes a lexical class using a regular expression."""

    def __init__(self, name, class_tokens, relevance):
        """
        :param name: The name of this class.
        :param class_tokens: The tokens comprising this class regex, in a list.
        :param relevance: The semantic relevance of this class.
        """
        self.name = name
        self.regex, ignored = BuildExpression(class_tokens)
        self.relevance = relevance

    def __str__(self):
        return "Name: " + self.name + ", Regex: " + \
               str(self.regex) + ", Relevance: " + self.relevance


class Token:
    '''Essentially a tuple of a String, LexicalClass, and a relevance as
       defined in the lexical desciption of the grammar
    '''

    def __init__(self, string, lex_class_name, relevance):
        self.string = string
        self.lexical_class = lex_class_name
        self.relevance = relevance

    def __str__(self):
        return "Class: " + str(self.lexical_class) + "\n\tString: "\
               + str(self.string)
