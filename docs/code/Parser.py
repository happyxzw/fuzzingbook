#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This material is part of "Generating Software Tests".
# Web site: https://www.fuzzingbook.org/html/Parser.html
# Last change: 2019-03-05 00:22:52-08:00
#
#
# Copyright (c) 2018 Saarland University, CISPA, authors, and contributors
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS
# OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY
# CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
# TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE
# SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# # Parsing Inputs

if __name__ == "__main__":
    print('# Parsing Inputs')




# ## Fuzzing a Simple Program

if __name__ == "__main__":
    print('\n## Fuzzing a Simple Program')




def process_inventory(inventory):
    res = []
    for vehicle in inventory.split('\n'):
        ret = process_vehicle(vehicle)
        res.extend(ret)
    return '\n'.join(res)

def process_vehicle(vehicle):
    year, kind, company, model, *_ = vehicle.split(',')
    if kind == 'van':
        return process_van(year, company, model)

    elif kind == 'car':
        return process_car(year, company, model)

    else:
        raise Exception('Invalid entry')

def process_van(year, company, model):
    res = ["We have a %s %s van from %s vintage." % (company, model, year)]
    iyear = int(year)
    if iyear > 2010:
        res.append("It is a recent model!")
    else:
        res.append("It is an old but reliable model!")
    return res

def process_car(year, company, model):
    res = ["We have a %s %s car from %s vintage." % (company, model, year)]
    iyear = int(year)
    if iyear > 2016:
        res.append("It is a recent model!")
    else:
        res.append("It is an old but reliable model!")
    return res

if __name__ == "__main__":
    mystring = """\
    1997,van,Ford,E350
    2000,car,Mercury,Cougar\
    """
    print(process_inventory(mystring))


import string

CSV_GRAMMAR = {
    '<start>': ['<csvline>'],
    '<csvline>': ['<items>'],
    '<items>': ['<item>,<items>', '<item>'],
    '<item>': ['<letters>'],
    '<letters>': ['<letter><letters>', '<letter>'],
    '<letter>': list(string.ascii_letters + string.digits + string.punctuation + ' \t\n')
}

if __name__ == "__main__":
    # We use the same fixed seed as the notebook to ensure consistency
    import random
    random.seed(2001)


if __package__ is None or __package__ == "":
    from Grammars import EXPR_GRAMMAR, START_SYMBOL, RE_NONTERMINAL, is_valid_grammar, syntax_diagram
else:
    from .Grammars import EXPR_GRAMMAR, START_SYMBOL, RE_NONTERMINAL, is_valid_grammar, syntax_diagram

if __package__ is None or __package__ == "":
    from Fuzzer import Fuzzer
else:
    from .Fuzzer import Fuzzer

if __package__ is None or __package__ == "":
    from GrammarFuzzer import GrammarFuzzer, FasterGrammarFuzzer, display_tree, tree_to_string, dot_escape
else:
    from .GrammarFuzzer import GrammarFuzzer, FasterGrammarFuzzer, display_tree, tree_to_string, dot_escape


if __package__ is None or __package__ == "":
    from ExpectError import ExpectError
else:
    from .ExpectError import ExpectError

if __package__ is None or __package__ == "":
    from Timer import Timer
else:
    from .Timer import Timer


if __name__ == "__main__":
    syntax_diagram(CSV_GRAMMAR)


if __name__ == "__main__":
    gf = GrammarFuzzer(CSV_GRAMMAR, min_nonterminals=4)
    trials = 1000
    valid = []
    time = 0
    for i in range(trials):
        with Timer() as t:
            vehicle_info = gf.fuzz()
            try:
                process_vehicle(vehicle_info)
                valid.append(vehicle_info)
            except:
                pass
            time += t.elapsed_time()
    print("%d valid strings, that is GrammarFuzzer generated %f%% valid entries from %d inputs" %
          (len(valid), len(valid) * 100.0 / trials, trials))
    print("Total time of %f seconds" % time)


if __name__ == "__main__":
    gf = GrammarFuzzer(CSV_GRAMMAR, min_nonterminals=4)
    trials = 10
    valid = []
    time = 0
    for i in range(trials):
        vehicle_info = gf.fuzz()
        try:
            print(repr(vehicle_info), end="")
            process_vehicle(vehicle_info)
        except Exception as e:
            print("\t", e)
        else:
            print()


import copy

import random

class PooledGrammarFuzzer(GrammarFuzzer):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._node_cache = {}

    def update_cache(self, key, values):
        self._node_cache[key] = values

    def expand_node_randomly(self, node):
        (symbol, children) = node
        assert children is None
        if symbol in self._node_cache:
            if random.randint(0, 1) == 1:
                return super().expand_node_randomly(node)
            return copy.deepcopy(random.choice(self._node_cache[symbol]))
        return super().expand_node_randomly(node)

if __name__ == "__main__":
    gf = PooledGrammarFuzzer(CSV_GRAMMAR, min_nonterminals=4)
    gf.update_cache('<item>', [
        ('<item>', [('car', [])]),
        ('<item>', [('van', [])]),
    ])
    trials = 10
    valid = []
    time = 0
    for i in range(trials):
        vehicle_info = gf.fuzz()
        try:
            print(repr(vehicle_info), end="")
            process_vehicle(vehicle_info)
        except Exception as e:
            print("\t", e)
        else:
            print()


# ## Using a Parser

if __name__ == "__main__":
    print('\n## Using a Parser')




# ## An Ad Hoc Parser

if __name__ == "__main__":
    print('\n## An Ad Hoc Parser')




def parse_csv(mystring):
    children = []
    tree = (START_SYMBOL, children)
    for i, line in enumerate(mystring.split('\n')):
        children.append(("record %d" % i, [(cell, [])
                                           for cell in line.split(',')]))
    return tree

def lr_graph(dot):
    dot.attr('node', shape='plain')
    dot.graph_attr['rankdir'] = 'LR'

if __name__ == "__main__":
    tree = parse_csv(mystring)
    display_tree(tree, graph_attr=lr_graph)


if __name__ == "__main__":
    mystring = '''\
    1997,Ford,E350,"ac, abs, moon",3000.00\
    '''
    print(mystring)


def highlight_node(predicate):
    def hl_node(dot, nid, symbol, ann):
        if predicate(dot, nid, symbol, ann):
            dot.node(repr(nid), dot_escape(symbol), fontcolor='red')
        else:
            dot.node(repr(nid), dot_escape(symbol))
    return hl_node

if __name__ == "__main__":
    tree = parse_csv(mystring)
    bad_nodes = {5, 6, 7, 12, 13, 20, 22, 23, 24, 25}


def hl_predicate(_d, nid, _s, _a): return nid in bad_nodes

if __name__ == "__main__":
    highlight_err_node = highlight_node(hl_predicate)
    display_tree(tree, log=False, node_attr=highlight_err_node,
                 graph_attr=lr_graph)


def parse_quote(string, i):
    v = string[i + 1:].find('"')
    return v + i + 1 if v >= 0 else -1

def find_comma(string, i):
    slen = len(string)
    while i < slen:
        if string[i] == '"':
            i = parse_quote(string, i)
            if i == -1:
                return -1
        if string[i] == ',':
            return i
        i += 1
    return -1

def comma_split(string):
    slen = len(string)
    i = 0
    while i < slen:
        c = find_comma(string, i)
        if c == -1:
            yield string[i:]
            return
        else:
            yield string[i:c]
        i = c + 1

def parse_csv(mystring):
    children = []
    tree = (START_SYMBOL, children)
    for i, line in enumerate(mystring.split('\n')):
        children.append(("record %d" % i, [(cell, [])
                                           for cell in comma_split(line)]))
    return tree

if __name__ == "__main__":
    tree = parse_csv(mystring)
    display_tree(tree, graph_attr=lr_graph)


if __name__ == "__main__":
    mystring = '''\
    1999,Chevy,"Venture \\"Extended Edition, Very Large\\"",,5000.00\
    '''
    print(mystring)


if __name__ == "__main__":
    tree = parse_csv(mystring)
    bad_nodes = {4, 5}
    display_tree(tree, node_attr=highlight_err_node, graph_attr=lr_graph)


if __name__ == "__main__":
    mystring = '''\
    1996,Jeep,Grand Cherokee,"MUST SELL!
    air, moon roof, loaded",4799.00
    '''
    print(mystring)


if __name__ == "__main__":
    tree = parse_csv(mystring)
    bad_nodes = {5, 6, 7, 8, 9, 10}
    display_tree(tree, node_attr=highlight_err_node, graph_attr=lr_graph)


# ## Grammars

if __name__ == "__main__":
    print('\n## Grammars')




A1_GRAMMAR = {
    "<start>": ["<expr>"],
    "<expr>": ["<expr>+<expr>", "<expr>-<expr>", "<integer>"],
    "<integer>": ["<digit><integer>", "<digit>"],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

if __name__ == "__main__":
    syntax_diagram(A1_GRAMMAR)


if __name__ == "__main__":
    mystring = '1+2'


if __name__ == "__main__":
    tree = ('<start>', [('<expr>',
                         [('<expr>', [('<integer>', [('<digit>', [('1', [])])])]),
                          ('+', []),
                          ('<expr>', [('<integer>', [('<digit>', [('2',
                                                                   [])])])])])])
    assert mystring == tree_to_string(tree)
    display_tree(tree)


A2_GRAMMAR = {
    "<start>": ["<expr>"],
    "<expr>": ["<integer><expr_>"],
    "<expr_>": ["+<expr>", "-<expr>", ""],
    "<integer>": ["<digit><integer_>"],
    "<integer_>": ["<integer>", ""],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

if __name__ == "__main__":
    syntax_diagram(A2_GRAMMAR)


if __name__ == "__main__":
    tree = ('<start>', [('<expr>', [('<integer>', [('<digit>', [('1', [])]),
                                                   ('<integer_>', [])]),
                                    ('<expr_>', [('+', []),
                                                 ('<expr>',
                                                  [('<integer>',
                                                    [('<digit>', [('2', [])]),
                                                     ('<integer_>', [])]),
                                                   ('<expr_>', [])])])])])
    assert mystring == tree_to_string(tree)
    display_tree(tree)


# #### Recursion

if __name__ == "__main__":
    print('\n#### Recursion')




LR_GRAMMAR = {
    '<start>': ['<A>'],
    '<A>': ['<A>a', ''],
}

if __name__ == "__main__":
    syntax_diagram(LR_GRAMMAR)


if __name__ == "__main__":
    mystring = 'aaaaaa'
    display_tree(
        ('<start>', (('<A>', (('<A>', (('<A>', []), ('a', []))), ('a', []))), ('a', []))))


RR_GRAMMAR = {
    '<start>': ['<A>'],
    '<A>': ['a<A>', ''],
}

if __name__ == "__main__":
    syntax_diagram(RR_GRAMMAR)


if __name__ == "__main__":
    display_tree(('<start>', ((
        '<A>', (('a', []), ('<A>', (('a', []), ('<A>', (('a', []), ('<A>', []))))))),)))


# #### Ambiguity

if __name__ == "__main__":
    print('\n#### Ambiguity')




if __name__ == "__main__":
    mystring = '1+2+3'
    tree = ('<start>',
            [('<expr>',
              [('<expr>', [('<expr>', [('<integer>', [('<digit>', [('1', [])])])]),
                           ('+', []),
                           ('<expr>', [('<integer>',
                                        [('<digit>', [('2', [])])])])]), ('+', []),
               ('<expr>', [('<integer>', [('<digit>', [('3', [])])])])])])
    assert mystring == tree_to_string(tree)
    display_tree(tree)


if __name__ == "__main__":
    tree = ('<start>',
            [('<expr>', [('<expr>', [('<integer>', [('<digit>', [('1', [])])])]),
                         ('+', []),
                         ('<expr>',
                          [('<expr>', [('<integer>', [('<digit>', [('2', [])])])]),
                           ('+', []),
                           ('<expr>', [('<integer>', [('<digit>', [('3',
                                                                    [])])])])])])])
    assert tree_to_string(tree) == mystring
    display_tree(tree)


class Parser(object):
    def __init__(self, grammar, **kwargs):
        self._grammar = grammar
        self._start_symbol = kwargs.get('start_symbol', START_SYMBOL)
        self.log = kwargs.get('log', False)
        self.coalesce = kwargs.get('coalesce', True)
        self.tokens = kwargs.get('tokens', set())

    def grammar(self):
        return self._grammar

    def start_symbol(self):
        return self._start_symbol

    def parse_prefix(self, text):
        """Return pair (cursor, forest) for longest prefix of text"""
        raise NotImplemented()

    def parse(self, text):
        cursor, forest = self.parse_prefix(text)
        if cursor < len(text):
            raise SyntaxError("at " + repr(text[cursor:]))
        return [self.prune_tree(tree) for tree in forest]

    def coalesce(self, children):
        last = ''
        new_lst = []
        for cn, cc in children:
            if cn not in self._grammar:
                last += cn
            else:
                if last:
                    new_lst.append((last, []))
                    last = ''
                new_lst.append((cn, cc))
        if last:
            new_lst.append((last, []))
        return new_lst

    def prune_tree(self, tree):
        name, children = tree
        if self.coalesce:
            children = self.coalesce(children)
        if name in self.tokens:
            return (name, [(tree_to_string(tree), [])])
        else:
            return (name, [self.prune_tree(c) for c in children])

# ## Parsing Expression Grammars

if __name__ == "__main__":
    print('\n## Parsing Expression Grammars')




PEG1 = {
    '<start>': ['a', 'b']
}

PEG2 = {
    '<start>': ['ab', 'abc']
}

# ### The Packrat Parser for Predicate Expression Grammars

if __name__ == "__main__":
    print('\n### The Packrat Parser for Predicate Expression Grammars')




import re

def canonical(grammar, letters=False):
    def split(expansion):
        if isinstance(expansion, tuple):
            expansion = expansion[0]

        return [token for token in re.split(
            RE_NONTERMINAL, expansion) if token]

    def tokenize(word):
        return list(word) if letters else [word]

    def canonical_expr(expression):
        return [
            token for word in split(expression)
            for token in ([word] if word in grammar else tokenize(word))
        ]

    return {
        k: [canonical_expr(expression) for expression in alternatives]
        for k, alternatives in grammar.items()
    }

if __name__ == "__main__":
    canonical(EXPR_GRAMMAR)


class Parser(Parser):
    def __init__(self, grammar, **kwargs):
        self._grammar = grammar
        self._start_symbol = kwargs.get('start_symbol', START_SYMBOL)
        self.log = kwargs.get('log', False)
        self.tokens = kwargs.get('tokens', set())
        self.cgrammar = canonical(grammar)

# ### The Parser

if __name__ == "__main__":
    print('\n### The Parser')




class PEGParser(Parser):
    def parse_prefix(self, text):
        cursor, tree = self.unify_key(self.start_symbol(), text, 0)
        return cursor, [tree]

# #### Unify Key

if __name__ == "__main__":
    print('\n#### Unify Key')




class PEGParser(PEGParser):
    def unify_key(self, key, text, at=0):
        if self.log:
            print("unify_key: %s with %s" % (repr(key), repr(text[at:])))
        if key not in self.cgrammar:
            if text[at:].startswith(key):
                return at + len(key), (key, [])
            else:
                return at, None
        for rule in self.cgrammar[key]:
            to, res = self.unify_rule(rule, text, at)
            if res:
                return (to, (key, res))
        return 0, None

if __name__ == "__main__":
    mystring = "1"
    peg = PEGParser(EXPR_GRAMMAR, log=True)
    peg.unify_key('1', mystring)


if __name__ == "__main__":
    mystring = "2"
    peg.unify_key('1', mystring)


# #### Unify Rule

if __name__ == "__main__":
    print('\n#### Unify Rule')




class PEGParser(PEGParser):
    def unify_rule(self, rule, text, at):
        if self.log:
            print('unify_rule: %s with %s' % (repr(rule), repr(text[at:])))
        results = []
        for token in rule:
            at, res = self.unify_key(token, text, at)
            if res is None:
                return at, None
            results.append(res)
        return at, results

if __name__ == "__main__":
    mystring = "0"
    peg = PEGParser(EXPR_GRAMMAR, log=True)
    peg.unify_rule(peg.cgrammar['<digit>'][0], mystring, 0)


if __name__ == "__main__":
    mystring = "12"
    peg.unify_rule(peg.cgrammar['<integer>'][0], mystring, 0)


if __name__ == "__main__":
    mystring = "1 + 2"
    peg = PEGParser(EXPR_GRAMMAR, log=False)
    peg.parse(mystring)


from functools import lru_cache

class PEGParser(PEGParser):
    @lru_cache(maxsize=None)
    def unify_key(self, key, text, at=0):
        if key not in self.cgrammar:
            if text[at:].startswith(key):
                return at + len(key), (key, [])
            else:
                return at, None
        for rule in self.cgrammar[key]:
            to, res = self.unify_rule(rule, text, at)
            if res:
                return (to, (key, res))
        return 0, None

if __name__ == "__main__":
    mystring = "1 + (2 * 3)"
    peg = PEGParser(EXPR_GRAMMAR)
    for tree in peg.parse(mystring):
        assert tree_to_string(tree) == mystring
        display_tree(tree)


if __name__ == "__main__":
    mystring = "1 * (2 + 3.35)"
    for tree in peg.parse(mystring):
        assert tree_to_string(tree) == mystring
        display_tree(tree)


# ## Parsing Context-Free Grammars

if __name__ == "__main__":
    print('\n## Parsing Context-Free Grammars')




# ###  Problems with PEG

if __name__ == "__main__":
    print('\n###  Problems with PEG')




PEG_SURPRISE = {
    "<A>": ["a<A>a", "aa"]
}

if __name__ == "__main__":
    strings = []
    for e in range(4):
        f = GrammarFuzzer(PEG_SURPRISE, start_symbol='<A>')
        tree = ('<A>', None)
        for _ in range(e):
            tree = f.expand_tree_once(tree)
        tree = f.expand_tree_with_strategy(tree, f.expand_node_min_cost)
        strings.append(tree_to_string(tree))
        display_tree(tree)
    strings


if __name__ == "__main__":
    peg = PEGParser(PEG_SURPRISE, start_symbol='<A>')
    for s in strings:
        with ExpectError():
            for tree in peg.parse(s):
                display_tree(tree)
            print(s)


# ### The Earley Parser

if __name__ == "__main__":
    print('\n### The Earley Parser')




SAMPLE_GRAMMAR = {
    '<start>': ['<A><B>'],
    '<A>': ['a<B>c', 'a<A>'],
    '<B>': ['b<C>', '<D>'],
    '<C>': ['c'],
    '<D>': ['d']
}
C_SAMPLE_GRAMMAR = canonical(SAMPLE_GRAMMAR)

if __name__ == "__main__":
    syntax_diagram(SAMPLE_GRAMMAR)


# ### Columns

if __name__ == "__main__":
    print('\n### Columns')




class Column(object):
    def __init__(self, index, letter):
        self.index, self.letter = index, letter
        self.states, self._unique = [], {}

    def __str__(self):
        return "%s chart[%d]\n%s" % (self.letter, self.index, "\n".join(
            str(state) for state in self.states if state.finished()))

class Column(Column):
    def add(self, state):
        if state in self._unique:
            return self._unique[state]
        self._unique[state] = state
        self.states.append(state)
        state.e_col = self
        return self._unique[state]

# ### Items

if __name__ == "__main__":
    print('\n### Items')




class Item(object):
    def __init__(self, name, expr, dot):
        self.name, self.expr, self.dot = name, expr, dot

class Item(Item):
    def finished(self):
        return self.dot >= len(self.expr)

    def advance(self):
        return Item(self.name, self.expr, self.dot + 1)

    def at_dot(self):
        return self.expr[self.dot] if self.dot < len(self.expr) else None

if __name__ == "__main__":
    item_name = '<B>'
    item_expr = C_SAMPLE_GRAMMAR[item_name][1]
    an_item = Item(item_name, tuple(item_expr), 0)


if __name__ == "__main__":
    an_item.at_dot()


if __name__ == "__main__":
    another_item = an_item.advance()


if __name__ == "__main__":
    another_item.finished()


# ### States

if __name__ == "__main__":
    print('\n### States')




class State(Item):
    def __init__(self, name, expr, dot, s_col, e_col=None):
        super().__init__(name, expr, dot)
        self.s_col, self.e_col = s_col, e_col

    def __str__(self):
        def idx(var):
            return var.index if var else -1

        return self.name + ':= ' + ' '.join([
            str(p)
            for p in [*self.expr[:self.dot], '|', *self.expr[self.dot:]]
        ]) + "(%d,%d)" % (idx(self.s_col), idx(self.e_col))

    def copy(self):
        return State(self.name, self.expr, self.dot, self.s_col, self.e_col)

    def _t(self):
        return (self.name, self.expr, self.dot, self.s_col.index)

    def __hash__(self):
        return hash(self._t())

    def __eq__(self, other):
        return self._t() == other._t()

    def advance(self):
        return State(self.name, self.expr, self.dot + 1, self.s_col)

if __name__ == "__main__":
    col_0 = Column(0, None)
    item_expr = tuple(*C_SAMPLE_GRAMMAR[START_SYMBOL])
    start_state = State(START_SYMBOL, item_expr, 0, col_0)
    col_0.add(start_state)
    start_state.at_dot()


if __name__ == "__main__":
    sym = start_state.at_dot()
    for alt in C_SAMPLE_GRAMMAR[sym]:
        col_0.add(State(sym, tuple(alt), 0, col_0))
    for s in col_0.states:
        print(s)


# ### The Parsing Algorithm

if __name__ == "__main__":
    print('\n### The Parsing Algorithm')




class EarleyParser(Parser):
    def __init__(self, grammar, **kwargs):
        super().__init__(grammar, **kwargs)
        self.cgrammar = canonical(grammar, letters=True)

class EarleyParser(EarleyParser):
    def chart_parse(self, words, start):
        alt = tuple(*self.cgrammar[start])
        chart = [Column(i, tok) for i, tok in enumerate([None, *words])]
        chart[0].add(State(start, alt, 0, chart[0]))
        return self.fill_chart(chart)

# ### Predicting States

if __name__ == "__main__":
    print('\n### Predicting States')




class EarleyParser(EarleyParser):
    def predict(self, col, sym, state):
        for alt in self.cgrammar[sym]:
            col.add(State(sym, tuple(alt), 0, col))

if __name__ == "__main__":
    col_0 = Column(0, None)
    col_0.add(start_state)
    ep = EarleyParser(SAMPLE_GRAMMAR)
    ep.chart = [col_0]


if __name__ == "__main__":
    for s in ep.chart[0].states:
        print(s)


if __name__ == "__main__":
    ep.predict(col_0, '<A>', s)
    for s in ep.chart[0].states:
        print(s)


# ### Scanning Tokens

if __name__ == "__main__":
    print('\n### Scanning Tokens')




class EarleyParser(EarleyParser):
    def scan(self, col, state, letter):
        if letter == col.letter:
            col.add(state.advance())

if __name__ == "__main__":
    ep = EarleyParser(SAMPLE_GRAMMAR)
    col_1 = Column(1, 'a')
    ep.chart = [col_0, col_1]


if __name__ == "__main__":
    new_state = ep.chart[0].states[1]
    print(new_state)


if __name__ == "__main__":
    ep.scan(col_1, new_state, 'a')
    for s in ep.chart[1].states:
        print(s)


# ### Completing Processing

if __name__ == "__main__":
    print('\n### Completing Processing')




class EarleyParser(EarleyParser):
    def complete(self, col, state):
        return self.earley_complete(col, state)

    def earley_complete(self, col, state):
        parent_states = [
            st for st in state.s_col.states if st.at_dot() == state.name
        ]
        for st in parent_states:
            col.add(st.advance())

if __name__ == "__main__":
    ep = EarleyParser(SAMPLE_GRAMMAR)
    col_1 = Column(1, 'a')
    col_2 = Column(2, 'd')
    ep.chart = [col_0, col_1, col_2]
    ep.predict(col_0, '<A>', s)
    for s in ep.chart[0].states:
        print(s)


if __name__ == "__main__":
    for state in ep.chart[0].states:
        if state.at_dot() not in SAMPLE_GRAMMAR:
            ep.scan(col_1, state, 'a')
    for s in ep.chart[1].states:
        print(s)


if __name__ == "__main__":
    for state in ep.chart[1].states:
        if state.at_dot() in SAMPLE_GRAMMAR:
            ep.predict(col_1, state.at_dot(), state)
    for s in ep.chart[1].states:
        print(s)


if __name__ == "__main__":
    for state in ep.chart[1].states:
        if state.at_dot() not in SAMPLE_GRAMMAR:
            ep.scan(col_2, state, state.at_dot())

    for s in ep.chart[2].states:
        print(s)


if __name__ == "__main__":
    for state in ep.chart[2].states:
        if state.finished():
            ep.complete(col_2, state)

    for s in ep.chart[2].states:
        print(s)


# ### Filling the Chart

if __name__ == "__main__":
    print('\n### Filling the Chart')




class EarleyParser(EarleyParser):
    def fill_chart(self, chart):
        for i, col in enumerate(chart):
            for state in col.states:
                if state.finished():
                    self.complete(col, state)
                else:
                    sym = state.at_dot()
                    if sym in self.cgrammar:
                        self.predict(col, sym, state)
                    else:
                        if i + 1 >= len(chart):
                            continue
                        self.scan(chart[i + 1], state, sym)
            if self.log:
                print(col, '\n')
        return chart

if __name__ == "__main__":
    ep = EarleyParser(SAMPLE_GRAMMAR, log=True)
    columns = ep.chart_parse('adcd', START_SYMBOL)


if __name__ == "__main__":
    last_col = columns[-1]
    for s in last_col.states:
        if s.name == '<start>':
            print(s)


# ### The Parse Method

if __name__ == "__main__":
    print('\n### The Parse Method')




class EarleyParser(EarleyParser):
    def parse_prefix(self, text):
        self.table = self.chart_parse(text, self.start_symbol())
        for col in reversed(self.table):
            states = [
                st for st in col.states if st.name == self.start_symbol()
            ]
            if states:
                return col.index, states
        return -1, []

if __name__ == "__main__":
    ep = EarleyParser(SAMPLE_GRAMMAR)
    cursor, last_states = ep.parse_prefix('adcd')
    print(cursor, [str(s) for s in last_states])


class EarleyParser(EarleyParser):
    def parse(self, text):
        cursor, states = self.parse_prefix(text)
        start = next((s for s in states if s.finished()), None)
        if cursor < len(text) or not start:
            raise SyntaxError("at " + repr(text[cursor:]))

        forest = self.extract_trees(self.parse_forest(self.table, start))
        return [self.prune_tree(tree) for tree in forest]

# ### Parsing Paths

if __name__ == "__main__":
    print('\n### Parsing Paths')




class EarleyParser(EarleyParser):
    def parse_paths(self, named_expr, chart, frm, til):
        def paths(state, start, k, e):
            if not e:
                return [[(state, k)]] if start == frm else []
            else:
                return [[(state, k)] + r
                        for r in self.parse_paths(e, chart, frm, start)]

        *expr, var = named_expr
        starts = None
        if var not in self.cgrammar:
            starts = ([(var, til - len(var),
                        't')] if til > 0 and chart[til].letter == var else [])
        else:
            starts = [(s, s.s_col.index, 'n') for s in chart[til].states
                      if s.finished() and s.name == var]

        return [p for s, start, k in starts for p in paths(s, start, k, expr)]

if __name__ == "__main__":
    print(SAMPLE_GRAMMAR['<start>'])
    ep = EarleyParser(SAMPLE_GRAMMAR)
    completed_start = last_states[0]
    paths = ep.parse_paths(completed_start.expr, columns, 0, 4)
    for path in paths:
        print([list(str(s_) for s_ in s) for s in path])


# ### Parsing Forests

if __name__ == "__main__":
    print('\n### Parsing Forests')




class EarleyParser(EarleyParser):
    def parse_forest(self, chart, state):
        def forest(s, kind):
            return self.parse_forest(chart, s) if kind == 'n' else (s, [])

        pathexprs = self.parse_paths(state.expr, chart, state.s_col.index,
                                     state.e_col.index) if state.expr else []
        return state.name, [[forest(v, k) for v, k in reversed(pathexpr)]
                            for pathexpr in pathexprs]

if __name__ == "__main__":
    ep = EarleyParser(SAMPLE_GRAMMAR)
    result = ep.parse_forest(columns, last_states[0])
    result


# ### Extracting Trees

if __name__ == "__main__":
    print('\n### Extracting Trees')




class EarleyParser(EarleyParser):
    def extract_a_tree(self, forest_node):
        name, paths = forest_node
        if not paths:
            return (name, [])
        return (name, [self.extract_a_tree(p) for p in paths[0]])

    def extract_trees(self, forest):
        return [self.extract_a_tree(forest)]

A3_GRAMMAR = {
    "<start>": ["<expr>"],
    "<expr>": ["<expr>+<expr>", "<expr>-<expr>", "(<expr>)", "<integer>"],
    "<integer>": ["<digit><integer>", "<digit>"],
    "<digit>": ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
}

if __name__ == "__main__":
    syntax_diagram(A3_GRAMMAR)


if __name__ == "__main__":
    mystring = '(1+24)-33'
    parser = EarleyParser(A3_GRAMMAR)
    for tree in parser.parse(mystring):
        assert tree_to_string(tree) == mystring
        display_tree(tree)


# ### Ambiguous Parsing

if __name__ == "__main__":
    print('\n### Ambiguous Parsing')




class EarleyParser(EarleyParser):
    def extract_trees(self, forest_node):
        name, paths = forest_node
        if not paths:
            return [(name, [])]
        results = []
        for path in paths:
            ptrees = zip(*[self.extract_trees(p) for p in path])
            results.extend([(name, p) for p in ptrees])
        return results

if __name__ == "__main__":
    mystring = '12+23-34'
    parser = EarleyParser(A1_GRAMMAR)
    for tree in parser.parse(mystring):
        assert mystring == tree_to_string(tree)
        display_tree(tree)


if __name__ == "__main__":
    gf = GrammarFuzzer(A1_GRAMMAR)
    for i in range(5):
        s = gf.fuzz()
        print(i, s)
        for tree in parser.parse(s):
            assert tree_to_string(tree) == s


# ### The Aycock Epsilon Fix

if __name__ == "__main__":
    print('\n### The Aycock Epsilon Fix')




E_GRAMMAR_1 = {
    '<start>': ['<A>', '<B>'],
    '<A>': ['a', ''],
    '<B>': ['b']
}

EPSILON = ''
E_GRAMMAR = {
    '<start>': ['<S>'],
    '<S>': ['<A><A><A><A>'],
    '<A>': ['a', '<E>'],
    '<E>': [EPSILON]
}

if __name__ == "__main__":
    syntax_diagram(E_GRAMMAR)


if __name__ == "__main__":
    mystring = 'a'
    parser = EarleyParser(E_GRAMMAR)
    with ExpectError():
        trees = parser.parse(mystring)


# #### Fixpoint

if __name__ == "__main__":
    print('\n#### Fixpoint')




def fixpoint(f):
    def helper(arg):
        while True:
            sarg = str(arg)
            arg_ = f(arg)
            if str(arg_) == sarg:
                return arg
            arg = arg_

    return helper

def my_sqrt(x):
    @fixpoint
    def _my_sqrt(approx):
        return (approx + x / approx) / 2

    return _my_sqrt(1)

if __name__ == "__main__":
    my_sqrt(2)


# #### Nullable

if __name__ == "__main__":
    print('\n#### Nullable')




def rules(grammar):
    return [(key, choice)
            for key, choices in grammar.items()
            for choice in choices]

def terminals(grammar):
    return set(token
               for key, choice in rules(grammar)
               for token in choice if token not in grammar)

def nullable_expr(expr, nullables):
    return all(token in nullables for token in expr)

def nullable(grammar):
    productions = rules(grammar)

    @fixpoint
    def nullable_(nullables):
        for A, expr in productions:
            if nullable_expr(expr, nullables):
                nullables |= {A}
        return (nullables)

    return nullable_({EPSILON})

if __name__ == "__main__":
    for key, grammar in {
            'E_GRAMMAR': E_GRAMMAR,
            'E_GRAMMAR_1': E_GRAMMAR_1
    }.items():
        print(key, nullable(canonical(grammar)))


class EarleyParser(EarleyParser):
    def __init__(self, grammar, **kwargs):
        super().__init__(grammar, **kwargs)
        self.cgrammar = canonical(grammar, letters=True)
        self.epsilon = nullable(self.cgrammar)

    def predict(self, col, sym, state):
        for alt in self.cgrammar[sym]:
            col.add(State(sym, tuple(alt), 0, col))
        if sym in self.epsilon:
            col.add(state.advance())

if __name__ == "__main__":
    mystring = 'a'
    parser = EarleyParser(E_GRAMMAR)
    for tree in parser.parse(mystring):
        display_tree(tree)


# ### More Earley Parsing

if __name__ == "__main__":
    print('\n### More Earley Parsing')




# ## Testing the Parsers

if __name__ == "__main__":
    print('\n## Testing the Parsers')




def prod_line_grammar(nonterminals, terminals):
    g = {
        '<start>': ['<symbols>'],
        '<symbols>': ['<symbol><symbols>', '<symbol>'],
        '<symbol>': ['<nonterminals>', '<terminals>'],
        '<nonterminals>': ['<lt><alpha><gt>'],
        '<lt>': ['<'],
        '<gt>': ['>'],
        '<alpha>': nonterminals,
        '<terminals>': terminals
    }

    if not nonterminals:
        g['<nonterminals>'] = ['']
        del g['<lt>']
        del g['<alpha>']
        del g['<gt>']

    return g

if __name__ == "__main__":
    syntax_diagram(prod_line_grammar(["A", "B", "C"], ["1", "2", "3"]))


def make_rule(nonterminals, terminals, num_alts):
    prod_grammar = prod_line_grammar(nonterminals, terminals)

    gf = GrammarFuzzer(prod_grammar, min_nonterminals=3, max_nonterminals=5)
    name = "<%s>" % ''.join(random.choices(string.ascii_uppercase, k=3))

    return (name, [gf.fuzz() for _ in range(num_alts)])

if __name__ == "__main__":
    make_rule(["A", "B", "C"], ["1", "2", "3"], 3)


if __package__ is None or __package__ == "":
    from Grammars import unreachable_nonterminals
else:
    from .Grammars import unreachable_nonterminals


def make_grammar(num_symbols=3, num_alts=3):
    terminals = list(string.ascii_lowercase)
    grammar = {}
    name = None
    for _ in range(num_symbols):
        nonterminals = [k[1:-1] for k in grammar.keys()]
        name, expansions = \
            make_rule(nonterminals, terminals, num_alts)
        grammar[name] = expansions

    grammar[START_SYMBOL] = [name]
    
    # Remove unused parts
    for nonterminal in unreachable_nonterminals(grammar):
        del grammar[nonterminal]
    
    assert is_valid_grammar(grammar)
    
    return grammar

if __name__ == "__main__":
    make_grammar()


if __name__ == "__main__":
    for i in range(5):
        my_grammar = make_grammar()
        print(my_grammar)
        parser = EarleyParser(my_grammar)
        mygf = GrammarFuzzer(my_grammar)
        s = mygf.fuzz()
        print(s)
        for tree in parser.parse(s):
            assert tree_to_string(tree) == s
            display_tree(tree)


# ## Background

if __name__ == "__main__":
    print('\n## Background')




# ## Lessons Learned

if __name__ == "__main__":
    print('\n## Lessons Learned')




# ## Next Steps

if __name__ == "__main__":
    print('\n## Next Steps')




# ## Exercises

if __name__ == "__main__":
    print('\n## Exercises')




# ### Exercise 1: An Alternative Packrat

if __name__ == "__main__":
    print('\n### Exercise 1: An Alternative Packrat')




class PackratParser(Parser):
    def parse_prefix(self, text):
        txt, res = self.unify_key(self.start_symbol(), text)
        return len(txt), [res]

    def parse(self, text):
        remain, res = self.parse_prefix(text)
        if remain:
            raise SyntaxError("at " + res)
        return res

    def unify_rule(self, rule, text):
        results = []
        for token in rule:
            text, res = self.unify_key(token, text)
            if res is None:
                return text, None
            results.append(res)
        return text, results

    def unify_key(self, key, text):
        if key not in self.cgrammar:
            if text.startswith(key):
                return text[len(key):], (key, [])
            else:
                return text, None
        for rule in self.cgrammar[key]:
            text_, res = self.unify_rule(rule, text)
            if res:
                return (text_, (key, res))
        return text, None

if __name__ == "__main__":
    mystring = "1 + (2 * 3)"
    for tree in PackratParser(EXPR_GRAMMAR).parse(mystring):
        assert tree_to_string(tree) == mystring
        display_tree(tree)


# ### Exercise 2: More PEG Syntax

if __name__ == "__main__":
    print('\n### Exercise 2: More PEG Syntax')




# ### Exercise 3: PEG Predicates

if __name__ == "__main__":
    print('\n### Exercise 3: PEG Predicates')




# ### Exercise 4: Earley Fill Chart

if __name__ == "__main__":
    print('\n### Exercise 4: Earley Fill Chart')




# ### Exercise 5: Leo Parser

if __name__ == "__main__":
    print('\n### Exercise 5: Leo Parser')




if __name__ == "__main__":
    mystring = 'aaaaaa'


if __name__ == "__main__":
    result = EarleyParser(LR_GRAMMAR, log=True).parse(mystring)


if __name__ == "__main__":
    result = EarleyParser(RR_GRAMMAR, log=True).parse(mystring)


class LeoParser(EarleyParser):
    def complete(self, col, state):
        return self.leo_complete(col, state)

    def leo_complete(self, col, state):
        detred = self.deterministic_reduction(state)
        if detred:
            col.add(detred.copy())
        else:
            self.earley_complete(col, state)

    def deterministic_reduction(self, state):
        raise NotImplemented()

class Column(Column):
    def __init__(self, index, letter):
        self.index, self.letter = index, letter
        self.states, self._unique, self.transitives = [], {}, {}

    def add_transitive(self, key, state):
        assert key not in self.transitives
        self.transitives[key] = state
        return self.transitives[key]

class LeoParser(LeoParser):
    def uniq_postdot(self, st_A):
        col_s1 = st_A.s_col
        parent_states = [
            s for s in col_s1.states if s.expr and s.at_dot() == st_A.name
        ]
        if len(parent_states) > 1:
            return None
        matching_st_B = [s for s in parent_states if s.dot == len(s.expr) - 1]
        return matching_st_B[0] if matching_st_B else None

if __name__ == "__main__":
    lp = LeoParser(RR_GRAMMAR)
    [(str(s), str(lp.uniq_postdot(s))) for s in columns[-1].states]


class LeoParser(LeoParser):
    def get_top(self, state_A):
        st_B_inc = self.uniq_postdot(state_A)
        if not st_B_inc:
            return None

        t_name = st_B_inc.name
        if t_name in st_B_inc.e_col.transitives:
            return st_B_inc.e_col.transitives[t_name]

        st_B = st_B_inc.advance()

        top = self.get_top(st_B) or st_B
        return st_B_inc.e_col.add_transitive(t_name, top)

class LeoParser(LeoParser):
    def deterministic_reduction(self, state):
        return self.get_top(state)

if __name__ == "__main__":
    lp = LeoParser(RR_GRAMMAR)
    columns = lp.chart_parse(mystring, lp.start_symbol())
    [(str(s), str(lp.get_top(s))) for s in columns[-1].states]


if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR, log=True).parse(mystring)


RR_GRAMMAR2 = {
    '<start>': ['<A>'],
    '<A>': ['ab<A>', ''],
}
mystring2 = 'ababababab'

if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR2, log=True).parse(mystring2)


RR_GRAMMAR3 = {
    '<start>': ['c<A>'],
    '<A>': ['ab<A>', ''],
}
mystring3 = 'cababababab'

if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR3, log=True).parse(mystring3)


RR_GRAMMAR4 = {
    '<start>': ['<A>c'],
    '<A>': ['ab<A>', ''],
}
mystring4 = 'ababababc'

if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR4, log=True).parse(mystring4)


RR_GRAMMAR5 = {
    '<start>': ['<A>'],
    '<A>': ['ab<B>', ''],
    '<B>': ['<A>'],
}
mystring5 = 'abababab'

if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR5, log=True).parse(mystring5)


RR_GRAMMAR6 = {
    '<start>': ['<A>'],
    '<A>': ['a<B>', ''],
    '<B>': ['b<A>'],
}
mystring6 = 'abababab'

if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR6, log=True).parse(mystring6)


RR_GRAMMAR7 = {
    '<start>': ['<A>'],
    '<A>': ['a<A>', 'a'],
}
mystring7 = 'aaaaaaaa'

if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR7, log=True).parse(mystring7)


if __name__ == "__main__":
    result = LeoParser(LR_GRAMMAR, log=True).parse(mystring)
    for tree in result:
        print(tree_to_string(tree))


class Column(Column):
    def add_transitive(self, key, state):
        assert key not in self.transitives
        self.transitives[key] = TState(state.name, state.expr, state.dot,
                                       state.s_col, state.e_col)
        return self.transitives[key]

class TState(State):
    def copy(self):
        return TState(self.name, self.expr, self.dot, self.s_col, self.e_col)

class LeoParser(LeoParser):
    def traverse_constraints(self, st_C_name, s_3, e, r_table):
        candidates = [
            s for s in r_table[s_3].states if s.name == st_C_name
            and s.dot == len(s.expr) - 1 and s.e_col.index <= e.index
            and s.at_dot() in self.cgrammar
        ]
        if not candidates:
            return
        c_C, *empty = candidates
        assert empty == []
        e.add(c_C.advance())
        self.traverse_constraints(c_C.at_dot(), c_C.e_col.index, e, r_table)

class LeoParser(LeoParser):
    def rearrange(self, table):
        f_table = [Column(c.index, c.letter) for c in table]
        for col in table:
            for s in col.states:
                f_table[s.s_col.index].states.append(s)
        return f_table

if __name__ == "__main__":
    ep = LeoParser(RR_GRAMMAR)
    columns = ep.chart_parse(mystring, ep.start_symbol())
    r_table = ep.rearrange(columns)
    for col in r_table:
        print(col, "\n")


class LeoParser(LeoParser):
    def parse(self, text):
        cursor, states = self.parse_prefix(text)
        start = next((s for s in states if s.finished()), None)
        if cursor < len(text) or not start:
            raise SyntaxError("at " + repr(text[cursor:]))

        self.r_table = self.rearrange(self.table)
        forest = self.extract_trees(self.parse_forest(self.table, start))
        return [self.prune_tree(tree) for tree in forest]

class LeoParser(LeoParser):
    def parse_forest(self, chart, state):
        if isinstance(state, TState):
            self.traverse_constraints(state.name, state.s_col.index,
                                      state.e_col, self.r_table)
        return super().parse_forest(chart, state)

if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR).parse(mystring)
    for tree in result:
        assert mystring == tree_to_string(tree)


if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR2).parse(mystring2)
    for tree in result:
        assert mystring2 == tree_to_string(tree)


if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR3).parse(mystring3)
    for tree in result:
        assert mystring3 == tree_to_string(tree)


if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR4).parse(mystring4)
    for tree in result:
        assert mystring4 == tree_to_string(tree)


if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR5).parse(mystring5)
    for tree in result:
        assert mystring5 == tree_to_string(tree)


if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR6).parse(mystring6)
    for tree in result:
        assert mystring6 == tree_to_string(tree)


if __name__ == "__main__":
    result = LeoParser(RR_GRAMMAR7).parse(mystring7)
    for tree in result:
        assert mystring7 == tree_to_string(tree)


if __name__ == "__main__":
    result = LeoParser(LR_GRAMMAR).parse(mystring)
    for tree in result:
        assert mystring == tree_to_string(tree)


# ### Exercise 6: First Set of a Nonterminal

if __name__ == "__main__":
    print('\n### Exercise 6: First Set of a Nonterminal')




def firstset(grammar, nullable):
    first = {i: {i} for i in terminals(grammar)}
    for k in grammar:
        first[k] = {EPSILON} if k in nullable else set()
    return firstset_((rules(grammar), first, nullable))[1]

def first_expr(expr, first, nullable):
    tokens = set()
    for token in expr:
        tokens |= first[token]
        if token not in nullable:
            break
    return tokens

@fixpoint
def firstset_(arg):
    (rules, first, epsilon) = arg
    for A, expression in rules:
        first[A] |= first_expr(expression, first, epsilon)
    return (rules, first, epsilon)

if __name__ == "__main__":
    firstset(canonical(A1_GRAMMAR), EPSILON)


# ### Exercise 7: Follow Set of a Nonterminal

if __name__ == "__main__":
    print('\n### Exercise 7: Follow Set of a Nonterminal')




EOF = '\0'

def followset(grammar, start):
    follow = {i: set() for i in grammar}
    follow[start] = {EOF}

    epsilon = nullable(grammar)
    first = firstset(grammar, epsilon)
    return followset_((grammar, epsilon, first, follow))[-1]

@fixpoint
def followset_(arg):
    grammar, epsilon, first, follow = arg
    for A, expression in rules(grammar):
        f_B = follow[A]
        for t in reversed(expression):
            if t in grammar:
                follow[t] |= f_B
            f_B = f_B | first[t] if t in epsilon else (first[t] - {EPSILON})

    return (grammar, epsilon, first, follow)

if __name__ == "__main__":
    followset(canonical(A1_GRAMMAR), START_SYMBOL)


# ### Exercise 8: A LL(1) Parser

if __name__ == "__main__":
    print('\n### Exercise 8: A LL(1) Parser')




# #### Part 1: A LL(1) Parsing Table

if __name__ == "__main__":
    print('\n#### Part 1: A LL(1) Parsing Table')




class LL1Parser(Parser):
    def parse_table(self):
        self.my_rules = rules(self.cgrammar)
        self.table = ...          # fill in here to produce

    def rules(self):
        for i, rule in enumerate(self.my_rules):
            print(i, rule)

    def show_table(self):
        ts = list(sorted(terminals(self.cgrammar)))
        print('Rule Name\t| %s' % ' | '.join(t for t in ts))
        for k in self.table:
            pr = self.table[k]
            actions = list(str(pr[t]) if t in pr else ' ' for t in ts)
            print('%s  \t| %s' % (k, ' | '.join(actions)))

if __name__ == "__main__":
    for i, r in enumerate(rules(canonical(A2_GRAMMAR))):
        print("%d\t %s := %s" % (i, r[0], r[1]))


class LL1Parser(LL1Parser):
    def predict(self, rulepair, first, follow, epsilon):
        A, rule = rulepair
        rf = first_expr(rule, first, epsilon)
        if nullable_expr(rule, epsilon):
            rf |= follow[A]
        return rf

    def parse_table(self):
        self.my_rules = rules(self.cgrammar)
        epsilon = nullable(self.cgrammar)
        first = firstset(self.cgrammar, epsilon)
        # inefficient, can combine the three.
        follow = followset(self.cgrammar, self.start_symbol())

        ptable = [(i, self.predict(rule, first, follow, epsilon))
                  for i, rule in enumerate(self.my_rules)]

        parse_tbl = {k: {} for k in self.cgrammar}

        for i, pvals in ptable:
            (k, expr) = self.my_rules[i]
            parse_tbl[k].update({v: i for v in pvals})

        self.table = parse_tbl

if __name__ == "__main__":
    ll1parser = LL1Parser(A2_GRAMMAR)
    ll1parser.parse_table()
    ll1parser.show_table()


# #### Part 2: The Parser

if __name__ == "__main__":
    print('\n#### Part 2: The Parser')




class LL1Parser(LL1Parser):
    def parse_helper(self, stack, inplst):
        inp, *inplst = inplst
        exprs = []
        while stack:
            val, *stack = stack
            if isinstance(val, tuple):
                exprs.append(val)
            elif val not in self.cgrammar:  # terminal
                assert val == inp
                exprs.append(val)
                inp, *inplst = inplst or [None]
            else:
                if inp is not None:
                    i = self.table[val][inp]
                    _, rhs = self.my_rules[i]
                    stack = rhs + [(val, len(rhs))] + stack
        return self.linear_to_tree(exprs)

    def parse(self, inp):
        self.parse_table()
        k, _ = self.my_rules[0]
        stack = [k]
        return self.parse_helper(stack, inp)

    def linear_to_tree(self, arr):
        stack = []
        while arr:
            elt = arr.pop(0)
            if not isinstance(elt, tuple):
                stack.append((elt, []))
            else:
                # get the last n
                sym, n = elt
                elts = stack[-n:] if n > 0 else []
                stack = stack[0:len(stack) - n]
                stack.append((sym, elts))
        assert len(stack) == 1
        return stack[0]

if __name__ == "__main__":
    ll1parser = LL1Parser(A2_GRAMMAR)
    tree = ll1parser.parse('1+2')
    display_tree(tree)

