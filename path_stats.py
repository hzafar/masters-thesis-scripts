from collections import Counter
import constants
import csv
from hierarchy_utils import HierarchyUtils
import jsonlines
import math
import statistics

def population_stdev(counts):
  m = statistics.mean(counts)
  d = [(c - m)**2 for c in counts]
  v = sum(d) / len(counts)
  return math.sqrt(v)

def path_distribution(sd):
  if sd > 1:
    return 'imbalanced'
  elif sd > 0.5:
    return 'slightly imbalanced'
  else:
    return 'balanced'

stats = {
  'imbalanced': [],
  'slightly imbalanced': [],
  'balanced': [],
}

hierarchy = HierarchyUtils()

with open('concept_paths.jsonl', 'r') as infile:
  reader = jsonlines.Reader(infile)
  for paths in reader:
    concept             = hierarchy.get_concept(paths[0])
    ancestors           = [hierarchy.get_ancestor(path) for path in paths]
    counts              = Counter(ancestors) 
    common_tail         = hierarchy.common_tail(paths)
    common_tail_len     = common_tail.count('->')
    path_lens           = [path.count('->') for path in paths]
    sd                  = population_stdev(counts.values())
    distribution        = path_distribution(sd)
    related_ancestors   = hierarchy.related_ancestors(set(ancestors))

    stats[distribution].append(
      {
        'concept':              concept,
        'paths':                paths,
        'common_tail':          common_tail[:-2],
        'common_tail_len':      common_tail_len,
        'path_len_avg':         int(sum(path_lens) / len(path_lens)),
        'ancestor_counts':      counts,
        'related_ancestors':    related_ancestors,
        'standard_deviation':   sd,
        'path_distribution':    distribution
      }
    )
      
with open(f'''path_stats_imbalanced.jsonl''', 'w') as outfile:
  writer = jsonlines.Writer(outfile)
  writer.write_all(stats['imbalanced'])

with open(f'''path_stats_slightly_imbalanced.jsonl''', 'w') as outfile:
  writer = jsonlines.Writer(outfile)
  writer.write_all(stats['slightly imbalanced'])

with open(f'''path_stats_balanced.jsonl''', 'w') as outfile:
  writer = jsonlines.Writer(outfile)
  writer.write_all(stats['balanced'])

print('Done.')
