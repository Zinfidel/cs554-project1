class RegexExpression:
    def __init__(self):
        pass
    
    def matches(self, string):
        pass


class Alternative(RegexExpression):
    def __init__(self, left, right):
        self.left = left
        self.right = right

    def __str__(self):
        return '|' + str(left) + ' ' +  str(right)

    def matches(self, string):
        #        string.
        pass
    

class NilExpression(RegexExpression):
    def __str__(self):
        return ''

    def matches(self, string):
        return string == ''


if __name__ == "__main__":
    print '' == ''
