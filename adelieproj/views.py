from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.models import User
from adelieproj.models import *
from django.core.context_processors import csrf
from django.template import RequestContext
from .forms import GamePictureForm
from datetime import datetime
from django.utils import timezone
import time, os, json, base64, hmac, sha, math, hashlib

authorizedUsers = ["skier2k5", "admin"]

def sign_s3(request):
    AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY_ID')       
    AWS_SECRET_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY')
    S3_BUCKET = os.environ.get('S3_BUCKET')
    object_name = request.POST['gameTitle'].replace(" ", "").replace(":", "") + ".mp4"
    mime_type = request.POST['type']
    expires = int(time.time()+10)
    amz_headers = "x-amz-acl:public-read"
    put_request = "PUT\n\n%s\n%d\n%s\n/%s/%s" % (mime_type, expires, amz_headers, S3_BUCKET, object_name)
    signature = base64.encodestring(hmac.new(AWS_SECRET_KEY, put_request, sha).digest())
    url = 'https://%s.s3.amazonaws.com/%s' % (S3_BUCKET, object_name)
    return HttpResponse(json.dumps({
        'signed_request': '%s?AWSAccessKeyId=%s&Expires=%d&Signature=%s' % (url, AWS_ACCESS_KEY, expires, signature),
         'url': url
      }))

def admin(request):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            games = Game.objects.all()
            consoles = Console.objects.all()
            return render_to_response("admin.html", RequestContext(request, {'games':games, 'consoles':consoles}))
    return redirect('/')
    
def adminAddConsole(request):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            if request.method == "POST":
                consoleName = request.POST['console']
                if consoleName == "":
                    return HttpResponse("No name")
                try:
                    console = Console.objects.get(name=consoleName)
                    return HttpResponse("Already Exists")
                except ObjectDoesNotExist:
                    console = Console(name = consoleName)
                    console.save()
                    return HttpResponse("saved")
    return HttpResponse("Not Authorized")
    
def adminEditConsole(request):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            if request.method == "POST":
                consoleId = request.POST['consoleId']
                consoleName = request.POST['consoleName']
                if consoleName == "":
                    return HttpResponse("No Name")
                try:
                    console = Console.objects.get(id=consoleId)
                    console.name = consoleName
                    console.save()
                except ObjectDoesNotExist:
                    return HttpResponse("No Console")
    
def adminGiveCredit(request):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            if request.method == "POST":
                try:
                    gameId = request.POST['gameId']
                    game = Game.objects.get(id=gameId)
                    tiers = list()
                    totalGames = len(game.orders.all())
                    n = 2
                    for x in range(1, 11):
                        tiers.append(math.ceil(totalGames / n))
                        n *= 2
                    print tiers
                    return HttpResponse("gave credit")
                except ObjectDoesNotExist:
                    return HttpResponse("no game")
    return HttpResponse("go away")
    
def adminShowGame(request, gameId):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            try:
                game = Game.objects.get(id=gameId)
                if request.method == 'POST':
                    form = GamePictureForm(request.POST, request.FILES)
                    if form.is_valid():
                        picture = form.save()
                        game.pictures.add(picture)
                        return redirect('/admin/showgame/' + gameId)
                else:
                    pictureForm = GamePictureForm()
                    consoles = list(Console.objects.all())
                    selectedConsoles = list(game.consoles.all())
                    tempConsoles = consoles
                    consoles = list()
                    for c in tempConsoles:
                        check = False
                        for sc in selectedConsoles:
                            if sc.name == c.name:
                                check = True
                        if not check:
                            consoles.append(c)
                    return render_to_response("adminshowgame.html", RequestContext(request, {"game":game, 
                                                                                                "pictureForm":pictureForm,
                                                                                                "consoles":consoles, 
                                                                                                "selectedconsoles":selectedConsoles}))
            except ObjectDoesNotExist:
                return redirect('/admin')
    return redirect('/')
    
def adminShowCredit(request, gameId):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            try:
                game = Game.objects.get(id=gameId)
                return render_to_response("adminshowcredit.html", RequestContext(request, {"game":game}))
            except ObjectDoesNotExist:
                return redirect('/admin')
    
def adminAddTrailer(request):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            gameId = request.POST.get('gameId', None)
            try:
                game = Game.objects.get(id=gameId)
                if request.method == 'POST':
                    url = request.POST.get('url', None)
                    game.trailerUrl = url
                    game.save()
                    return HttpResponse('Added')
            except ObjectDoesNotExist:
                return redirect('Not Added')
            return redirect('Not Added')
    return HttpResponse("Get Out")
    
def adminDeletePic(request):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            try:
                picId = request.POST.get('picId', None)
                picture = GamePicture.objects.get(id=picId)
                picture.delete()
                return HttpResponse("Success")
            except ObjectDoesNotExist:
                return HttpResponse("Failed")
    return HttpResponse("really failed")

#def adminDeleteVideo(request):
#    if request.user.is_authenticated():
#        if request.user.username in authorizedUsers:
#            try:
#                videoId = request.POST.get('videoId', None)
#                trailer = GameTrailer.objects.get(id=videoId)
#                trailer.delete()
#                return HttpResponse("Success")
#            except ObjectDoesNotExist:
#                return HttpResponse("Failed")
#    return HttpResponse("really failed")
    
def logout(request):
    auth.logout(request)
    return redirect('/')

def checkEmail(request, email):
    try:
        user = User.objects.get(email=email)
        if user == request.user:
            check = False
        else:
            check = True
    except ObjectDoesNotExist:
        check = False
    return HttpResponse(check)
    
def checkUser(request, username):
    try:
        user = User.objects.get(username=username)
        check = True
    except ObjectDoesNotExist:
        check = False
    return HttpResponse(check)
    
def checkPassword(request):
    if request.user.is_authenticated():
        if request.user.check_password(request.POST['password']):
            check = False
        else:
            check = True
        return HttpResponse(check)
    return HttpResponse("Not Logged In")
    
def checkGameTitle(request, title):
    try:
        game = Game.objects.get(title=title)
        check = True
    except ObjectDoesNotExist:
        check = False
    return HttpResponse(check)
    
def regUser(request):
    if request.is_ajax():
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']
        regUser = True
        if username == "" or email == "" or pass1 == "":
            regUser = False
        if pass1 != pass2:
            regUser = False
        try:
            user = User.objects.get(username=username)
            user = User.objects.get(email=email)
            regUser = False
        except ObjectDoesNotExist:
            pass
        if regUser == True:
            #send_mail('Thank you for registering at TuftSched.com', 'Thank you for registering.', 
            #       'TuftSched@TuftSched.com', [email], fail_silently=False)
            user = User.objects.create_user(username, email, pass1)
            user.save()
            return HttpResponse("Success")
        else:
            return HttpResponse("Failed")
    else:
        return HttpResponse("Failed")
        
def adminSaveGame(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if request.user.username in authorizedUsers:
                title = request.POST['title']
                publisher = request.POST['publisher']
                description = request.POST['desc']
                start = request.POST['start']
                startTime = request.POST['startTime']
                end = request.POST['end']
                endTime = request.POST['endTime']
                price = request.POST['price']
                ship = request.POST['ship']
                consoles = request.POST.getlist('consoles[]')
                tagline = request.POST['tagline']
                saveGame = True
                if title == "" or publisher == "" or description == "" or start == "" or startTime == ""  or end == "" or endTime == "" or price == "" or price <= 0 or ship == "" or consoles == "" or tagline == "":
                    saveGame = False
                #if len(description) > 500:
                #    saveGame = False
                if len(start) != 10 or len(end) != 10 or len(ship) != 10:
                    saveGame = False
                try:
                    game = Game.objects.get(title=title)
                    saveGame = False
                except ObjectDoesNotExist:
                    pass
                try:
                    for consoleId in consoles:
                        console = Console.objects.get(id=consoleId)
                except ObjectDoesNotExist:
                    saveGame = False
                if saveGame == True:
                    startYear = start[6:10]
                    startMonth = start[0:2]
                    startDay = start[3:5]
                    endYear = end[6:10]
                    endMonth = end[0:2]
                    endDay = end[3:5]
                    shipYear = ship[6:10]
                    shipMonth = ship[0:2]
                    shipDay = ship[3:5]
                    start = startYear + "-" + startMonth + "-" + startDay + " " + startTime
                    end = endYear + "-" + endMonth + "-" + endDay + " " + endTime
                    ship = shipYear + "-" + shipMonth + "-" + shipDay
                    game = Game(title = title, publisher = publisher, description = description, startTime = start, endTime = end, price = price, shipDate = ship, tagLine = tagline)
                    game.save()
                    for consoleId in consoles:
                        console = Console.objects.get(id=consoleId)
                        game.consoles.add(console)
                        game.save()
                    return HttpResponse(game.id)
                else:
                    return HttpResponse("Failed")
            else:
                return HttpResponse("Failed")
        else:
            return HttpResponse("Failed")
    else:
        return HttpResponse("Failed")
        
def adminEditGame(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if request.user.username in authorizedUsers:
                title = request.POST['title']
                publisher = request.POST['publisher']
                description = request.POST['desc']
                start = request.POST['start']
                end = request.POST['end']
                price = request.POST['price']
                gameId = request.POST['gameid']
                ship = request.POST['ship']
                consoles = request.POST.getlist('consoles[]')
                tagline = request.POST['tagline']
                saveGame = True
                if title == "" or publisher == "" or description == "" or start == ""  or end == "" or price == "" or price <= 0 or ship == "" or consoles == "" or tagline == "":
                    saveGame = False
                #if len(description) > 500:
                #    saveGame = False
                if len(start) != 10 or len(end) != 10 or len(ship) != 10:
                    saveGame = False
                try:
                    for consoleId in consoles:
                        console = Console.objects.get(id=consoleId)
                except ObjectDoesNotExist:
                    saveGame = False
                if saveGame == True:
                    try:
                        game = Game.objects.get(id=gameId)
                        startYear = start[6:10]
                        startMonth = start[0:2]
                        startDay = start[3:5]
                        endYear = end[6:10]
                        endMonth = end[0:2]
                        endDay = end[3:5]
                        shipYear = ship[6:10]
                        shipMonth = ship[0:2]
                        shipDay = ship[3:5]
                        start = startYear + "-" + startMonth + "-" + startDay + " 10:00:00"
                        end = endYear + "-" + endMonth + "-" + endDay + " 10:00:00"
                        ship = shipYear + "-" + shipMonth + "-" + shipDay
                        game.title = title
                        game.publisher = publisher
                        game.description = description
                        game.startTime = start
                        game.endTime = end
                        game.price = price
                        game.tagLine = tagline
                        game.shipDate = ship
                        game.save()
                        game.consoles.clear()
                        game.save()
                        for consoleId in consoles:
                            console = Console.objects.get(id=consoleId)
                            game.consoles.add(console)
                            game.save()
                        return HttpResponse(game.id)
                    except ObjectDoesNotExist:
                        pass
                else:
                    return HttpResponse("Failed")
            else:
                return HttpResponse("Failed")
        else:
            return HttpResponse("Failed")
    else:
        return HttpResponse("Failed")

def login(request):
    if request.is_ajax():
        username = request.POST['username']
        password = request.POST['pass']
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            if request.session.get('cart', False) != False:
                try:
                    cart = Cart.objects.get(user = user, checkedOut = False)
                    found = False
                    for item in request.session['cart']:
                        try:
                            game = Game.objects.get(title=item['game'].title)
                            console = Console.objects.get(id=item['console'].id)
                            for i in cart.items.all():
                                if game == i.game:
                                    found = True
                            if not found:
                                tempItem = CartItem(game = game, quantity = item['quantity'], user = user, console = console)
                                tempItem.save()
                                cart.items.add(tempItem)
                                cart.save()
                        except ObjectDoesNotExist:
                            pass
                except ObjectDoesNotExist:
                    cart = Cart(user = user)
                    cart.save()
                    for item in request.session['cart']:
                        try:
                            game = Game.objects.get(title=item['game'].title)
                            console = Console.objects.get(id=item['console'].id)
                            tempItem = CartItem(game = game, quantity = item['quantity'], user = user, console = console)
                            tempItem.save()
                            cart.items.add(tempItem)
                            cart.save()
                        except ObjectDoesNotExist:
                            pass
            return HttpResponse("Success")
        else:
            return HttpResponse("Failed")
            
def addToCart(request):
    if request.user.is_authenticated():
        quantity = request.POST['quantity']
        consoleId = request.POST['consoleId']
        if quantity > 0:
            try:
                cart = Cart.objects.get(user=request.user, checkedOut=False)
                try:
                    game = Game.objects.get(id=request.POST['gameId'])
                    console = Console.objects.get(id=consoleId)
                    for item in cart.items.all():
                        if item.game == game:
                            item.quantity = item.quantity + int(quantity)
                            item.save()
                            return HttpResponse("Game existed")
                    item = CartItem(user = request.user, game = game, quantity = quantity, console = console)
                    item.save()
                    cart.items.add(item)
                    return HttpResponse("Added Cart")
                except ObjectDoesNotExist:
                    return HttpResponse("No Game")
            except ObjectDoesNotExist:
                cart = Cart(user=request.user)
                cart.save()
                try:
                    game = Game.objects.get(id=request.POST['gameId'])
                    console = Console.objects.get(id=consoleId)
                    item = CartItem(user = request.user, game = game, quantity = quantity, console = console)
                    item.save()
                    cart.items.add(item)
                    return HttpResponse("Create and Add Cart")
                except ObjectDoesNotExist:
                    return HttpResponse("No Game")
        else:
            return HttpResponse("Bad quantity")
    else:
        if request.session.get('cart', False) == False:
            request.session['cart'] = list()
        quantity = request.POST['quantity']
        consoleId = request.POST['consoleId']
        try:
            game = Game.objects.get(id=request.POST['gameId'])
            console = Console.objects.get(id=consoleId)
            for item in request.session['cart']:
                if item['game'].title == game.title:
                    item['quantity'] = int(item['quantity']) + int(quantity)
                    request.session.modified = True
                    return HttpResponse("Updated")
            id = len(request.session['cart']) + 1
            item = {'id': id, 'game': game, 'quantity': quantity, 'console': console}
            request.session['cart'].append(item)
            request.session.modified = True
            return HttpResponse("Session Modified")
        except ObjectDoesNotExist:
            return HttpResponse("No Game")
        
def updateCart(request):
    if request.user.is_authenticated():
        quantity = request.POST['quantity']
        itemId = request.POST['itemId']
        consoleId = request.POST['consoleId']
        try:
            item = CartItem.objects.get(user = request.user, id = itemId)
            console = Console.objects.get(id=consoleId)
            if int(quantity) >= 1:
                item.quantity = quantity
                item.console = console
                item.save()
                return HttpResponse("Updated")
            else:
                item.delete()
                return HttpResponse("Deleted")
        except ObjectDoesNotExist:
            return HttpResponse("No Item")
    else:
        quantity = request.POST['quantity']
        itemId = request.POST['itemId']
        consoleId = request.POST['consoleId']
        try:
            console = Console.objects.get(id=consoleId)
            if request.session.get('cart', False) == False:
                return HttpResponse("No Item")
            for item in request.session['cart']:
                if int(item['id']) == int(itemId):
                    if int(quantity) > 0:
                        item['quantity'] = int(quantity)
                        item['console'] = console
                    else:
                        request.session['cart'].remove(item)
                request.session.modified = True
            return HttpResponse("Updated")
        except ObjectDoesNotExist:
            return HttpResponse("No Console")
        
def showCart(request):
    if request.user.is_authenticated():
        try:
            cart = Cart.objects.get(user=request.user, checkedOut=False)
            return render_to_response("showcart.html", RequestContext(request, {"cart":cart}))
        except ObjectDoesNotExist:
            cart = Cart(user=request.user)
            cart.save()
            return render_to_response("showcart.html", RequestContext(request, {"cart":cart}))
    else:
        if request.session.get('cart', False) == False:
            request.session['cart'] = list()
            request.session.modified = True
        return render_to_response("showcart.html", RequestContext(request, {"cart":request.session['cart']}))

def checkoutPage(request):
    if request.user.is_authenticated():
        if request.method == 'POST':
            try:
                cart = Cart.objects.get(user=request.user, checkedOut=False)
                shippingName = request.POST['shippingName']
                shippingAddressOne = request.POST['shippingAddressOne']
                shippingAddressTwo = request.POST['shippingAddressTwo']
                shippingCity = request.POST['shippingCity']
                shippingState = request.POST['shippingState']
                shippingZip = request.POST['shippingZip']
                sameAsShipping = request.POST.get('sameAsShipping', False)
                billingName = request.POST['billingName']
                billingAddressOne = request.POST['billingAddressOne']
                billingAddressTwo = request.POST['billingAddressTwo']
                billingCity = request.POST['billingCity']
                billingState = request.POST['billingState']
                billingZip = request.POST['billingZip']
                paymentName = request.POST['paymentName']
                paymentCard = request.POST['paymentCard']
                paymentMonth = request.POST['paymentMonth']
                paymentYear = request.POST['paymentYear']
                paymentCode = request.POST['paymentCode']
                shipping = True
                billing = True
                payment = True
                if shippingName == "" or shippingAddressOne == "" or shippingCity == "" or shippingState == "" or shippingZip == "":
                    shipping = False
                if not sameAsShipping:
                    if billingName == "" or billingAddressOne == "" or billingCity == "" or billingState == "" or billingZip == "":
                        billing = False
                if paymentName == "" or paymentCard == "" or paymentMonth == "" or paymentYear == "" or paymentCode == "":
                    payment = False
                if shipping and billing and payment:
                    if sameAsShipping:
                        billing = BillingAddress(country="United States", addressOne=shippingAddressOne, addressTwo=shippingAddressTwo, city=shippingCity, state=shippingState, zipcode=shippingZip, user=request.user)
                    else:
                        billing = BillingAddress(country="United States", addressOne=billingAddressOne, addressTwo=billingAddressTwo, city=billingCity, state=billingState, zipcode=billingZip, user=request.user)
                    billing.save()
                    shipping = ShippingAddress(title="No Title", user=request.user, name=shippingName, addressOne=shippingAddressOne, addressTwo=shippingAddressTwo, city=shippingCity, state=shippingState, country="United States")
                    shipping.save()
                    payment = CreditCard(name=paymentName, cardNum=paymentCard, expirationMonth=paymentMonth, expirationYear=paymentYear, cvc=paymentCode, billingAddress=billing, user=request.user)
                    payment.save()
                    for item in cart.items.all():
                        for x in range(0, int(item.quantity)):
                            gameOrder = GameOrder(user=request.user, creditCard=payment, shippingAddress=shipping, billingAddress=billing, console=item.console)
                            gameOrder.save()
                            item.game.orders.add(gameOrder)
                    return redirect('/')
                else:
                    return redirect('/')
            except ObjectDoesNotExist:
                return HttpResponse("No Cart")
        else:
            try:
                cart = Cart.objects.get(user=request.user, checkedOut = False)
            except ObjectDoesNotExist:
                cart = Cart(user=request.user)
            price = 0.0;
            tax = 0.0;
            total = 0.0;
            items = 0
            for item in cart.items.all():
                items += int(item.quantity)
                price += float(item.game.price) * float(item.quantity)
            tax = price * .0625
            total = price + tax
            return render_to_response("checkout.html", RequestContext(request, {'cart':cart, 'price': price, 'tax': tax, 'total':total, 'items':items}))
    else:
        return HttpResponse("Make a login page")

def showGame(request, title):
    try:
        game = Game.objects.get(title=title)
        countdown = game.endTime.astimezone(timezone.utc).replace(tzinfo=None) - datetime.now()
        if countdown.days >= 0:
            game.daysLeft = countdown.days
            game.hoursLeft = countdown.seconds / 3600
            game.minutesLeft = (countdown.seconds - (game.hoursLeft * 3600)) / 60
            game.secondsLeft = (countdown.seconds - (game.hoursLeft * 3600)) - (game.minutesLeft * 60)
        else:
            game.daysLeft = 0
            game.hoursLeft = 0
            game.minutesLeft = 0
            game.secondsLeft = 0
        consoles = Console.objects.all().order_by("name")
        return render_to_response("showgame.html", RequestContext(request, {"game":game, "consoles":consoles}))
    except ObjectDoesNotExist:
        return redirect('/')
        
def myAccount(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            email = request.POST['email']
            currPass = request.POST['currPass']
            newPass = request.POST['newPass']
            confPass = request.POST['confPass']
            if email == "" or currPass == "" or newPass == "" or newPass != confPass or len(newPass) < 8:
                return redirect('/')
            user = User.objects.get(id=request.user.id)
            user.set_password(newPass)
            user.email = email
            user.save()
            return redirect('/account')
        else:
            cartLength = 0
            rewardsLeft = 0
            rewardsTotal = 0
            orders = None
            try:
                cart = Cart.objects.get(user=request.user)
                cartLength = len(cart.items.all())
                credits = GameCredit.objects.filter(user=request.user)
                for credit in credits:
                    rewardsTotal += credit.credit
                    rewardsLeft += credit.credit - credit.used
                orders = GameOrder.objects.filter(user=request.user)
                for order in orders:
                    order.game = order.game_set.all()[0]
                    order.tier = order.gamecredit_set.all()
                    if len(order.tier) > 0:
                        order.tier = order.tier[0].tier
                    else:
                        order.tier = "N/A"
                    order.picture = ""
                    if len(order.game.pictures.all()) > 0:
                        order.picture = order.game.pictures.all()[0]
            except ObjectDoesNotExist:
                pass
            return render_to_response("account.html", RequestContext(request, {"cartLength":cartLength, 
                                                                            "rewardsLeft":rewardsLeft, 
                                                                            "rewardsTotal":rewardsTotal,
                                                                            "orders":orders}))
    else:
        return HttpResponse("Please Login first")
        
def upcomingGames(request):
    consoles = Console.objects.all().order_by("name")
    games = list()
    g = Game.objects.all().order_by("startTime")
    for game in g:
        if game.is_upcoming():
            if len(game.pictures.all()) > 0:
                game.picture = game.pictures.all()[0]
            game.orderCount = len(game.orders.all())
            countdown = game.startTime.astimezone(timezone.utc).replace(tzinfo=None) - datetime.now()
            game.daysLeft = countdown.days
            game.hoursLeft = countdown.seconds / 3600
            game.minutesLeft = (countdown.seconds - (game.hoursLeft * 3600)) / 60
            game.secondsLeft = (countdown.seconds - (game.hoursLeft * 3600)) - (game.minutesLeft * 60)
            games.append(game)
    return render_to_response("upcoming.html", RequestContext(request, {"consoles":consoles, "games":games}))
        
def allGames(request):
    consoles = Console.objects.all().order_by("name")
    games = list()
    g = Game.objects.all().order_by("endTime")
    for game in g:
        if game.is_active():
            if len(game.pictures.all()) > 0:
                game.picture = game.pictures.all()[0]
            game.orderCount = len(game.orders.all())
            countdown = game.endTime.astimezone(timezone.utc).replace(tzinfo=None) - datetime.now()
            game.daysLeft = countdown.days
            game.hoursLeft = countdown.seconds / 3600
            game.minutesLeft = (countdown.seconds - (game.hoursLeft * 3600)) / 60
            game.secondsLeft = (countdown.seconds - (game.hoursLeft * 3600)) - (game.minutesLeft * 60)
            games.append(game)
    return render_to_response("allgames.html", RequestContext(request, {"consoles":consoles, "games":games}))
    
def consoleGames(request, console):
    try:
        console = Console.objects.get(name=console)
    except ObjectDoesNotExist:
        return redirect('/games')
    consoles = Console.objects.all().order_by("name")
    games = list()
    g = Game.objects.all().order_by("endTime")
    for game in g:
        isConsole = False
        if game.is_active():
            for c in game.consoles.all():
                if c == console:
                    isConsole = True
            if len(game.pictures.all()) > 0:
                game.picture = game.pictures.all()[0]
            game.orderCount = len(game.orders.all())
            countdown = game.endTime.astimezone(timezone.utc).replace(tzinfo=None) - datetime.now()
            game.daysLeft = countdown.days
            game.hoursLeft = countdown.seconds / 3600
            game.minutesLeft = (countdown.seconds - (game.hoursLeft * 3600)) / 60
            game.secondsLeft = (countdown.seconds - (game.hoursLeft * 3600)) - (game.minutesLeft * 60)
            if isConsole:
                games.append(game)
    return render_to_response("allgames.html", RequestContext(request, {"consoles":consoles, "games":games}))

def index(request):
    allGames = Game.objects.all().order_by("endTime")
    startGames = Game.objects.all().order_by("startTime")
    games = list()
    upcoming = list()
    now = datetime.now()
    for game in allGames:
        if game.is_active():
            if len(games) < 5:
                countdown = game.endTime.astimezone(timezone.utc).replace(tzinfo=None) - now
                game.daysLeft = countdown.days
                game.hoursLeft = countdown.seconds / 3600
                game.minutesLeft = (countdown.seconds - (game.hoursLeft * 3600)) / 60
                game.secondsLeft = (countdown.seconds - (game.hoursLeft * 3600)) - (game.minutesLeft * 60)
                games.append(game);
    for game in startGames:
        if not game.is_active():
            delta = game.startTime.astimezone(timezone.utc).replace(tzinfo=None) - now
            if delta.days >= 0 and len(upcoming) == 0:
                game.daysLeft = delta.days
                game.hoursLeft = delta.seconds / 3600
                game.minutesLeft = (delta.seconds - (game.hoursLeft * 3600)) / 60
                game.secondsLeft = (delta.seconds - (game.hoursLeft * 3600)) - (game.minutesLeft * 60)
                upcoming.append(game)
    return render_to_response("index.html", RequestContext(request, {"games":games, "upcoming":upcoming}))