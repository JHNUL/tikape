import queries
import texts
from time import perf_counter


def no_op(cursor):
    pass


def add_tables(cursor):
    cursor.executescript(queries.INIT_DB)


def add_location(cursor, params):
    cursor.execute(queries.ADD_LOCATION, params)


def add_customer(cursor, params):
    cursor.execute(queries.ADD_CUSTOMER, params)


def add_parcel(cursor, params):
    cursor.execute(queries.ADD_PARCEL, params)


def add_event(cursor, params):
    cursor.execute(queries.ADD_EVENT, params)


def get_events_for_parcel(cursor, params):
    cursor.execute(queries.GET_EVENTS_FOR_PARCEL, params)
    print(cursor.fetchall())


def get_parcels_for_customer(cursor, params):
    cursor.execute(queries.GET_PARCELS_FOR_CUSTOMER, params)
    print(cursor.fetchall())


def get_events_per_date(cursor, params):
    cursor.execute(queries.GET_EVENTS_PER_DATE, params)
    print(cursor.fetchall())


def performance_test(cursor):
    """ Tests database configuration efficiency by performing multiple queries.
        Each step is timed with perf_counter()
    """
    cursor.execute(queries.BEGIN_TRANSACTION)
    start = perf_counter()
    for x in range(1000):
        cursor.execute(queries.ADD_LOCATION, ['P{}'.format(x+1)])
    stop = perf_counter()
    print('Vaihe 1: {} s'.format(stop-start))
    start = perf_counter()
    for x in range(1000):
        cursor.execute(queries.ADD_CUSTOMER, ['A{}'.format(x+1)])
    stop = perf_counter()
    print('Vaihe 2: {} s'.format(stop-start))
    start = perf_counter()
    for x in range(1000):
        cursor.execute(queries.ADD_PARCEL, [
                       'ITEM{}'.format(x+1), 'A{}'.format(x+1)])
    stop = perf_counter()
    print('Vaihe 3: {} s'.format(stop-start))
    start = perf_counter()
    for x in range(1000000):
        cursor.execute(queries.ADD_EVENT, [
            'ITEM{}'.format((x % 1000)+1),
            'P{}'.format((x % 1000)+1),
            'foo'
        ])
    stop = perf_counter()
    print('Vaihe 4: {} s'.format(stop-start))
    cursor.execute(queries.COMMIT)
    start = perf_counter()
    for x in range(1000):
        cursor.execute(queries.GET_PARCELS_FOR_CUSTOMER, ['A{}'.format(x+1)])
    stop = perf_counter()
    print('Vaihe 5: {} s'.format(stop-start))
    start = perf_counter()
    for x in range(1000):
        cursor.execute(queries.GET_EVENTS_FOR_PARCEL, ['ITEM{}'.format(x+1)])
    stop = perf_counter()
    print('Vaihe 6: {} s'.format(stop-start))


def execute_action(action_num: int, cursor):
    """Map input number to correct action and execute it with params when applicable"""
    action_mapper = {
        0: [no_op],
        1: [add_tables],
        2: [add_location, texts.PROMPT_LOCATION_NAME],
        3: [add_customer, texts.PROMPT_CUSTOMER_NAME],
        4: [add_parcel, texts.PROMPT_PARCEL_CODE, texts.PROMPT_CUSTOMER_NAME],
        5: [add_event, texts.PROMPT_PARCEL_CODE, texts.PROMPT_EVENT_LOCATION, texts.PROMPT_EVENT_DESCRIPTION],
        6: [get_events_for_parcel, texts.PROMPT_PARCEL_CODE],
        7: [get_parcels_for_customer, texts.PROMPT_CUSTOMER_NAME],
        8: [get_events_per_date, texts.PROMPT_LOCATION_NAME, texts.PROMPT_DATE],
        9: [performance_test]
    }
    action = action_mapper.get(action_num, 0)
    if len(action) > 1:
        params = []
        for prompt in action[1:]:
            print(prompt)
            user_input = input()
            params.append(user_input)
        action[0](cursor, params)
    else:
        action[0](cursor)
