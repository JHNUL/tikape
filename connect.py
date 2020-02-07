import sqlite3
import queries
import constants
import utils

def connect_db() -> 'cursor':
  """Connect to db and return curson on success"""
  db = sqlite3.connect("test.db")
  db.isolation_level = None
  return db.cursor()

# c.executescript(queries.INIT_DB)
# c.executescript(queries.SET_TEST_VALUES)

def start(c):
  print(constants.LIST_ACTIONS)
  while True:
    print(constants.SELECT_ACTION)
    user_input = input()
    if not user_input:
      break
    else:
      try:
        action_num = utils.cast_input(user_input)
        print(action_num)
      except Exception as i:
        print(i)

# c.execute("SELECT koodi, nimi FROM Paketti, Asiakas as A WHERE asiakas_id = A.id;")
# print(c.fetchall())

if __name__ == "__main__":
  try:
    c = connect_db()
    start(c)
  except Exception as inst:
    print(inst)