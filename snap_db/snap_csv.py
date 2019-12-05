import snap_db
import csv


class CsvOptions:
    def __init__(self, determine_column_types=True, drop_tables=True, delimiter=","):
        self.determine_column_types = determine_column_types
        self.drop_tables = drop_tables
        self.delimiter = delimiter


class CsvFileInfo:
    def __init__(self, path, options=None):
        self.path = path
        self.column_names = None
        self.column_types = None
        self.data = []
        self.options = options
        if not options:
            self.options = CsvOptions()

    def get_table_name(self):
        return snap_db.ITEMS_TABLE_NAME

    def get_minimal_type(self, value):
        try:
            int(value)
            return "integer"
        except ValueError:
            pass
        try:
            float(value)
            return "real"
        except ValueError:
            pass
        return "text"

    def process_file(self):
        with open(self.path, encoding="utf8") as csvfile:
            reader = csv.reader(csvfile, delimiter=self.options.delimiter)            
            self.column_names = [name for name in next(reader)]
            cols = len(self.column_names)
            self.column_types = ["string"] * cols if not self.options.determine_column_types else ["integer"] * cols

            for row in reader:
                self.data.append(row)
                for col in range(cols):

                    if self.column_types[col] == "text":
                        continue

                    col_type = self.get_minimal_type(row[col])

                    if self.column_types[col] != col_type:

                        if col_type == "text" or (col_type == "real" and self.column_types[col] == "integer"):
                            self.column_types[col] = col_type

    def save_to_db(self, connection):
        # print("Writing table " + self.get_table_name())
        cols = len(self.column_names)

        if self.options.drop_tables:
            try:
                # print("Dropping table " + self.get_table_name())
                connection.execute('drop table [{table_name}]'.format(table_name=self.get_table_name()))
            except:
                # print("Error Dropping table " + self.get_table_name())
                pass      

        connection.execute('create table [{table_name}] (\n'.format(table_name=self.get_table_name()) +
                           ',\n'.join("\t[%s] %s" % (i[0], i[1]) for i in zip(self.column_names, self.column_types)) +
                           '\n);')

        print("Inserting {0} records into {1}".format(len(self.data), self.get_table_name()))

        connection.executemany('insert into [{table_name}] values ({cols})'.format(table_name=self.get_table_name(),
                               cols=','.join(['?'] * cols)),
                               self.data)

        return len(self.data)