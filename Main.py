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
    print(v)

def createBooking(data):
    #Check if booking is available for the date and duration
    cursor.execute("SELECT * FROM bookings ORDER BY roomId")
    available_rooms = []
    bookingData = pack(cursor.fetchall(), table="bookings")

    #group rooms by room id
    prev_val = 0
    temp = []
    final_list = []
    for i in bookingData:
        if i["roomId"] != prev_val:
            final_list.append(temp)
            prev_val = i["roomId"]
            temp = [i]
        else:
            temp.append(i)
    else:
        final_list.append(temp)
        final_list.pop(0)
    print(final_list)

    for group in final_list:
        for i in range(1, len(group)):
            #check if date comes after the end of a booking and before the beginning of a new one
            if data["dateBooked"].date() > group[i-1]["dateBooked"] + datetime.timedelta(days = group[i-1]["duration"]):
                if data["dateBooked"].date() + datetime.timedelta(days = data["duration"]) < group[i]["dateBooked"]:
                    available_rooms.append(group[i]["roomId"])

            #check if date comes after the end of the last booking
            if data["dateBooked"].date() > group[-1]["dateBooked"] + datetime.timedelta(days = group[-1]["duration"]):
                available_rooms.append(group[-1]["roomId"])

    print(available_rooms)

createBooking({"dateBooked":datetime.datetime(2026, 9, 10),"duration": 2,"roomId": 1})


