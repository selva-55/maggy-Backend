import json
import uuid

from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.decorators import api_view
from .models import Login, Hotels, Items, Cart, ItemsOrdered, OrderData
from django.utils import timezone
from datetime import datetime
import pytz

# Create your views here.
@csrf_exempt
def login_user(request):
    try:
        if request.method == 'POST':
            request_data = json.loads(request.body)
            phonenumber = request_data.get('phonenumber')
            password = request_data.get('password')
            auth = Login.objects.filter(phonenumber=phonenumber)
            if phonenumber and password !=None:
                if auth:
                    for value in auth:
                        id = value.id
                        dbphonenumber = value.phonenumber
                        dbpassword = value.password
                        if check_password(password, dbpassword):
                            refresh = RefreshToken()
                            return JsonResponse(
                                {
                                    'refresh': str(refresh),
                                    'access': str(refresh.access_token),
                                    'msg': 'success',
                                    'name':value.name,
                                    'id':value.id,
                                    'location':value.location
                                }
                            )
                        else:
                            raise ValueError('Password Incorrect!!!')
                else:
                    raise ValueError('Register')
            else:
                raise ValueError('Fields empty*')
    except ValueError as vs:
        return JsonResponse({
            'msg':f'{vs}'
        }, status=500)


@api_view(['GET'])
def User(request):
    value = request.GET.get('id')
    user_details = Login.objects.filter(id=value)
    for details in user_details:

        data = {
            'name':details.name,
            'id':details.id,
            'location':details.location,
            'phoneNumber':details.phonenumber,
            'address':details.address,
            'email':details.email        }
        return JsonResponse(data,safe=False)


@api_view(['POST'])
def userUpdate(request):
    load = json.loads(request.body)
    userId = load.get('userId')
    name = load.get('name')
    email = load.get('email')
    phoneNumber = load.get('phoneNumber')
    password = load.get('password')
    if not password :
        Login.objects.filter(id=userId).update(name=name, email=email, phonenumber=phoneNumber)
        return JsonResponse('Profile updated',safe=False)
    else:
        Login.objects.filter(id=userId).update(name=name, email=email, phonenumber=phoneNumber, password=make_password(password))
        return JsonResponse('Password updated',safe=False)


@api_view(['POST'])
def hotelReg(request):
    value = json.loads(request.body)
    for multiple_hotel in value:
        restaurantName = multiple_hotel.get('restaurantsName')
        rating = multiple_hotel.get('rating')
        deliveryTime = multiple_hotel.get('deliveryTime')
        cityLocation = multiple_hotel.get('cityLocation')
        city = multiple_hotel.get('city')
        distance = multiple_hotel.get('distance')
        items_data = multiple_hotel.get('items')
        hotel_instance = Hotels.objects.create(
            restaurantName=restaurantName,
            rating=rating,
            deliveryTime=deliveryTime,
            cityLocation=cityLocation,
            city=city,
            distance=distance
        )

        for loopItems in items_data:
            item = loopItems.get('item')
            rate = loopItems.get('rate')
            item_create = Items.objects.create(item=item, rate=rate)
            hotel_instance.items.add(item_create)

    return JsonResponse({
        'msg': 'hotels Register Successfully'
    })

@api_view(['GET'])
def fetch(request):
    data = []
    value = Hotels.objects.all()
    for hotels in value:
        restaurantName = hotels.restaurantName
        rating = hotels.rating
        deliveryTime = hotels.deliveryTime
        cityLocation = hotels.cityLocation
        distance = hotels.distance
        item_id = hotels.id
        items_list = Items.objects.filter(hotels__id=item_id)
        hotel_items=[]
        for loopItem in items_list:
            hotel_items.append({
                'item':loopItem.item,
                'rate':loopItem.rate
            })
        data.append({
            'restaurantName': restaurantName,
            'rating': rating,
            'deliveryTime': deliveryTime,
            'cityLocation': cityLocation,
            'distance': distance,
            'items':hotel_items
        })
    return JsonResponse(data,safe=False)

@csrf_exempt
def Resigter(request):
    try:
        if request.method == 'POST':
            request_data = json.loads(request.body)
            email = request_data.get('email')
            password = request_data.get('password')
            phonenumber = request_data.get('phonenumber')
            name = request_data.get('name')
            hashed_password = make_password(password)
            verify_phonenumber = Login.objects.filter(phonenumber=phonenumber)
            if (email and password and phonenumber and name != None):
                if verify_phonenumber:
                    return JsonResponse({
                        'message': 'Login'
                    })
                else:
                    Login.objects.create(email=email, password=hashed_password, phonenumber=phonenumber,
                                         name=name)
                    return JsonResponse({
                        'msg': 'success'
                    })

            else:
                raise ValueError("Require all fields*")
        else:
            raise ValueError("method not allowed")
    except ValueError as ve:
        return JsonResponse({
            'msg':f'{ve}'
        },status=500)

@api_view(['POST'])
def LocationSetup(request):
    request_load = json.loads(request.body)
    user_id = request_load.get('user_id')
    location = request_load.get('location')
    Login.objects.filter(id=user_id).update(location=location)
    city_restaurants = Hotels.objects.filter(city=location)
    data=[]
    for city_based_restaurants in city_restaurants:
        restaurantName = city_based_restaurants.restaurantName
        rating = city_based_restaurants.rating
        deliveryTime = city_based_restaurants.deliveryTime
        cityLocation = city_based_restaurants.cityLocation
        distance = city_based_restaurants.distance
        city = city_based_restaurants.city
        item_id = city_based_restaurants.id
        items_list = Items.objects.filter(hotels__id=item_id)
        hotel_items = []
        for loopItem in items_list:
            hotel_items.append({
                'item': loopItem.item,
                'rate': loopItem.rate
            })
        data.append({
            'restaurantName': restaurantName,
            'rating': rating,
            'deliveryTime': deliveryTime,
            'cityLocation': cityLocation,
            'distance': distance,
            'city': city,
            'items': hotel_items
        })
    return JsonResponse(data, safe=False)

@api_view(['GET'])
def RestaurantsItem(request):
    city = request.GET.get('city')
    restaurantName = request.GET.get('restaurantName')
    fil = Hotels.objects.filter(city=city, restaurantName=restaurantName)
    data = []
    for city_based_restaurants in fil:
        restaurantName = city_based_restaurants.restaurantName
        rating = city_based_restaurants.rating
        deliveryTime = city_based_restaurants.deliveryTime
        cityLocation = city_based_restaurants.cityLocation
        distance = city_based_restaurants.distance
        city = city_based_restaurants.city
        item_id = city_based_restaurants.id
        items_list = Items.objects.filter(hotels__id=item_id)
        hotel_items = []
        for loopItem in items_list:
            hotel_items.append({
                'item': loopItem.item,
                'rate': loopItem.rate
            })
        data.append({
            'restaurantName': restaurantName,
            'rating': rating,
            'deliveryTime': deliveryTime,
            'cityLocation': cityLocation,
            'distance': distance,
            'city': city,
            'items': hotel_items
        })
    return JsonResponse(data, safe=False)




@api_view(['POST'])
def CartAdd(request):
    load = json.loads(request.body)
    userId = load.get('userId')
    item = load.get('item')
    HotelName = load.get('HotelName')
    city = load.get('city')
    Hotellocation = load.get('Hotellocation')
    itemRate = load.get('itemRate')
    distance = load.get('distance')
    deliveryTime = load.get('deliveryTime')
    Cart.objects.create(
        userId=userId,
        item=item,
        HotelName=HotelName,
        city=city,
        Hotellocation=Hotellocation,
        itemRate=itemRate,
        distance=distance,
        deliveryTime=deliveryTime
    )
    return JsonResponse("Item Added To Cart", safe=False)

@api_view(['DELETE'])
def CartDelete(request):
    id = request.GET.get('id')
    Cart.objects.filter(
        id=id
    ).delete()
    return JsonResponse("Item Deleted From Cart", safe=False)

@api_view(['GET'])
def CartItems(request):
    id = request.GET.get('id')
    city = request.GET.get('city')
    cartItems = Cart.objects.filter(userId=id,city=city)
    data=[]
    for items in cartItems:
        data.append({
            "id":items.id,
            "userId": items.userId,
            "item": items.item,
            "HotelName": items.HotelName,
            "city": items.city,
            "Hotellocation": items.Hotellocation,
            "itemRate": items.itemRate,
            "distance": items.distance,
            'deliveryTime':items.deliveryTime
        })
    return JsonResponse(data, safe=False)

@api_view(['POST'])
def Remove_different_cart_restaurant(request):
    load = json.loads(request.body)
    user_id = load.get('userId')
    Cart.objects.filter(userId=user_id).delete()
    return JsonResponse('Cart Item Removed Successfully', safe=False)

@api_view(['POST'])
def AddAddress(request):
    load = json.loads(request.body)
    userId = load.get('userId')
    address = load.get('address')
    Login.objects.filter(id=userId).update(address=address)
    return JsonResponse({
        'msg':'success',
        'address':address
    }, safe=False)

@api_view(['POST'])
def OrderItem(request):
    load = json.loads(request.body)
    order_data_ids = []
    for details in load:
        userId = details.get('userId')
        HotelName = details.get('HotelName')
        city = details.get('city')
        Hotellocation = details.get('Hotellocation')
        item_data = details.get('item')
        totalItems = details.get('totalItems')
        deliveryPerson = details.get('deliveryPerson')
        deliveryTime = details.get('deliveryTime')
        TotalItemAmount = details.get('TotalItemAmount')
        TotalPay = details.get('TotalPay')
        orderStatus = details.get('orderStatus')

        hotel_instance = OrderData.objects.create(
            id=uuid.uuid4(),
            userId=details.get('userId'),
            HotelName=details.get('HotelName'),
            city=details.get('city'),
            Hotellocation=details.get('Hotellocation'),
            totalItems=details.get('totalItems'),
            deliveryPerson=details.get('deliveryPerson'),
            deliveryTime=details.get('deliveryTime'),
            TotalItemAmount=details.get('TotalItemAmount'),
            TotalPay=details.get('TotalPay'),
            orderStatus=details.get('orderStatus')
        )
        for itemDetails in item_data:
            item = itemDetails.get('item')
            itemCount = itemDetails.get('itemCount')
            rate = itemDetails.get('rate')
            item_create = ItemsOrdered.objects.create(item=item, rate=rate, itemCount=itemCount)
            hotel_instance.item.add(item_create)


        order_data_ids.append({'id':hotel_instance.id, 'deliveryTime':hotel_instance.deliveryTime})  # Add the id to the list
    return JsonResponse({
        'msg': 'success',
        'orderId':order_data_ids[0].get('id'),
        'deliveryTime':order_data_ids[0].get('deliveryTime')
    })

@api_view(['GET'])
def OrderItemRemoveCart(request):
    userId = request.GET.get('id')
    Cart.objects.filter(userId=userId).delete()
    return JsonResponse({
        'msg': 'Cart Items deleted'
    })


@api_view(['POST'])
def passwordCheck(request):
    load = json.loads(request.body)
    userId = load.get('userId')
    password = load.get('password')
    dbfilter = Login.objects.filter(id=userId)
    for get_password in dbfilter:
        dbpassword = get_password.password
        if check_password(password, dbpassword):
            return JsonResponse({
                'msg':'success'
            })
        else:
            return JsonResponse({
                'msg': 'fail'
            })


@api_view(['GET'])
def OrderHistoryFetch(request):
    userId = request.GET.get('id')
    get_history = OrderData.objects.filter(userId=userId)
    ordered_history_data = []
    for order_data in get_history:
        id = order_data.id
        userId = order_data.userId
        HotelName = order_data.HotelName
        city = order_data.city
        Hotellocation = order_data.Hotellocation
        item_data = ItemsOrdered.objects.filter(OrderedItems=id)
        totalItems = order_data.totalItems
        deliveryPerson = order_data.deliveryPerson
        deliveryPerson = order_data.deliveryPerson
        TotalItemAmount = order_data.TotalItemAmount
        TotalPay = order_data.TotalPay
        orderStatus = order_data.orderStatus
        orderTime = order_data.orderTime


        input_timestamp = datetime.strptime(str(orderTime), "%Y-%m-%d %H:%M:%S.%f%z")
        ist_timezone = pytz.timezone("Asia/Kolkata")
        ist_timestamp = input_timestamp.astimezone(ist_timezone)
        formatted_ist_timestamp = ist_timestamp.strftime("%Y-%m-%d %H:%M:%S.%f")

        item_list = []
        for items in item_data:
            item = items.item
            itemCount = items.itemCount
            rate = items.rate
            item_list.append({
                'item':item,
                'itemCount':itemCount,
                'rate':rate
            })
        ordered_history_data.append({
            "id": id,
            "userId": userId,
            "HotelName": HotelName,
            "city": city,
            "Hotellocation": Hotellocation,
            "items": item_list,
            "totalItems": totalItems,
            "deliveryPerson": deliveryPerson,
            "TotalItemAmount": TotalItemAmount,
            "TotalPay": TotalPay,
            "orderStatus": orderStatus,
            'orderTime': formatted_ist_timestamp
        })
    print(timezone.now())
    return JsonResponse(ordered_history_data, safe=False)


@api_view(['POST'])
def ReorderToCart(request):
    load = json.loads(request.body)
    userId = load.get('userId')
    items = load.get('items')
    HotelName = load.get('HotelName')
    city = load.get('city')
    Hotellocation = load.get('Hotellocation')
    get_hotel_Detail = Hotels.objects.filter(restaurantName=HotelName)
    for get_detail in get_hotel_Detail:
        distance = get_detail.distance
        deliveryTime = get_detail.deliveryTime
    for get_item in items:
        item = get_item.get('item')
        itemRate = get_item.get('rate')
        Cart.objects.create(
            userId=userId,
            item=item,
            HotelName=HotelName,
            city=city,
            Hotellocation=Hotellocation,
            itemRate=itemRate,
            distance=distance,
            deliveryTime=deliveryTime
        )

    return JsonResponse("Item Reloaded To Cart", safe=False)

@api_view(['POST'])
def ResetPassword(request):
    try:
        load = json.loads(request.body)
        email = load.get('email')
        password = load.get('password')
        print(email, password)
        email_check = Login.objects.filter(email=email)
        if email_check :
            Login.objects.filter(email=email).update(password=make_password(password))
            return JsonResponse({
                'msg': 'success'
            }, safe=False)

        else:
            raise ValueError(f'email not found')

    except ValueError as error:
        return JsonResponse({
            'msg':f'{error}'
        },safe=False , status=500)













