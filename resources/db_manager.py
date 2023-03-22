from flask_restful import Resource
from pythonsqlite import Base


class managerDB(Resource):

    db = ''

    def getFileInfo(self):
        db = self.getConnection()
        info = db.read_all_file()
        return info

    def getExtraInfo(self):
        db = self.getConnection()
        info = db.read_all_extra()
        return info

    def clean(self):
        db = self.getConnection()
        info = db.clean_data()
        db.create_db()
        return info

    def getConnection(self):
        if not self.db:
            self.db = Base()
        return self.db
