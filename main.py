from uuid import uuid4

import boto3
from boto3.dynamodb.conditions import Key

def get_db_table():
    dynamodb_resource = boto3.resource("dynamodb")
    return dynamodb_resource.Table("academia")

def register_account(user_email: str, user_name: str) -> dict:
    ddb_table = get_db_table()

    response = ddb_table.put_item(
        Item={
            "PK": user_email,
            "SK": "#PROFILE",
            "name": user_name,
        }
    )

    return response

def register_inventory(user_email: str, inventory_name: str, inventory_price: int):
    ddb_table = get_db_table()

    response = ddb_table.put_item(
        Item={
            "PK": user_email,
            "SK": f"#INVENTORY{str(uuid4())}",
            "name": inventory_name,
            "price": inventory_price,
        }
    )

    return response

def get_inventory(user_email: str):
    ddb_table = get_db_table()

    response = ddb_table.query(
        KeyConditionExpression=Key("PK").eq(user_email)
        & Key("SK").begins_with("#INVENTORY")
    )

    return response["Items"]

def invite_account(user_email: str, invited_user_email: str, invited_user_name: str):
    ddb_table = get_db_table()

    response = ddb_table.put_item(
        Item={
            "PK": user_email,
            "SK": f"USER#{invited_user_email}",
            "name": invited_user_name,
        }
    )

    return response

def get_invited_users(user_email: str):
    ddb_table = get_db_table()

    response = ddb_table.query(
        KeyConditionExpression=Key("PK").eq(user_email) & Key("SK").begins_with("USER#")
    )

    return response["Items"]

def delete_inventory(user_email: str, inventory_id: str):
    ddb_table = get_db_table()

    response = ddb_table.delete_item(
        Key={
            "PK": user_email,
            "SK": f"#INVENTORY{inventory_id}",
        }
    )

    return response

def update_inventory(
    user_email: str,
    inventory_id: str,
    new_inventory_name: str,
    new_inventory_price: int,
):
    ddb_table = get_db_table()

    response = ddb_table.put_item(
        Item={
            "PK": user_email,
            "SK": f"#INVENTORY{inventory_id}",
            "name": new_inventory_name,
            "price": new_inventory_price,
        }
    )

    return response

#print(register_account(
#      user_email = input("Telcea tu email: "),
#      user_name = input("Teclea tu nombre de usuario: ")
#))
#print(register_inventory(
#      user_email = input("Telcea tu email: "),
#      inventory_name = input("Teclea el nombre del inventario: "),
#      inventory_price = input("Teclea el precio ")
#))
#print(get_inventory(
#      user_email = input("Telcea tu email: ")
#))
#print(invite_account(
#      user_email = input("Telcea tu email: "),
#      invited_user_email = input("Teclea el email invitado: "),
#      invited_user_name = input("Teclea el nombre invitado: ")
#))
#print(get_invited_users(
#      user_email = input("Telcea tu email: "),
#))
#print(delete_inventory(
#      user_email = input("Telcea tu email: "),
#      inventory_id = input("Teclea el ID del producto a eliminar: ")
#))
#print(update_inventory(
#      user_email = input("Telcea tu email: "),
#      inventory_id = input("Teclea el ID del producto a actualizar: "),
#      new_inventory_name = input("Teclea el nuevo nombre: "),
#      new_inventory_price = input("Teclea el nuevo precio: ")

#))