import re


query = 'football'

documents = [
    ['Why I love Football', 'Football is my life and ...', 'http://blah.blah/blah'],
    ['My sporting interests', 'Tennis, football and rugby are sports I love...', 'http://blah.blah/blah'],
    ['Football, football, football', 'This is a guide to the best things about...', 'http://blah.blah/blah'],
    ['Liverpool boss Jurgen Klopp believes Fabio Carvalho\'s last-gasp', 'That\'s the pain of football," said Howe.', 'https://www.bbc.co.uk/sport/football/62655347'],
    ['US Open: Andy Murray beats Emilio Nava', 'Britain''s Murray missed chances before losing a long first set but fought back to win tennis', 'https://www.bbc.co.uk/sport/tennis/62734089'],
    ['Erling Haaland: Nine goals in five games', '\'Ridiculous talent\' - football reacts to Haaland','https://www.bbc.co.uk/sport/football/62746383'],
    ['Celtic maintained their unbeaten start to the season', 'First, Stephen Welsh crashed a header off the woodwork, football football', 'https://www.bbc.co.uk/sport/football/62712765'],
    ['Emma Raducanu: US Open defeat', 'My philosophy is that there''s no point in lying to the player," he told the Tennis Majors website in January','https://www.bbc.co.uk/sport/tennis/62735291'],
    ['Arsenal maintained their 100% start to the season', 'Arsenal good value for victory football cricket', 'https://www.bbc.co.uk/sport/football/62655351'],
    ['Defender criticises former club Leicester City', 'football Fofana, 21, signed for Chelsea on a seven-year deal on Wednesday. tennis ', 'https://www.bbc.co.uk/sport/football/62742837'],
    ['The slight tactical fix for the All Blacks', 'It is clear the Argentinians are superior up front in strength in rugby', 'https://www.rugbypass.com/news/the-slight-tactical-fix-for-the-all-blacks-to-make-is-an-easy-one/'],
    ['All Blacks boost bench experience in latest team naming', 'Not a lot of rebuilding going on in this "rebuild" | Aotearoa Rugby Pod','https://www.rugbypass.com/news/all-blacks-boost-bench-experience-in-latest-team-naming/'],
    ['Tim David earns Australia call for T20 World Cup', 'natural ball-striker who will add extra batting depth to the group which has had a lot of success in T20 cricket', 'https://www.espncricinfo.com/story/men-s-t20-world-cup-2022-tim-david-earns-australia-call-for-t20-world-cup-1331876'],
    ['Manchester Originals scrape through as Josh Little spearheads fifth straight win', 'It was an amazing game of cricket,', 'https://www.espncricinfo.com/series/the-hundred-men-s-competition-2022-1299141/manchester-originals-men-vs-oval-invincibles-men-32nd-match-1299202/match-report'],
    ['what else do Bangladesh and Sri Lanka have in store', 'He has the best economy rate in world cricket among bowlers who have played at least 25 innings', 'https://www.espncricinfo.com/series/asia-cup-2022-1327237/bangladesh-vs-sri-lanka-5th-match-group-b-1327273/match-preview'],
    ['Football, Tennis and rain', 'How an Afghan soccer player and her teammates fled their homes, outran a murderous regime ', 'https://www.nytimes.com/section/sports'],
    ['Rugby, cricket and day time sleeping', 'How an Afghan soccer player and her teammates fled their homes, outran a murderous regime ', 'https://www.nytimes.com/section/sports'],
    ['Rugby, tennis and other good past times', 'How an Afghan soccer player and her teammates fled their homes, outran a murderous regime ', 'https://www.nytimes.com/section/sports'],
    ['Tennis, cricket and the iphone', 'How an Afghan soccer player and her teammates fled their homes, outran a murderous regime ', 'https://www.nytimes.com/section/sports'],
    ['Cricket, football and tennis - someone help me','How an Afghan soccer player and her teammates fled their homes, outran a murderous regime ', 'https://www.nytimes.com/section/sports'],


]


'''
AND intersection
OR  union
NOT difference

(A AND B NOT (C OR D))

'''


class AbstractSyntaxTree():

    def __init__(self, operators, operands):
        self.root = None
        self.vocab = {
            'operators':operators,
            'operands':operands
        }

    def set_root(self, node):        
        self._translate(node)
        self.root = node

    def _translate(self, node):
        if isinstance(node, Node):
            node.val = self.vocab.get('operators')[node.val]
            self._translate(node.left)
            self._translate(node.right)
        elif isinstance(node, Leaf):
            keyword, subject = self._parse_operand(node.val)
            func = self.vocab.get('operands')[keyword]
            node.val = f"{func}('{subject}')"

    def _parse_operand(self, op):

        kw = ''
        subj = ''

        for l in op:
            if l.isupper():
                kw += l
            elif l in {'(', ')'}:
                continue
            else:
                subj += l

        return kw, subj

class Node():

    def __init__(self, val):
        self.val = val
        self.parent = None
        self.left = None
        self.right = None

    def __repr__(self):
        return f"{self.val}({self.left} ,{self.right})"

class Leaf():

    def __init__(self, val):
        self.val = val
        self.parent = None

    def __repr__(self):
        return f"{self.val}"


class Interpreter():

    def __init__(self):
        self.operands = self._operands()
        self.operators = self._operators()
        self.tree = AbstractSyntaxTree(self.operators, self.operands)

    def _operators(self):
        '''
        ops is a mapping for data type: operators
        '''
        ops = {
            'AND': 'set.intersection',
            'OR': 'set.union',
            'NOT': 'set.difference'
        }
        return ops

    def _operands(self):
        '''
        '''
        ops = {
            'SELECT': 'self._select'
        }
        return ops

    def parse_syntax(self, query):
        
        operations = ''
        terms = []

        tokens = self._tokenise(query)

        for l in tokens:

            if l == '(':
                operations += l + ' '
            elif l in self.operators.keys():
                operations += l + ' '
            elif l == ')':
                operations += l + ' '
            else:
                terms.append(l)
                operations += f'SELECT({l})' + ' '

        return operations, terms

    
    def _tokenise(self, string):

        tokens = []

        in_word = False
        word = ''

        for l in string:
            if l == '(':
                tokens.append(l)
            elif l.isalnum():
                in_word = True
                word += l
            elif l.isspace():
                in_word = False
                tokens.append(word)
                word = ''
            elif  l == ')':
                if in_word:
                    in_word = False
                    tokens.append(word)
                    word = ''
                tokens.append(l)

        if in_word == True:
            tokens.append(word)

        return tokens

    def _is_operand(self, token):
        return token.startswith('SELECT')

    def _is_operator(self, token):
        return token in self.operators.keys()
    
    def translate_query(self, tokens):
        
        root = self._translate(tokens)

        self.tree.set_root(root)

        return self.tree.root

    def _translate(self, tokens, idx=0):

        prev = None
        while idx < len(tokens):
            token = tokens[idx]
            if token == '(': # Recursive call for subexpressions
                subexpr, idxx = self._translate(tokens, idx=idx+1)
                if isinstance(prev, Node):
                    prev.right = subexpr
                else:
                    prev = subexpr
                idx = idxx + 1
            elif self._is_operand(token):
                leaf = Leaf(token)
                if prev == None:
                    prev = leaf
                elif isinstance(prev, Node):
                    prev.right = leaf
                    leaf.parent = prev
                idx += 1
            elif self._is_operator(token):
                node = Node(token)
                prev.parent = node
                node.left = prev
                prev = node
                idx += 1
            elif token == ')': # Recursive termination criteria
                return prev, idx

        return prev    

class SearchEngine:


    def __init__(self, documents:list):
        self._documents = self._make_documents(documents)
        self.interpreter = Interpreter()    

    def search(self, query:str):    
  

        query, terms = self.interpreter.parse_syntax(query)
        
        self._update_tf(terms)
        
        statement = self.interpreter.translate_query(query.split())

        locals = {
            'self':self,
            'result':None
        }

        print('\n', 'Query: ', statement)

        exec(f"result = {statement}", globals(), locals)

        result = locals['result']
        docs = self._get_docs(result) 

        print('\n', 'Result: ', f'\033[1m{result}\033[0m\n')

        self._print_results(docs[:4], terms)

    def _print_results(self, results, terms):

        for r in results:
            id_ = r['id']
            title = r['title_orig']
            body = r['body_orig']
            url = r['url']

            # self._highlight_terms(title, terms)
            print('\tID: '.ljust(15), id_)
            print('\tTitle: '.ljust(15), title)
            print('\tContent: '.ljust(15), body)
            print('\tURL: '.ljust(15), url)
            print()

    
    # def _highlight_terms(self, string, terms):
        
    #     copy = string.casefold()
    #     copy = copy.translate(str.maketrans('!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~', 32*' ')) 

    #     for t in terms:
    #         while re.search(t, copy):
    #             match = re.search(t, copy)
    #             print(match.start)


    #     print(copy)
    #     print(len(copy) == len(string))


    def _filter(self, query):

        docs = []

        for d in self._documents:
            if query in d['tf'].keys() and d['tf'][query] > 0:
                docs.append(d)
        
        return sorted(docs, key=lambda x: x['tf'][query], reverse=True)

    def _select(self, query):
        
        docs = self._filter(query)

        return {d['id'] for d in docs}

    def _update_tf(self, query):
        
        for d in self._documents:

            title = d['title'] 
            body = d['body']
            url = d['url']

            for q in query:
                if q in d['tf'].keys():
                    continue
                title_count = self._count_occurence(q, title)
                body_count = self._count_occurence(q, body)            
                d['tf'][q] = title_count + body_count        


    def _count_occurence(self, query, content):

        count = 0

        for item in content:
            if item == query:
                count +=1 

        return count


    def _make_documents(self, documents):

        assert isinstance(documents, list)

        docs = []

        counter = 0

        for d in documents:
            obj = {
                'id': counter,
                'title': self._process_strings(d[0]),
                'title_orig': d[0],
                'body': self._process_strings(d[1]),
                'body_orig': d[1],
                'url': d[2],
                'tf': {}
            }

            docs.append(obj)
            counter += 1

        return docs

    def _process_strings(self, string):

        string = string.split()
        string = [s.lower().translate(str.maketrans('','','!"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~')) for s in string]

        return string

    def _get_docs(self, indices):
        if not hasattr(indices, '__iter__'):
            indices = [indices]
        return [d for d in self._documents if d['id'] in indices]






if __name__   ==  "__main__":
    se = SearchEngine(documents)

    while True:

        inp = input("query=> ")
        if inp in {'q()', 'quit()', 'exit()'}:
            exit()
        se.search(inp)
