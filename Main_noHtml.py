import database
import datetime
while True:
    print('''select option: 
    1) Add guest
    2) View guest records
    3) Search for a guest
    4) Check available rooms for booking
    5) Update Booking
    6) Cancel Booking
    7) Exit''')
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
            data['roomId'] = int(input('Enter room ID(skip if not specified): ')) or None
            data['guestId'] = int(input('Enter guest ID(skip if not specified): ')) or None
            success, bookingId, guestId = database.create_booking(data)
            if success:
                print('Booking added')
                print(f"Booking ID: {bookingId}\nGuest ID: {guestId}")
            else:
                print('Booking not added')

        case 2:
            data = database.get_guest_records()
            for i in data:
                for ii, v in i.items():
                    print(ii+":", v)
                print()
                print("-"*80)
                print()

        case 3:
            guestId = input('Enter guest ID: ')
            if guestId:
                data = database.search_guest(guestId)
                for i in data:
                    for ii, v in i.items():
                        print(ii+":", v)
                if not data:
                    print('No guests found')

        case 4:
            data = {}
            dateBooked = input('Enter date of booking(DD/MM/YYYY): ')
            data["dateBooked"] = datetime.datetime.strptime(dateBooked, '%d/%m/%Y')
            data["duration"] = int(input('Enter duration of booking: '))
            data["roomId"] = None
            rooms = database.check_availability(data)
            for i in rooms:
                print(i, end=", ")

        case 5:
            data = {}
            dateBooked = input('Enter date of booking(DD/MM/YYYY): ')
            dateBooked = datetime.datetime.strptime(dateBooked, '%d/%m/%Y')
            data["dateBooked"] = dateBooked
            data["duration"] = int(input('Enter duration of booking: '))
            data["roomId"] = int(input('Enter room ID(skip if not specified): ')) or None
            data['bookingId'] = int(input('Enter booking ID: '))
            success = database.update_booking(data)
            if success:
                print('Booking updated')
            else:
                print('Booking not updated')
