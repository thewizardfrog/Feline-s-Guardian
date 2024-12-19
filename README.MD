# Feline's Guardian
#### Video Demo:  <https://youtu.be/Zs3Mf7G-fpM>

**Feline's Guardian** is a **full-stack web application** built with **Flask** that aims to support animal welfare by managing inquiries related to stray cats, accepting donations, and facilitating merchandise sales. The app allows users to submit and track inquiries, shop for merchandise, and contribute to the cause.

## Features

### **User Authentication**
- **Sign Up** and **Login**: Users can register and log in with their telephone number and password.
- **Session Management**: Secure user sessions are managed using **Flask-Session** to ensure authenticated access.

### **Inquiry Management**
- **Submit Inquiries**: Users can submit inquiries regarding stray cats that need assistance, such as rescue, neutering, or medical care.
- **Track Inquiries**: Users can view the status of their submitted inquiries, which are updated as the request progresses.

### **Admin Dashboard**
- **Inquiry Management**: Admins can manage incoming inquiries, view user details, and update the status of each request.
- **Notes System**: Admins can create and manage personal notes related to inquiries for internal tracking.

### **E-commerce Functionality**
- **Browse Merchandise**: Users can browse and purchase merchandise, with all proceeds supporting stray cat welfare.
- **Shopping Cart and Checkout**: Users can add items to their shopping cart, review their order, and proceed to checkout.
- **Donation System**: Users can make one-time or recurring donations to help fund animal welfare initiatives.

### **Responsive Design**
- The app is built using **Bootstrap** to ensure a **responsive** design across different screen sizes, making it accessible on both desktop and mobile devices.

### **Data Security**
- Passwords are securely hashed using **Werkzeug**, and **Flask-Session** manages user sessions to ensure safe and secure interaction with the app.

## Technologies Used

- **Flask**: Backend web framework for routing and rendering templates.
- **SQLite**: Database for storing user data, inquiries, orders, and products.
- **Werkzeug**: Used for password hashing and secure authentication.
- **Flask-Session**: Manages user sessions to keep users logged in.
- **Bootstrap**: Frontend framework for responsive design and styling.
- **Jinja**: Templating engine for dynamic HTML content rendering.
- **SQL**: Database queries for managing users, inquiries, orders, and products.

## Installation

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/felines-guardian.git

