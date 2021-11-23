import json

from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q, Max, Min
from datetime         import datetime, timedelta

from accomodations.models import Accomodation, Room
from bookings.models      import Booking

class AccomodationListView(View):
    def get_available_accomodations(self, start_date, end_date):
        date_list = []

        start_date_converted = datetime.strptime(start_date, '%Y-%m-%d')
        end_date_converted   = datetime.strptime(end_date, '%Y-%m-%d')

        num_days = (end_date_converted - start_date_converted).days

        for x in range(num_days):
            date_to_add = start_date_converted + timedelta(days=x)
            date_list.append(date_to_add)

        available_accomodations = []

        is_available = True

        for accomodation in Accomodation.objects.all():
            bookings = accomodation.booking_set.all()
        
            for booking in bookings:
                if not is_available:
                    break

                for date in date_list:
                    if booking.start_date <= datetime.date(date) < booking.end_date:
                        is_available = False
                        break

            if is_available:
                available_accomodations.append(accomodation)

            if not is_available:
                is_available = True

        return available_accomodations

    def get(self, request):
        try:
            category   = request.GET.get('category')
            sorting    = request.GET.get('sort','id')
            max_price  = request.GET.get('max_price', 1000000)
            min_price  = request.GET.get('min_price', 0)
            max_people = request.GET.get('max_people')
            start_date = request.GET.get('start_date', '2021-11-01')
            end_date   = request.GET.get('end_date', '2021-11-30')
            OFFSET     = int(request.GET.get('offset',0))
            LIMIT      = int(request.GET.get('limit', 6))
            search     = request.GET.get('search')

            q = Q(room__price__range = (min_price, max_price))

            if category:
                q &= Q(category_id = category)   

            if max_people:
                q &= Q(room__max_people__gte = max_people)
            
            if search:
                q &= Q(name__icontains = search)
            
            sort = {
                'high' : '-max_price',
                 'low' : 'min_price',
                  'id' : 'id',
                 '-id' : '-id'
            }
            
            accomodations = self.get_available_accomodations(start_date, end_date)
            
            ids = [acc.id for acc in accomodations]

            q &= Q(id__in=ids)

            accomodations = Accomodation.objects.filter(q)\
                                                .annotate(max_price=Max('room__price'), min_price=Min('room__price'))\
                                                .order_by(sort[sorting])\
                                                .distinct()[OFFSET:OFFSET+LIMIT]

            result = {
                'info_list' : [{
                    'id'         : accomodation.id,
                    'name'       : accomodation.name,
                    'category'   : accomodation.category.name,
                    'address'    : accomodation.address,
                    'max_people' : accomodation.room_set.aggregate(max_people=Max('max_people'))['max_people'],
                    'min_people' : accomodation.room_set.first().min_people,
                    'max_price'  : accomodation.max_price,
                    'min_price'  : accomodation.min_price,
                    'image_url'  : [image.image_url for image in accomodation.images.all()]
                } for accomodation in accomodations]
            }
            return JsonResponse({'result' : result}, status=200)
        
        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400)

class AccomodationDetailView(View):
    def get(self, request, accomodation_id):
        try:
            if not Accomodation.objects.filter(id=accomodation_id).exists():
                return JsonResponse({'message' : 'DOES NOT EXISTS'}, status=404)

            accomodation = Accomodation.objects.get(id=accomodation_id)
            rooms        = accomodation.room_set.all()
            

            start_date = request.GET.get('start_date')
            end_date = request.GET.get('end_date')

            if start_date and end_date:
                start_dates = datetime.strptime(start_date, '%Y-%m-%d') 
                end_dates   = datetime.strptime(end_date, '%Y-%m-%d') 

            result = {
                'id'           : accomodation.id,
                'name'         : accomodation.name,
                'introduction' : accomodation.introduction,
                'address'      : accomodation.address,
                'longitude'    : accomodation.longitude,
                'latitude'     : accomodation.latitude,
                'phone_number' : accomodation.phone_number,
                'email'        : accomodation.email,
                'images'       : [room.roomimage_set.all()[0].image_url for room in Room.objects.filter(accomodation_id=accomodation_id)],
                'rooms'        :[{
                    'id'            : room.id,
                    'name'          : room.name,
                    'max_people'    : room.max_people,
                    'min_people'    : room.min_people,
                    'price'         : room.price,
                    'number_of_bed' : room.number_of_bed,
                    'options'        : [{
                        'name' : option.name, 
                    }for option in room.option.all()],
                    'room_image' : [{
                        'url' : room_image.image_url,
                    }for room_image in room.roomimage_set.all()]
                }for room in rooms]}
            
            return JsonResponse({'result' : result}, status = 200)

        except KeyError:
            return JsonResponse({'message' : 'KEY_ERROR'}, status=400) 
