import json
from query_utils import QueryUtils
import sys

query_utils = QueryUtils(port=5433)
concepts_map = {}
for concept in query_utils.get_concepts():
  concepts_map[concept.concept_id] = concept.to_dict()

with open('top_level_ancestors.json') as f:
  parents = json.load(f)

result = []
group = set(sys.argv[1:])

for concept, ancestors in parents.items():
  if group.intersection(ancestors) == group:
    result.append(concepts_map[concept])

print(f'''Found {len(result)} concepts with {', '.join(group)} as top-level ancestors''', file=sys.stderr)
print(json.dumps(result, indent=4))

print('Done.')
