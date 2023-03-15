import sqlite3

# The class that works with the database
class Database:
    # The constructor of the class
    def __init__(self, path_to_db="main.db"):
        self.path_to_db = path_to_db

    # The property that returns the connection to the database
    @property
    def connection(self):
        return sqlite3.connect(self.path_to_db)

    # The method that executes the SQL query
    def execute(self, sql: str, parameters: tuple = None, fetchone=False, fetchall=False, commit=False):
        if not parameters:
            parameters = ()
        connection = self.connection
        # connection.set_trace_callback(logger)
        cursor = connection.cursor()
        data = None
        cursor.execute(sql, parameters)

        if commit:
            connection.commit()
        if fetchall:
            data = cursor.fetchall()
        if fetchone:
            data = cursor.fetchone()
        connection.close()
        return data

    # The method that creates the table
    def create_table_users(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY,
            Name varchar(255) NOT NULL,
            language varchar(3)
            );
"""
        self.execute(sql, commit=True)


    # the metod that creates the table
    def create_smartphone_ads(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Smartphone (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id int,
            model varchar(255),
            memory varchar(255),
            phone_state varchar(255),
            cost varchar(255),
            box varchar(255),
            docs varchar(255),
            number varchar(255),
            address varchar(255),
            photo varchar(255)
        );
        """
        self.execute(sql, commit=True)




    def create_auto_ads(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Auto (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id int,
            model varchar(255),
            year varchar(255),
            position varchar(255),
            car_state varchar(1000),
            cost varchar(255),
            transbox varchar(255),
            distance varchar(255),
            color varchar(255),
            number varchar(255),
            address varchar(255),
            photo varchar(255)
        );
        """
        self.execute(sql, commit=True)






    def create_house_ads(self):
        sql = """
        CREATE TABLE IF NOT EXISTS House (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id int,
            area varchar(255),
            rooms varchar(255),
            house_state varchar(255),
            cost varchar(255),
            conven varchar(255),
            number varchar(255),
            address varchar(255),
            photo varchar(255)
        );
        """
        self.execute(sql, commit=True)



    def create_home_ads(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Home (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id int,
            total_floors varchar(255),
            current_floor varchar(255),
            rooms varchar(255),
            home_state varchar(255),
            cost varchar(255),
            conven varchar(255),
            number varchar(255),
            address varchar(255),
            photo varchar(255)
        );
        """
        self.execute(sql, commit=True)


    def create_status_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Status (
            id INTEGER PRIMARY KEY,
            status varchar(255)
        );
        """
        self.execute(sql, commit=True)
    


    def create_services_table(self):
        sql = """
        CREATE TABLE IF NOT EXISTS Service (
            id INTEGER PRIMARY KEY,
            user_id int,
            service_name varchar(500),
            description varchar(1000),
            regions varchar(500),
            number varchar(255),
            photo varchar(255)
        );
        """
        self.execute(sql, commit=True)





    # the format of the sql query
    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ?" for item in parameters
        ])
        return sql, tuple(parameters.values())






    def add_user(self, id: int, name: str, language: str = 'uz'):
        sql = """
        INSERT or IGNORE INTO Users(id, Name, language) VALUES(?, ?, ?)
        """
        self.execute(sql, parameters=(id, name, language), commit=True)


    def add_status(self, id: int, status: str):
        sql = """
        INSERT or IGNORE INTO Status(id, status) VALUES(?, ?)
        """
        self.execute(sql, parameters=(id, status), commit=True)
    

    def get_status(self, id: int):
        sql = """
        SELECT status FROM Status WHERE id = ?
        """
        return self.execute(sql, parameters=(id,), fetchone=True)
    

    def update_status(self, id: int, status: str):
        sql = """
        UPDATE Status SET status = ? WHERE id = ?
        """
        self.execute(sql, parameters=(status, id), commit=True)

    def delete_status(self, id: int):
        sql = """
        DELETE FROM Status WHERE id = ?
        """
        self.execute(sql, parameters=(id,), commit=True)

    # add smartphone advertisements to the database
    def add_smartphone(
        self,
        user_id: int,
        model: str,
        memory: str,
        phone_state: str,
        cost: str,
        box: str,
        docs: str,
        number: str,
        address: str,
        photo: str,
        ):
        unique_id = self.unique_value()
        sql = """
        INSERT or IGNORE INTO Smartphone(id, user_id, model, memory, phone_state, cost, box, docs, number, address, photo) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(
            sql,
            parameters=(
                unique_id,
                user_id,
                model,
                memory,
                phone_state,
                cost,
                box,
                docs,
                number,
                address,
                photo,
            ),
            commit=True,
        )
        self.add_status(id=unique_id, status='active')
        return unique_id


    # add auto advertisements to the database
    def add_auto(
        self,
        user_id: int,
        model: str,
        year: str,
        position: str,
        car_state: str,
        cost: str,
        transbox: str,
        distance: str,
        color: str,
        number: str,
        address: str,
        photo: str,
        ):
        unique_id = self.unique_value()
        sql = """
        INSERT or IGNORE INTO Auto(id, user_id, model, year, position, car_state, cost, transbox, distance, color, number, address, photo) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(
            sql,
            parameters=(
                unique_id,
                user_id,
                model,
                year,
                position,
                car_state,
                cost,
                transbox,
                distance,
                color,
                number,
                address,
                photo
            ),
            commit=True,
        )
        self.add_status(id=unique_id, status='active')
        return unique_id




    # add House advertisements to the database
    def add_house(
        self,
        user_id: int,
        area: str,
        rooms: str,
        house_state: str,
        cost: str,
        conven: str,
        number: str,
        address: str,
        photo: str,
        ):
        unique_id = self.unique_value()
        sql = """
        INSERT or IGNORE INTO House(id, user_id, area, rooms, house_state, cost, conven, number, address, photo) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(
            sql=sql,
            parameters=(
                unique_id,
                user_id,
                area,
                rooms,
                house_state,
                cost,
                conven,
                number,
                address,
                photo
            ),
            commit=True,
        )
        self.add_status(id=unique_id, status='active')
        return unique_id
    


    # add the Home advertisements to the database
    def add_home(
        self,
        user_id: int,
        total_floors: str,
        current_floor: str,
        rooms: str,
        home_state: str,
        cost: str,
        conven: str,
        number: str,
        address: str,
        photo: str,
        ):
        unique_id = self.unique_value()
        sql = """
        INSERT or IGNORE INTO Home(id, user_id, total_floors, current_floor, rooms, home_state, cost, conven, number, address, photo) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(
            sql=sql,
            parameters=(
                unique_id,
                user_id,
                total_floors,
                current_floor,
                rooms,
                home_state,
                cost,
                conven,
                number,
                address,
                photo,
            ),
            commit=True,
        )
        self.add_status(id=unique_id, status='active')
        return unique_id
    

    # add service advertisements to the database
    def add_service(
        self,
        user_id: int,
        service_name: str,
        description: str,
        regions: str,
        number: str,
        photo: str,
        ):
        unique_id = self.unique_value()
        sql = """
        INSERT or IGNORE INTO Service(id, user_id, service_name, description, regions, number, photo) VALUES(?, ?, ?, ?, ?, ?, ?)
        """
        self.execute(
            sql=sql,
            parameters=(
                unique_id,
                user_id,
                service_name,
                description,
                regions,
                number,
                photo,
            ),
            commit=True,
        )
        self.add_status(id=unique_id, status='active')
        return unique_id







    def all(self) -> list:
        sql = "SELECT id FROM Users"
        result = self.execute(sql, fetchall=True)
        return [x[0] for x in result]
    


    def unique_value(self):
        sql = """
        SELECT max(id) FROM Auto"""
        result1 = self.execute(sql, fetchone=True)[0] if self.execute(sql, fetchone=True)[0] else 0
        sql = """
        SELECT max(id) FROM Home"""
        result2 = self.execute(sql, fetchone=True)[0] if self.execute(sql, fetchone=True)[0] else 0
        sql = """
        SELECT max(id) FROM House"""
        result3 = self.execute(sql, fetchone=True)[0] if self.execute(sql, fetchone=True)[0] else 0
        
        sql = """
        SELECT max(id) FROM Service"""
        result4 = self.execute(sql, fetchone=True)[0] if self.execute(sql, fetchone=True)[0] else 0
        return max(result1, result2, result3, result4) + 1
    


    def find_ad(self, user_id, ads_id):
        sql = """
        SELECT * FROM Auto WHERE user_id = ? AND id = ?"""
        result1 = self.execute(sql, parameters=(user_id, ads_id), fetchone=True)
        if result1:
            return result1, 1
        sql = """
        SELECT * FROM Home WHERE user_id = ? AND id = ?"""
        result2 = self.execute(sql, parameters=(user_id, ads_id), fetchone=True)
        if result2:
            return result2, 2
        sql = """
        SELECT * FROM House WHERE user_id = ? AND id = ?"""
        result3 = self.execute(sql, parameters=(user_id, ads_id), fetchone=True)
        if result3:
            return result3, 3
        # sql = """
        # SELECT * FROM Smartphone WHERE user_id = ? AND id = ?"""
        # result4 = self.execute(sql, parameters=(user_id, ads_id), fetchone=True)
        # if result4:
        #     return result4, 4
        sql = """
        SELECT * FROM Service WHERE user_id = ? AND id = ?"""
        result4 = self.execute(sql, parameters=(user_id, ads_id), fetchone=True)
        if result4:
            return result4, 4
        return None, None
    



    def delete_ad(self, user_id, ads_id):
        sql = """
        DELETE FROM Auto WHERE user_id = ? AND id = ?"""
        result1 = self.execute(sql, parameters=(user_id, ads_id), commit=True)
        self.delete_status(ads_id)
        sql = """
        DELETE FROM Home WHERE user_id = ? AND id = ?"""
        result2 = self.execute(sql, parameters=(user_id, ads_id), commit=True)
        self.delete_status(ads_id)
        sql = """
        DELETE FROM House WHERE user_id = ? AND id = ?"""
        result3 = self.execute(sql, parameters=(user_id, ads_id), commit=True)
        self.delete_status(ads_id)
        sql = """
        DELETE FROM Service WHERE user_id = ? AND id = ?"""
        result4 = self.execute(sql, parameters=(user_id, ads_id), commit=True)
        self.delete_status(ads_id)
        # return result1 or result2 or result3 or result4





    def get_my_ads(self, user_id: int):
        sql = """SELECT id FROM Auto WHERE user_id = ?"""
        result1 = self.execute(sql, parameters=(user_id,), fetchall=True)
        sql = """SELECT id FROM Home WHERE user_id = ?"""
        result2 = self.execute(sql, parameters=(user_id,), fetchall=True)
        sql = """SELECT id FROM House WHERE user_id = ?"""
        result3 = self.execute(sql, parameters=(user_id,), fetchall=True)
        sql = """SELECT id FROM Service WHERE user_id = ?"""
        result4 = self.execute(sql, parameters=(user_id,), fetchall=True)
        return result1 + result2 + result3 + result4



def logger(statement):
    print(f"""
_____________________________________________________        
Executing: 
{statement}
_____________________________________________________
""")


