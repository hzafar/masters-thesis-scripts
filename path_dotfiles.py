import csv
from queryutils import QueryUtils
import sys

query_utils = QueryUtils(port=5433)
concept_info = query_utils.get_concept(sys.argv[1])
concepts = [concept_info]
visited = set()
paths = []

while concepts:
  concept   = concepts.pop()
  parents   = query_utils.get_parents(c.concept_id, c.level)

  for parent in parents:
    paths.append({'source': '"' + parent.name.replace(' ', '\\n') + '"', 'target': '"' + concept.name.replace(' ', '\\n') + '"'})
    if parent.concept_id not in visited:
      concepts.append(parent)
    visited.add(parent.concept_id)

print('digraph {')
print('\trank="LR"')
#print('\tbgcolor="transparent"')
edges = set([e['source'] for e in paths] + [e['target'] for e in paths])
for edge in edges:
  print(f'''\t{edge} [fontname="Comic Sans", shape=egg, penwidth=2];''')
for edge in paths:
  print(f'''\t{edge['source']} -> {edge['target']} [penwidth=1.5, arrowhead=none]''')
print('}')
