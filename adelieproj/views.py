from django.http import HttpResponse
from django.shortcuts import render_to_response, redirect
from django.core.exceptions import ObjectDoesNotExist
from django.contrib import auth
from django.contrib.auth.models import User
from adelieproj.models import ProductTier, Arrival, TrafficType, ProductArrivalType, ProductView, BillingAddress, CreditCard, ShippingAddress, Picture, Order, Credit, CartItem, Cart, Product
from django.template import RequestContext
from .forms import PictureForm
from django.utils import timezone
from datetime import datetime, timedelta, date
import math

authorizedUsers = ["skier2k5", "admin"]

def admin(request):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            products = Product.objects.all()
            cart_number = get_cart_number(request)
            return render_to_response("admin.html", RequestContext(request, {"cart_number":cart_number, "products":products}))
    return redirect('/')


def admin_give_credit(request, product_id = None):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            if request.is_ajax():
                product_id = request.POST['product_id']
                product = Product.objects.get(id=product_id)
                if product.credited:
                    return HttpResponse("Already Credited")
                orders = product.orders.all().order_by("created_at")
                tiers = product.tiers.all().order_by("-tier_number")
                total_orders = len(orders)
                all_discounted = 0
                tier_games = []
                tier_discounts = []
                for tier in tiers:
                    tier_discounts.append(tier.discount)
                    products_discounted = math.ceil(tier.percent * total_orders / 100)
                    if all_discounted + products_discounted > total_orders:
                        products_discounted = total_orders - all_discounted
                    tier_games.append(products_discounted)
                    all_discounted += products_discounted
                on_order = 0
                on_tier = 0
                next_tier = tier_games[on_tier]
                for order in orders:
                    credit = Credit(user=order.user, credit=tier_discounts[on_tier], tier=(10-on_tier), product=product, order=order)
                    credit.save()
                    on_order += 1
                    if on_tier != 10 and on_order >= next_tier:
                        on_tier += 1
                        next_tier += tier_games[on_tier]
                product.credited = True
                product.save()
                return HttpResponse(product.id)
            else:
                product = Product.objects.get(id=product_id)
                product.order_count = len(product.orders.all())
                return render_to_response("admingivecredit.html", RequestContext(request, {"product":product}))
    return HttpResponse("go away")


def admin_change_tiers(request):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            product_id = request.POST['product_id']
            product = Product.objects.get(id=product_id)
            tier_discounts = request.POST.getlist('tier_discounts[]')
            tier_percents = request.POST.getlist('tier_percents[]')
            total_percent = 0
            change_tiers = True
            for x in range(0, 11):
                discount = float(tier_discounts[x])
                percent = float(tier_percents[x])
                if discount == "" or percent == "":
                    change_tiers = False
                elif discount > product.price or discount < 0 or percent > 100 or percent < 0:
                    change_tiers == False
                total_percent += percent
            if total_percent != 100:
                change_tiers = False
            if change_tiers:
                for tier in product.tiers.all():
                    tier.delete()
                    product.tiers.remove(tier)
                for x in range(0, 11):
                    discount = tier_discounts[x]
                    percent = tier_percents[x]
                    tier = ProductTier(discount = discount, percent = percent, tier_number = x)
                    tier.save()
                    product.tiers.add(tier)
            return HttpResponse("Success")
    return HttpResponse("Fuck off")


def adminShowCredit(request, gameId):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            return redirect('/admin')


def admin_show_product(request, product_id):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            try:
                product = Product.objects.get(id=product_id)
                if request.method == 'POST':
                    form = PictureForm(request.POST, request.FILES)
                    if form.is_valid():
                        picture = form.save()
                        product.pictures.add(picture)
                        return redirect('/admin/showproduct/' + product_id)
                else:
                    pictureForm = PictureForm()
                    cart_number = get_cart_number(request)
                    return render_to_response("adminshowproduct.html", RequestContext(request, {"product":product,
                                                                                             "pictureForm":pictureForm,
                                                                                             "cart_number":cart_number,}))
            except ObjectDoesNotExist:
                return redirect('/admin')
    return redirect('/')


def admin_delete_pic(request):
    if request.user.is_authenticated():
        if request.user.username in authorizedUsers:
            try:
                picId = request.POST.get('picId', None)
                picture = Picture.objects.get(id=picId)
                picture.delete()
                return HttpResponse("Success")
            except ObjectDoesNotExist:
                return HttpResponse("Failed")
    return HttpResponse("really failed")


def logout(request):
    auth.logout(request)
    return redirect('/')


def check_email(request, email):
    try:
        user = User.objects.get(email=email)
        if user == request.user:
            check = False
        else:
            check = True
    except ObjectDoesNotExist:
        check = False
    return HttpResponse(check)


def check_user(request, username):
    try:
        User.objects.get(username=username)
        check = True
    except ObjectDoesNotExist:
        check = False
    return HttpResponse(check)


def check_password(request):
    if request.user.is_authenticated():
        if request.user.check_password(request.POST['password']):
            check = False
        else:
            check = True
        return HttpResponse(check)
    return HttpResponse("Not Logged In")


def check_product_name(request, name):
    try:
        Product.objects.get(name=name)
        check = True
    except ObjectDoesNotExist:
        check = False
    return HttpResponse(check)


def reg_user(request):
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
            user = User.objects.create_user(username, email, pass1)
            user.save()
            return HttpResponse("Success")
        else:
            return HttpResponse("Failed")
    else:
        return HttpResponse("Failed")


def admin_save_product(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if request.user.username in authorizedUsers:
                name = request.POST['name']
                description = request.POST['desc']
                start = request.POST['start']
                startTime = request.POST['startTime']
                end = request.POST['end']
                endTime = request.POST['endTime']
                price = request.POST['price']
                ship = request.POST['ship']
                tagline = request.POST['tagline']
                saveGame = True
                if name == "" or description == "" or start == "" or startTime == ""  or end == "" or endTime == "" or price == "" or price <= 0 or ship == "" or tagline == "":
                    saveGame = False
                #if len(description) > 500:
                #    saveGame = False
                if len(start) != 10 or len(end) != 10 or len(ship) != 10:
                    saveGame = False
                try:
                    Product.objects.get(name=name)
                    saveGame = False
                except ObjectDoesNotExist:
                    pass
                tier_discounts = request.POST.getlist('tier_discounts[]')
                tier_percents = request.POST.getlist('tier_percents[]')
                total_percent = 0
                for x in range(0, 11):
                    discount = float(tier_discounts[x])
                    percent = float(tier_percents[x])
                    if discount == "" or percent == "":
                        saveGame = False
                    elif discount > price or discount < 0 or percent > 100 or percent < 0:
                        saveGame == False
                    total_percent += percent
                if total_percent != 100:
                    saveGame == False
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
                    product = Product(name = name, description = description, startTime = start, endTime = end, price = price, shipDate = ship, tagLine = tagline)
                    product.save()
                    for x in range(0, 11):
                        discount = tier_discounts[x]
                        percent = tier_percents[x]
                        tier = ProductTier(discount = discount, percent = percent, tier_number = x)
                        tier.save()
                        product.tiers.add(tier)
                    return HttpResponse(product.id)
                else:
                    return HttpResponse("Failed")
            else:
                return HttpResponse("Failed")
        else:
            return HttpResponse("Failed")
    else:
        return HttpResponse("Failed")


def admin_edit_product(request):
    if request.is_ajax():
        if request.user.is_authenticated():
            if request.user.username in authorizedUsers:
                name = request.POST['name']
                description = request.POST['desc']
                start = request.POST['start']
                start_time = request.POST['start_time']
                end = request.POST['end']
                end_time = request.POST['end_time']
                price = request.POST['price']
                product_id = request.POST['product_id']
                ship = request.POST['ship']
                tagline = request.POST['tagline']
                saveGame = True
                if name == "" or description == "" or start == "" or start_time == ""  or end == "" or end_time == "" or price == "" or price <= 0 or ship == "" or tagline == "":
                    saveGame = False
                #if len(description) > 500:
                #    saveGame = False
                if len(start) != 10 or len(end) != 10 or len(ship) != 10:
                    saveGame = False
                if saveGame == True:
                    try:
                        product = Product.objects.get(id=product_id)
                        startYear = start[6:10]
                        startMonth = start[0:2]
                        startDay = start[3:5]
                        endYear = end[6:10]
                        endMonth = end[0:2]
                        endDay = end[3:5]
                        shipYear = ship[6:10]
                        shipMonth = ship[0:2]
                        shipDay = ship[3:5]
                        start = startYear + "-" + startMonth + "-" + startDay + " " + start_time
                        end = endYear + "-" + endMonth + "-" + endDay + " " + end_time
                        ship = shipYear + "-" + shipMonth + "-" + shipDay
                        product.name = name
                        product.description = description
                        product.startTime = start
                        product.endTime = end
                        product.price = price
                        product.tagLine = tagline
                        product.shipDate = ship
                        product.save()
                        return HttpResponse(product.id)
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
        username = request.POST['username'].lower()
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
                            product = Product.objects.get(name=item['product'].name)
                            for i in cart.items.all():
                                if product == i.product:
                                    found = True
                            if not found:
                                tempItem = CartItem(product = product, quantity = item['quantity'], user = user)
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
                            product = Product.objects.get(name=item['product'].name)
                            tempItem = CartItem(product = product, quantity = item['quantity'], user = user)
                            tempItem.save()
                            cart.items.add(tempItem)
                            cart.save()
                        except ObjectDoesNotExist:
                            pass
            return HttpResponse("Success")
        else:
            return HttpResponse("Failed")


def add_to_cart(request):
    if request.user.is_authenticated():
        quantity = request.POST['quantity']
        if quantity > 0:
            try:
                cart = Cart.objects.get(user=request.user, checkedOut=False)
                try:
                    product = Product.objects.get(id=request.POST['product_id'])
                    for item in cart.items.all():
                        if item.product == product:
                            item.quantity = item.quantity + int(quantity)
                            item.save()
                            return HttpResponse("Game existed")
                    item = CartItem(user = request.user, product = product, quantity = quantity)
                    item.save()
                    cart.items.add(item)
                    return HttpResponse("Added Cart")
                except ObjectDoesNotExist:
                    return HttpResponse("No Game")
            except ObjectDoesNotExist:
                cart = Cart(user=request.user)
                cart.save()
                try:
                    product = Product.objects.get(id=request.POST['product_id'])
                    item = CartItem(user = request.user, product = product, quantity = quantity)
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
        try:
            product = Product.objects.get(id=request.POST['product_id'])
            for item in request.session['cart']:
                if item['product'].name== product.name:
                    item['quantity'] = int(item['quantity']) + int(quantity)
                    request.session.modified = True
                    return HttpResponse("Updated")
            id = len(request.session['cart']) + 1
            item = {'id': id, 'product': product, 'quantity': quantity}
            request.session['cart'].append(item)
            request.session.modified = True
            return HttpResponse("Session Modified")
        except ObjectDoesNotExist:
            return HttpResponse("No Game")


def update_cart(request):
    if request.user.is_authenticated():
        quantity = request.POST['quantity']
        itemId = request.POST['itemId']
        try:
            item = CartItem.objects.get(user = request.user, id = itemId)
            if int(quantity) >= 1:
                item.quantity = quantity
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
        try:
            if request.session.get('cart', False) == False:
                return HttpResponse("No Item")
            for item in request.session['cart']:
                if int(item['id']) == int(itemId):
                    if int(quantity) > 0:
                        item['quantity'] = int(quantity)
                    else:
                        request.session['cart'].remove(item)
                request.session.modified = True
            return HttpResponse("Updated")
        except ObjectDoesNotExist:
            return HttpResponse("No Console")


def show_cart(request):
    track_arrival(request, "unknown")
    cart_number = get_cart_number(request)
    if request.user.is_authenticated():
        try:
            cart = Cart.objects.get(user=request.user, checkedOut=False)
            return render_to_response("showcart.html", RequestContext(request, {"cart_number":cart_number, "cart":cart}))
        except ObjectDoesNotExist:
            cart = Cart(user=request.user)
            cart.save()
            return render_to_response("showcart.html", RequestContext(request, {"cart_number":cart_number, "cart":cart}))
    else:
        if request.session.get('cart', False) == False:
            request.session['cart'] = list()
            request.session.modified = True
        return render_to_response("showcart.html", RequestContext(request, {"cart_number":cart_number, "cart":request.session['cart']}))


def checkout_page(request):
    track_arrival(request, "unknown")
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
                            order = Order(user=request.user, creditCard=payment, shippingAddress=shipping, billingAddress=billing)
                            order.save()
                            item.product.orders.add(order)
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
                price += float(item.product.price) * float(item.quantity)
            tax = price * .0625
            total = price + tax
            cart_length = len(cart.items.all())
            return render_to_response("checkout.html", RequestContext(request, {"cart_number":cart_length, 'cart_length': cart_length, 'cart':cart, 'price': price, 'tax': tax, 'total':total, 'items':items}))
    else:
        return HttpResponse("Make a login page")


def show_product(request, name):
    try:
        product = Product.objects.get(name=name)
        if product.is_active() or (request.user.is_authenticated() and request.user.username in authorizedUsers):
            product.daysLeft, product.hoursLeft, product.minutesLeft, product.secondsLeft = get_product_time_left(product.endTime)
            if product.daysLeft < 0:
                product.daysLeft = 0
                product.hoursLeft = 0
                product.minutesLeft = 0
                product.secondsLeft = 0
            current_arrival = track_arrival(request, "unknown")
            track_product_view(request, current_arrival, product, request.GET.get('pat', False))
            cart_number = get_cart_number(request)
            return render_to_response("showgame.html", RequestContext(request, {"cart_number":cart_number, "product":product}))
        else:
            return redirect('/')
    except ObjectDoesNotExist:
        return redirect('/')


def account_page(request):
    if request.user.is_authenticated():
        if request.method == "POST":
            email = request.POST['email']
            curr_pass = request.POST['currPass']
            new_pass = request.POST['newPass']
            conf_pass = request.POST['confPass']
            if email == "" or curr_pass == "" or new_pass == "" or new_pass != conf_pass or len(new_pass) < 8:
                return redirect('/')
            if auth.authenticate(username=request.user.username, password=curr_pass):
                user = User.objects.get(id=request.user.id)
                user.set_password(new_pass)
                user.email = email
                user.save()
                return redirect('/account')
            else:
                return redirect('/')
        else:
            cartLength = 0
            rewardsLeft = 0
            rewardsTotal = 0
            orders = None
            try:
                cart = Cart.objects.get(user=request.user)
                cartLength = len(cart.items.all())
                credits = Credit.objects.filter(user=request.user)
                for credit in credits:
                    rewardsTotal += credit.credit
                    rewardsLeft += credit.credit - credit.used
                orders = Order.objects.filter(user=request.user)
                for order in orders:
                    order.product = order.product_set.all()[0]
                    order.tier = order.credit_set.all()
                    if len(order.tier) > 0:
                        order.tier = order.tier[0].tier
                    else:
                        order.tier = "N/A"
                    order.picture = ""
                    if len(order.product_set.all()[0].pictures.all()) > 0:
                        order.picture = order.product_set.all()[0].pictures.all()[0]
            except ObjectDoesNotExist:
                pass
            track_arrival(request, "unknown")
            cart_number = get_cart_number(request)
            return render_to_response("account.html", RequestContext(request, {"cartLength":cartLength,
                                                                            "rewardsLeft":rewardsLeft,
                                                                            "rewardsTotal":rewardsTotal,
                                                                            "orders":orders,
                                                                            "cart_number":cart_number}))
    else:
        return HttpResponse("Please Login first")


def upcoming_products(request):
    track_arrival(request, "unknown")
    cart_number = get_cart_number(request)
    products = get_products(mode="upcoming", order="startTime")
    for product in products:
        pictures = product.pictures.all()
        if len(pictures) > 0:
            product.picture = pictures[0]
    return render_to_response("upcoming.html", RequestContext(request, {"cart_number":cart_number, "products":products}))


def all_products(request):
    track_arrival(request, "unknown")
    cart_number = get_cart_number(request)
    products = get_products("active")
    for product in products:
        pictures = product.pictures.all()
        if len(pictures) > 0:
            product.picture = pictures[0]
        product.order_count = len(product.orders.all())
    return render_to_response("allgames.html", RequestContext(request, {"cart_number":cart_number, "products":products}))


def index(request):
    track_arrival(request, "unknown")
    cart_number = get_cart_number(request)
    products = get_products("active")
    upcoming = get_products("upcoming-next", "startTime")
    return render_to_response("index.html", RequestContext(request, {"cart_number":cart_number, "products":products, "upcoming":upcoming}))


def get_products(mode = "all", order = "endTime", name = None):
    """
        active = Product is currently on sale and > 0 pictures, startTime < Now < endTime
        past = Product has past sale and > 0 pictures
        upcoming-shown = Product is going on sale within 24 hours
        upcoming-hidden = Product is going on sale but not within 24 hours
    """
    products = list()
    upcoming = None
    single_product = None
    all_products = Product.objects.all().order_by(order)
    for product in all_products:
        if mode == "all":
            product.daysLeft, product.hoursLeft, product.minutesLeft, product.secondsLeft = get_product_time_left(product.endTime)
            products.append(product)
        elif mode == "active":
            if product.is_active() and product.is_ready():
                product.daysLeft, product.hoursLeft, product.minutesLeft, product.secondsLeft = get_product_time_left(product.endTime)
                products.append(product)
        elif mode == "past":
            if product.is_past() and product.is_ready():
                product.daysLeft, product.hoursLeft, product.minutesLeft, product.secondsLeft = get_product_time_left(product.endTime)
                products.append(product)
        elif mode == "upcoming":
            if product.is_upcoming() and product.is_ready():
                product.daysLeft, product.hoursLeft, product.minutesLeft, product.secondsLeft = get_product_time_left(product.startTime)
                products.append(product)
        elif mode == "upcoming-shown":
            if product.is_upcoming_show():
                product.daysLeft, product.hoursLeft, product.minutesLeft, product.secondsLeft = get_product_time_left(product.startTime)
                products.append(product)
        elif mode == "upcoming-hidden":
            if product.is_upcoming_hide():
                product.daysLeft, product.hoursLeft, product.minutesLeft, product.secondsLeft = get_product_time_left(product.startTime)
                products.append(product)
        elif mode == "upcoming-next":
            if product.is_upcoming():
                product.daysLeft, product.hoursLeft, product.minutesLeft, product.secondsLeft = get_product_time_left(product.startTime)
                upcoming = product
        elif mode == "single":
            try:
                single_product = Product.objects.get(name=name)
                single_product.daysLeft, single_product.hoursLeft, single_product.minutesLeft, single_product.secondsLeft = get_product_time_left(product.endTime)
            except ObjectDoesNotExist:
                single_product = None
    if mode == "upcoming-next":
        return upcoming
    return products


def get_product_time_left(product_time):
    now = datetime.now()
    delta = product_time.astimezone(timezone.utc).replace(tzinfo=None) - now
    daysLeft = delta.days
    hoursLeft = delta.seconds / 3600
    minutesLeft = (delta.seconds - (hoursLeft * 3600)) / 60
    secondsLeft = (delta.seconds - (hoursLeft * 3600)) - (minutesLeft * 60)
    return [daysLeft, hoursLeft, minutesLeft, secondsLeft]


def track_arrival(request, traffic_type):
    ip = get_client_ip(request)
    user_agent = request.META.get('HTTP_USER_AGENT')
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    yesterday = date.today() - timedelta(days=1)
    last_arrival = Arrival.objects.filter(user=user,
                                          user_agent=user_agent,
                                          ip=ip,
                                          created_at__gte=yesterday).order_by("created_at")
    if len(last_arrival) == 0:
        traffic_type = TrafficType.objects.get(name=traffic_type)
        last_arrival = Arrival(ip = ip, user_agent = user_agent, traffic_type = traffic_type, user = user)
        last_arrival.save()
    else:
        last_arrival = last_arrival[0]
    return last_arrival


def track_product_view(request, current_arrival, product, product_arrival_type):
    if request.user.is_authenticated():
        user = request.user
    else:
        user = None
    if product_arrival_type == "i":
        pat = ProductArrivalType.objects.get(name="index_page")
    elif product_arrival_type == "ap":
        pat = ProductArrivalType.objects.get(name="products_page")
    else:
        pat = None
    product_view = ProductView(user=user, product_arrival_type=pat, product=product, arrival=current_arrival)
    product_view.save()


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[-1].strip()
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def get_cart_number(request):
    if request.user.is_authenticated():
        try:
            cart = Cart.objects.get(user=request.user, checkedOut=False)
            return len(cart.items.all())
        except ObjectDoesNotExist:
            cart = Cart(user=request.user)
            cart.save()
            return 0
    else:
        if request.session.get('cart', False) == False:
            request.session['cart'] = list()
            request.session.modified = True
            return 0
        else:
            return len(request.session.get('cart'))
