📚 BookVerse — Online Book Store (Django)
A full-stack Django web application for an online bookstore with AI-powered book summaries using Google Gemini API.

🗂️ Project Structure
bookstore/
├── bookstore/               ← Django project config
│   ├── settings.py          ← All settings (DB, API keys, etc.)
│   ├── urls.py              ← Root URL routing
│   └── wsgi.py
├── store/                   ← Main app
│   ├── models.py            ← Database models
│   ├── views.py             ← All page logic
│   ├── urls.py              ← App URL routing
│   ├── admin.py             ← Admin panel config
│   ├── templates/store/     ← All HTML templates
│   │   ├── base.html        ← Navbar, footer, layout
│   │   ├── home.html        ← Homepage
│   │   ├── book_list.html   ← Browse/filter books
│   │   ├── book_detail.html ← Single book + AI summary
│   │   ├── cart.html        ← Shopping cart
│   │   ├── checkout.html    ← Order form
│   │   └── order_success.html
│   └── management/commands/
│       └── seed_data.py     ← Sample data loader
├── manage.py
├── requirements.txt
└── README.md
⚡ SETUP INSTRUCTIONS (Step by Step)
STEP 1 — Install Python
Make sure Python 3.10 or higher is installed. Download from: https://www.python.org/downloads/

STEP 2 — Create a Virtual Environment
Open a terminal/command prompt inside the bookstore/ folder, then run:

python -m venv venv
Activate it:

Windows: venv\Scripts\activate
Mac/Linux: source venv/bin/activate
STEP 3 — Install Dependencies
pip install -r requirements.txt
STEP 4 — Add Your Gemini API Key (Optional but Recommended)
Go to https://aistudio.google.com/app/apikey
Create a free API key
Open bookstore/settings.py
Replace YOUR_GEMINI_API_KEY_HERE with your key:
GEMINI_API_KEY = 'your-actual-key-here'
Without this, a placeholder message appears instead of real AI summaries — the rest of the site works fine.

STEP 5 — Apply Database Migrations
python manage.py makemigrations
python manage.py migrate
STEP 6 — Create an Admin (Superuser) Account
python manage.py createsuperuser
Enter a username, email, and password when prompted.

STEP 7 — Load Sample Books & Categories
python manage.py seed_data
This adds 8 categories and 16 sample books to the database.

STEP 8 — Run the Development Server
python manage.py runserver
Open your browser and go to:

🌐 Website: http://127.0.0.1:8000/
🔧 Admin Panel: http://127.0.0.1:8000/admin/
🔧 Admin Panel Guide
Log in at /admin/ with your superuser credentials.

Adding Books
Go to Store > Books > Add Book
Fill in Title, Author, Category, Price, Stock
Upload a cover image (optional)
Check Is Best Seller / Is New Arrival / Is Audiobook as needed
Save
Adding Categories
Go to Store > Categories > Add Category
Enter Name (slug auto-fills), an emoji Icon, and optional Description
Save
Viewing Subscribers
Go to Store > Subscribers to see all newsletter email signups
Managing Orders
Go to Store > Orders to view and update order status
🤖 AI Book Summary Feature
When a user visits a book detail page, they see a "Generate Summary" button. Clicking it calls /books/<id>/ai-summary/ which:

Checks if a summary is already saved in the DB
If not, sends the book title/author to Google Gemini API
Saves and displays the response
The summary is cached in book.ai_summary so it's only fetched once per book.

📄 Pages Summary
URL	What it shows
/	Homepage: Hero, Best Sellers, New Arrivals, Audiobooks
/books/	Browse all books with search/filter/sort
/books/<id>/	Single book detail + AI summary
/cart/	Shopping cart
/checkout/	Checkout form
/order/success/<id>/	Order confirmation
/admin/	Admin panel (superuser only)
🛠️ Technologies Used
Django 4.2 — Backend framework
SQLite — Default database (zero config)
Bootstrap 5.3 — Responsive UI
Pillow — Image handling for book covers
Google Gemini API — AI book summaries
Font Awesome — Icons
🚀 Optional Enhancements
Add user authentication (login/register)
Integrate Razorpay or Stripe for real payments
Add book ratings and reviews
Deploy to Heroku, Railway, or Render
Add pagination to book lists
Built with ❤️ as a Django Major Project
