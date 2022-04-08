from flask_app.config.mysqlconnection import connectToMySQL
# from datetime import datetime
# import math
from flask import flash
from flask_app.models.user_model import User

db_name='final_project_schema'

class MOC:
    def __init__( self, data ):
        self.id = data['id']
        self.moc_name = data['moc_name']
        self.description = data['description']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        

        if 'username' in data:
            self.username = data['username']



    @staticmethod
    def moc_validate(moc):
        is_valid = True
        # if len(car['price']) == "":
        #     is_valid = False
        #     flash("Must Enter Price","car")
        if len(moc['moc_name']) < 3:
            is_valid = False
            flash("Name must be at least 3 characters","moc")
        # if len(car['make']) < 3:
        #     is_valid = False
        #     flash("Make must be at least 3 characters","car")
        # if car['year'] == "":
        #     is_valid = False
        #     flash("Must enter Model Year","car")
        if len(moc['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters","moc")
        
        return is_valid


    @classmethod
    def save(cls, data):
        query = """
                INSERT INTO mocs ( moc_name, description,  user_id )
                VALUES ( %(moc_name)s,  %(description)s, %(user_id)s );
                """
        return connectToMySQL(db_name).query_db(query, data)

    @classmethod
    def get_all_users(cls, data):
        query = "SELECT * FROM mocs JOIN users ON mocs.user_id = users.id;"
                                # JOIN users ON cars.user_id = users.id WHERE cars.id = %(id)s;
        results = connectToMySQL(db_name).query_db(query,data)
        mocs = []
        print(mocs)
        for moc in results:
            creator_moc = cls(moc)
            creator_data = {
                "id" : moc["id"],
                "username" : moc["username"],
                "email" : moc["email"],
                "password" : moc["password"],
                "created_at" : moc["created_at"],
                "updated_at" : moc["updated_at"]
            }
            creator_moc.seller=User(creator_data)
            mocs.append( creator_moc)
        # query = "SELECT * FROM cars JOIN users ON cars.user_id = users.id WHERE cars.id = %(id)s;"
        # results = connectToMySQL(db_name).query_db(query, data)
        return mocs
        


    @classmethod
    def get_one(cls, data ):
        query = "SELECT * FROM mocs JOIN users ON mocs.user_id = users.id WHERE mocs.id = %(id)s;"
        # redid this with Drew, then had an error where it was taking the user id instead of the show id. fixed it by changing "WHERE user_id" to "WHERE shows.id"
        results = connectToMySQL(db_name).query_db(query, data)
        # print (cls(results[0]))
        return (cls(results[0]))

    @classmethod
    def update(cls, data):
        query = "UPDATE mocs SET moc_name=%(moc_name)s, description=%(description)s, updated_at=NOW() WHERE id=%(id)s;"
        return connectToMySQL(db_name).query_db(query, data)

    @classmethod
    def destroy(cls,data):
        query = "DELETE FROM mocs WHERE id = %(id)s;"
        return connectToMySQL(db_name).query_db(query,data)























    # def time_span(self):
    #     now = datetime.now()
    #     delta = now - self.created_at
    #     print(delta.days)
    #     print(delta.total_seconds())
    #     if delta.days > 0:
    #         return f"{delta.days} days ago"
    #     elif (math.floor(delta.total_seconds() / 60)) >= 60:
    #         return f"{math.floor(math.floor(delta.total_seconds() / 60)/60)} hours ago"
    #     elif delta.total_seconds() >= 60 :
    #         return f"{math.floor(delta.total_seconds() / 60)} minutes ago"
    #     else:
    #         return f"{math.floor(delta.total_seconds())} seconds ago"

    # @classmethod
    # def get_user_messages(cls,data):
    #     query = "SELECT users.first_name as sender, users2.first_name as receiver, messages.* FROM users LEFT JOIN messages ON users.id = messages.sender_id LEFT JOIN users as users2 ON users2.id = messages.receiver_id WHERE users2.id =  %(id)s"
    #     results = connectToMySQL(db_name).query_db(query,data)
    #     messages = []
    #     for message in results:
    #         messages.append( cls(message) )
    #     return messages

    # @classmethod
    # def save(cls,data):
    #     query = "INSERT INTO messages (content,sender_id,receiver_id) VALUES (%(content)s,%(sender_id)s,%(receiver_id)s);"
    #     return connectToMySQL(db_name).query_db(query,data)

    # @classmethod
    # def sent_messages(cls, data):
    #     query = "SELECT Count(*) from messages JOIN users as sender on sender.id = \
    #     messages.sender_id JOIN users as receiver on receiver.id = \
    #     messages.receiver_id WHERE sender_id = %(id)s;"
    #     results = connectToMySQL(db_name).query_db(query,data)
    #     return results[0]



    # @classmethod
    # def destroy(cls,data):
    #     query = "DELETE FROM messages WHERE messages.id = %(id)s;"
    #     return connectToMySQL(db_name).query_db(query,data)
