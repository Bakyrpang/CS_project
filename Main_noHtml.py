import database
import datetime

#define values in outer scope
dateBooked = roomId = guestId = success = data = rooms = duration = None

def refresh_values():
    dateBooked = roomId = guestId = success = data = rooms = duration = None

while True:
    print('''select option: 
    1) Add booking
    2) View guest records
    3) Search for a guest
    4) Search booking record
    5) Check available rooms for booking
    6) Update Booking
    7) Cancel Booking
    8) Exit''')
    option = int(input("Enter option: "))
    print("-"*80)
    match option:
        case 1:
            data = {}
            dateBooked = input('Enter date of booking(DD/MM/YYYY): ')
            dateBooked = datetime.datetime.strptime(dateBooked, '%d/%m/%Y')
            data['dateBooked'] = dateBooked
            data['duration'] = int(input('Enter duration of booking: '))
            data['name'] = input('Enter name of guest: ')
            data['age'] = int(input('Enter age of guest: '))
            roomId = input('Enter room ID(skip if not specified): ')
            data['roomId'] = int(roomId) if roomId else None
            guestId = input('Enter guest ID(skip if not specified): ')
            data['guestId'] = int(guestId) if guestId else None
            success, bookingId, guestId = database.create_booking(data)
            if success:
                print('Booking added')
                print(f"Booking ID: {bookingId}\nGuest ID: {guestId}")
            else:
                print('Booking not added')
            print("-" * 80)
            refresh_values()

        case 2:
            data = database.get_guest_records()
            for i in data:
                for ii, v in i.items():
                    print(ii+":", v)
                print("-"*80)
            refresh_values()

        case 3:
            guestId = input('Enter guest ID: ')
            if guestId:
                data = database.search_guest(guestId)
                for i in data:
                    for ii, v in i.items():
                        print(ii+":", v)
                if not data:
                    print('No guests found')
            print("-" * 80)
            refresh_values()
        case 4:
            bookingId = input('Enter booking ID: ')
            booking = database.search_booking(bookingId)
            if booking:
                for i, v in booking[0].items():
                    print(i+":", v)
            else:
                print('No booking found')
            print("-" * 80)
            refresh_values()

        case 5:
            data = {}
            dateBooked = input('Enter date of booking(DD/MM/YYYY): ')
            data["dateBooked"] = datetime.datetime.strptime(dateBooked, '%d/%m/%Y')
            data["duration"] = int(input('Enter duration of booking: '))
            data["roomId"] = None
            rooms = database.check_availability(data)
            if rooms:
                print("Available rooms: ")
                for i in rooms:
                    print(i)
            else:
                print('No rooms found')
            print()
            print("-"*80)
            refresh_values()

        case 6:
            data = {}
            bookingId = input('Enter booking ID: ')
            bookingId = int(bookingId) if bookingId else None
            print("skip following parameters if unchanged")
            data['bookingId'] = int(bookingId) if bookingId else None
            dateBooked = input('Enter date of booking(DD/MM/YYYY): ')
            dateBooked = datetime.datetime.strptime(dateBooked, '%d/%m/%Y') if dateBooked else None
            data["dateBooked"] = dateBooked
            duration = input('Enter duration of booking: ')
            data['duration'] = int(duration) if duration else None
            roomId = input('Enter room ID: ')
            data['roomId'] = int(roomId) if roomId else None
            success = database.update_booking(data['bookingId'], data)
            if success:
                print('Booking updated')
            else:
                print('Booking not updated')
            print("-"*80)
            refresh_values()

        case 7:
            bookingId = input('Enter booking ID: ')
            database.cancel_booking(bookingId)
            print("Booking deleted")
            print("-"*80)
            refresh_values()

        case 8:
            break
