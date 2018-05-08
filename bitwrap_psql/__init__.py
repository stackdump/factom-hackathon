"""
bitwrap_psql - provies stateful event storage using postgresql

"""

from string import Template
from bitwrap_psql.postgres import ProgrammingError, connect

_DB = {}

class Storage(object):
    """ PGSQL Storage provider """

    def __init__(self, schema, **kwargs):
        global _DB

        if schema in _DB:
            self.db = _DB[schema]
        else:
            self.db = Database(schema, kwargs)
            _DB[schema] = self.db

    def commit(self, req):
        """ execute transition and persist to storage on success """

        if req['payload'] == '':
            req['payload'] = '{}'

        curr = self.db.cursor()
        sql = """
        INSERT INTO %s.events(oid, action, payload)
          VALUES('%s', '%s', '%s')
        RETURNING
          to_json((hash, oid, seq )::%s.event) as event;
        """ % (self.db.schema, req['oid'], req['action'], req['payload'], self.db.schema)

        try:
            curr.execute(sql)
            res = curr.fetchone()

            if res:
                return res[0]

        except ProgrammingError:
            if self.db.conn.error.args[3][:5] == 'value':
                return {'oid': req['oid'], '__err__': 'INVALID_OUTPUT'}

            return {'oid': req['oid'], '__err__': 'INVALID_INPUT'}


class Database(object):
    """ store """

    def __init__(self, schema, rds_config):
        self.conn = connect(**rds_config)
        self.conn.autocommit = True

        self.schema = schema
        self.states = States(self)
        self.events = Events(self)

    def cursor(self):
        """ open db transaction """
        return self.conn.cursor()

    def schema_exists(self):
        """
        test that an event-machine schema exists
        """
        cur = self.conn.cursor()

        cur.execute("""
        SELECT exists(select tablename from pg_tables where schemaname = '%s' and tablename = 'states');
        """ % self.schema)

        return cur.fetchone()[0]

    def stream_exists(self, oid):
        """
        test that a stream exists
        """
        cur = self.conn.cursor()

        cur.execute("""
        SELECT exists(select oid FROM %s.states where oid = '%s');
        """ % (self.schema, oid))

        return cur.fetchone()[0]

    def create_stream(self, oid):
        """
        create a new stream if it doesn't exist 
        """
        cur = self.conn.cursor()

        sql = """
        INSERT into %s.states (oid) values ('%s')
        """ % (self.schema, oid)

        cur.execute(sql)

        return True

class States(object):
    """ Model """

    def __init__(self, db):
        self.db = db

    def fetch(self, key):
        """ get event by eventid """

        tpl = Template("""
        SELECT
          to_json((ev.hash, st.oid, ev.action, st.rev, st.state, ev.payload, modified, created)::${name}.current_state)
        FROM
          ${name}.states st
        LEFT JOIN
          ${name}.events ev ON ev.oid = st.oid AND ev.seq = st.rev
        WHERE
          st.oid = '${oid}'
        """)

        sql = tpl.substitute(
            name=self.db.schema,
            oid=key
        )

        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchone()[0]

class Events(object):
    """ Model """

    def __init__(self, db):
        self.db = db

    def fetch(self, key):
        """ get event by eventid """

        sql = """
        SELECT
            row_to_json((hash, oid, seq, action, payload, timestamp)::%s.event_payload)
        FROM
            %s.events
        WHERE
            hash = '%s'
        ORDER BY seq DESC
        """  % (self.db.schema, self.db.schema, key)

        cursor = self.db.cursor()
        cursor.execute(sql)
        return cursor.fetchone()[0]

    def fetchall(self, key):

        sql = """
        SELECT
            row_to_json((hash, oid, seq, action, payload, timestamp)::%s.event_payload)
        FROM
            %s.events
        WHERE
            oid = '%s'
        ORDER BY seq DESC
        """  % (self.db.schema, self.db.schema, key)

        cursor = self.db.cursor()
        cursor.execute(sql)
        rows = cursor.fetchall()

        return [row[0] for row in rows]
