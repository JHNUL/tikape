import re
import queries

def cast_input(input_str: str) -> int:
    """Check that input value is allowed, otherwise complain with raised exception."""
    input_str = str.strip(input_str)
    if re.match('^[0-9]{1}$', input_str) is None:
        raise Exception('Input values must be between 0-9')
    else:
        return int(input_str)

def no_op(cursor):
    cursor.execute(queries.PAIKAT)
    print('{}'.format('PAIKAT:'))
    print('{}'.format(cursor.fetchall()))
    cursor.execute(queries.ASIAKKAAT)
    print('{}'.format('ASIAKKAAT:'))
    print('{}'.format(cursor.fetchall()))
    cursor.execute(queries.TAPAHTUMAT)
    print('{}'.format('TAPAHTUMAT:'))
    print('{}'.format(cursor.fetchall()))
    cursor.execute(queries.PAKETIT)
    print('{}'.format('PAKETIT:'))
    print('{}'.format(cursor.fetchall()))


def add_tables(cursor):
    cursor.executescript(queries.INIT_DB)

def add_location(cursor, location):
    cursor.execute(queries.ADD_LOCATION, location)
    print('Paikka lisätty id:llä {}'.format(cursor.lastrowid))

def add_customer(cursor, name):
    cursor.execute(queries.ADD_CUSTOMER, name)
    print('Asiakas lisätty id:llä {}'.format(cursor.lastrowid))

def add_parcel(cursor, params):
    cursor.execute(queries.ADD_PARCEL, params)
    print('Paketti lisätty id:llä {}'.format(cursor.lastrowid))

def add_event(cursor, params):
    cursor.execute(queries.ADD_EVENT, params)
    print('Tapahtuma lisätty id:llä {}'.format(cursor.lastrowid))

def get_events_for_parcel(cursor, code):
    cursor.execute(queries.GET_EVENTS_FOR_PARCEL, code)
    print('{}'.format(cursor.fetchall()))

def get_parcels_for_customer(cursor, name):
    cursor.execute(queries.GET_PARCELS_FOR_CUSTOMER, name)
    print('{}'.format(cursor.fetchall()))

def execute_action(action_num: int, cursor):
    """Map input number to correct action and execute it with args when applicable"""
    action_mapper = {
        0: [no_op],
        1: [add_tables],
        2: [add_location, 'Anna paikan nimi:'],
        3: [add_customer, 'Anna asiakkaan nimi:'],
        4: [add_parcel, 'Anna paketin koodi:', 'Anna paketin asiakas:'],
        5: [add_event, 'Anna paketin koodi:', 'Anna tapahtuman paikka:', 'Anna tapahtuman kuvaus:'],
        6: [get_events_for_parcel, 'Anna paketin koodi:'],
        7: [get_parcels_for_customer, 'Anna asiakkaan nimi:']
    }
    action = action_mapper.get(action_num, 0)
    if len(action) > 1:
        params = []
        for prompt in action[1:]:
            print('{}'.format(prompt))
            user_input = input()
            params.append(user_input)
        action[0](cursor, params)
    else:
        action[0](cursor)
