import os
import yaml

from jsonschema import Draft7Validator

from .counter import Counter
from .items import Item
from .errors import SchemaException


curDir = os.path.abspath(os.path.dirname(__file__))


with open(os.path.join(curDir, "schema.yaml")) as fstream:
    protocol = yaml.load(fstream, Loader=yaml.FullLoader)

Draft7Validator.check_schema(protocol)

class Schema(object):

    _root = os.getcwd()
    _validator = Draft7Validator(protocol)

    @classmethod
    def setRoot(cls, root):
        cls._root = root

    @property
    def counter(self):
        return self._counter

    @property
    def absPath(self):
        return self._absPath

    @property
    def relPath(self):
        return os.path.relpath(self._absPath, Schema._root)

    @property
    def fileName(self):
        return self._fileName

    @property
    def dir(self):
        return self._dir

    @property
    def data(self):
        return self._data

    @property
    def items(self):
        return self._items

    @property
    def type(self):
        return self.__class__.__name__.lower()

    def __init__(self, schemaPath, parents=[]):
        self._absPath = os.path.abspath(os.path.join(Schema._root, schemaPath))
        self._fileName = os.path.basename(self._absPath)
        self._dir = os.path.dirname(self._absPath)

        if self.relPath in parents:
            raise SchemaException("Circular include schema {}, parents={}".format(
                self.relPath,
                parents
            ))

        with open(self._absPath) as fstream:
            self._data = yaml.load(fstream, Loader=yaml.FullLoader)

        if not Schema._validator.is_valid(self._data):
            error = "Invalid schema {}".format(self._absPath)
            for err in Schema._validator.iter_errors(self._data):
                print("Error: {}".format(err.message))
                print("Context: {}".format(err.absolute_schema_path))

            raise SchemaException(error)

        self._counter = Counter()

        self._items = []
        for itemDict in self._data["main"]:
            if "include" in itemDict:
                subSchemaAbsPath = os.path.abspath(os.path.join(self._dir, itemDict["include"]))
                subSchemaRelPath = os.path.relpath(subSchemaAbsPath, Schema._root)
                self._items.append(Schema(subSchemaRelPath, parents + [self.relPath]))
            else:
                self._items.append(Item.create(self, itemDict))
