import re

class Parser:
    def __init__(self, *regex_dict):
        self.regex = dict()

        try:
            for name, regex_tuple in regex_dict.items():
                self.regex[name] = re.compile(regex_tuple[0], regex_tuple[1])   # regex_tuple[0] = regex string | regex_tuple[1] = option string
                                    
        except:
            raise

        
