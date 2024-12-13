import constants
from itertools import zip_longest
from query_utils import QueryUtils
import json
import jsonlines

query_utils = QueryUtils(port=5433)

def find_paths(concept_id):
  concept_info  = query_utils.get_concept(concept_id)
  concepts      = [concept_info]
  all_paths     = {concept_info.name: set([concept_info.name])}
  
  while concepts:
    concept = concepts.pop()
    parents = query_utils.get_parents(concept.concept_id, concept.level)
    for parent in parents:
      existing = all_paths[concept.name]
      added = set([e + '->' + parent.name for e in existing])
      if parent.name in all_paths:
        all_paths[parent.name] = all_paths[parent.name].union(added.copy())
      else:
        all_paths[parent.name] = added.copy()
      concepts.append(parent)

  return [path for (root, paths) in all_paths.items() for path in paths if root in constants.L0_CONCEPTS]

with open('top_level_ancestors.json') as f:
  top_level_ancestors = json.load(f)
  with open(f'''concept_paths.jsonl''', 'w') as outfile:
    writer = jsonlines.Writer(outfile)
    for concept,ancestors in top_level_ancestors.items():
      if len(ancestors) < 2:
        continue

      paths = find_paths(concept)
      writer.write(paths)

print('Done.')
