import json
import requests
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.conf import settings
from .models import Book, Category, Subscriber, Cart, CartItem, Order, OrderItem


# ─── Helper: get or create cart ──────────────────────────────────────────────
def get_cart(request):
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    cart, _ = Cart.objects.get_or_create(session_key=session_key)
    return cart


# ─── Home Page ────────────────────────────────────────────────────────────────
def home(request):
    best_sellers = Book.objects.filter(is_best_seller=True).select_related('category')[:8]
    new_arrivals = Book.objects.filter(is_new_arrival=True).select_related('category')[:8]
    audiobooks = Book.objects.filter(is_audiobook=True).select_related('category')[:6]
    categories = Category.objects.all()
    cart = get_cart(request)
    cart_count = cart.get_item_count()
    context = {
        'best_sellers': best_sellers,
        'new_arrivals': new_arrivals,
        'audiobooks': audiobooks,
        'categories': categories,
        'cart_count': cart_count,
    }
    return render(request, 'store/home.html', context)


# ─── Book List ────────────────────────────────────────────────────────────────
def book_list(request):
    books = Book.objects.select_related('category').all()
    categories = Category.objects.all()
    category_slug = request.GET.get('category')
    search_query = request.GET.get('q', '')
    sort_by = request.GET.get('sort', '')

    if category_slug:
        books = books.filter(category__slug=category_slug)
    if search_query:
        books = books.filter(title__icontains=search_query) | books.filter(author__icontains=search_query)
    if sort_by == 'price_asc':
        books = books.order_by('price')
    elif sort_by == 'price_desc':
        books = books.order_by('-price')
    elif sort_by == 'rating':
        books = books.order_by('-rating')

    cart = get_cart(request)
    context = {
        'books': books,
        'categories': categories,
        'selected_category': category_slug,
        'search_query': search_query,
        'sort_by': sort_by,
        'cart_count': cart.get_item_count(),
    }
    return render(request, 'store/book_list.html', context)


# ─── Book Detail ──────────────────────────────────────────────────────────────
def book_detail(request, pk):
    book = get_object_or_404(Book, pk=pk)
    related_books = Book.objects.filter(category=book.category).exclude(pk=pk)[:4]
    cart = get_cart(request)
    context = {
        'book': book,
        'related_books': related_books,
        'cart_count': cart.get_item_count(),
    }
    return render(request, 'store/book_detail.html', context)


# ─── AI Summary ──────────────────────────────────────────────────────────────
def get_ai_summary(request, pk):
    book = get_object_or_404(Book, pk=pk)
    if book.ai_summary:
        return JsonResponse({'summary': book.ai_summary})

    api_key = settings.GEMINI_API_KEY
    if api_key == 'YOUR_GEMINI_API_KEY_HERE' or not api_key:
        summary = (
            f'"{book.title}" by {book.author} is an engaging read that explores compelling themes '
            f'and offers readers a unique perspective. '
            f'(Connect your Gemini API key in settings.py to get real AI summaries.)'
        )
        book.ai_summary = summary
        book.save()
        return JsonResponse({'summary': summary})

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent?key={api_key}"
        payload = {
            "contents": [{
                "parts": [{
                    "text": f"Provide a concise 3-4 sentence summary of the book '{book.title}' by {book.author}. Focus on the main themes, plot overview, and why readers would enjoy it."
                }]
            }]
        }
        response = requests.post(url, json=payload, timeout=15)
        data = response.json()
        summary = data['candidates'][0]['content']['parts'][0]['text']
        book.ai_summary = summary
        book.save()
        return JsonResponse({'summary': summary})
    except Exception as e:
        return JsonResponse({'summary': f'Could not fetch AI summary at this time. Error: {str(e)}'})


# ─── Cart Views ──────────────────────────────────────────────────────────────
def cart_view(request):
    cart = get_cart(request)
    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('book').all(),
        'cart_total': cart.get_total(),
        'cart_count': cart.get_item_count(),
    }
    return render(request, 'store/cart.html', context)


def add_to_cart(request, pk):
    book = get_object_or_404(Book, pk=pk)
    cart = get_cart(request)
    cart_item, created = CartItem.objects.get_or_create(cart=cart, book=book)
    if not created:
        cart_item.quantity += 1
        cart_item.save()
    messages.success(request, f'"{book.title}" added to cart!')
    next_url = request.GET.get('next', 'cart')
    return redirect(next_url)


def remove_from_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    cart_item.delete()
    messages.info(request, 'Item removed from cart.')
    return redirect('cart')


def update_cart(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id)
    qty = int(request.POST.get('quantity', 1))
    if qty > 0:
        cart_item.quantity = qty
        cart_item.save()
    else:
        cart_item.delete()
    return redirect('cart')


# ─── Checkout ────────────────────────────────────────────────────────────────
def checkout(request):
    cart = get_cart(request)
    if cart.get_item_count() == 0:
        return redirect('cart')

    if request.method == 'POST':
        order = Order.objects.create(
            session_key=request.session.session_key,
            full_name=request.POST['full_name'],
            email=request.POST['email'],
            address=request.POST['address'],
            city=request.POST['city'],
            pincode=request.POST['pincode'],
            phone=request.POST['phone'],
            total_amount=cart.get_total(),
        )
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                book=item.book,
                quantity=item.quantity,
                price=item.book.price,
            )
        cart.items.all().delete()
        return redirect('order_success', order_id=order.id)

    context = {
        'cart': cart,
        'cart_items': cart.items.select_related('book').all(),
        'cart_total': cart.get_total(),
        'cart_count': cart.get_item_count(),
    }
    return render(request, 'store/checkout.html', context)


def order_success(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'store/order_success.html', {'order': order, 'cart_count': 0})


# ─── Newsletter ──────────────────────────────────────────────────────────────
def subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip()
        if email:
            sub, created = Subscriber.objects.get_or_create(email=email)
            if created:
                messages.success(request, '🎉 Thank you for subscribing!')
            else:
                messages.info(request, 'You are already subscribed!')
    return redirect(request.META.get('HTTP_REFERER', 'home'))
