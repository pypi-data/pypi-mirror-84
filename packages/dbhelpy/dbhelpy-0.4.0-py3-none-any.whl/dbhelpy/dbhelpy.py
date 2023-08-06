import sqlite3


class Helpy:
    def __init__(self, database):
        self.database = database
        self.connection = sqlite3.connect(self.database, check_same_thread=False)
        self.cursor = self.connection.cursor()

    def __repr__(self):
        """Returns object string"""
        return 'Your Helpy object'

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Db connection close"""
        self.connection.close()
        return None

    def get_all_data(self, table):
        """
        Retrieve all data from a table.

        :param string table: your table
        :returns: all data from a given table
        """
        data = [x for x in self.cursor.execute(f'SELECT * FROM {table}')]
        return data

    def get_all_data_by(self, table, column, condition):
        """
        Retrieve all data from a specified table and column filtered by a condition of that column.

        Example: To get the number of cars with the color red -> get_all_data_by('cars', 'color', 'red')

        :param string table: your table
        :param string column: your column
        :param string condition: filter condition
        :returns: all filtered data
        """
        data = [x for x in self.cursor.execute(f'SELECT * FROM {table} WHERE {column} = ?', (condition,))]
        return data

    def get_all_column(self, table, column):
        """
        Retrieve all data from a column.

        :param string table: your table
        :param string column: your column
        :returns: all data from that column
        """
        data = [x for x in self.cursor.execute(f"SELECT {column} FROM {table}")]
        return data

    def get_column_by(self, table, column, condition):
        """
        Retrieve all data from a column in a table with the ability to sort out conditions from another column or
        columns.

        Example 1 :
            get_column_by('table1', 'cars', "blue="red"")

        Example 2 :
            get_column_by('table1', 'cars', "blue='red' price='1000'")

        Example 2 :
            get_column_by('table1', 'cars', "blue='red' price='1000' year='2020'")

        :param string table: your table
        :param string column: your column
        :param string condition: your condition (can be multiple, make sure to follow the format in examples)
        :returns: all filtered data
        """
        data = [x for x in self.cursor.execute(f"SELECT {column} FROM {table} {filter_condition(condition)}")]
        return data

    def get_calc_column(self, table, column):
        """
        Adds all integer data from a given column.

        :param string table: your table
        :param string column: your column
        :returns: the sum of all integer data from your column
        """
        data = self.get_all_column(table, column)
        total = 0
        for d in data:
            if d[0] is None:
                pass
            else:
                total += d[0]
        return total

    def get_cal_column_by(self, table, column, condition):
        """
        Adds all integer data from a given column and filter by condition(s)

        Example 1 :
            get_cal_column_by('table1', 'cars', "blue='red'")

        Example 2 :
            get_cal_column_by('table1', 'cars', "blue='red' price='1000'")

        Example 3 :
            get_cal_column_by('table1', 'cars', "blue='red' price='1000' year='2020'")

        :param string table: your table
        :param string column: your column
        :param string condition: your condition (can be multiple, make sure to follow the format in examples)
        :returns: all data from the column of choice
        """
        data = self.get_column_by(table, column, condition)
        total = 0
        for d in data:
            if d[0] is None:
                pass
            else:
                total += d[0]
        return total

    def get_all_dec(self, table, column):
        """
        Query your database and sort descending from a column of choice

        :param string table: the table would like to query
        :param string column: the column you would like sort by
        :returns: all data from the table sorted by descending
        """
        data = [x for x in self.cursor.execute(f'SELECT * FROM {table} ORDER BY {column} DESC')]
        return data

    def get_all_asc(self, table, column):
        """
        Query your database and sort ascending from a column of choice

        :param string table: the table would like to query
        :param string column: the column you would like sort by
        :returns: all data from the table sorted by ascending
        """
        data = [x for x in self.cursor.execute(f'SELECT * FROM {table} ORDER BY {column}')]
        return data

    def get_all_dec_by(self, table, dec_column, con_column, condition):
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
        data = [x for x in self.cursor.execute(f'SELECT * FROM {table} WHERE {con_column} = ? ORDER BY {dec_column} '
                                               f'DESC', (condition,))]
        return data

    def get_all_asc_by(self, table, dec_column, con_column, condition):
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
        data = [x for x in self.cursor.execute(f'SELECT * FROM {table} WHERE {con_column} = ? ORDER BY {dec_column}',
                                               (condition,))]
        return data

    def get_single_data(self, table, column, id):
        """
        Query a single cell in your db

        :param string table: the table would like to query
        :param string column: the column you would like to point to
        :param int id: primary id
        :returns: single cell data from a given id
        """
        data = [x for x in self.cursor.execute(f'SELECT {column} FROM {table} WHERE id = {id}')]
        return str(data[0][0])

    def get_single_row(self, id, table):
        """
        Get all row data by id

        :param int id: id
        :param string table: table
        :returns: single row data
        """
        data = self.cursor.execute(f'SELECT * FROM {table} WHERE id = {id}')
        return data.fetchall()[0]

    def search_all_data(self, table, condition):
        """
        Allows you to search the entire database for data.

        :param string table: table
        :param condition: search condition
        :returns: searched data (multiples also)
        """
        list_data = []
        for data in Helpy.get_all_data(self, table):
            if condition in data:
                list_data.append(self.get_single_row(data[0], table))
            else:
                pass
        return list_data

    def update_single_column(self, table, column, id, data):
        """
        Updates a single column cell in your db

        :param string table: the table would like to query
        :param string column: the column you would like to point to
        :param int id: primary id
        :param int data: the data you would like to update with
        :returns: None
        """
        self.cursor.execute(f'UPDATE {table} SET {column} = {data} WHERE id = {id}')
        self.connection.commit()
        return None


def filter_condition(condition):
    split_str = condition.split()
    count = 1
    query = 'WHERE'
    if len(split_str) > 1:
        for s in split_str:
            if count == len(split_str):
                query += f' {s}'
            else:
                query += f' {s} AND'
            count += 1
    else:
        query += f' {split_str[0]}'
    return query
