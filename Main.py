import mysql.connector
import flask
import datetime

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

cursor.execute("SELECT * FROM bookings")
vals = pack(cursor.fetchall(), table="bookings")
for i, v in vals[0].items():
    print(type(v))

def createBooking(data):
    #Check if booking is available for the date and duration
    cursor.execute("SELECT * FROM bookings")
    available_rooms = []
    bookingData = pack(cursor.fetchall(), table="bookings")
    for i in range(1, len(bookingData)):
        if bookingData[i-1]["dateBooked"]+datetime.timedelta(days = bookingData[i-1]["duration"]) < datetime.timedelta(days = data["dateBooked"]):
            if bookingData[i] > data["dateBooked"] + datetime.timedelta(days = data[i]["duration"]):
                available_rooms.append(bookingData[i]["roomId"])

createBooking({"dateBooked":datetime.datetime(2026, 9, 7),"duration": 1,"roomId": 1})


