from models.user import save_data_to_db
from psycopg2 import DatabaseError

class Message:
    def __init__(self, from_id, to_id, text):
        self._id = -1
        self.from_id = from_id
        self.to_id = to_id
        self.text = text
        self.creation_date = None
    
    @property
    def id(self):
        return self._id
    
    def save_to_db(self):

        try: 
            with save_data_to_db() as cursor:
                sql = "INSERT INTO message (from_id, to_id, text) VALUES (%s, %s, %s) RETURNING id;"
                data = (self.from_id, self.to_id, self.text)
                cursor.execute(sql, data)
        
        except DatabaseError as e:
            print(f"Błąd {e}")
    
    @staticmethod
    def load_all_messages():

        try:
            with save_data_to_db() as cursor:
                sql = "SELECT from_id, to_id, text FROM message;"
                cursor.execute(sql)
                result = cursor.fetchall()
                
                message_list = []
                for row in result:
                    message_list.append({
                        "from_id": row[0],
                        "to_id": row[1],
                        "text": row[2]
                    })

                return message_list

        except DatabaseError as e:
            print(f"błąd {e}")
            return []