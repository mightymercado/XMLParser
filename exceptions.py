class ParserException(Exception):
    message = 'Parser error'
    def __init__(self):
        super().__init__(self.message)

class InvalidToken(ParserException):
    message = 'invalid token while scanning name'
    
class TagNotFound(ParserException):
    message = 'tag could not be found'

class ClosingTagMismatch(ParserException):
    message = 'closing tag name does not match starting tag'

class AttributeHasNoValue(ParserException):
    message = 'attribute does not specify a value'

class InvalidAttributes(ParserException):
    message = 'atrribute list is malformed'

class InvalidTagName(ParserException):
    message = 'tag name is malformed'

class CannotCastToBool(ParserException):
    message = 'right operand cannot cast to boolean'

class CannotCastToString(ParserException):
    message = 'right operand cannot cast to string'

class CannotCastToInteger(ParserException):
    message = 'right operand cannot cast to integer'