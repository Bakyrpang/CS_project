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
cursor.execute("CREATE TABLE IF NOT EXISTS Bookings(bookingId INT AUTO_INCREMENT PRIMARY KEY, dateBooked DATE, duration INT, guestId INT, roomId INT)")
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

def checkAvailability(data):
    #Check if booking is available for the date and duration
    cursor.execute("SELECT * FROM bookings ORDER BY roomId, dateBooked")
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

    for group in final_list:
        for i in range(1, len(group)):
            #check if date comes after the end of a booking and before the beginning of a new one
            if data["dateBooked"].date() > group[i-1]["dateBooked"] + datetime.timedelta(days = group[i-1]["duration"]):
                if data["dateBooked"].date() + datetime.timedelta(days = data["duration"]) < group[i]["dateBooked"]:
                    available_rooms.append(group[i]["roomId"])

        #check if date comes after the end of the last booking
        if data["dateBooked"].date() > group[-1]["dateBooked"] + datetime.timedelta(days = group[-1]["duration"]):
                available_rooms.append(group[-1]["roomId"])

    if len(final_list) == 0: #if final list is 0, no bookings made, therefore all rooms are available
        return "all rooms are available"

    if data["roomId"] is None:
        return available_rooms if len(available_rooms) > 0 else None
    else:
        available_rooms = list((n for n in available_rooms if n == data["roomId"]))
        return available_rooms if len(available_rooms) > 0 else None

def create_booking(data: dict):
    if checkAvailability(data) is not None:
        if data.get("guestId") is None:
            #generate guest Id using sql
            cursor.execute("INSERT INTO Guests(roomId, bookingId, name, age) VALUES(%s, NULL, %s, %s)", [data.get("roomId"), data.get("name"), data.get("age")])
            #add newly generated guest Id into data
            data["guestId"] = cursor.lastrowid
        else:
            cursor.execute("INSERT INTO Guests(guestId, roomId, bookingId, name, age) VALUES(%s, %s, %s, %s, %s)", [data.get("guestId"), data.get("roomId"), data.get("bookingId"), data.get("name"), data.get("age")])
        cursor.execute("INSERT INTO BOOKINGS(dateBooked, duration, guestId, roomId) VALUES(%s, %s, %s, %s)", [data.get("dateBooked"), data.get("duration"), data.get("guestId"), data.get("roomId")])

        #get generated booking Id
        data["bookingId"] = cursor.lastrowid
        cursor.execute("UPDATE GUESTS SET bookingId = %s WHERE bookingId IS NULL", [data.get("bookingId")])
        database.commit() #commit changes

create_booking({"roomId" : 1,
                "name" : "a",
                "age" : 18,
                "dateBooked" : datetime.datetime.today(),
                "duration": 7})
