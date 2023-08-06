"""
Brandwatch Query Parser
==================
Parsing a Brandwatch Query to extract key terms that can be used to properly convey what is being searched for.
"""

import sys

from lark import Lark, Transformer, v_args, Tree
from itertools import product


bw_query_grammar = r"""
    ?start: query

    query: searchterms stopwords
    searchterms: term
    term: leafterm 
          | ored_terms
          | anded_terms
          | near_terms
          | "(" ored_terms ")"
          | "(" anded_terms ")"
          | "(" near_terms ")"
          
    near_terms: "(" leafterm "NEAR" "/" NUMBER leafterm ")"
        | "(" "(" ored_terms ")" "NEAR" "/" NUMBER leafterm ")"
        | "(" leafterm "NEAR" "/" NUMBER "(" ored_terms ")" ")"
        | "(" "(" ored_terms ")" "NEAR" "/" NUMBER "(" ored_terms ")" ")"
    
    stopwords: [ (stopword)* ]
    ored_terms: leafterm ("OR" term)+
    anded_terms: leafterm ("AND" term)+
    
    leafterm: simple_term
        | complex_term
        | mention
        | hashtag
    
    stopword: "-" leafterm
    
    hashtag: "#" WORD
    mention: "@" WORD
    simple_term: WORD
        | NUMBER
    complex_term: ESCAPED_STRING

    %import common.WORD
    %import common.ESCAPED_STRING
    %import common.NUMBER
    %import common.WS
    %ignore WS
"""

def flatten_ors(ored):
    """
     {
            "or": [
                {
                    "simple_term": "POSTPARTUM"
                },
                {
                    "or": [
                        {
                            "complex_term": "\"my newborn\""
                        },
                        {
                            "or": [
                                {
                                    "complex_term": "\"my new born\""
                                },
                                {
                                    "or": [
                                        {
                                            "simple_term": "TEST"
                                        },
                                        {
                                            "simple_term": "BLAH"
                                        }
                                    ]
                                }
                            ]
                        }
                    ]
                }
            ]
        }

    """
    if is_or_node(ored) and is_or_node(ored["or"][-1]):
        return flatten_ors({
            "or": [ored["or"][0]] + ored["or"][-1]["or"]
        })
    return ored


def is_or_node(n):
    if isinstance(n, dict) and 'or' in n:
        return True
    return False

def flatten_terms(terms):
    """ 
    [
        {
            "simple_term": "A"
        },
        {
            "simple_term": "B"
        },
        {
            "simple_term": "C"
        }
    ]
    to
    ["A", "B", "C"]
    """
    return [list(i.values())[0] if isinstance(i, dict) else i for i in terms]


def blank_permutations(within): 
    return [
        "".join([" ___"] * int(x))
        for x in range(within)
    ]

def generate_near_permutations(within, aa, bb):
    return [
        x
        for blank in blank_permutations(within)
        for x in [
            f"{aa}{blank} {bb}",
            # f"{bb}{blank} {aa}"
        ]
    ]

def near_to_or(nt): 
    return {
        "or": [
            x
            for aa, bb in product(nt["near"][0], nt["near"][2])
            for x in generate_near_permutations(int(nt["near"][1]), aa, bb)
        ]
    }

class TreeToQueryStruct(Transformer):

    def near_terms(self, x):
        """
        {
            "near": [
                {
                    "or": [
                        {
                            "simple_term": "A"
                        },
                        {
                            "simple_term": "B"
                        },
                        {
                            "simple_term": "C"
                        }
                    ]
                },
                "2",
                {
                    "simple_term": "B"
                }
            ]
        }
        """
        
        a, within, b = [flatten_ors(i) if isinstance(i, dict) else i for i in x]
        
        if is_or_node(a) and not is_or_node(b):
            a = flatten_terms(a['or'])
            b = flatten_terms([b])
        elif is_or_node(b) and not is_or_node(a):
            a = flatten_terms([a])
            b = flatten_terms(b['or'])
        elif is_or_node(a) and is_or_node(b):
            a = flatten_terms(a['or'])
            b = flatten_terms(b['or'])
        else: 
            a=flatten_terms([a])
            b=flatten_terms([b])
        print(a, b)
        return near_to_or({
            "near": [
                a,
                int(within),
                b
            ]
        })

    def searchterms(self, x):
        return {
            "searchterms": flatten_ors(x[0])
        }

    def stopwords(self, x):
        return {
            "stopwords": x
        }

    def anded_terms(self, x):
        return {
            "and": x
        }

    def ored_terms(self, x):
        return {
            "or": x
        }

    def term(self, x):
        return x[0]

    def query(self, x): 
        return x
    
    def leafterm(self, x): 
        return x[0]
    
    def stopword(self, x): 
        return {
            "stopword": x[0]
        }
    
    def hashtag(self, x): 
        return {"hashtag": str(x[0])}
    
    def mention(self, x): 
        return {"mention": str(x[0])}

    def simple_term(self, x):
        return {"simple_term": str(x[0])}

    def complex_term(self, x):
        return {"complex_term": str(x[0])}


### Create the JSON parser with Lark, using the LALR algorithm
query_parser = Lark(bw_query_grammar, parser='lalr',
                   # Using the standard lexer isn't required, and isn't usually recommended.
                   # But, it's good enough for JSON, and it's slightly faster.
                   lexer='standard',
                   # Disabling propagate_positions and placeholders slightly improves speed
                   propagate_positions=False,
                   maybe_placeholders=False,
                   # Using an internal transformer is faster and more memory efficient
                   transformer=TreeToQueryStruct())
parse = query_parser.parse


def test():
    import json
    test_query = '''
       POSTPARTUM
        OR 
        "my newborn" OR "my new born"
        OR 
        (TEST AND BLAH)
        OR 
        (A NEAR/2 B)
        OR
        ( ( A OR B OR C ) NEAR/2 D )
        OR
        ( ( 1 OR 2 OR 3 ) NEAR/5 ( 6 OR 7 ) )
        -a -b
    '''

    j = parse(test_query)
    print(j)
    print(json.dumps(j, indent=4))
    

if __name__ == '__main__':
    test()
