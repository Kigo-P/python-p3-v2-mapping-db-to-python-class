from __init__ import CURSOR, CONN


class Department:

    # creating a class variable that will store data from the DB
    all = {}

    def __init__(self, name, location, id=None):
        self.id = id
        self.name = name
        self.location = location

    def __repr__(self):
        return f"<Department {self.id}: {self.name}, {self.location}>"

    @classmethod
    def create_table(cls):
        """ Create a new table to persist the attributes of Department instances """
        sql = """
            CREATE TABLE IF NOT EXISTS departments (
            id INTEGER PRIMARY KEY,
            name TEXT,
            location TEXT)
        """
        CURSOR.execute(sql)
        CONN.commit()

    @classmethod
    def drop_table(cls):
        """ Drop the table that persists Department instances """
        sql = """
            DROP TABLE IF EXISTS departments;
        """
        CURSOR.execute(sql)
        CONN.commit()

    def save(self):
        """ Insert a new row with the name and location values of the current Department instance.
        Update object id attribute using the primary key value of new row.
        """
        sql = """
            INSERT INTO departments (name, location)
            VALUES (?, ?)
        """

        CURSOR.execute(sql, (self.name, self.location))
        CONN.commit()

        self.id = CURSOR.lastrowid

        # add the current department instance to the dictionary
        type(self).all[self.id] = self

    @classmethod
    def create(cls, name, location):
        """ Initialize a new Department instance and save the object to the database """
        department = cls(name, location)
        department.save()
        return department

    def update(self):
        """Update the table row corresponding to the current Department instance."""
        sql = """
            UPDATE departments
            SET name = ?, location = ?
            WHERE id = ?
        """
        CURSOR.execute(sql, (self.name, self.location, self.id))
        CONN.commit()

    def delete(self):
        """Delete the table row corresponding to the current Department instance"""
        sql = """
            DELETE FROM departments
            WHERE id = ?
        """

        CURSOR.execute(sql, (self.id,))
        CONN.commit()

        # deleting from the dictionary
        del type(self).all[self.id]

        #setting id to None
        self.id = None

    #creating  class method that gets the instance of the class from the table and adds it to the dictionary above
    @classmethod
    def instance_from_db(cls, row):
        """Return a Department object having the attribute values from the table row."""

        # Check the dictionary for an existing instance using the row's primary key
        department = cls.all.get(row[0])
        if department:
            # ensure attributes match row values in case local object was modified
            department.name = row[1]
            department.location = row[2]
        else:
            # not in dictionary, create new instance and add to dictionary
            department = cls(row[1], row[2])
            department.id = row[0]
            cls.all[department.id] = department
        return department
        
    #creating a classmethod that gets all the instances of the class from rows in the DB
    @classmethod
    def get_all(cls):
        """Return a list containing a Department object per row in the table"""
        sql = """
            SELECT *
            FROM departments
        """

        rows = CURSOR.execute(sql).fetchall()

        return [cls.instance_from_db(row) for row in rows]

    # a class method that returns an instance in the table row of a specified id
    @classmethod
    def find_by_id(cls,id):
        """Returns an instance corresponding to te table row matching a specific id"""
        sql_statement = """SELECT * FROM departments WHERE id = ?;"""
        #Executing the cursor object 
        row = CURSOR.execute(sql_statement, (id, )).fetchone()
        # using an if statement to find the id
        # if row: 
        #     return cls.instance_from_db(row)
        # else:
        #     return None
        return cls.instance_from_db(row) if row else None
    
    # a class method that returns the istance of the class correspoding to the table row matching a specific name
    @classmethod
    def find_by_name(cls, name):
        """Returns an instance corresponding to the table row for a specified name"""
        sql_statement = """SELECT * FROM departments WHERE name = ?;"""
        #Executing the cursor object
        row = CURSOR.execute(sql_statement, (name, )).fetchone()
        # returning the row if the name has been found
        # if row:
        #     return cls.instance_from_db(row)
        # else: 
        #     return None
        
        return cls.instance_from_db(row) if row else None