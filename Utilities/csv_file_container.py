class csv_file_container():
    def __init__(self, header_string = "pass;header;here", delimiter = ";"):
        self.delimiter = delimiter
        self.header = tuple(header_string.split(self.delimiter))
        self.rows = {0 : self.header}
        self.row_size = len(self.header)

    def add_row(self, row_string, local_delimiter = ";"):
        row = tuple(row_string.split(local_delimiter))
        if(len(row) != self.row_size):
            raise Exception("Wrong number of elements for new row.")

        self.rows[len(self.rows)] = row

    def change_value(self, row, column, value):
        self.rows[row][column] = value

    def write_to_file(self, filename = "my_csv_file"):
        with open(filename + ".csv", "w+") as file:
            for row in self.rows.values():
                file.write(self.delimiter.join(list(row)) + "\n")
