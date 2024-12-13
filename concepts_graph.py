import constants
import json
from math import sqrt
from query_utils import QueryUtils
from viz_utils import VizUtils

query_utils = QueryUtils(port=5433)
viz_utils = VizUtils()

concepts_map = {}
for concept in query_utils.get_concepts():
  concepts_map[concept.concept_id] = {'name': concept.name, 'level': concept.level}
       
concept_graph_query = '''select a.display_name as concept, a.level as clevel, b.display_name as ancestor, b.level as alevel from openalex.concepts_ancestors, openalex.concepts as a, openalex.concepts as b where a.id = concept_id and b.id = ancestor_id;'''
concept_graph = query_utils.execute(concept_graph_query)

with open('top_level_ancestors.json') as f:
  top_level_ancestors = json.load(f)
  with open('concepts_graph.csv', 'w') as graph_file:
    graph_file.write('source;target\n')
    with open('concepts_graph_metadata.csv', 'w') as metadata_file:
      metadata_file.write('id;size;color;label\n')
      for concept,ancestors in top_level_ancestors.items():
        for ancestor in ancestors:
          graph_file.write(f'''{ancestor} (L0);{concept}\n''')
        node_type = f'''L{concepts_map[concept]['level']}'''
        node_colour = '#%02x%02x%02x' % viz_utils.average_rgb([viz_utils.get_colour(ancestor) for ancestor in ancestors])
        metadata_file.write(f'''{concept};{6 - concepts_map[concept]['level']};{node_colour};{node_type}\n''')
      for l0_concept in constants.L0_CONCEPTS:
        colour = '#%02x%02x%02x' % viz_utils.get_colour(l0_concept)
        metadata_file.write(f'''{l0_concept} (L0);10000000;{colour};L0\n''')

print('Done.')
