import json
import datetime

from django.views     import View
from django.http      import JsonResponse
from enum             import Enum

from bookings.models  import Booking
from core.utils       import signin_decorator

class Status(Enum):
    INITIATED = 1
    PENDING   = 2
    COMPLETED = 3
    CANCELED  = 4

class BookingView(View):
    @signin_decorator
    def post(self, request):
        try:
            user = request.user    
            data = json.loads(request.body)
            booked_rooms = data["booked_rooms"]

            Booking.objects.bulk_create([
                Booking(
                    user_id         = user.id,
                    accomodation_id = booked_room['accomodation_id'],
                    room_id         = booked_room['room_id'],
                    start_date      = booked_room['start_date'],
                    end_date        = booked_room['end_date'],
                    price           = booked_room['price'],
                    number_of_adult = booked_room['number_of_adult'],
                    payment_type_id = booked_room['payment_type_id'],
                    user_request    = booked_room['user_request'],
                    name            = booked_room['name'],
                    phone_number    = booked_room['phone_number'],
                    status_id       = Status.INITIATED.value
                ) for booked_room in booked_rooms
            ])

            return JsonResponse({'message' : 'CREATED'}, status = 201)

        except KeyError:
            return JsonResponse({'message' : 'KEY ERROR'}, status = 400)

    @signin_decorator
    def get(self, request):
        user_id = request.user.id
        
        bookings = Booking.objects.filter(user_id=user_id)

        results = [
            {
                "accomodation"    : booking.accomodation.name,
                "room"            : booking.room.name,
                "price"           : booking.price, 
                "start_date"      : booking.start_date,
                "end_date"        : booking.end_date,
                "number_of_adult" : booking.number_of_adult,
                "user_request"    : booking.user_request,
                "name"            : booking.name,
                "phone_number"    : booking.phone_number,
                "status"          : booking.status_id
            } for booking in bookings]
        
        return JsonResponse( {'results' : results}, status = 201)

    @signin_decorator
    def delete(self, request, booking_id):
        try:
            user_id = request.user.id
            booking = Booking.objects.get(user_id=user_id, id=booking_id)

            booking.status_id  = Status.CANCELED.value
            booking.deleted_at = datetime.datetime.now()
            booking.save()

            return JsonResponse({'message' : 'BOOKED INFORMATION DELETED'}, status = 200)
            
        except KeyError:
            return JsonResponse({'message' : 'KEY ERROR'}, status = 400)