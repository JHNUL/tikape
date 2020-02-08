import sqlite3
import queries
import constants
import utils


def connect_db() -> 'cursor':
    """Connect to db and return curson on success"""
    db = sqlite3.connect("test.db")
    db.isolation_level = None
    return db.cursor()


def start(c):
    """Start loop where user can select actions"""
    print(constants.LIST_ACTIONS)
    while True:
        print(constants.SELECT_ACTION)
        user_input = input()
        # exit loop with empty string
        if not user_input:
            c.close()
            break
        else:
            try:
                action_num = utils.cast_input(user_input)
                utils.execute_action(action_num, c)
            except Exception as i:
                print('from user loop {}'.format(i))

# c.execute("SELECT koodi, nimi FROM Paketti, Asiakas as A WHERE asiakas_id = A.id;")
# print(c.fetchall())


if __name__ == "__main__":
    try:
        c = connect_db()
        start(c)
    except Exception as inst:
        print('from main: {}'.format(inst))
