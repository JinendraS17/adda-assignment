from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

# Configuration - facility, start_time, end_time, booking_amount
facilities = {
    "Clubhouse": {
        "10:00-16:00": 100,
        "16:00-22:00": 500
    },
    "Tennis Court": {
        "00:00-23:59": 50
    }
}

bookings = {}  # Store booked slots


def is_slot_available(facility, date, start_time, end_time):
    if facility not in bookings:
        bookings[facility] = {}
    if date not in bookings[facility]:
        return True
    for booked_start, booked_end in bookings[facility][date]:
        if not (end_time <= booked_start or start_time >= booked_end):
            return False
    return True


def book_facility(facility, date, start_time, end_time):
    if facility not in bookings:
        bookings[facility] = {}
    if date not in bookings[facility]:
        bookings[facility][date] = []
    bookings[facility][date].append((start_time, end_time))


def calculate_booking_amount(facility, start_time, end_time):
    booking_amount = 0
    for period, amount in facilities[facility].items():
        start_period, end_period = period.split("-")
        if start_time >= start_period and end_time <= end_period:
            booking_amount += amount * (int(end_time.split(':')[0]) - int(start_time.split(':')[0]))
            break
    return booking_amount


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/book', methods=['POST'])
def book():
    facility = request.form['facility']
    date = request.form['date']
    start_time = request.form['start_time']
    end_time = request.form['end_time']
    if is_slot_available(facility, date, start_time, end_time):
        booking_amount = calculate_booking_amount(facility, start_time, end_time)
        book_facility(facility, date, start_time, end_time)
        response = f"{facility}, {date}, {start_time} - {end_time}, Booked, Rs. {booking_amount}"
    else:
        response = f"{facility}, {date}, {start_time} - {end_time}, Booking Failed, Already Booked"
    return jsonify({'message': response})


if __name__ == '__main__':
    app.run(debug=True)
