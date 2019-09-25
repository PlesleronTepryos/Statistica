"""Command parser for Statistica"""

import re

from .utils import InfoList

class ProductionRule:
    """Production rule class for easier parsing"""

    def __init__(self):
        pass

    def match(self, ast, terminals):
        """Finds the best match for the production rule"""

        full_match = []

        pos = -1

        for symbol in ast[::-1]:

            match_symbol, quantifier = self.symbols[pos]

            if symbol == match_symbol:
                pass

class CommandParser:
    """Configurable parser for commands with varying syntax requirements"""

    def __init__(self, grammar_str):

        # Splitting the grammar file into lines
        pre_grammar = grammar_str.split('\n')
        grammar_tokens = []

        # Creating a list of tokens in the grammar not from blank or comment lines
        for line in pre_grammar:
            if line and not line.startswith('#'):
                grammar_tokens.extend(line.split())

        # Building a list of each of the grammar entries
        entries = ' '.join(grammar_tokens).split('; ')

        # Initializing the dict of terminal symbols
        self.terminals = {}

        # Compiling each entry into a proto production rule
        proto_prod_rules = self._interpret_entries(entries)

        # Final compilation of each production rule
        self.production_rules = self._build_production_rules(proto_prod_rules)

    def _interpret_entries(self, entries):

        # Initializing the proto production rules dict and depth stack
        proto_prod_rules = {}
        depth = []

        # Iterating through each entry in the grammar
        for entry in entries:
            entry = list(re.findall(r"'[^' ]+'\$?|\w+|[(){}:*+?]", entry))

            node = entry[0]

            proto_prod_rules[node] = InfoList([], {
                'name': node,
                'type': 'symbol_list',
                'count': [1, 1]
            })

            # Compiling each token
            for token in entry[2:]:

                # Returning to the root and climbing to the current branch
                branch = proto_prod_rules[node]
                for _ in range(len(depth)):
                    branch = branch[-1]

                # Nonterminal symbol
                if re.match(r'\w+', token):

                    branch.append(InfoList([token], {
                        'name': token,
                        'type': 'nonterminal',
                        'count': [1, 1]
                    }))

                # Literal-matched terminal symbol
                elif re.match(r"'[^' ]+'", token):

                    branch.append(InfoList([token[1:-1]], {
                        'name': token[1:-1],
                        'type': 'terminal',
                        'count': [1, 1]
                    }))

                    self.terminals[token[1:-1]] = (token[1:-1], 'literal')

                # Regex-matched terminal symbol
                elif re.match(r"'[^' ]+'\$", token):

                    branch.append(InfoList([token[1:-2]], {
                        'name': token[1:-2],
                        'type': 'terminal-r',
                        'count': [1, 1]
                    }))

                    self.terminals[token[1:-2]] = (token[1:-2], 'regex')

                # Opening a list of symbols
                elif token == '(':

                    branch.append(InfoList([], {
                        'name': branch['name'] + '.' + str(len(branch)),
                        'type': 'symbol_list',
                        'count': [1, 1]
                    }))

                    depth.append('L')

                # Closing a list of symbols
                elif token == ')':
                    if depth.pop() != 'L':
                        raise ValueError('mismatched branch types')

                # Opening a list of symbol choices
                elif token == '{':

                    branch.append(InfoList([], {
                        'name': branch['name'] + '.' + str(len(branch)),
                        'type': 'choice_list',
                        'count': [1, 1]
                    }))

                    depth.append('C')

                # Closing a list of symbol choices
                elif token == '}':
                    if depth.pop() != 'C':
                        raise ValueError('mismatched branch types')

                # Quantifying the latest branch as 'one or more'
                elif token == '+':
                    branch[-1]['count'] = [1, float('inf')]

                # Quantifying the latest branch as 'zero or more'
                elif token == '*':
                    branch[-1]['count'] = [0, float('inf')]

                # Quantifying the latest branch as 'zero or one'
                elif token == '?':
                    branch[-1]['count'] = [0, 1]

                else:
                    raise ValueError('invalid token')

        return proto_prod_rules

    def _build_production_rules(self, proto_prod_rules):
        return proto_prod_rules

    def lrparse(self, command):
        """Returns the context defined by the command"""
        cmd_tokens = self.tokenize(command)
        cmd_ast = self.build_ast(cmd_tokens)

    def tokenize(self, command_str):
        """Breaks a command into a set of usable tokens"""

        # List of matched tokens in the command
        tokens = []

        # Working until the command string is empty
        while command_str:

            # Creating a list of possible matching tokens
            candidates = []

            # For each possible terminal symbol
            for name, (match_str, match_type) in self.terminals.items():

                # If the symbol matches literally
                if match_type == 'literal':

                    # If the symbol successfully matches
                    if match_str == command_str[:len(match_str)]:
                        candidates.append((name, match_str))

                # If the symbol matches with a regex
                elif match_type == 'regex':

                    # Saving the match
                    match = re.match(match_str, command_str)

                    # If the symbol matched successfully
                    if match is not None:
                        candidates.append((name, match))

            # Raising an error if none of the terminal symbols match
            if not candidates:
                raise ValueError('invalid command syntax')

            # Sorting the matches by length of the matched string
            candidates = sorted(candidates, key=lambda x: len(x[1]))

            # Recorcing the longest match
            tokens.append(candidates[-1])

            # Cutting off the matched part of the command string
            command_str = command_str[len(candidates[-1][1]):]

        return tokens

    def build_ast(self, tokens):
        """Constructs an abstract syntax tree from the given tokens"""

        pos = 0

        ast = []

        while pos < len(tokens):
            
            for name, prod_rule in self.production_rules.items():

                match = prod_rule.match(ast, tokens[pos:])

        return tokens
