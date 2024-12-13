import json
from math import sqrt
from query_utils import QueryUtils
import sys
from viz_utils import VizUtils

size = int(sys.argv[1])

query_utils = QueryUtils(port=5433)
viz_utils = VizUtils()

concepts_map = {}
for concept in query_utils.get_concepts():
  concepts_map[concept.concept_id] = {'name': concept.name, 'level': concept.level}

with open('top_level_ancestors.json') as f:
  top_level_ancestors = json.load(f)
  with open(f'''concepts_limited_graph_{size}.csv''', 'w') as graph_file:
    graph_file.write('source;target\n')
    with open(f'''concepts_limited_graph_metadata_{size}.csv''', 'w') as metadata_file:
      metadata_file.write('id;size;color;label\n')
      metadata_ancestors = set()
      for concept,ancestors in top_level_ancestors.items():
        if len(ancestors) != size:
          continue
        concept_name = f'''{concepts_map[concept]['name']} (L{concepts_map[concept]['level']})'''
        ancestors.sort()
        ancestor_name = f'''{'-'.join(ancestors)} (L0)'''
        graph_file.write(f'''{ancestor_name};{concept_name}\n''')
        node_type = f'''L{concepts_map[concept]['level']}'''
        node_colour = '#%02x%02x%02x' % viz_utils.average_rgb([viz_utils.get_colour(ancestor) for ancestor in ancestors])
        metadata_file.write(f'''{concept_name};{6 - concepts_map[concept]['level']};{node_colour};{node_type}\n''')
        metadata_ancestors.add(ancestor_name)
      for ancestor in metadata_ancestors:
        metadata_file.write(f'''{ancestor};100;#708090;L0\n''')

print('Done.')
