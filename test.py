def sterilize(s):
    if type(s) is str:
        return s.replace("'", "`").replace("\n", " ")
    else:
        return s

class insert_writer:
    def __init__(self, table_name, file_name, batch_size=42069):
        self.table_name = table_name
        self.file_name = file_name
        self.count = 0
        self.rows = 0
        self.batch_size = batch_size
        self.schema = []

    def __enter__(self):
        self.out_stream = open(self.file_name, "w")
        return self

    def __exit__(self, *args):
        self.out_stream.write(";\n")
        self.out_stream.close()

    def add_row(self, row_data):
        items = list(row_data.items())
        items.sort()
        keys = [x[0] for x in items]
        values = ["'%s'" % sterilize(x[1]) for x in items]
        output = ""
        if self.rows is 0:
            self.schema = keys

        if keys != self.schema:
            print(f"row {self.rows}: {keys} mismatches {self.schema}\n")

        if self.count is 0:
            output += ";\nINSERT INTO "
            output += self.table_name
            output += "(" + ", ".join(keys) + ") VALUES "
            output += "\n(" + ", ".join(values) + ")"
        else:
            output += ",\n(" + ", ".join(values) + ")"

        self.count = self.count + 1 if self.count < self.batch_size - 1 else 0
        self.rows += 1
        self.out_stream.write(output)