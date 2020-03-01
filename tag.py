from __future__ import annotations
from typing import Dict, List, Optional
from exceptions import TagNotFound
from enum import Enum
from utils import is_name_start

class Tag:
    TYPES = Enum('TagType', 'PROCESSOR NORMAL')

    def __init__(self, value: str = '', name: str = ''):
        self.attributes: Dict[str, str] = {}
        self.children: Dict[str, List[Tag]] = {}
        self.value = ''
        self.name = ''

    def find(self,
             name: str, 
             order: Optional[int] = None,
             **kwargs: typing.Dict[str, str]) -> Tag:
        """
            Finds a tag given set of attributes
            Example:
                tag.find('span', class='large')
        """
        tags = self.children.get(name) or []

        if len(tags) == 0:
            raise TagNotFound()

        if order is not None:
            if order >= len(tags):
                raise TagNotFound()
            return tags[order]
        
        for tag in tags:
            if all([ tag.attributes.get(name) == value 
                     for name, value in kwargs.items()
                   ]):
                return tag
        else:
            raise TagNotFound()

    def execute_query(self, query: str) -> str:
        """
            Convert query language to python syntax
                (1) token. -> token.find()
                (2) token{x} -> .find(order=x)
                (3) token[y=5,z=3] -> .find(y = 5, z = 3)
        """

        query_python = ''
        token_start = False
        wait_close = False
        
        i = 0
        
        while i < len(query):
            if query[i] == '.':
                # Close previous parenthesis
                if wait_close:
                    query_python += '")'

                # Convert . to .find()
                query_python += '.find("'
                wait_close = True
                
            elif query[i] == '[':
                # Parse attributes from square brackets
                query_python += '"'
                
                # Paste closing bracket
                j = i + 1
                while j < len(query) and query[j] != ']': j += 1
                
                # Paste attributes as keyword arguments
                for pair in query[i+1:j].split(','):
                    name, value = pair.strip().split('=')
                    query_python += f', {name} = "{value}"'
                
                query_python += ')'

                i = j
                wait_close = False

            elif query[i] == '{':
                # Parse index from curly braces
                query_python += '", order = '

                # Find end curly braces
                j = i + 1 
                while j < len(query) and query[j] != '}': j += 1

                # Paste index into order argument
                query_python += query[i+1:j] + ')'

                i = j
                wait_close = False
            elif query[i] == ' ':
                # White space
                if wait_close:
                    query_python += '").value'
                    wait_close = False
                query_python += ' '
                token_start = False
            elif is_name_start(query[i]) and not token_start:
                if query[i:i+4] in ['not ', 'and ']:
                    query_python += query[i:i+4]
                    i += 4
                    continue
                if query[i:i+3] in ['or ']:
                    query_python += query[i:i+3]
                    i += 3
                    continue
                
                query_python += 'self.find("' + query[i]
                token_start = True
                wait_close = True
            else:
                query_python += query[i]

            i += 1

        if wait_close:
            query_python += '").value'
            wait_close = False

        try:
            return str(eval(query_python))
        except:
            return 'INVALID'