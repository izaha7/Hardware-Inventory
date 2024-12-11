import sqlite3

connection = sqlite3.connect("hardware.db")
#The following sets of SQL queries conduct various actions that the user can do
CREATE_ITEMS_TABLE = """CREATE TABLE IF NOT EXISTS items
    (item_id INTEGER PRIMARY KEY AUTOINCREMENT,
    item_name TEXT,
    category TEXT,
    cost REAL,
    manufacturer_id,
    FOREIGN KEY(manufacturer_id) REFERENCES manufacturer(id)
    );"""

CREATE_MANUFACTURER_TABLE = """CREATE TABLE IF NOT EXISTS manufacturer (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    address TEXT,
    delivery_day TEXT
);"""

CREATE_INVENTORY_TABLE = """CREATE TABLE IF NOT EXISTS inventory (
    inventory_id INTEGER PRIMARY KEY AUTOINCREMENT,
    quantity INTEGER,
    out_of_stock BOOLEAN,
    FOREIGN KEY(inventory_id) REFERENCES items(item_id)
);"""

CREATE_DELIVERY_INFORMATION_TABLE = """CREATE TABLE IF NOT EXISTS delivery (
    delivery_id INTEGER PRIMARY KEY,
    deliveryman TEXT,
    phone_number TEXT,
    FOREIGN KEY(delivery_id) REFERENCES items(item_id)
);"""

INSERT_MANUFACTURER = "INSERT INTO manufacturer (name, address, delivery_day) VALUES (?, ?, ?);"
INSERT_ITEM = "INSERT INTO items (item_name, category, cost, manufacturer_id) VALUES (?, ?, ?, ?);"
INSERT_INVENTORY = "INSERT INTO inventory (inventory_id, quantity, out_of_stock) VALUES (?, ?, ?);"
INSERT_DELIVERY_PERSON = "INSERT INTO delivery (delivery_id, deliveryman, phone_number) VALUES (?, ?, ?);"
UPDATE_DELIVERY_PERSON = "UPDATE delivery SET deliveryman = ?, phone_number = ? WHERE delivery_id = ?;"
GET_PREVIOUS_DELIVERY_PERSON = "SELECT deliveryman, phone_number FROM delivery WHERE delivery_id = ?"
UPDATE_INVENTORY = "UPDATE inventory SET quantity = ?, out_of_stock = ? WHERE inventory_id = ?;"
DELETE_ITEM = "DELETE FROM items WHERE item_id = ?;"
DELETE_STOCK_INFO = "DELETE FROM inventory WHERE inventory_id = ?;"
DELETE_DELIVERY_INFO = "DELETE FROM delivery WHERE delivery_id = ?;"
SEARCH_ITEMS_OR_CATEGORY = """SELECT items.item_name, inventory.quantity, manufacturer.delivery_day 
                            FROM items JOIN inventory ON items.item_id = inventory.inventory_id
                            JOIN manufacturer ON items.manufacturer_id = manufacturer.id
                            WHERE items.item_name LIKE ? OR items.category LIKE ?
                            """
SEARCH_OUT_OF_STOCK = "SELECT items.item_name FROM items JOIN inventory ON items.item_id = inventory.inventory_id WHERE inventory.out_of_stock = 1"
SELECT_MANUFACTURER = "SELECT id FROM manufacturer WHERE name = ?"

#Creates the 4 tables required for the database
def create_tables():
    with connection:
        connection.execute(CREATE_MANUFACTURER_TABLE)
        connection.execute(CREATE_ITEMS_TABLE)
        connection.execute(CREATE_INVENTORY_TABLE)
        connection.execute(CREATE_DELIVERY_INFORMATION_TABLE)

#Sets up a manufacturer to be inserted in the next function
def add_manufacturer(name, address, delivery_day):
    cursor = connection.cursor()
    cursor.execute(SELECT_MANUFACTURER, (name,))
    manufacturer = cursor.fetchone()
    if manufacturer:
        return manufacturer[0]
    else:
        cursor.execute(INSERT_MANUFACTURER, (name, address, delivery_day))
        cursor.execute(SELECT_MANUFACTURER, (name,))
        return cursor.fetchone()[0]

#Adds an item and all of its information as designated by the user
def add_item(item_name, category, cost, manufacturer_name, manufacturer_address, manufacturer_delivery_day):
    man_id = add_manufacturer(manufacturer_name, manufacturer_address, manufacturer_delivery_day)
    with connection:
        cursor = connection.cursor()
        cursor.execute(INSERT_ITEM, (item_name, category, cost, man_id))
        inventory_id = cursor.fetchone()
        connection.execute(INSERT_INVENTORY, (inventory_id, 0, True))

#Deletes item and all of it connections throughout the database
def delete_item(item_id):
    with connection:
        connection.execute(DELETE_ITEM, (item_id,))
        connection.execute(DELETE_STOCK_INFO, (item_id,))
        connection.execute(DELETE_DELIVERY_INFO, (item_id,))

#Searches for a specific keyword given by the user and returns that keyword if it is found.
def find_item(keyword):
    cursor = connection.cursor()
    cursor.execute(SEARCH_ITEMS_OR_CATEGORY, (f'%{keyword}%', f'%{keyword}%'))
    return cursor.fetchall()

#Updates the number of a given item available, the user chooses how much to add or subtract.
def update_inventory(inventory_id, quantity):
    with connection:
        if quantity == 0:
            out_of_stock = True
        else:
            out_of_stock = False
        connection.execute(UPDATE_INVENTORY, (quantity,out_of_stock, inventory_id))

#Checks if the number of any item is 0, and returns those items.
def sold_out_items():
    cursor = connection.cursor()
    cursor.execute(SEARCH_OUT_OF_STOCK)
    return cursor.fetchall()

#Returns the most recent delivery person entered for a specific item, if available.
def previous_delivery_person(delivery_id):
    cursor = connection.cursor()
    cursor.execute(GET_PREVIOUS_DELIVERY_PERSON, (delivery_id,))
    return cursor.fetchone()

#Allows the user to change the most recent delivery person.
def update_delivery_person(delivery_id, deliveryman, phone_number):
    with connection:
        if previous_delivery_person(delivery_id) is None:
            connection.execute(INSERT_DELIVERY_PERSON, (delivery_id, deliveryman, phone_number))
        else:
            connection.execute(UPDATE_INVENTORY, (deliveryman, phone_number, delivery_id))




