"""Simple wrapper around psycopg2 library.

A wrapper around psycopg2 library to simplify using the database operations.
For SELECT operation it returns a list of dicts.
For UPDATE, DELETE it stores affected rows in affected_row member variable.

Typical usage example:

from pypgdb import pgdb
import logging
db = pgdb.PGDB("host=127.0.0.1 dbname=my_db port=5432 user=myUser password=myPassword")
pgdb.logger.setLevel(logging.INFO)
res = db.query("SELECT 'hello world'::TEXT, NOW()")

"""
import psycopg2
import psycopg2.extras
import psycopg2.extensions
import logging

logger = logging.getLogger("pgdb_log")
logger.setLevel(logging.NOTSET)
ch = logging.StreamHandler()
ch.setFormatter(logging.Formatter(
    fmt='[%(asctime)s] - [%(name)s] - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S')
)
logger.addHandler(ch)


class PGDB:
    """Wrapper around psycopg2 library.

    Stores connection, cursor and connection string to simplify usage of psycopg2.
    The connection is established after the very first query.

    Attributes:
        _conn_string: Connection string to establish a connection to database.
            It should contain host, port, database name, user and password. See `Typical usage example`
            in module docstring.
        _db: Connection object for database session.
        _cursor: Cursor object for connection.
        affected_rows: Number of affected rows for the last query.
    """

    def __init__(self, conn_str=None):
        """c-tor

        Args:
            conn_str: Connection string for database connection.
        """
        if conn_str is not None:
            self._conn_string = conn_str

        self._db = None
        self._cursor = None
        self.affected_rows = 0

    def __del__(self):
        self.close()

    def open(self):
        """Creates connection and grabs cursor for it.

        Connects to database using connection string stored in object and grabs connection and cursor objects.

        Returns:
            (bool): Status of the connection - True if it succeed.

        Raises:
            Exception: An error occurred when trying to connect while connection is active.
        """
        if self._db is not None:
            logger.error("PGDB already connected to {}".format(self._db.info.host))
            raise Exception("PGDB already connected to " + self._db.info.host)

        self._db = psycopg2.connect(self._conn_string)
        self._cursor = self._db.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        logger.info("PGDB connected to {}".format(self._db.info.host))
        return self._db.status == psycopg2.extensions.STATUS_READY

    def close(self):
        """Closes connection to database

        Closes connection and clearing stored data for it.

        Returns:

        """
        if self._db is None:
            return

        self._cursor.close()
        self._db.close()

        self._db = None
        self._cursor = None
        self.affected_rows = 0
        logger.info("PGDB disconnected")

    def query(self, sql, params=None):
        """Performs SQL query

        Performs SQL query with given parameters. If it is the very first query for this connection
        it opens connection first. Sets affected rows for this query and returns a list of dicts for it if needed.

        Args:
            sql: SQL query string.
            params: Optional parameters for query.

        Returns:
            If cursor description is not None the method returns list of dicts.
            If it is None it returns True if number of affected rows by SQL is greater than 0.
            Otherwise it returns False.

        Raises:
            TypeError: An error occurred when params argument is not of type dict or tuple.
        """
        if self._db is None:
            self.open()

        if params is not None and type(params) not in (dict, tuple):
            logger.error("Parameter `params` must be dict or tuple type. {} given.".format(str(type(params))))
            raise TypeError("Parameter `params` must be dict or tuple type")

        try:
            self._cursor.execute(sql) if params is None else self._cursor.execute(sql, params)
        except:
            if self._db:
                self._db.rollback()
            logger.error("Error during executing a query.\nSQL:\n{}\nparams:\n{}".format(sql, params))
            raise
        else:
            self._db.commit()
        self.affected_rows = self._cursor.rowcount

        logger.info("Query succeed. Affected rows: {}".format(str(self.affected_rows)))

        if self._cursor.description:
            return self._cursor.fetchall()

        if self.affected_rows > 0:
            return True
        return False
