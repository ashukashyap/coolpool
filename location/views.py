from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from django.contrib import messages
from django.contrib.gis.geoip2 import GeoIP2
from geoip2.errors import AddressNotFoundError
from user_agents import parse
# Create your views here.

def index(request):
    return HttpResponse("this is a device")

def login_req(request):
    if request.method == "POST":
        username = request.POST['userName']
        password = request.POST['password']
        user = authenticate(username = username,password = password)
        if user is not None:
            login(request,user)
            messages.success(request,"login successful")
            return redirect("index")
        else:
            messages.error(request,"Invalid credential! Try Again")
            return redirect("login_req")



    else:
        return render(request,'login.html')

def register(request):
    if request.method == "POST":
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['userName']
        password = request.POST['password']

        user = User.objects.create_user(username, email,password)
        user.first_name = fname
        user.last_name = lname
        
        user.save()
        return redirect('/')
    else:
        return render(request,'register.html')
    

from pprint import pprint
from django.shortcuts import render, HttpResponse
from django.contrib.gis.geoip2 import GeoIP2

import geoip2.database

import geoip

# def home(request):
#     # Get the user's IP address from the request object
#     user_ip = request.META.get('REMOTE_ADDR')
    
#     # Create a GeoIP object
#     geoip_reader = geoip.GeoIP('./geoip/GeoLiteCity.dat')
    
#     # Retrieve the location information based on the user's IP address
#     location_info = geoip_reader.record_by_addr(user_ip)
    
#     # Access the location information
#     print(location_info.get('city'))
#     print(location_info.get('country_code'))
#     print(location_info.get('latitude'))
#     print(location_info.get('longitude'))



def home(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    
    device_type = ""
    browser_type = ""
    browser_version = ""
    os_type = ""
    os_version = ""
    if request.user_agent.is_mobile:
        device_type = "Mobile"
    if request.user_agent.is_tablet:
        device_type = "Tablet"
    if request.user_agent.is_pc:
        device_type = "PC"
    
    browser_type = request.user_agent.browser.family
    browser_version = request.user_agent.browser.version_string
    os_type = request.user_agent.os.family
    os_version = request.user_agent.os.version_string
    
    g = GeoIP2()
    location = g.city(ip)
    location_country = location["country_name"]
    location_city = location["city"]
    context = {
        "ip": ip,
        "device_type": device_type,
        "browser_type": browser_type,
        "browser_version": browser_version,
        "os_type":os_type,
        "os_version":os_version,
        "location_country": location_country,
        "location_city": location_city
    }
    return render(request, "home.html", context)



# def get_device_location(request):
#     g = GeoIP2()
#     ip_address = request.META.get('REMOTE_ADDR', None)
    
    
#     print(ip_address)
#     user_agent_string = request.META.get('HTTP_USER_AGENT', '')
#     print(user_agent_string)
#     user_agent = parse(user_agent_string)
#     if ip_address:
#         try:
#             location = g.city(ip_address)
#             return {
#                 'ip_address': ip_address,
#                 'city': location.city,
#                 'country_code': location.country_code,
#                 'country_name': location.country_name,
#                 'latitude': location.latitude,
#                 'longitude': location.longitude,
#                 'device': user_agent.device.family,
#                 'browser': user_agent.browser.family,
#                 'os': user_agent.os.family,
#                 'user_agent_string': user_agent_string,
#             }
#         except AddressNotFoundError:
#             pass
#     return None

# def my_view(request):
#     location = get_device_location(request)
#     print(location)
#     if location:
#         loca = location
#         # Do something with the location information
#     else:
#         location = ''

#     return HttpResponse('here is the {}'.format(location))