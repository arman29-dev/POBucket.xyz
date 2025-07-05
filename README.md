# 🎓 P.O.Bucket.io — Academic Auction Platform

> Empowering students to auction and monetize their academic creations.

---

## 📘 Project Overview

**P.O.Bucket.io** is a Django-powered online marketplace where school and college students can **auction or sell academic projects** (e.g., robotics kits, software prototypes) to potential buyers. This platform supports registration, secure authentication, product listings, bidding, and full auction lifecycle management.

> Developed with robust MVC principles, this project showcases a modular and scalable approach to marketplace applications.

---

## 🧱 Tech Stack

| Layer            | Technology                             |
|------------------|----------------------------------------|
| Backend          | Django 5.1.2 (Python)                  |
| Frontend         | HTML, CSS, Bulma                       |
| Database         | SQLite3/MySQL                          |
| Environment Vars | Python `dotenv`                        |
| Auth & Security  | Django Hashers, Session Middleware     |
| Payment Logic    | Razorpay integration                   |
| Dev Tools        | Termcolor, Sqlparse, Werkzeug          |

---

## 🛠️ Features

- 🧑‍🎓 Student/Buyer Portal  
- 🧑‍💼 Seller Dashboard  
- 📦 Product Listings & Auction Controls  
- 📊 Bid Management System  
- 🧾 Purchase History Tracking  
- 🛡️ Admin Panel with Moderation  
- 📝 Error Logging via `RouteError`  
- 📄 Modular Django Apps (`buyer`, `seller`)  
- 💳 Payment Processing with Razorpay

---

## 🗃️ Database Schema

### `buyer`

| Field Name | Field Type | Arguments                     |
|------------|------------|-------------------------------|
| username   | CharField  | max_length=100                |
| email      | EmailField | max_length=255, unique=True   |
| phone      | CharField  | max_length=20, null=True      |
| password   | CharField  | max_length=256                |

### `history`

| Field Name       | Field Type    | Arguments                                                   |
|------------------|---------------|-------------------------------------------------------------|
| product          | ForeignKey    | to seller.Product, on_delete=models.SET_NULL, null=True     |
| seller           | ForeignKey    | to seller.Seller, on_delete=models.SET_NULL, null=True      |
| date_of_purchase | DateTimeField | default=timezone.now, verbose_name="date of purchase"       |
| owner            | ForeignKey    | to buyer.Buyer, on_delete=models.CASCADE                    |

### `seller`

| Field Name | Field Type | Arguments |
|------------|------------|-----------|
| name       | CharField  | max_length=255 |
| email      | EmailField | unique=True |
| phone      | CharField  | max_length=20 |
| password   | CharField  | max_length=256 |

### `product`

| Field Name        | Field Type    | Arguments |
|-------------------|---------------|-----------|
| name              | CharField     | max_length=255 |
| description       | TextField     |             |
| category          | CharField     | max_length=50 |
| price             | DecimalField  | max_digits=10, decimal_places=2 |
| upi_id            | CharField     | max_length=255 |
| contact_info      | TextField     |             |
| bidding_enabled   | BooleanField  | default=False |
| seller            | ForeignKey    | to seller.Seller, on_delete=models.CASCADE |
| created_at        | DateTimeField | auto_now_add=True |

### `bids`

| Field Name  | Field Type    | Arguments                                                 |
|-------------|---------------|-----------------------------------------------------------|
| product     | ForeignKey    | to `seller.Product`, on_delete=models.CASCADE             |
| buyer       | ForeignKey    | to `buyer.Buyer`, on_delete=models.CASCADE                |
| amount      | DecimalField  | max_digits=10, decimal_places=2                           |
| status      | CharField     | max_length=20 (e.g., 'pending', 'accepted', 'rejected')   |
| created_at  | DateTimeField | auto_now_add=True                                         |

### `sales`

| Field Name       | Field Type    | Arguments                                                 |
|------------------|---------------|-----------------------------------------------------------|
| product          | ForeignKey    | to `seller.Product`, on_delete=models.SET_NULL, null=True |
| buyer            | ForeignKey    | to `buyer.Buyer`, on_delete=models.SET_NULL, null=True    |
| seller           | ForeignKey    | to `seller.Seller`, on_delete=models.SET_NULL, null=True  |
| amount           | DecimalField  | max_digits=10, decimal_places=2                           |
| payment_method   | CharField     | max_length=20 (e.g., 'upi', 'cash', 'razorpay')           |
| status           | CharField     | max_length=20 (e.g., 'initiated', 'completed')            |
| transaction_time | DateTimeField | default=timezone.now                                      |

---

## 🗃️ Project Structure

```
POBucket/
├── buyer/              # Buyer app: models, views, URLs
├── seller/             # Seller app: products, auctions
├── static/css/         # Custom styling and themes
├── templates/          # HTML templates
├── POBucket/           # Main project configuration
├── manage.py           # Django launcher
├── requirements.txt    # Python dependencies
├── LICENSE             # GNU GPLv3
└── README.md           # You are here
```

---

## 🔧 Installation & Running Locally

1. **Clone the Repository**
   ```bash
   git clone https://github.com/bunny-k28/POBucket.git
   cd POBucket
   ```

2. **Set Up Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # or `venv\\Scripts\\activate` on Windows
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the root directory:
   ```env
   SECRET_KEY=your-secret-key
   DEBUG=True
   RAZORPAY_KEY_ID=your-razorpay-key
   RAZORPAY_KEY_SECRET=your-razorpay-secret
   ```

5. **Run Migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Start the Development Server**
   ```bash
   python manage.py runserver
   ```

7. **Access in Browser**
   ```
   http://127.0.0.1:8000
   ```

---

## 🚀 Future Enhancements

- Add **Email/OTP authentication**  
- Deploy via **Docker + Vercel or Railway**  
- Real-time bidding with Django Channels  
- Ratings & reviews for sellers  
- In-app messaging system
- Product inventory tracking
- Optional escrow system

---

## 👨‍💻 Author

**Arman Das**  
_This project was developed to explore and demonstrate scalable, multi-role Django applications._

---

## 📫 Contact

Need help or have suggestions?

- 📧 Email: [pob.help@gmail.com](mailto:pob.help@gmail.com)  
- 💬 WhatsApp: [Chat on WhatsApp](https://api.whatsapp.com/send?phone=8745951248&text=POB%20NeedHelp)
- GitHub: [github.com/bunny-k28](https://github.com/arman29-dev)

---

## 📜 License

This project is open-source and licensed under the [GNU GPLv3 License](LICENSE).

---

> _"Build systems that build futures."_
