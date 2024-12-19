# Feline's Guardian
#### Video Demo:  <https://youtu.be/Zs3Mf7G-fpM>
#### Description:
# Feline's Guardian

This project is a Flask-based web application designed to manage and track inquiries related to animal welfare, primarily focusing on stray cats. The application integrates user inquiry management with a merchandising system, allowing users to submit inquiries, track their progress, and purchase related merchandise. Admins can manage inquiries, users, and create notes for internal tracking. The project also features a shopping cart system for users to add products and complete purchases. It uses **SQLite** as the database, **Flask** for backend routing, and **HTML/CSS** templates for the frontend.

## Key Features

### 1. User Authentication and Session Management:
- **User Registration and Login**: Users can register and log in with a telephone number and password. After logging in, their session is managed using Flask-Session, allowing them to track their interactions with the site (e.g., submitting inquiries, and viewing past orders).
- **Secure Authentication**: The app uses **Werkzeug** to hash and verify passwords, ensuring secure authentication.

### 2. Inquiry Submission and Tracking:
- **Submit Inquiries**: Users can submit inquiries related to stray cats or other animal welfare issues. These inquiries include details such as the issue, the user’s contact information, and any additional context.
- **Track Inquiries**: Users can view the status of their submitted inquiries. They can see the current progression (e.g., "Received", "In Progress", "Completed"), along with the details of the inquiry.
- **Admin Management of Inquiries**: Admins have a dedicated page to manage user inquiries. They can view, update, and track the progress of all user inquiries.

### 3. Admin Panel:
- **Dashboard**: The admin dashboard (`admin_index.html`) allows admins to view new assignments (inquiries) and manage personal notes.
  - New inquiries are displayed in card-style elements with user details (name, phone number, issue).
  - Admins can also view a list of existing notes and select specific notes to view more details. The admin can create new notes for internal tracking if no note is selected.
- **Dynamic Content Rendering**: The admin panel uses dynamic rendering to show new inquiries, selected notes, and the ability to create or update notes based on user interaction.

### 4. Merchandise Section:
- **Browse Merchandise**: The application features a merchandise section, where users can browse items related to animal welfare. Each product includes a name, price, and image.
- **Shopping Cart**: Users can add items to their cart. The cart dynamically updates the quantity of items as users add more. If a user attempts to add the same product again, the quantity is updated rather than creating duplicate entries.
- **Checkout Flow**:
  - **Review Cart**: Users can review their cart, which displays the items, quantities, and total price.
  - **Order Finalization**: After reviewing the cart, users provide their address and personal information to complete the order.
  - **Order Tracking**: After order submission, users are redirected to a track order page.

### 5. Database and Data Management:
- **SQLite Database**: The app uses SQLite for storing data. It contains several tables:
  - **Users Table**: Stores user information, including the telephone number and hashed password.
  - **Inquiries Table**: Contains details of submitted inquiries, such as issue description and user contact information.
  - **Progression Table**: Tracks the status of each inquiry (e.g., "Received", "In Progress").
  - **Orders Table**: Stores data related to merchandise orders, including product names, quantities, and user details.
  - **Products Table**: Stores information about the available merchandise, including product names, prices, and images.

### 6. Frontend Design:
- **Responsive Layout**: The user interface uses **Bootstrap** for responsive design, ensuring the site works well on various devices.
- **Dynamic Rendering**: **Jinja templates** are used to dynamically render content based on the user’s session and interactions. For instance, the admin dashboard displays different content based on whether new inquiries or notes are available.
- **Admin Interaction**: Admins can interact with the system by clicking on inquiry cards to view more details or selecting notes to read.

## User Flow:
1. **User Registration and Login**: Users sign up or log in using their telephone number and password.
2. **Inquiry Submission**: After logging in, users submit inquiries about stray cats or animal welfare.
3. **Tracking Inquiries**: Users can track the progress of their inquiries.
4. **Browsing and Purchasing Merchandise**: Users browse the merchandise section, add items to their cart, and complete purchases.
5. **Admin Management**: Admins manage inquiries, view user data, and track progress. They can also create and view personal notes for internal use.

## Conclusion:
This project is a well-rounded web application that showcases the ability to build a complete Flask-based system with **user authentication**, **dynamic content rendering**, **inquiry management**, and **merchandise functionality**. It offers practical features for managing animal welfare inquiries and processing online orders, making it suitable for a **CS50x final project**.
