import mysql.connector
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
cursor.execute("CREATE TABLE IF NOT EXISTS Guests(guestId INT AUTO_INCREMENT, roomId INT, bookingId INT, name VARCHAR(30), age INT)")
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

def check_availability(data):
    #Check if booking is available for the date and duration
    cursor.execute("SELECT * FROM bookings ORDER BY roomId, dateBooked")
    available_rooms = []
    bookingData = pack(cursor.fetchall(), table="bookings")
    cursor.execute("SELECT * FROM rooms ORDER BY roomId")
    rooms = pack(cursor.fetchall(), table="rooms")
    rooms = [i["roomId"] for i in rooms] #get just the room Id's

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
            if data["dateBooked"].date() >= group[i-1]["dateBooked"] + datetime.timedelta(days = group[i-1]["duration"]):
                if data["dateBooked"].date() + datetime.timedelta(days = data["duration"]) <= group[i]["dateBooked"]:
                    available_rooms.append(group[i]["roomId"])

        #check if date comes after the end of the last booking
        if data["dateBooked"].date() >= group[-1]["dateBooked"] + datetime.timedelta(days = group[-1]["duration"]):
            available_rooms.append(group[-1]["roomId"])

        #check if date comes before the first booking
        if data["dateBooked"].date() + datetime.timedelta(days = data["duration"]) <= group[0]["dateBooked"]:
            available_rooms.append(group[0]["roomId"])

    #add rooms that have no booking data whatsoever
    available_rooms.extend([i for i in rooms if all(i != group[0]["roomId"] for group in final_list)])

    if data["roomId"] is None:
        return available_rooms if len(available_rooms) > 0 else None
    else:
        available_rooms = list((n for n in available_rooms if n == data["roomId"]))
        return available_rooms if len(available_rooms) > 0 else None

def create_booking(data: dict):
    available_rooms = check_availability(data)
    if available_rooms is not None:
        data["roomId"] = data["roomId"] or available_rooms[0] #give the first available room incase no room is specified
        if data.get("guestId") is None:
            #generate guest Id using sql
            cursor.execute("INSERT INTO Guests(roomId, bookingId, name, age) VALUES(%s, NULL, %s, %s)", [data.get("roomId"), data.get("name"), data.get("age")])
            #add newly generated guest Id into data
            data["guestId"] = cursor.lastrowid
        else:
            cursor.execute("INSERT INTO Guests(guestId, roomId, bookingId, name, age) VALUES(%s, %s, NULL, %s, %s)", [data.get("guestId"), data.get("roomId"), data.get("name"), data.get("age")])
        cursor.execute("INSERT INTO BOOKINGS(dateBooked, duration, guestId, roomId) VALUES(%s, %s, %s, %s)", [data.get("dateBooked"), data.get("duration"), data.get("guestId"), data.get("roomId")])

        #get generated booking Id
        data["bookingId"] = cursor.lastrowid
        cursor.execute("UPDATE GUESTS SET bookingId = %s WHERE bookingId IS NULL", [data.get("bookingId")])
        database.commit() #commit changes

        return True #booking successful
    else:
        return False #booking unsuccessful

def search_guest(guestId, sorting = "guestId", desc = False):
    cursor.execute("SELECT * FROM Guests WHERE guestId = %s ORDER BY %s %s", [guestId, sorting, "DESC" if desc else "ASC"])
    data = pack(cursor.fetchall(), table="guests")
    return data

def search_booking(bookingId, sorting = "bookingId", desc = False):
    cursor.execute("SELECT * FROM Bookings WHERE bookingId = %s ORDER BY %s %s", [bookingId, sorting, "DESC" if desc else "ASC"])
    data = pack(cursor.fetchall(), table="bookings")
    return data

print(search_booking(3))

print(create_booking({"roomId" : None,
                "name" : "d",
                "age" : 18,
                "dateBooked" : datetime.datetime.today()+datetime.timedelta(days = 7),
                "duration": 7,
                "guestId" : 4}))