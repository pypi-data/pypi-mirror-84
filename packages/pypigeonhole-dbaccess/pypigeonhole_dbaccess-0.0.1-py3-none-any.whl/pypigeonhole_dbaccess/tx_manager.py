import contextlib
import threading


# local / connection based transaction manager. This is for 2 DAOs in the same
# database. Work for nested transactions.
#
# Global transaction is not supported. These transaction manager works across
# multiple connections for different databases or across database and
# messaging. These need extra work with underlying support. Java has JTA
# support, Python doesn't have.

# Decorator is a wild jump in this case, since it's a crosscut mechanism
# without context knowledge(conneciton in this case). So a context is more
# reasonable.
class LocalTransactionManager:
    tx_tc = threading.local()
    tx_tc.count = {}

    def __init__(self, db_conn):
        self._db_conn = db_conn
        self._old_state = db_conn.autocommit
        db_conn.autocommit = False

    def _inc_count(self):
        counter = self.tx_tc.count.get(id(self._db_conn), 0)
        self.tx_tc.count[id(self._db_conn)] = counter + 1  # one layer down

    def _dec_count(self):
        counter = self.tx_tc.count.get(id(self._db_conn), 0)
        self.tx_tc.count[id(self._db_conn)] = counter - 1  # one layer up

    def __enter__(self):
        self._inc_count()
        return self

    def rollback(self):
        self.tx_tc.count[id(self._db_conn)] = 0
        self._db_conn.rollback()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self._dec_count()

        if self.tx_tc.count.get(id(self._db_conn), 0) == 0:
            self._db_conn.commit()
            self._db_conn.autocommit = self._old_state

        return False  # do not swallow exception


# for with ... as
@contextlib.contextmanager
def transact(db_conn):
    txm = LocalTransactionManager(db_conn)
    try:
        txm.__enter__()
        yield txm
        txm.__exit__(None, None, None)
    except Exception as e:
        txm.rollback()
        raise e
