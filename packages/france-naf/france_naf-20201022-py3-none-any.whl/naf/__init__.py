import pickle
import json
from dataclasses import dataclass, is_dataclass, asdict
from pathlib import Path

try:
    import xlrd
except ImportError:
    print("xlrd not found, naf library is open in read-only")

DB_PATH = Path(__file__).parent / "db"


class DBSingleton(dict):
    def persist(self):
        DB_PATH.write_bytes(pickle.dumps(self))
        print(f"Data saved to {DB_PATH}")

    def load(self):
        print(f"Loading NAF data from {DB_PATH}")
        self.clear()
        self.update(pickle.loads(DB_PATH.read_bytes()))

    def __iter__(self):
        return iter(self.values())

    def __str__(self):
        return json.dumps(self, cls=JSONEncoder)

    def pairs(self):
        for code, obj in self.items():
            yield code, str(obj)


DB = DBSingleton()


@dataclass
class Category:
    code: str
    description: str

    def __str__(self):
        return self.description

    def __eq__(self, other):
        return other == self.code


@dataclass
class NAF:
    code: str
    description: str
    classe: Category
    group: Category
    division: Category
    section: Category

    def __str__(self):
        return self.description


class JSONEncoder(json.JSONEncoder):
    def default(self, o):
        if is_dataclass(o):
            return asdict(o)
        return super().default(o)


def update_db(path):
    book = xlrd.open_workbook(path)
    sheet = book.sheet_by_index(0)
    for idx in range(1, sheet.nrows):
        row = sheet.row(idx)
        code = row[1].value
        description = row[2].value
        if not code:
            continue
        if len(code) != 6:
            if code.startswith("SECTION"):
                section = Category(code[8:], description)
            elif len(code) == 2:
                division = Category(code, description)
            elif len(code) == 4:
                group = Category(code, description)
            elif len(code) == 5:
                classe = Category(code, description)
        else:
            DB[code] = NAF(
                code=code,
                description=description,
                classe=classe,
                group=group,
                division=division,
                section=section,
            )
    DB.persist()


DB.load()
