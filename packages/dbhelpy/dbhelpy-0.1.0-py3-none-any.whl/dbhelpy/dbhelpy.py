import sqlite3

database = ''


def get_all_data(table):
    """
    Query's all data from a specified table

    :param string table: the table would like to query
    :returns: all data from the given table
    """
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    data = [x for x in cursor.execute(f'SELECT * FROM {table}')]
    connection.close()
    return data


def get_all_data_by(table, column, condition):
    """
    Query's all data from a specified table with a choice of column condition

    Example: You want to know how many cars have color red -> get_all_data_by(cars, color, red)

    :param string table: the table would like to query
    :param string column: the column you would like to point to for your condition
    :param string condition: the condition you would like to filter with
    :returns: all data that equals the condition of your column
    """
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    data = [x for x in cursor.execute(f'SELECT * FROM {table} WHERE {column} = ?', (condition,))]
    connection.close()
    return data


def get_all_column(table, column):
    """
    Query's all data from one specific column in a table

    :param string table: the table would like to query
    :param string column: the column you would like to point to
    :returns: all data from the column of choice
    """
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    data = [x for x in cursor.execute(f"SELECT {column} FROM {table}")]
    connection.close()
    return data


def get_all_calc_column(table, column):
    """
    Adds all integer data from a given column

    :param string table: the table would like to query
    :param string column: the column you would like to point to
    :returns: sum of all integer data from your column
    """
    data = get_all_column(column, table)
    total = 0
    for d in data:
        if d[0] is None:
            pass
        else:
            total += d[0]
    return total


def get_all_dec(table, column):
    """
    Query your database and sort descending from a column of choice

    :param string table: the table would like to query
    :param string column: the column you would like sort by
    :returns: all data from the table sorted by descending
    """
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    data = [x for x in cursor.execute(f'SELECT * FROM {table} ORDER BY {column} DESC')]
    connection.close()
    return data


def get_all_asc(table, column):
    """
    Query your database and sort ascending from a column of choice

    :param string table: the table would like to query
    :param string column: the column you would like sort by
    :returns: all data from the table sorted by ascending
    """
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    data = [x for x in cursor.execute(f'SELECT * FROM {table} ORDER BY {column}')]
    connection.close()
    return data


def get_all_dec_by(table, dec_column, con_column, condition):
    """
    Query your database, sort descending by a column of choice, and specify a condition

    Example: get_all_data_by(cars, price, color, red) will return all cars that are red and sort them descending by
    price

    :param string table: the table would like to query
    :param string dec_column: the column you would like sort by
    :param string con_column: the column you would use your condition for
    :param string condition: the condition that will determine your filter
    :returns: all data from the table sorted by descending and a given condition
    """
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    data = [x for x in cursor.execute(f'SELECT * FROM {table} WHERE {con_column} = ? ORDER BY {dec_column} DESC',
                                      (condition,))]
    connection.close()
    return data


def get_all_asc_by(table, dec_column, con_column, condition):
    """
    Query your database, sort ascending by a column of choice, and specify a condition

    Example: get_all_data_by(cars, price, color, red) will return all cars that are red and sort them ascending by
    price

    :param string table: the table would like to query
    :param string dec_column: the column you would like sort by
    :param string con_column: the column you would use your condition for
    :param string condition: the condition that will determine your filter
    :returns: all data from the table sorted by ascending and a given condition
    """
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    data = [x for x in cursor.execute(f'SELECT * FROM {table} WHERE {con_column} = ? ORDER BY {dec_column}',
                                      (condition,))]
    connection.close()
    return data


def get_single_data(table, column, id):
    """
    Query a single cell in your db

    :param string table: the table would like to query
    :param string column: the column you would like to point to
    :param string id: primary id
    :returns: single cell data from a given id
    """
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    data = [x for x in cursor.execute(f'SELECT {column} FROM {table} WHERE id = {id}')]
    connection.close()
    return data[0][0]


def update_single_column(table, column, id, data):
    """
    Updates a single column cell in your db

    :param string table: the table would like to query
    :param string column: the column you would like to point to
    :param string id: primary id
    :param string data: the data you would like to update with
    :returns: None
    """
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    cursor.execute(f'UPDATE {table} SET {column} = {data} WHERE id = {id}')
    connection.commit()
    connection.close()
    return None



