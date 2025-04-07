# P.O.Bucket

**P.O.Bucket** is a peer-to-peer e-commerce platform that enables direct buying and selling of products such as software, hardware, and embedded systems. The platform fosters transparency by allowing direct communication between buyers and sellers, eliminating third-party involvement in transactions.

---

## 🚀 Project Overview

P.O.Bucket is designed to be a minimal-friction marketplace for tech-oriented products. Sellers can list their offerings, and buyers can browse, bid, and purchase directly. Every transaction is between the buyer and the seller — P.O.Bucket serves as a platform to facilitate discovery, connection, and negotiation.

---

## 🧩 Key Features

### 🛍️ Product Listings
- Sellers can list products under three main categories:
  - **Software**
  - **Hardware**
  - **Embedded Systems**
- Product descriptions include:
  - Detailed specs
  - Images
  - Pricing
  - Seller's contact information

### 🤝 Direct Buyer-Seller Interaction
- No intermediaries or platform fees.
- Buyers directly contact sellers via provided contact details.
- Negotiation and meet-ups can be arranged outside the platform.

### 💸 Simple Purchase Flow
1. Buyer logs in with their account.
2. Browses and selects a product of interest.
3. Clicks **Buy** to initiate a payment or contacts the seller directly.

### 🧾 Bidding System
- Sellers can enable **bidding** on products.
- Buyers can place bids.
- Sellers can review and accept any bid they find suitable.

### 💰 Payment Methods
- **Online via UPI**
- **Offline cash transactions**, enabled through direct meet-ups.

---

## 🧑‍💼 User Roles

### Seller
- Register and log in to the platform.
- List products with full details.
- Enable or disable the bidding feature per product.
- Accept or reject bids.
- Manage product visibility and availability.

### Buyer
- Register and log in to the platform.
- Browse listings by category or interest.
- Place bids if enabled by seller.
- Initiate purchases using UPI or arrange offline meet-ups.
- Contact seller using the contact info in the product description.

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

### `routeerror`

| Field Name | Field Type    | Arguments                          |
|------------|---------------|------------------------------------|
| title      | CharField     | max_length=122                     |
| message    | TextField     |                                    |
| field      | CharField     | max_length=122                     |
| time       | DateTimeField | default=timezone.now               |

---

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
| payment_method   | CharField     | max_length=20 (e.g., 'upi', 'cash')                       |
| status           | CharField     | max_length=20 (e.g., 'initiated', 'completed')            |
| transaction_time | DateTimeField | default=timezone.now                                      |

---

## 📈 Future Enhancements
- In-app messaging system.
- Seller and buyer review/rating system.
- Notifications for bidding and updates.
- Product inventory tracking.
- Optional escrow system.

---

## 🧪 Tech Stack

- **Backend**: Django (Python)
- **Frontend**: HTML, CSS, JS
- **Database**: MySQL
- **Payment Gateway**: UPI (QR or payment link)
- **Hosting**: VPS / AWS / Heroku

---

## 📜 License

This project is open-source and licensed under the [MIT License](LICENSE).

---

## 📞 Contact

For queries, issues, or collaborations:
- Email: [armandevilk282004@gmail.com]
- GitHub: [github.com/bunny-k28]
<!-- - Project Website: [https://yourdomain.com] -->