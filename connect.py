from sqlite3 import connect, PARSE_DECLTYPES
from re import match
import queries
import texts
import query_actions


def connect_db() -> 'cursor':
    """Connect to db and return curson on success"""
    db = connect("test.db")
    db.isolation_level = None
    return db.cursor()


def cast_input(input_str: str) -> int:
    """Check that input value is allowed, otherwise complain with raised exception."""
    input_str = str.strip(input_str)
    if match('^[1-9]{1}$', input_str) is None:
        raise Exception(texts.NUMBER_EXCEPTION)
    else:
        return int(input_str)


def main(cursor):
    """Start loop where user can select actions"""
    print(texts.LIST_ACTIONS)
    while True:
        print(texts.SELECT_ACTION)
        user_input = input()
        # exit loop with empty string
        if not user_input:
            cursor.close()
            break
        else:
            try:
                action_num = cast_input(user_input)
                query_actions.execute_action(action_num, cursor)
            except (Exception) as warning:
                if str.startswith(str(warning), "NOT NULL"):
                    print(texts.ERROR_NOT_NULL)
                elif str.startswith(str(warning), "UNIQUE"):
                    print(texts.ERROR_NOT_UNIQUE)
                else:
                    print(warning)

if __name__ == "__main__":
    try:
        cursor = connect_db()
        main(cursor)
    except Exception as show_stopper:
        print('Virhe: {}'.format(show_stopper))
    finally:
        if (cursor):
            cursor.close()
