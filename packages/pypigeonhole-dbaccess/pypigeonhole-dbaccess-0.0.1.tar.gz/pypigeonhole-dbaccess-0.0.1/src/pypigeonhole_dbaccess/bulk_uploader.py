import pandas
import numpy
import math

import pypigeonhole_simple_utils.simple.simple_log as simple_log
import pypigeonhole_simple_utils.simple.simple_timer as simple_timer

logger = simple_log.get_logger(__name__)

SQL_TRUNCATE_TBL = 'TRUNCATE TABLE '
SQL_DROP_TBL = 'DROP TABLE '
SQL_CREATE_TBL = 'CREATE TABLE '


# The first choice for uploading large amount of data is always database
# bulk load tools, because they are generally faster. This tool works slower
# but universal to all SQL based databases. It's built on top of SQL and
# ODBC.
def sql_upload(conn, tbl_name: str, data_df: pandas.DataFrame, if_exist='truncate',
               use_df_type=False, batch_size=70, sql_chunk_size=100):
    """
    This method uses fast_executemany way to execute many values.

    Pack many rows of data to one insert sql statement:
    insert into <table> (?, ?, ..., ?) values (...), (...), ..., (...)
    the number of rows is controlled by sql_chunk_size.

    Then pack many such sql statements into one batch. The number of statements
    is controlled by batch_size.

    PyODBC uses executemany() instead of packing many values in one SQL.

    Packing too little data (1 row and 1 statement) suffers from network
    traffic overhead. Packing too much data suffers from server handling.
    Each database has different sweet spot. Some database has data restriction
    too, e.g., microsoft sql server has a limit of 2100 parameter value limit.
    """
    with simple_timer.PerfBenchmark(tbl_name + ' loading', logger.info) as pbm:
        logger.info('if_exist flag: ' + if_exist)

        conn_am = conn.autocommit
        try:
            conn.autocommit = False
            cursor = conn.cursor()
            cursor.fast_executemany = True
            _ensure_table(cursor, data_df, if_exist, pbm, tbl_name, use_df_type)

            insert_sql = _gen_insert_sql(data_df, tbl_name)

            logger.info('data chunk size: {0}'.format(batch_size * sql_chunk_size))
            num_rows = data_df.shape[0]
            tail_sql_size = num_rows % sql_chunk_size
            tail_start = num_rows - tail_sql_size
            params = []
            batch_count = 0
            for i in range(tail_start):  # full size batch
                _add_row_to_sql_data(params, data_df.iloc[i])

                if (i+1) % sql_chunk_size == 0:  # one sql insert with many values
                    cursor.executemany(insert_sql, params)
                    # cursor.execute(insert_sql, params[0])
                    params = []

                    if batch_count == batch_size:
                        cursor.commit()
                        pbm.print('executed batch: ' + str(i // (batch_count * sql_chunk_size)))
                        batch_count = 0
                    batch_count += 1

            if batch_count > 0:
                cursor.commit()
                pbm.print('executed leftover batch: size=' + str(batch_count))

            if tail_sql_size > 0:
                params = []
                for i in range(tail_start, num_rows):
                    _add_row_to_sql_data(params, data_df.iloc[i])

                cursor.executemany(insert_sql, params)
                cursor.commit()
                pbm.print('executed sql leftover batch: size=' + str(tail_sql_size))

            cursor.close()
        finally:
            conn.autocommit = conn_am


def _gen_insert_sql(data_df, tbl_name):
    num_cols = data_df.shape[1]
    chunk_sql = ', '.join(['?' for _ in range(num_cols)])
    chunk_sql = '(' + chunk_sql + ')'
    sql_header = 'INSERT INTO ' + tbl_name + ' (' + ', '.join([x for x in data_df.columns]) + ') VALUES '
    insert_sql = sql_header + chunk_sql
    return insert_sql


def _ensure_table(cursor, data_df, if_exist, pbm, tbl_name, use_df_type):
    tbl_exist = cursor.tables(table=tbl_name, tableType='TABLE').fetchone()
    if tbl_exist:
        logger.info('table ' + tbl_name + ' exists.')
    else:
        logger.info('table ' + tbl_name + ' does not exist.')
    if tbl_exist:
        if if_exist == 'fail':
            raise Exception('table ' + tbl_name + ' exists, exit.')
        elif if_exist == 'truncate':
            cursor.execute(SQL_TRUNCATE_TBL + tbl_name)
        elif if_exist == 'drop':
            cursor.execute(SQL_DROP_TBL + tbl_name)
            cursor.commit()
            pbm.print('dropped table ' + tbl_name)

            tbl_exist = None
        # else we treat it as append, leave the table intact
    if not tbl_exist:  # include not exist from beginning or drop table.
        sql = SQL_CREATE_TBL + tbl_name + '(\n'
        for col in data_df.columns:
            if not use_df_type:
                sql += col + ' VARCHAR(128),\n'  # is 128 enough
            else:
                if data_df[col].dtype == numpy.int64:
                    sql += col + ' INT,\n'
                elif data_df[col].dtype == numpy.float64:
                    sql += col + ' FLOAT,\n'
                elif data_df[col].dtype == numpy.datetime64:
                    sql += col + ' DATETIME,\n'
                else:
                    sql += col + ' VARCHAR(128),\n'
        sql = sql[0:len(sql) - 2]
        sql += ')'
        logger.info('create table sql=' + sql)
        cursor.execute(sql)
        cursor.commit()
        pbm.print('created table ' + tbl_name)


def _add_row_to_sql_data(params, row):
    vs = [x.item() if ((not isinstance(x, str)) and (x == float('nan'))) else x for x in row.values]
    # unwrap numpy types back to python types
    vs = [x.item() if isinstance(x, numpy.generic) else x for x in vs]
    vs = [None if isinstance(x, float) and math.isnan(x) else x for x in vs]
    params.append(tuple(vs))
