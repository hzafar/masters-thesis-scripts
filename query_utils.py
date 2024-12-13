from dataclasses import dataclass
import psycopg2

@dataclass
class ConceptInfo:
  """Class to represent simple concept information."""

  concept_id: str
  name: str
  level: int
  description: str

  def to_dict(self):
    return {
      'concept_id': self.concept_id,
      'name': self.name,
      'level': self.level,
      'description': self.description
    }
  

class QueryUtils:
  def __init__(self, database: str = 'postgres', user: str = 'postgres', host: str = 'localhost', port: int = 5432):
    self.conn = psycopg2.connect(f'''dbname={database} user={user} host={host} port={port}''')

  def execute(self, query):
    with self.conn.cursor() as cur:
      cur.execute(query)
      result = cur.fetchall()

    return result

  def get_parents(self, concept, level):
    q = f'''select ancestor_id, display_name, level, description from openalex.concepts, openalex.concepts_ancestors where level = {level - 1} and concepts.id = ancestor_id and concept_id = '{concept}';'''
    with self.conn.cursor() as cur:
      cur.execute(q)
      result = cur.fetchall()

    return [ConceptInfo(r[0], r[1], int(r[2]), r[3]) for r in result]

  def get_concept(self, concept):
    q = f'''select id, display_name, level, description from openalex.concepts where concepts.id = '{concept}';'''
    with self.conn.cursor() as cur:
      cur.execute(q)
      result = cur.fetchone()
  
    return ConceptInfo(result[0], result[1], int(result[2]), result[3])

  def get_concepts(self):
    q = 'select id, display_name, level, description from openalex.concepts;'
    with self.conn.cursor() as cur:
      cur.execute(q)
      result = cur.fetchall()

    return [ConceptInfo(r[0], r[1], int(r[2]), r[3]) for r in result]

  def get_concepts_by_level(self, level):
    q = f'''select id, display_name, description from openalex.concepts where level = {level} order by display_name;'''
    with self.conn.cursor() as cur:
      cur.execute(q)
      result = cur.fetchall()

    return [ConceptInfo(r[0], r[1], level, r[2]) for r in result]

