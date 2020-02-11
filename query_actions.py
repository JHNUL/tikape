import queries
import texts
from time import perf_counter


def add_tables(cursor):
    cursor.executescript(queries.INIT_DB_WITH_INDICES)
    print(texts.DATABASE_CREATED)


def add_location(cursor, params: list, output: bool = True):
    """params
        - [0] location name
    """
    cursor.execute(queries.ADD_LOCATION, params)
    if output:
        print(texts.LOCATION_ADDED)

def add_customer(cursor, params: list, output: bool = True):
    """params
        - [0] customer name
    """
    cursor.execute(queries.ADD_CUSTOMER, params)
    if output:
        print(texts.CUSTOMER_ADDED)


def add_parcel_for_customer(cursor, params: list, output: bool = True):
    """params
        - [0] parcel code
        - [1] customer name
    """
    cursor.execute(queries.GET_CUSTOMER_ID, [params[1]])
    customer_id = cursor.fetchone()
    if not customer_id:
        raise Exception(texts.ERROR_CUSTOMER_NOT_FOUND.format(params[1]))
    cursor.execute(queries.ADD_PARCEL, [params[0], customer_id[0]])
    if output:
        print(texts.PARCEL_ADDED)

def add_event(cursor, params: list, output: bool = True):
    """params
        - [0] parcel code
        - [1] location name
        - [2] event description
    """
    cursor.execute(queries.GET_PARCEL_ID, [params[0]])
    parcel_id = cursor.fetchone()
    if not parcel_id:
        raise Exception(texts.ERROR_PARCEL_NOT_FOUND.format(params[0]))
    cursor.execute(queries.GET_LOCATION_ID, [params[1]])
    location_id = cursor.fetchone()
    if not location_id:
        raise Exception(texts.ERROR_LOCATION_NOT_FOUND.format(params[1]))
    cursor.execute(queries.ADD_EVENT, [parcel_id[0], location_id[0], params[2]])
    if output:
        print(texts.EVENT_ADDED)


def get_events_for_parcel(cursor, params: list, output: bool = True):
    """params
        - [0] parcel code
    """
    cursor.execute(queries.GET_EVENTS_FOR_PARCEL, params)
    if output:
        results = cursor.fetchall()
        for res in results:
            print(', '.join(res))


def get_parcels_for_customer(cursor, params: list, output: bool = True):
    """params
        - [0] customer name
    """
    cursor.execute(queries.GET_PARCELS_FOR_CUSTOMER, params)
    if output:
        results = cursor.fetchall()
        for res in results:
            print('{}, {} tapahtumaa'.format(res[0], res[1]))


def get_events_per_location_and_date(cursor, params: list, output: bool = True):
    """params
        - [0] location name
        - [1] date
    """
    cursor.execute(queries.GET_EVENTS_PER_DATE, params)
    if output:
        result = cursor.fetchone()
        print('Tapahtumien määrä: {}'.format(result[0]))


def performance_test(cursor):
    """ Tests database efficiency by performing multiple queries.
        Each step is timed with perf_counter()
    """
    cursor.execute(queries.BEGIN_TRANSACTION)
    # step 1: add 1000 locations
    start = perf_counter()
    for x in range(1000):
        add_location(cursor, ['P{}'.format(x+1)], False)
    stop = perf_counter()
    print('Vaihe 1: {} s'.format(stop-start))

    # step 2: add 1000 customers
    start = perf_counter()
    for x in range(1000):
        add_customer(cursor, ['A{}'.format(x+1)], False)
    stop = perf_counter()
    print('Vaihe 2: {} s'.format(stop-start))

    # step 3: add 1000 parcels
    start = perf_counter()
    for x in range(1000):
        add_parcel_for_customer(cursor, ['ITEM{}'.format(x+1), 'A{}'.format(x+1)], False)
    stop = perf_counter()
    print('Vaihe 3: {} s'.format(stop-start))

    # step 4: add 1000000 events
    start = perf_counter()
    for x in range(1000000):
        add_event(cursor, ['ITEM{}'.format((x % 1000)+1), 'P{}'.format((x % 1000)+1), 'foo'], False)
    stop = perf_counter()
    print('Vaihe 4: {} s'.format(stop-start))
    cursor.execute(queries.COMMIT)

    # step 5: do 1000 queries for a customer's parcels
    start = perf_counter()
    for x in range(1000):
        cursor.execute(queries.GET_PARCEL_COUNT_FOR_CUSTOMER, ['CUST{}'.format(x+1)])
        cursor.fetchone()
    stop = perf_counter()
    print('Vaihe 5: {} s'.format(stop-start))

    # step 6: do 1000 queries for a parcel's events
    start = perf_counter()
    for x in range(1000):
        get_events_for_parcel(cursor, ['ITEM{}'.format(x+1)], False)
        cursor.fetchall()
    stop = perf_counter()
    print('Vaihe 6: {} s'.format(stop-start))


def execute_action(action_num: int, cursor):
    """Map input number to correct action and execute it with params when applicable"""
    action_mapper = {
        1: [add_tables],
        2: [add_location, texts.PROMPT_LOCATION_NAME],
        3: [add_customer, texts.PROMPT_CUSTOMER_NAME],
        4: [add_parcel_for_customer, texts.PROMPT_PARCEL_CODE, texts.PROMPT_CUSTOMER_NAME],
        5: [add_event, texts.PROMPT_PARCEL_CODE, texts.PROMPT_EVENT_LOCATION, texts.PROMPT_EVENT_DESCRIPTION],
        6: [get_events_for_parcel, texts.PROMPT_PARCEL_CODE],
        7: [get_parcels_for_customer, texts.PROMPT_CUSTOMER_NAME],
        8: [get_events_per_location_and_date, texts.PROMPT_LOCATION_NAME, texts.PROMPT_DATE],
        9: [performance_test]
    }
    action = action_mapper.get(action_num)
    if len(action) > 1:
        params = []
        for prompt in action[1:]:
            print(prompt)
            user_input = input() or None
            params.append(user_input)
        action[0](cursor, params)
    else:
        action[0](cursor)
