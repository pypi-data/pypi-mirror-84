# PyODBC DbAccess

There are 3 tools in the library:
- OR mapping: assume object property name matches database columns
    - row to object: ```pypigeonhole_dbaccess.obj_mapper.row_to_obj()```
    - rows to list of object: ```pypigeonhole_dbaccess.obj_mapper.query_list()```
    - generate sql statements for insert
    - generate select statement based on an object. This is not natural.
    - may have to handle _name and __name cases because of property.
- Local transaction manager: ```pypigeonhole_dbaccess.tx_manager```  
  It handles nested transactions, i.e., if any part of database operations 
  fails, all operations rollback.
- Bulk SQL uploader: To insert one row into a database, we use  
  ```insert into <table> (?, ?, ..., ?) values (...)```  
  To insert many rows,  
  ```insert into <table> (?, ?, ..., ?) values (...), (...), ..., (...)```  
  and then batch them.
  Python twists the insert statements with ```executemany()```.


