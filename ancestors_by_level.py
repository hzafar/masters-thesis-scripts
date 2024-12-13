import csv
from query_utils import QueryUtils

query_utils = QueryUtils(port=5433)

for level in range(1, 6):
  concepts = query_utils.get_concepts_by_level(level)

  with open(f'''level_{level}_concept_ancestors_counts.csv''', 'w') as f:
    fieldnames = ['id', 'display_name', 'ancestors_count', 'children_count']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
  
    for concept in concepts:
      ancestors_count_query = f'''select count(*) from openalex.concepts_ancestors where concept_id = '{concept.concept_id}';'''
      ancestors_count = query_utils.execute(ancestors_count_query)[0]

      children_count_query = f'''select count(*) from openalex.concepts_ancestors where ancestor_id = '{concept.concept_id}';'''
      children_count = query_utils.execute(children_count_query)[0]

      writer.writerow({'id': concept.concept_id, 'display_name': concept.name, 'ancestors_count': ancestors_count[0], 'children_count': children_count[0]})
    
print('Done.')
