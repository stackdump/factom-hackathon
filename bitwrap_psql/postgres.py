from string import Template
import pg8000
ProgrammingError = pg8000.core.ProgrammingError

UNSIGNED_MAX = 65536

def connect(**kwargs):
    return pg8000.connect(
        host=kwargs['pg-host'],
        user=kwargs['pg-username'],
        password=kwargs['pg-password'],
        database=kwargs['pg-database'],
        timeout=5
    )

def drop_schema(schema, **kwargs):
    "" ""
    conn = connect(**kwargs)
    conn.autocommit = True
    txn = conn.cursor()

    def try_execute(sql):
        try:
            txn.execute(sql)
        except:
            print('__SQL_ERR__')
            print(sql)

    try_execute("DROP SCHEMA IF EXISTS %s" % schema)


def create_schema(machine, **kwargs):
    """ add a new schema to an existing db """

    schema = kwargs.get('schema_name', machine.name)

    conn = connect(**kwargs)
    conn.autocommit = True
    txn = conn.cursor()

    txn.execute("""
    CREATE schema %s
    """ % schema)


    txn.execute("""
    CREATE DOMAIN %s.token as smallint CHECK(VALUE >= 0 and VALUE <= %i)
    """ % (schema, UNSIGNED_MAX))

    num_places = len(machine.machine['state'])
    columns = [''] * num_places
    vector = [''] * num_places
    delta = [''] * num_places

    for key, props  in  machine.net.places.items():
        i = props['offset']
        columns[i] = ' %s %s.token' % (key, schema)
        vector[i] = ' %s int4' % key
        delta[i] = " (state).%s + txn.%s" % (key, key)

    txn.execute("""
    CREATE TYPE %s.state as ( %s )
    """ % (schema, ','.join(columns)))

    txn.execute("""
    CREATE TYPE %s.vector as ( %s )
    """ % (schema, ','.join(vector)))

    txn.execute("""
    CREATE TYPE %s.event as (
      id varchar(32),
      oid varchar(255),
      rev int4
    )
    """ % (schema))

    txn.execute("""
    CREATE TYPE %s.event_payload as (
      id varchar(32),
      oid varchar(255),
      seq int4,
      action varchar(255),
      payload json,
      timestamp timestamp
    )
    """ % (schema))

    txn.execute("""
    CREATE TYPE %s.current_state as (
      id varchar(32),
      oid varchar(255),
      action varchar(255),
      rev int4,
      state %s.state,
      payload json,
      modified timestamp,
      created timestamp
    )
    """ % (schema, schema))

    initial_vector = machine.net.initial_vector()

    # KLUDGE: this seems to be a limitation of how default values are declared
    # this doesn't work when state vector has only one element
    # state %s.state DEFAULT (0), # FAILS
    # state %s.state DEFAULT (0,0), # WORKS
    if len(initial_vector) < 2:
        raise Exception('state vector must be an n-tuple where n >= 2')

    txn.execute("""
    CREATE TABLE %s.states (
      oid VARCHAR(256) PRIMARY KEY,
      rev int4 default 0,
      state %s.state DEFAULT %s::%s.state,
      created timestamp DEFAULT now(),
      modified timestamp DEFAULT now()
    );
    """ % (schema, schema, tuple(initial_vector), schema))

    txn.execute("""
    CREATE TABLE %s.transitions (
      action VARCHAR(255) PRIMARY KEY,
      vector %s.vector
    );
    """ % (schema, schema))

    for key, props  in  machine.net.transitions.items():
        txn.execute("""
        INSERT INTO %s.transitions values('%s', %s)
        """ % (schema, key, tuple(props['delta'])))

    txn.execute("""
    CREATE TABLE %s.events (
      oid VARCHAR(255) REFERENCES %s.states(oid) ON DELETE CASCADE ON UPDATE CASCADE,
      seq SERIAL,
      action VARCHAR(255) NOT NULL,
      payload jsonb DEFAULT '{}',
      hash VARCHAR(32) NOT NULL,
      timestamp timestamp DEFAULT NULL
    );
    """ % (schema, schema))

    txn.execute("""
    ALTER TABLE %s.events ADD CONSTRAINT %s_oid_seq_pkey PRIMARY KEY (oid, seq);
    """ % (schema, schema))

    txn.execute("""
    CREATE INDEX CONCURRENTLY %s_hash_idx on %s.events (hash);
    """ % (schema, schema))


    function_template = Template("""
    CREATE OR REPLACE FUNCTION ${name}.vclock() RETURNS TRIGGER
    AS $MARKER
        DECLARE
            txn ${name}.vector;
            revision int4;
        BEGIN
            SELECT
                (vector).* INTO STRICT txn
            FROM
                ${name}.transitions
            WHERE
                action = NEW.action;

            UPDATE
              ${name}.states set 
                state = ( ${delta} ),
                rev = rev + 1,
                modified = now()
            WHERE
              oid = NEW.oid
            RETURNING
              rev into STRICT revision;

            NEW.seq = revision;
            NEW.hash = md5(row_to_json(NEW)::TEXT);
            NEW.timestamp = now();

            RETURN NEW;
        END
    $MARKER LANGUAGE plpgsql""")
    
    fn_sql = function_template.substitute(
        MARKER='$$',
        name=schema,
        var1='$1',
        var2='$2',
        var3='$3',
        delta=','.join(delta)
    )

    txn.execute(fn_sql)

    function_template = Template("""
    CREATE TRIGGER ${name}_dispatch
    BEFORE INSERT on ${name}.events
      FOR EACH ROW EXECUTE PROCEDURE ${name}.vclock();
    """)

    trigger_sql = function_template.substitute(name=schema)
    txn.execute(trigger_sql)
