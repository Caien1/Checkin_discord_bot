
import sqlite3
from datetime import datetime


def create_table(cursor):
    create_table_query = """
                    CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    points INTEGER DEFAULT 0 ,
                    last_checkin DATETIME DEFAULT CURRENT_TIMESTAMP
                    )
                    """
    cursor.execute(create_table_query)
    pass


def check_if_user_exists(cursor,user_id):
   
    user_checker_query = """
                SELECT EXISTS(
                SELECT 1 FROM users
                WHERE
                user_id =?
                )
    """

    cursor.execute(user_checker_query,[user_id])
    result=cursor.fetchone()[0]
    return result==1
    pass
    
def create_user_and_update_points(cursor,user_id):

    create_user_query = """
                    INSERT INTO users(
                    user_id,points,last_checkin
                    )
                     values(
                     ?,?,CURRENT_TIMESTAMP
                     )
                     """
    cursor.execute(create_user_query,[user_id,10])


def update_points(cursor,user_id):
    update_points_query = """
                            UPDATE users
                            SET points = points + ? , last_checkin = CURRENT_TIMESTAMP
                            WHERE
                            user_id = ?
    """
    cursor.execute(update_points_query,[10,user_id])

def disply_users(cursor):
    query = "SELECT * FROM users"
    cursor.execute(query)
    return cursor.fetchall()

def can_checkin(cursor,user_id):
    last_checkin_query = """
    SELECT last_checkin from users
    WHERE user_id = ?

    """
    cursor.execute(last_checkin_query,[user_id])
   
    time_at_last_checkin = datetime.strptime(cursor.fetchone()[0],"%Y-%m-%d %H:%M:%S")
    time_delta= datetime.now()-time_at_last_checkin

    return time_delta.days>=1

def get_leaderboard(cursor,user_id, limit=10):
    max_points_qurery = """
        SELECT user_id ,points FROM users ORDER BY points DESC LIMIT ?;
    """
    cursor.execute(max_points_qurery,[limit])
    return cursor.fetchall()




def create_db_connection():
    connection = sqlite3.connect('users.db');
    cursor = connection.cursor()
    return connection,cursor



def close_connection(connection):
    connection.commit()
    connection.close()    




def main(user_id):
    tranction_success = False
    did_exist = True
    connection,cursor = create_db_connection()
    try:
        cursor.execute("BEGIN TRANSACTION")
        exists=check_if_user_exists(cursor,user_id)

        if not exists:
            create_user_and_update_points(cursor,user_id)
            did_exist = False
            tranction_success=True

        elif can_checkin(cursor,user_id):
            update_points(cursor,user_id)
            tranction_success =True

        

        connection.commit()

        

    except sqlite3.Error as e:
        connection.rollback()
        print(f"Some thing went wrong: {e}")
    
    finally:
        close_connection(connection)
        return tranction_success,did_exist
    
