from exceptions import InvalidToken, ClosingTagMismatch, \
                       AttributeHasNoValue, InvalidAttributes, \
                       InvalidTagName
from tag import Tag
from typing import List, Tuple, Dict
from utils import is_name_char, is_name_start, is_whitespace
from literals import String, Integer

class XMLParser:
    def parse(self, doc: str):
        """
            Parse an XML String
        """
        self.i = 0
        self.doc = doc
        tags, _ = self._parse_document()
        root = Tag()
        root.children = tags
        return root

    def _parse_document(self, parent: str = None) -> Tuple[List[Tag], str]:
        """
            Parsing a self.document containing a list of tags and comments.
            Anything within a tag is a treated as a subdocument so its is applied
            recursively.
        """
        tags: Dict[str, List[Tag]] = {}
        value = ''

        while self.i < len(self.doc):
            # Found closing tag
            if parent is not None and self.doc[self.i:self.i + 2] == '</':
                if parent != self.doc[self.i + 2:self.i + 2 + len(parent)]:
                    raise ClosingTagMismatch()
                self.i += 3 + len(parent)
                break
            # Found comment
            elif self.doc[self.i:self.i + 4] == '<!--':
                self.i += 4
                self._parse_comment()
            # Found tag, then recursively parse
            elif self.doc[self.i] == '<':
                self.i += 1
                tag = self._parse_tag()
                if tag.type == Tag.TYPES.NORMAL:
                    tags[tag.name] = (tags.get(tag.name) or []) + [tag]
            else:
                value += self.doc[self.i]
                self.i += 1
    
        value = value.strip()
        if value.isnumeric() or value[:1] == '-' and value[1:].isnumeric():
            # print(value)
            value = Integer(int(value))
            # print(value)
        elif value in ['True', 'False']:
            value = value == 'True'
            # print(value)
        else:
            # print(value)
            value = String(value)
            # print(value)

        return (tags, value)

    def _parse_name(self) -> str:
        """
            Parse a name (can be attribute name or tag name).
        """
        name = self.doc[self.i]

        while self.i < len(self.doc):
            self.i += 1
            if is_name_char(self.doc[self.i]):
                name += self.doc[self.i]
            elif self.doc[self.i] in [' ', '\n', '\t', '>', '?', '=']:
                break
            else:
                raise InvalidToken()

        return name

    def _parse_string(self) -> str:
        """
            Parse string literals
        """
        
        string = ""

        while self.i < len(self.doc):
            self.i += 1
            # If found unescaped apostrophe, break.
            # If it was escaped, then we treat it as string character
            if self.doc[self.i] == "\"" and self.doc[self.i - 1] != "\\": 
                self.i += 1
                break
            else:
                string += self.doc[self.i]

        return string

    def _parse_attributes(self) -> Dict[str, str]:
        """
            Parse attribute lists inside tags
            and return an attribute map that
            maps attribute names to values
        """
        attributes: Dict[str, str] = {}

        while self.i < len(self.doc):
            # If found a valid attribute name starting token
            if is_name_start(self.doc[self.i]):
                # Fully parse that name
                name = self._parse_name()
                if self.doc[self.i] != '=':
                    raise AttributeHasNoValue()
                
                self.i += 1
                # Parse the value of the attribute
                value = self._parse_string()

                attributes[name] = value
            elif self.doc[self.i] in ['\t', '\n', ' ']:
                # Whitespace that separates attributes
                self.i += 1
                continue
            elif self.doc[self.i] == '>':
                # Attribute ends
                self.i += 1
                break
            elif self.doc[self.i] == '?' and self.doc[self.i + 1] == '>':
                # End of processing tag
                self.i += 2
                break
            else:
                raise InvalidAttributes()
            
        return attributes

    def _parse_tag(self) -> Tag:
        """
            Parse a tag and its subdocument or value
        """
        tag = Tag()

        # If tag is a processing tag
        if self.doc[self.i] == '?':
            tag.type = Tag.TYPES.PROCESSOR
            self.i += 1
        else:
            tag.type = Tag.TYPES.NORMAL

        if not is_name_start(self.doc[self.i]):
            raise InvalidTagName()

        tag.name = self._parse_name()

        tag.attributes = self._parse_attributes()

        if tag.type == Tag.TYPES.NORMAL:
            # parse subdocument
            tag.children, tag.value = self._parse_document(tag.name)

        return tag

    def _parse_comment(self) -> None:
        """
            Consume comments, until comment closing tag is reached.
        """
        while self.i < len(self.doc):
            if self.doc[self.i:self.i + 3] == '-->':
                self.i += 3
                break
            else:
                self.i += 1