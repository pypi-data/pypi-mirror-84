import pyodbc
import inspect


# These are convenient mappers between database rows and domain objects.
# Assume we use simple class structure, all fields are public without prefix _
# the fields are mapped directly to database table columns (c convention)

def query_list(select_sql: str, conn, clz):
    ret = []
    cursor = conn.cursor()
    for row in cursor.execute(select_sql):
        ret.append(row_to_obj(row, clz))

    return ret


def row_to_obj(tbl_row: pyodbc.Row, target_clz):
    col_2_value = {}
    for idx, field in enumerate(tbl_row.cursor_description):
        col_2_value[field[0]] = tbl_row[idx]

    s = inspect.signature(target_clz.__init__)
    params = list(s.parameters.keys())[1:]  # 0 is self, skip that
    values = [col_2_value[p] for p in params]
    ret = target_clz(*values)

    missing = set(col_2_value.keys()) - set(params)
    mm = {key: col_2_value[key] for key in missing}
    ret.__dict__.update(mm)

    return ret


def gen_insert_sql(obj, tbl_name):
    fields = obj_vars(obj)
    sql = 'INSERT INTO ' + tbl_name + ' ' + str(fields) + ' VALUES '
    sql += '(' + ', '.join(['?'] * len(fields)) + ')'
    return sql


def gen_update_sql(obj, tbl_name, excluded: set):
    fields = obj_vars(obj)
    included = [f for f in fields if f not in excluded]  # maintain order
    sql = 'UPDATE ' + tbl_name + ' SET '
    for f in included:
        sql += f + ' = ?, '
    return sql[:-2]


# This is twisted, need a dummy object in order to know all fields of this
# class has. Without calling init(), we really don't know - inheritance
# could be on the way. It's dummy.
def gen_select_sql(obj, tbl_name):
    if obj is None:
        return 'SELECT * FROM ' + tbl_name

    fields = obj_vars(obj)
    return 'SELECT ' + ', '.join(fields) + ' FROM ' + tbl_name


def obj_vars(target):
    props = vars(target)
    return tuple(props.keys())


# used by insert & update as values
def obj_values(target, exclude: set = None):
    variables = obj_vars(target)
    values = []
    for v in variables:
        if not exclude or (exclude and v not in exclude):
            values.append(getattr(target, v))

    return tuple(values)
