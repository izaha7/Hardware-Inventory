#This file is responsible for handling everything that the user sees and everything that the user will do

import database
menu = '''\nPlease select one of the following options:
1. Insert new item
2. Remove item
3. Search items
4. Update inventory
5. View sold out items
6. Insert or update last delivery person
7. View last delivery person
8. Exit

Your selection: '''

def prompt_add_item():
    item_name = input("What is the name of the item?: ")
    item_category = input("What is the category of the item? (Hammer, Drill, etc): ")
    item_cost = float(input("What is the cost of the item?: "))
    manufacturer_name = input("What is the name of the manufacturer?: ")
    manufacturer_address = input("What is the address of the manufacturer?: ")
    manufacturer_delivery = input("What day of the week does the manufacturer deliver?: ")
    return item_name, item_category, item_cost, manufacturer_name, manufacturer_address, manufacturer_delivery

database.create_tables()


while (user_input := input(menu)) != "8":
    if user_input == "1":
        item_information = prompt_add_item()
        if item_information:
            item_name, item_category, item_cost, manufacturer_name, manufacturer_address, manufacturer_delivery = item_information
            database.add_item(item_name, item_category, item_cost, manufacturer_name, manufacturer_address, manufacturer_delivery)
        print("Item added")
    elif user_input == "2":
        item_id = int(input("What ID would you like to remove?: "))
        database.delete_item(item_id)
        print("Item deleted")
    elif user_input == "3":
        keyword =  input("What name or category would you like to search?: ")
        user_search = database.find_item(keyword)
        if user_search:
            for search in user_search:
                item_name, quantity, delivery_day = search
                if quantity > 0:
                    print(f"Item: {item_name}, Quantity: {quantity}")
                else:
                    print(f"Item: {item_name}, Quantity: {quantity}. The next delivery day is {delivery_day}")
        else:
            print("Item does not exist")
    elif user_input == "4":
        item_id = int(input("What ID would you like to update?: "))
        quantity = int(input("What is the amount you would like to enter?: "))
        database.update_inventory(item_id, quantity)
        print("Inventory updated")
    elif user_input == "5":
        sold_out = database.sold_out_items()
        if sold_out:
            for sold_out_item in sold_out:
                print(f"{sold_out_item[0]} is sold out.")
        else:
            print("All items available")
    elif user_input == "6":
        item_id = int(input("For which ID do you want to update the delivery person?: "))
        deliveryman = input("What is the updated name?: ")
        phone_number = input("What is the updated phone number?: ")
        database.update_delivery_person(item_id, deliveryman, phone_number)
    elif user_input == "7":
        item_id = int(input("For which ID do you want to view the last delivery person?: "))
        delivery_info = database.previous_delivery_person(item_id)
        if delivery_info:
            print(f"The most recent deliverer was {delivery_info[0]}. Contact at {delivery_info[1]} ")
    else: print("Please enter a valid input")





