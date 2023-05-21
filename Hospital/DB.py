import datetime
import os
import psycopg2
import pandas as pd
import calendar
import matplotlib.pyplot as plt
import numpy as np


class SqlDB:
    def __init__(self, table1='members', table2='covid', key='ID'):
        '''
        :param tabel1: Patients data
        :param tabel2: Covid data
        :param key: ID
        '''
        self.MEMBERS_TABLE = table1
        self.COVID_TABLE = table2
        self.primary_key = key
        self.conn = None
        self.cursor = None

    def connect(self, user, password, host, port, database):
        '''
        :param user: username
        :param password: password
        :param host: host
        :param port: port of postgres sql
        :param database: database
        :function: connect to postgres sql
        '''
        try:

            self.conn = psycopg2.connect(user=user,
                                         password=password,
                                         host=host,
                                         port=port,
                                         database=database)
            self.cursor = self.conn.cursor()
        except Exception as error:
            print("Error while connecting to PostgreSQL", error)
            raise error

    def create_tables(self):
        '''
        :function: This function creates the tables if not already exist.
        '''
        commands = (
            f"""
            CREATE TABLE IF NOT EXISTS public.{self.MEMBERS_TABLE}(
                id int,
                full_name varchar(100),
                address  varchar(100),
                date_of_birth date,
                phone_number varchar(10),
                cell_phone varchar(100),
                primary key(id)
            )
            """,
            f"""
            CREATE TABLE IF NOT EXISTS public.{self.COVID_TABLE}(
                id int,
                vaccination_date varchar(100),
                manufacturer  varchar(100),
                positive_result_date date,
                recovery_date date,
                primary key(id)
            )
            """
        )

        for command in commands:
            try:
                self.cursor.execute(command)
                self.conn.commit()
            except Exception as error:
                raise error

    def check_access(self, table, dict):
        '''
        :param table: gets the table name
        :param dict: dict with key and value to set in table.
        :function: check if the dict has the right keys that match the table type,
                    and check if its not missing the key id.
                    if its patients data check if all fields were sent.
        '''
        try:
            query = f"SELECT column_name FROM information_schema.columns WHERE table_name   = '{table}';"
            self.cursor.execute(query)
            table_column_names = [col[0].upper() for col in self.cursor]

            dict = {key.upper(): val for (key, val) in dict.items()}

            if self.primary_key not in dict.keys():
                raise ValueError("Information missing primary key")

            if not self.is_valid(dict[self.primary_key]):
                raise ValueError("Invalid ID")

            if table == self.MEMBERS_TABLE:
                for element in table_column_names:
                    if element not in dict.keys():
                        raise ValueError("Missing important properties")
            if table == self.COVID_TABLE:
                query = f"SELECT count(*) FROM {self.MEMBERS_TABLE} WHERE {self.primary_key} = {dict[self.primary_key]};"
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                if not result[0][0]:
                    raise ValueError("This patient is not exist in patients database")

            for element in dict.keys():
                if element not in table_column_names:
                    raise ValueError("Information not match table properties")

        except Exception as error:
            self.conn.rollback()
            raise error

    def append_record(self, table, dict):
        '''
        :param table: gets the table name
        :param dict: gets a dictionary with values of the new record.
        :return:
        '''
        try:
            self.check_access(table, dict)
            placeholder = ", ".join(["%s"] * len(dict))
            query = "insert into {table} ({columns}) values ({values});".format(table=table,
                                                                                columns=",".join(dict.keys()),
                                                                                values=placeholder)
            self.cursor.execute(query, list(dict.values()))
            self.conn.commit()
        except Exception as error:
            self.conn.rollback()
            raise error

    def get_data(self, table):
        '''
        :param table: gets the table name
        :function: create df with table names, gets the data from sql, and create html file with that table information.
        '''
        try:
            # query = f"SELECT column_name FROM information_schema.columns WHERE table_name   = '{table}';"
            # self.cursor.execute(query)
            # table_column_names = [col[0].upper() for col in self.cursor]
            # df = pd.DataFrame(columns=table_column_names)
            # query = f"SELECT * FROM {table}"
            # self.cursor.execute(query)
            # result = self.cursor.fetchall()
            # for i, x in enumerate(result):
            #     df.loc[i] = list(x)
            #
            # df['ID'] = df['ID'].astype(int)
            # data_html = df.to_html(index=False)

            query = f"SELECT * FROM {table}"
            df = pd.read_sql(query, self.conn)
            columns = {col:col.upper() for col in df.columns}
            df.rename(columns=columns,inplace=True)
            df['ID'] = df['ID'].astype(int)
            data_html = df.to_html(index=False)

            with open(f"templates/{table}_data.html", "w", encoding="utf-8") as file:
                html = f"""
                      <html>
                      <head>
                        <meta charset="UTF-8">
                        <title>{table[0].upper() + table[1:]} Data</title>

                        <link rel="stylesheet" type="text/css" href="../static/css/tables.css">
                      </head>
                      <body>
                        <h1>{table[0].upper() + table[1:]} Table Data</h1>
                        {data_html}
                      </body>
                      </html>
                      """
                file.write(html)
        except Exception as error:
            self.conn.rollback()
            raise error

    def active_patient(self):
        '''
        :function: create a bar-plot graph of all patients number on each day at the last month.
        '''
        fig_path ='./static/images/active_patient.png'
        if os.path.exists(fig_path):
            os.remove(fig_path)

        month = str(datetime.datetime.today().month)
        year = str(datetime.datetime.today().year)

        # query = f"""SELECT positive_result_date,recovery_date from covid" \
        #         "WHERE (Extract(MONTH from positive_result_date) = {month} AND Extract(YEAR from recovery_date) = {year})"""

        query = f"""SELECT positive_result_date,recovery_date from covid 
                    WHERE ( Extract(YEAR from positive_result_date) = {year} AND Extract(YEAR from recovery_date) = {year} AND
                    Extract(MONTH from positive_result_date) <=  {month} AND Extract(MONTH from recovery_date) >=  {month} )"""

        first_day = datetime.datetime.strptime(f'''01-0{month}-{year}''', '%d-%m-%Y').date()
        days = calendar.monthrange(int(year), int(month))[1]
        last_day = datetime.datetime.strptime(f'''{days}-0{month}-{year}''', '%d-%m-%Y').date()


        try:
            df = pd.read_sql(query, self.conn)
            if not df.empty:
                df = df.dropna()
            if not df.empty:
                start_dates = df.positive_result_date
                start_dates = start_dates.apply(lambda x: first_day if x.month < int(month) else x)
                end_dates = df.recovery_date
                end_dates = end_dates.apply(lambda x: last_day if x.month > int(month) else x)
                data = pd.DataFrame(dt.date().day for group in [pd.date_range(start, end) for start, end in zip(start_dates, end_dates)] for dt in group).value_counts()

                if data is not None:
                    x_data = [x[0] for x in data.index]
                    y_data = [y for y in data]
                    x_axis = np.arange(1, days+1)
                    y_axis = np.arange(0, max(y_data) + 1)

                    colors = ['#63A6FF', '#FF6666', '#99FFCC']
                    plt.bar(x_data, y_data, color=colors)

                    plt.xlim(0.5, 30.5)
                    plt.ylim(0, max(y_data) + 10)

                    plt.xticks(x_axis)
                    plt.yticks(y_axis)
                    plt.xticks(rotation=90, ha='right')

                    plt.xlabel('Days')
                    plt.ylabel('Number Of People')
                    plt.title(f'Active Patients {month} Month')

                    plt.savefig(fig_path, dpi=1200)
                else:
                    raise ValueError("There is no data available")
            else:
                raise ValueError("There is no data available")

        except Exception as error:
            self.conn.rollback()
            raise error

    def not_vaccinated(self):
        '''
        :function: check if the table is not empty, and count the people that didn't vaccinate.
        :return: the number of people that didn't vaccinate.
        '''
        try:
            query = f"select COUNT(*) from {self.COVID_TABLE} "
            self.cursor.execute(query)
            result = self.cursor.fetchall()
            if result[0][0]:
                query = f"select COUNT(*) from {self.COVID_TABLE} where vaccination_date is NULL"
                self.cursor.execute(query)
                result = self.cursor.fetchall()
                return result[0][0]
            else:
                raise ValueError("There is no data available")
        except Exception as error:
            self.conn.rollback()
            raise error


    def is_valid(self,id):
        if len(id) < 9:
            return False
        else:
            check_digit = int(id[0])
            sum = 0
            for i in range(1, len(id)):
                if i % 2 != 0:  # odd position
                    digit = int(id[i]) * 2
                    if digit // 10 != 0:
                        sum += digit % 10 + digit // 10
                    else:
                        sum += digit
                else:
                    sum += int(id[i])

        return (10 - sum) % 10 == check_digit



