import json
import pytz, datetime

from django.test           import TestCase, Client
from unittest              import mock

from accomodations.models  import Accomodation, Category, Room, Option, RoomOption, AccomodationImage
from bookings.models       import Booking, PaymentType, BookingStatus
from users.models          import User


class BookingsTest(TestCase):
    def setUp(self):
        self.maxDiff = None
        User.objects.bulk_create([
            User(
                id    = 1,
                email = 'aaa@aaa.com',
                kakao_id = '12321312',
                nick_name = 'qqq'
                ),
            User(
                id    = 2,
                email = 'bbb@bbb.com',
                kakao_id = '12332312',
                nick_name = 'aaa'
                ),
            User(
                id    = 3,
                email = 'ccc@ccc.com',
                kakao_id = '12312112',
                nick_name = 'bbb'
                )
        ])
        Category.objects.bulk_create([
            Category(
                id   = 1,
                name = '호텔'
            ),
            Category(
                id   = 2,
                name = '펜션'
            ),
            Category(
                id   = 3,
                name = '게스트하우스'
            )
        ])
        PaymentType.objects.bulk_create([
            PaymentType(
                id   = 1,
                name = '신용카드'
            ),
            PaymentType(
                id   = 2,
                name = '무통장입금'
            ),
            PaymentType(
                id   = 3,
                name = '카카오페이'
            )
        ])
        BookingStatus.objects.bulk_create([
            BookingStatus(
                id     = 1,
                status = 'INITIATED'
            ),
            BookingStatus(
                id     = 2,
                status = 'PENDING'
            ),
            BookingStatus(
                id     = 3,
                status = 'COMPLETED'
            ),
            BookingStatus(
                id     = 4,
                status = 'CANCELED'
            )
        ])
        Accomodation.objects.bulk_create([
            Accomodation(
                id           = 1,
                name         = 'sfsdf',
                introduction = 'sfsfsfs',
                address      = 'dsfsfssfsdfsf',
                longitude    = 111.00,
                latitude     = 121.00,
                phone_number = '01044445555',
                email        = 'sdfsdf@dsfsf.com',
                category_id  = 1
                ),
            Accomodation(
                id           = 2,
                name         = '좋은곳',
                introduction = '좋아',
                address      = '경기도어딘가',
                longitude    = 141.00,
                latitude     = 161.00,
                phone_number = '01055555555',
                email        = 'asd@dsfsf.com',
                category_id  = 2
                ),
            Accomodation(
                id           = 3,
                name         = '가고싶은곳',
                introduction = '너무좋아',
                address      = '제주도 어딘가',
                longitude    = 101.00,
                latitude     = 86.00,
                phone_number = '01077775555',
                email        = 'asdf@dsfsf.com',
                category_id  = 3
                )
        ])
        Room.objects.bulk_create([
            Room(
                id              = 1,
                name            = '1번방',
                max_people      = 4,
                min_people      = 2,
                price           = 123456.00,
                accomodation_id = 1,
                number_of_bed   = 2
            ),
            Room(
                id              = 2,
                name            = '2번방',
                max_people      = 6,
                min_people      = 3,
                price           = 323456.00,
                accomodation_id = 2,
                number_of_bed   = 4
            ),
            Room(
                id              = 3,
                name            = '3번방',
                max_people      = 5,
                min_people      = 3,
                price           = 223456.00,
                accomodation_id = 3,
                number_of_bed   = 3
            )
        ])
        Booking.objects.bulk_create([
            Booking(
                id              = 1,
                user_id         = 1,
                accomodation_id = 1,
                room_id         = 1,
                start_date      = '2021-11-18',
                end_date        = '2021-11-21',
                price           = 12300.00,
                number_of_adult = 3,
                payment_type_id = 1,
                user_request    = 'dkfssf',
                name            = '이찬규',
                phone_number    = '01011111111',
                status_id       = 1,
                deleted_at      = '2021-11-24 12:04:35.795671'
                ),
            Booking(
                id              = 2,
                user_id         = 2,
                accomodation_id = 2,
                room_id         = 2,
                start_date      = '2021-11-11',
                end_date        = '2021-11-21',
                price           = 22300.00,
                number_of_adult = 2,
                payment_type_id = 1,
                user_request    = 'dkfdssssf',
                name            = '권은경',
                phone_number    = '01022221111',
                status_id       = 1,
                deleted_at      = '2021-11-24 12:04:35.795631'    
            ),
            Booking(
                id              = 3,
                user_id         = 3,
                accomodation_id = 3,
                room_id         = 3,
                start_date      = '2021-11-21',
                end_date        = '2021-11-24',
                price           = 32300.00,
                number_of_adult = 4,
                payment_type_id = 1,
                user_request    = 'dkfdssssf',
                name            = '손승현',
                phone_number    = '01033331111',
                status_id       = 1,
                deleted_at      = '2021-11-24 12:04:35.715671'    
            )
        ])
        Option.objects.bulk_create([
            Option(
                id    = 1,
                name  = '기본형'
            ),
            Option(
                id    = 2,
                name  = '독채형'
            ),
            Option(
                id    = 3,
                name  = '복층형'
            )
        ])
        RoomOption.objects.bulk_create([
            RoomOption(
                id        = 1,
                room_id   = 1,
                option_id = 1,
            ),
            RoomOption(
                id        = 2,
                room_id   = 2,
                option_id = 2,
            ),
            RoomOption(
                id        = 3,
                room_id   = 3,
                option_id = 3
            )
        ])
        AccomodationImage.objects.bulk_create([
            AccomodationImage(
                id              = 1,
                image_url       = 'sdfsdfsjdlfsjl',
                accomodation_id = 1
            ),
            AccomodationImage(
                id              = 2,
                image_url       = 'sdfsdfsasdajdlfsjl',
                accomodation_id = 2
            ),
            AccomodationImage(
                id              = 3,
                image_url       = 'sdfsdfsasdasjdlfsjl',
                accomodation_id = 3
            )
        ])

    def tearDown(self):
        Booking.objects.all().delete()
        User.objects.all().delete()
        Accomodation.objects.all().delete()
        Category.objects.all().delete()
        PaymentType.objects.all().delete()
        Room.objects.all().delete()
        Option.objects.all().delete()
        RoomOption.objects.all().delete()
        AccomodationImage.objects.all().delete()
        BookingStatus.objects.all().delete()

    def test_bookingsview_post_method_success(self):
        client   = Client()
        
        booked_rooms = [{
            'user_id'         : 2,
            'accomodation_id' : 1,
            'room_id'         : 1,
            'start_date'      : '2021-11-24',
            'end_date'        : '2021-11-29',
            'price'           : 123456.00,
            'number_of_adult' : 3,
            'payment_type_id' : 1,
            'user_request'    : 'dkfssf',
            'name'            : '이찬규',
            'phone_number'    : '01011111111',
            'status_id'       : 1,
            'deleted_at'      : '2021-11-24 12:04:35.715671' 
        }]

        response = client.post('/bookings', json.dumps({'booked_rooms': booked_rooms}), content_type='application/json')
        
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(), {'message' : 'CREATED'})

    def test_bookingsview_get_method_success(self):
        client   = Client()
        response = client.get('/bookings')

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json(),{
            'results' : [
                    {
                    'accomodation'    : 'sfsdf',
                    'room'            : '1번방',
                    'price'           : '12300.00',
                    'start_date'      : '2021-11-18',
                    'end_date'        : '2021-11-21',
                    'number_of_adult' : 3,
                    'user_request'    : 'dkfssf',
                    'name'            : '이찬규',
                    'phone_number'    : '01011111111',
                    'status'          : 1,
                },
            ]
        })

    def test_bookingsview_delete_method_success(self):
        client = Client()
        response = client.delete('/bookings/1')
        self.assertEqual(response.status_code, 200)