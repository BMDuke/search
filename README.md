# Search Engine
This is a small script which implements a basic seach engine. The search engine is available via a read-eval-print-loop, for example:
```
query=> soccer

 Query:  self._select('soccer')

 Result:  {15, 16, 17, 18, 19}

    ID:            15
	Title:         Football, Tennis and rain
	Content:       How an Afghan soccer player and her teammates fled their homes
	URL:           https://www.nytimes.com/section/sports

	...

```
This works by defining a small langauge and mapping its keyword and primitives to underlying python functions. Queries are parsed in multiple phases and eventually translated into python, which is finally executed. 
<br><br>Keywords in this basic query langauge are the logical operators (capitalised). Primitives are search strings eg 'football'.



## NOTE:
- Logical operators 'AND', 'OR' , 'NOT' <b>MUST</b> be uppercase
- Arguments <b>MUST</b> all be lowercase

## Usage
### Project setup
```
cd ~/Desktop
mkdir search_engine
cd search_engine
git clone https://github.com/BMDuke/search.git
cd search
pip install -r requirements.txt
```

### Start the program
```
python search_engine.py
```

### Stop the program
```
query=> quit()
```

### Query documents
The query langauge is a custom language used to express set logic for search.

#### Search
```
query=> [ keyword ]
```

Example:
```
query=> soccer

...

query=> andy
```
#### AND
Logical AND is available by using the keyword 'AND'

```
query=> [ keyword 1 ] AND [ keyword 2 ]
```

Example:

```
query=> game AND win

...
```

#### OR 
Logical OR is available using the 'OR' keyword

```
query=> [ keyword 1 ] OR [ keyword 2 ]
```
Example:
```
query=> win OR draw
```

#### NOT
Logical NOT is available using the 'NOT' keyword

```
query=> [ keyword 1 ] NOT [ keyword 2 ]
```
Example:
```
query=> rugby NOT football
```

#### Complex Queries
More complex queries are supported with the use of brackets to indicate subexpressions

```
query=> football OR rugby NOT (manchester OR liverpool)
```
```
query=> football OR rugby NOT (manchester OR (tactical OR tennis))
```

Braces must be used to indicate subexpressions
