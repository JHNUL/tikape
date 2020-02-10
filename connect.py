from sqlite3 import connect, PARSE_DECLTYPES
from re import match
import queries
import texts
import query_actions


def connect_db() -> 'cursor':
    """Connect to db and return curson on success"""
    db = connect("test.db", detect_types=PARSE_DECLTYPES)
    db.isolation_level = None
    return db.cursor()


def cast_input(input_str: str) -> int:
    """Check that input value is allowed, otherwise complain with raised exception."""
    input_str = str.strip(input_str)
    if match('^[1-9]{1}$', input_str) is None:
        raise Exception(texts.NUMBER_EXCEPTION)
    else:
        return int(input_str)


def main(c):
    """Start loop where user can select actions"""
    print(texts.LIST_ACTIONS)
    while True:
        print(texts.SELECT_ACTION)
        user_input = input()
        # exit loop with empty string
        if not user_input:
            c.close()
            break
        else:
            try:
                action_num = cast_input(user_input)
                query_actions.execute_action(action_num, c)
            except (Exception) as warning:
                print(warning)


if __name__ == "__main__":
    try:
        c = connect_db()
        main(c)
    except Exception as show_stopper:
        print('Error: {}'.format(show_stopper))
    finally:
        if (c):
            c.close()
