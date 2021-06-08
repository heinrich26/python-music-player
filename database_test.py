from kivy.storage.jsonstore import JsonStore
import os


class Database(object):
    def __init__(self, path: str = ""):
        self._db = JsonStore(os.path.abspath(path))
        if not "queue" in self._db["root"]:
            self._db.put("root", queue=["hello"], **self._db.get("root"))
        self._mirror = self._db.get("root")

    def __setattr__(self, name, value):
        if not name in ("_mirror", "_db"):
            self._mirror.update({name: value})
            self._db.put("root", **self._mirror)
        super(Database, self).__setattr__(name, value)

    def __getattr__(self, name):
        if not name in ("_mirror", "_db"):
            if name in self._mirror:
                try:
                    return self._mirror[name]
                finally:
                    self._db.put("root", **self._mirror)
            else:
                return None


database = Database("database.json")
database._db.put("root", fish=["hi"])

database.car = "hello"

print(database.queue.pop(0))
print(database.queue)
