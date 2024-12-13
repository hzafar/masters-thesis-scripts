import jsonlines
import os
import sys

common_tails = []
size = int(sys.argv[1])

with open('concept_paths.jsonl', 'r') as infile:
  reader = jsonlines.Reader(infile)
  for paths in reader:
    longest_prefix = os.path.commonprefix(paths)
    if longest_prefix.count('->') == size:
      common_tails.append(paths)

with open(f'''common_tails_length_{size}.jsonl''', 'w') as outfile:
  writer = jsonlines.Writer(outfile)
  writer.write_all(common_tails)

print('Done.')
