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
| Payment Logic    | Placeholder for Razorpay integration   |
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

---

## 🗃️ Project Structure

```
bunny-k28-pobucket.io/
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
   git clone https://github.com/yourusername/bunny-k28-pobucket.io.git
   cd bunny-k28-pobucket.io
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

- Integrate **Razorpay API** for real payment flows  
- Add **Email/OTP authentication**  
- Deploy via **Docker + Vercel or Railway**  
- Real-time bidding with Django Channels  
- Ratings & reviews for sellers  

---

## 👨‍💻 Author

**Arman Das**  
_This project was developed to explore and demonstrate scalable, multi-role Django applications._

---

## 📫 Contact

Need help or have suggestions?

- 📧 Email: [pob.help@gmail.com](mailto:pob.help@gmail.com)  
- 💬 WhatsApp: [Chat on WhatsApp](https://api.whatsapp.com/send?phone=8745951248&text=POB%20NeedHelp)

---

> _"Build systems that build futures."_
