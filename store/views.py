from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Products, Category, Cart, Order, OrderItem, Review, Wishlist, Profile
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from urllib.parse import quote
from .forms import ProfileForm

def home(request):
    print(request.user)
    print(request.user.is_authenticated)

    products = Products.objects.all()
    categories = Category.objects.all()

    return render(request, 'store/home.html', {
        'products': products,
        'categories': categories
    })



def shop(request):
    q = request.GET.get('q')
    if q:
        products = Products.objects.filter(name__icontains=q)
    else:
        products = Products.objects.all()

    categories = Category.objects.all()

    context = {
        'products': products,
        'categories': categories,
    }

    return render(request, 'store/shop.html', context)


from django.contrib.auth.decorators import login_required

def product(request, pk):
    product = Products.objects.get(id=pk)
    reviews = Review.objects.filter(product=product).order_by('-created_at')

    if request.method == "POST" and request.user.is_authenticated:
        rating = request.POST.get("rating")
        comment = request.POST.get("comment")

        Review.objects.create(
            product=product,
            user=request.user,
            rating=rating,
            comment=comment,
        )

        return redirect("product", pk=product.id)

    context = {
        "product": product,
        "reviews": reviews,
    }

    return render(request, "store/product.html", context)

def category(request, pk):
    category_item = Category.objects.get(id=pk)
    products = Products.objects.filter(category=category_item)

    return render(request, 'store/category.html', {
        'category': category_item,
        'products': products
    })

@login_required
def add_to_cart(request, pk):
    product = Products.objects.get(id=pk)

    Cart.objects.create(
        user=request.user,
        product=product
    )
    messages.success(request, f"🛒 {product.name} has been added to your cart successfully!")

    return redirect('home')

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,"🎉 Account created successfully! Please log in.") 
            return redirect("login")
    else:
        form = UserCreationForm()

    return render(request, "store/register.html", {"form": form})
def about (request):
    return render (request,'store/about.html')

def contact(request):
    return render(request,'store/contact.html')

@login_required
def cart(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    context = {
        'cart_items': cart_items,
        'total': total,
    }

    return render(request, 'store/cart.html', context)

    return render(request, 'store/cart.html', context)

@login_required
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    total = 0

    for item in cart_items:
        total += item.product.price * item.quantity

    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        location = request.POST.get("location")

        order = Order.objects.create(
            user=request.user,
            name=name,
            phone=phone,
            location=location,
            total=total,
        )
        for item in cart_items:
         OrderItem.objects.create(
        order=order,
        product=item.product,
        quantity=item.quantity,
        price=item.product.price,
    )
        
            

        cart_items.delete()

        return redirect("order_success", order.id)

    context = {
        "cart_items": cart_items,
        "total": total,
    }

    return render(request, "store/checkout.html", context)

@login_required
def remove_from_cart(request, pk):
    item = Cart.objects.get(id=pk, user=request.user)
    item.delete()

    messages.success(request, "🗑️ Item removed from your cart.")

    return redirect('cart')

@login_required
def increase_quantity(request, pk):
    item = Cart.objects.get(id=pk, user=request.user)
    item.quantity += 1
    item.save()

    return redirect('cart')


@login_required
def decrease_quantity(request, pk):
    item = Cart.objects.get(id=pk, user=request.user)

    if item.quantity > 1:
        item.quantity -= 1
        item.save()
    else:
        item.delete()

    return redirect('cart')


@login_required
def orders(request):
    orders = Order.objects.filter(user=request.user)\
        .prefetch_related('orderitem_set')\
        .order_by('-created_at')

    return render(request, 'store/orders.html', {
        'orders': orders
    })

@login_required
def order_success(request, order_id):
    order = Order.objects.get(id=order_id, user=request.user)

    message = f"""
🌸 Hello Beauty Haven!

I have placed an order.

🆔 Order ID: BH{order.id}

👤 Name: {order.name}
📞 Phone: {order.phone}
📍 Delivery Address: {order.location}

💰 Total: Ksh {order.total}

Thank you!
"""

    whatsapp_url = (
        "https://wa.me/254745036877?text=" + quote(message)
    )

    context = {
        "order": order,
        "whatsapp_url": whatsapp_url,
    }

    return render(request, "store/order_success.html", context)

@login_required
def add_to_wishlist(request, pk):
    product = Products.objects.get(id=pk)

    Wishlist.objects.get_or_create(
        user=request.user,
        product=product
    )

    return redirect("product", pk=pk)
@login_required
def wishlist(request):
    wishlist_items = Wishlist.objects.filter(user=request.user)

    context = {
        "wishlist_items": wishlist_items,
    }

    return render(request, "store/wishlist.html", context)

from django.contrib.auth.decorators import login_required

@login_required
def profile(request):
    profile = request.user.profile

    return render(request, "store/profile.html", {
        "profile": profile
    })

   

@login_required
def edit_profile(request):
    profile = request.user.profile

    if request.method == "POST":
        form = ProfileForm(
            request.POST,
            request.FILES,
            instance=profile
        )

        if form.is_valid():
            form.save()
            return redirect("profile")

    else:
        form = ProfileForm(instance=profile)

    return render(request, "store/edit_profile.html", {
        "form": form
    })
