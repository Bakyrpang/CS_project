import mysql.connector
import flask

config = {
    'user': 'root',
    'password': 'Password123',
    'host': 'localhost',
}

database = mysql.connector.connect(**config)

#Create main database if it doesn't exist
database._execute_query("CREATE DATABASE IF NOT EXISTS Hotel")

database._execute_query("USE Hotel")
cursor = database.cursor()

#Create tables if they dont exist
cursor.execute("CREATE TABLE IF NOT EXISTS bookings(bookingId INT AUTO_INCREMENT PRIMARY KEY, dateBooked DATE, duration INT, guestId INT, roomId INT)")
cursor.execute("CREATE TABLE IF NOT EXISTS Guests(guestId INT AUTO_INCREMENT PRIMARY KEY, roomId INT, bookingId INT, name VARCHAR(30), age INT)")
cursor.execute("CREATE TABLE IF NOT EXISTS Rooms(roomId INT PRIMARY KEY, occupied BOOL)")

def pack(rawData, table):
    formatted_list = []
    match table:
        case "bookings":
            keys = ("bookingId","dateBooked","duration","guestId","roomId")
            for data in rawData:
                formatted_list.append(dict(zip(keys, data)))

        case "guests":
            keys = ("guestId","roomId", "bookingId", "name", "age")
            for data in rawData:
                formatted_list.append(dict(zip(keys, data)))

        case "rooms":
            keys = ("roomId","occupied")
            for data in rawData:
                formatted_list.append(dict(zip(keys, data)))

    return formatted_list


