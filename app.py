from flask import Flask, flash, redirect, render_template, request, session, url_for
from flask_session import Session

import sqlite3

import datetime

from werkzeug.security import check_password_hash, generate_password_hash

from nostril import nonsense

app = Flask(__name__)

key = 'super secret key'

app.config['SECRET_KEY'] = key

app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
app.config['TEMPLATES_AUTO_RELOAD'] = True
Session(app)

con = sqlite3.connect("database.db", check_same_thread=False)
db = con.cursor()

@app.route('/')
def index():
    return render_template("index.html")

@app.route('/get_inquiry', methods=["GET", "POST"])
def get_inquiry():
    if request.method == "POST":
        inquiry = request.form.get('inquiry')
        telephone = request.form.get('telephone')
       
        if not nonsense(inquiry):
            #make sure there's no prior inquiry with the same issue and telephone
            db.execute('SELECT issue and session FROM inquiry WHERE issue = ? AND session = ?', (inquiry.upper(), telephone))

            #if there is one
            if db.fetchone() != None:
                db.execute('SELECT * FROM user_information')
                if db.fetchone() is None:
                    db.execute("INSERT INTO user_information (telephone) VALUES (?)", telephone)
                    con.commit()
                    db.execute('SELECT id FROM inquiry WHERE issue = ? AND session = ?', (inquiry.upper(), telephone))
                    provide_more_info = True
                    session['username'] = telephone
                    return render_template('inquiry.html', inquiry=inquiry.upper(), id=db.fetchone()[0], telephone=session['username'], provide_more_info=provide_more_info) 
                
                flash('You already submit this inquiry.')
                return render_template('apology.html')
            else: 
                #new inquiry
                db.execute("INSERT INTO inquiry (issue, session) VALUES (?, ?)", (inquiry.upper(), telephone))
                con.commit()
                db.execute('SELECT telephone from user_information WHERE telephone = ?', [telephone])
                
                if db.fetchone() is None:
                    db.execute("INSERT INTO user_information (telephone) VALUES (?)", [telephone])
                    con.commit()

                    db.execute('SELECT id FROM inquiry WHERE issue = ? AND session = ?', (inquiry.upper(), telephone))
                    provide_more_info = True

                    session['username'] = telephone
                    return render_template('inquiry.html', inquiry=inquiry.upper(), id=db.fetchone()[0], telephone=session['username'], provide_more_info=provide_more_info)
                else:
                    db.execute('SELECT firstname, lastname FROM user_information WHERE telephone = ?', [telephone])
                    users = db.fetchone()

                    first_name = users[0]
                    last_name = users[1]

                    db.execute('SELECT id FROM inquiry WHERE issue = ? AND session = ?', (inquiry.upper(), telephone))
                    provide_more_info = None

                    session['username'] = telephone
                    return render_template('inquiry.html', inquiry=inquiry.upper(), id=db.fetchone()[0], telephone=session['username'], first_name=first_name, last_name=last_name, provide_more_info=provide_more_info) 
        else:
        
            flash("Your text appears to be unintelligible. Please try again.")
            return render_template('apology.html')

    return redirect('/')


@app.route('/submit_inquiry', methods=["GET", "POST"])
def submit_inquiry():
    if request.method == "POST":
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        password = request.form.get('password')
        info = request.form.get('info')

        if not nonsense(info):

            if first_name and last_name and password:
                db.execute('UPDATE user_information SET firstname = ?, lastname = ? WHERE telephone = ?', (first_name, last_name, session['username']))
                con.commit()
            
            db.execute('SELECT id FROM inquiry WHERE session = ?', [session['username']])
            list_of_inquiries = db.fetchall()
            last_index = len(list_of_inquiries) - 1

            db.execute('UPDATE inquiry SET information = ? WHERE id = ?', (info, list_of_inquiries[last_index][0]))
            con.commit()

            db.execute('SELECT telephone FROM users WHERE telephone = ?', [session['username']])
            username = db.fetchone()

            if username is None:
                db.execute('INSERT INTO users (telephone, password) VALUES (?, ?)', (session['username'], generate_password_hash(password, method='scrypt', salt_length=16)))
            
            db.execute('SELECT inquiry.id, inquiry.issue, inquiry.information, inquiry.progression, user_information.firstname, user_information.lastname, user_information.telephone, progression.color FROM ((inquiry FULL OUTER JOIN user_information ON inquiry.session = user_information.telephone) FULL OUTER JOIN progression ON inquiry.progression = progression.progression) WHERE inquiry.id = ?', [list_of_inquiries[last_index][0]])
            this_user_inquiries = db.fetchall()

            counter = session.get('counter')
            session['counter'] = sum(counter)
            
            return render_template('track_inquiry.html', users=all_inquiry(this_user_inquiries))
        
    return redirect('/user_login')

@app.route('/track_inquiry')
def track_inquiry():
    if 'username' in session:
        db.execute('SELECT inquiry.id, inquiry.issue, inquiry.information, inquiry.progression, user_information.firstname, user_information.lastname, user_information.telephone, progression.color FROM ((inquiry FULL OUTER JOIN user_information ON inquiry.session = user_information.telephone) FULL OUTER JOIN progression ON inquiry.progression = progression.progression) WHERE user_information.telephone = ?', [session['username']])
        this_user_inquiries = db.fetchall()
        return render_template('track_inquiry.html', users=all_inquiry(this_user_inquiries))
    return redirect('/user_login')

@app.route('/user_login', methods=['GET', 'POST'])
def user_login():
    if request.method == 'POST':
        telephone = request.form.get('telephone')
        password = request.form.get('password')

        db.execute('SELECT telephone, password FROM users WHERE telephone = ?', [telephone])
        user = db.fetchone()

        if user is None:
            db.execute('INSERT INTO users (telephone, password) VALUES (?, ?)', (telephone, generate_password_hash(password, method='scrypt', salt_length=16)))
            con.commit()
            session['username'] = telephone
            return redirect('/')
        else:
            if user[0] == telephone and check_password_hash(user[1], password):
                session['username'] = telephone
                return redirect('/')
    return render_template('login.html')

@app.route('/admin')
def admin():
    define()
    return render_template('admin_login.html')

@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        username = request.form.get('admin_username')
        password = request.form.get('admin_password')

        db.execute("SELECT username, password FROM admin WHERE username = ?", [username])
        admin = db.fetchone()

        if admin[0] == username and check_password_hash(admin[1], password):
            session['admin'] = admin[0]
            return redirect('/new_assignment')
        else:
            flash('Incorrect username or password.')
            return render_template('apology.html')
    return render_template('admin_login.html')

@app.route('/new_assignment')
def new_assignment():
    id = request.args.get('s-id')
    the_chosen_note = None
    
    if id:
        db.execute('SELECT header, description, date FROM note WHERE admin = ? AND id = ?', (session['admin'], id))
        the_chosen_note = db.fetchone()
        id = None

    db.execute('SELECT inquiry.id, inquiry.issue, inquiry.information, inquiry.progression, user_information.firstname, user_information.lastname, user_information.telephone FROM inquiry FULL OUTER JOIN user_information ON inquiry.session = user_information.telephone ORDER BY inquiry.id DESC')
    users = db.fetchall()

    db.execute('SELECT id, header, description FROM note WHERE admin = ? ORDER BY id DESC', [session['admin']])
    note = db.fetchall()

    new_users = users[0:session.get('counter')]

    if the_chosen_note:
        return render_template('admin_index.html', new_inquiry=session['counter'], users=all_inquiry(new_users), notes=all_note(note), the_chosen_note=info_about_note(the_chosen_note))
   
    return render_template('admin_index.html', new_inquiry=session['counter'], users=all_inquiry(new_users), notes=all_note(note))

@app.route('/inquiry_management')
def inquiry_management():
    db.execute('UPDATE inquiry SET progression = "This inquiry is now with us" WHERE progression IS NULL;')
    con.commit()

    db.execute('SELECT inquiry.id, inquiry.issue, inquiry.information, inquiry.progression, user_information.firstname, user_information.lastname, user_information.telephone, color_correspondence.functionality FROM (((inquiry FULL OUTER JOIN user_information ON inquiry.session = user_information.telephone) FULL OUTER JOIN progression ON inquiry.progression = progression.progression) FULL OUTER JOIN color_correspondence ON progression.color = color_correspondence.color) WHERE inquiry.id IS NOT NULL ORDER BY inquiry.id DESC')
    users = db.fetchall()

    db.execute('SELECT progression FROM progression')
    progressions = db.fetchall()

    return render_template('inquiry_management.html', users=all_inquiry(users), progressions=all_progression(progressions))

@app.route('/update_progression')
def update_progression():
    id = request.args.get('sid')
    progression = request.args.get('s-progression')
    db.execute('UPDATE inquiry SET progression = ? WHERE id = ?', (progression, int(id)))
    con.commit()
    return redirect('/inquiry_management')

@app.route('/new_progression', methods=["GET", "POST"])
def new_progression():
    if request.method == "POST":
        new_progression = request.form.get('new_progression')
        if not nonsense(new_progression):
            db.execute("INSERT INTO progression (progression) VALUES (?)", [new_progression])
            con.commit()
        else:
            flash("Your text appears to be unintelligible. Please try again.")
            return render_template('apology.html')
    return redirect('/inquiry_management')

@app.route('/to_be_edited_progression')
def to_be_edited_progression():
    selected_progression = request.args.get('s-progression')
    db.execute('UPDATE progression SET edit_progression = ? WHERE progression = ?', ('To be edited', selected_progression))
    con.commit()
    db.execute('SELECT id FROM progression WHERE edit_progression = "To be edited"')
    id_edit_progression = db.fetchone()
    return redirect(url_for('edited_progression', id_edit_progression=id_edit_progression[0]))

@app.route('/edited_progression', methods=["GET", "POST"])
def edited_progression():
    
    if request.method == "POST":
        colored_progression = request.form.get('colored_progression')
        edited_progression = request.form.get('edited_progression')
        db.execute("SELECT id FROM progression WHERE edit_progression = ?", ['To be edited'])
        id_edit_progression = db.fetchall()

        if len(id_edit_progression) == 1:
            db.execute("UPDATE progression SET progression = ?, color = ? WHERE id = ?", (edited_progression, colored_progression, id_edit_progression[0][0]))
            con.commit()
            db.execute("UPDATE progression SET edit_progression = NULL WHERE id = ?", [id_edit_progression[0][0]])
            con.commit()
            return redirect('/inquiry_management')
        elif len(id_edit_progression) > 1:
            db.execute("UPDATE progression SET edit_progression = NULL WHERE edit_progression = ?", ['To be edited'])
            con.commit()
             
            flash("There's an error happening. Please redo the action again")
            return render_template('apology.html')

    id_edit_progression = request.args['id_edit_progression']
    db.execute('SELECT progression from progression WHERE id = ?', [id_edit_progression])
    to_be_edited_progression = db.fetchone()   
    return render_template('admin_settings.html', to_be_edited_progression=to_be_edited_progression[0])

@app.route('/delete_inquiry')
def delete_inquiry():
    id = request.args.get('sid')
    db.execute('DELETE FROM inquiry WHERE id = ?', [id])
    con.commit()
    return redirect('/inquiry_management')

@app.route('/merchandise')
def merchandise():
    db.execute('SELECT product_code, product_name, product_price FROM products')
    products = db.fetchall()
    if 'username' in session:
        db.execute('SELECT orders.product_quantity, products.product_name, products.product_price FROM orders INNER JOIN products ON orders.product_name = products.product_code WHERE orders.telephone = ?', [session['username']])
        user_order_summary = db.fetchall()
        
        if user_order_summary:
            indicator = True
            return render_template('merchandise.html', products=all_product(products), user_order_summary=order_summary(user_order_summary), indicator=indicator)
        else:
            indicator = None
            return render_template('merchandise.html', products=all_product(products), indicator=indicator)
    else:
        indicator = None
        return render_template('merchandise.html', products=all_product(products), indicator=indicator)
        
@app.route('/add_to_cart')
def add_to_cart():
    product_name = request.args.get('s-product')
    
    if 'username' in session:
        db.execute('SELECT telephone, product_name FROM orders WHERE product_name = ? AND telephone = ?', (product_name, session['username']))
        
        if db.fetchone() is None:
            db.execute('INSERT INTO orders (telephone, product_name, product_quantity) VALUES (?, ?, 1)', (session['username'], product_name))
            con.commit()
            return redirect('/merchandise')
        else:
            db.execute('SELECT product_quantity FROM orders WHERE product_name = ? AND telephone = ?', (product_name, session['username']))
            db.execute('UPDATE orders SET product_quantity = ? WHERE product_name = ? AND telephone = ?', (db.fetchone()[0] + 1, product_name, session['username']))
            con.commit()
            return redirect('/merchandise')

    return redirect('/user_login')
    
@app.route('/drop_from_cart')
def drop_from_cart():
    product_name = request.args.get('s-product')
    db.execute('SELECT product_code FROM products WHERE product_name = ?', [product_name])
    product_code = db.fetchone()[0]

    db.execute('SELECT product_quantity FROM orders WHERE telephone = ? AND product_name = ?', (session['username'], product_code))
    product_quantity = db.fetchone()[0]
    if product_quantity == 1:
        db.execute('DELETE FROM orders WHERE telephone = ? AND product_name = ?', (session['username'], product_code))
        con.commit()
        return redirect('/merchandise')
    else:
        db.execute('UPDATE orders SET product_quantity = ? WHERE product_name = ? AND telephone = ?', (product_quantity - 1, product_code, session['username']))
        con.commit()
        return redirect('/merchandise')

@app.route('/check_out')
def check_out():
    db.execute('SELECT orders.product_quantity, products.product_name, products.product_price, orders.product_name FROM orders INNER JOIN products ON orders.product_name = products.product_code WHERE orders.telephone = ?', [session['username']])
    orders = order_summary(db.fetchall())
    return render_template('check_out.html', orders=orders)

@app.route('/make_the_order', methods=["GET", "POST"])
def make_the_order():
    if request.method == 'POST':
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        address = request.form.get('address')

        db.execute('SELECT firstname, lastname FROM user_information WHERE firstname = ? AND lastname = ?', (first_name, last_name))
        user = db.fetchone()
        if user is None:
            db.execute('UPDATE user_information SET firstname = ?, lastname = ?, address = ? WHERE telephone = ?', (first_name, last_name, address, session['username']))
            con.commit()
            db.execute('DELETE FROM orders WHERE telephone = ?', [session['username']])
            con.commit()
            return render_template('track_order.html')
        else:
            db.execute('UPDATE user_information SET address = ? WHERE firstname = ? AND lastname = ?', (address, first_name, last_name))
            con.commit()
            db.execute('DELETE FROM orders WHERE telephone = ?', [session['username']])
            con.commit()
            return render_template('track_order.html')
        
    return redirect('/merchandise')

@app.route('/make_new_note', methods=["GET", "POST"])
def make_new_note():
    if request.method == 'POST':
        header = request.form.get('header')
        description = request.form.get('description')
        date = datetime.datetime.now()

        db.execute('INSERT INTO note (admin, header, description, date) VALUES (?, ?, ?, ?)', (session['admin'], header, description, date))
        con.commit()
    
    return redirect('/new_assignment')

def all_inquiry(people):
    list = []
    column_name = ['id', 'issue', 'information', 'progression', 'first_name', 'last_name', 'telephone', 'progression_color']
    counter = 0

    for person in people:
        dict = {}

        if person:
            for x in range(len(person)):
                if person[x]:
                    dict.setdefault(column_name[x], person[x])
            list.insert(counter, dict)
            counter += 1
    return list 

def all_order(orders):
    list = []
    column_name = ['telephone', 'product_name', 'product_price', 'product_quantity']
    counter = 0

    for order in orders:
        dict = {}

        if order:
            for x in range(len(order)):
                if order[x]:
                    dict.setdefault(column_name[x], order[x])
            list.insert(counter, dict)
            counter += 1
    return list 

def all_progression(progressions):
    list = []
    column_name = ['progression']
    counter = 0

    for progression in progressions:
        dict = {}
        for x in range(len(progression)):
            dict.setdefault(column_name[x], progression[x])
        list.insert(counter, dict)
        counter += 1
    return list

def all_product(products):
    list = []
    column_name = ['product_code', 'product_name', 'product_price']
    counter = 0

    for product in products:
        dict = {}
        for x in range(len(product)):
            dict.setdefault(column_name[x], product[x])
        list.insert(counter, dict)
        counter += 1
    return list

def all_note(notes):
    list = []
    column_name = ['id', 'header', 'description']
    counter = 0

    for note in notes:
        dict = {}
        for x in range(len(note)):
            dict.setdefault(column_name[x], note[x])
        list.insert(counter, dict)
        counter += 1
    return list

def info_about_note(note):
    column_name = ['header', 'description', 'date']
    dict = {}

    for x in range(len(note)):
        dict.setdefault(column_name[x], note[x])
    
    return dict


def order_summary(orders):
    list = []
    column_name = ['product_quantity', 'product_name', 'product_price', 'product_code']
    counter = 0

    for order in orders:
        dict = {}
        for x in range(len(order)):
            dict.setdefault(column_name[x], order[x])
        list.insert(counter, dict)
        counter += 1
    return list

def generate_dict(person):
    dict = {}
    column_name = ['id', 'issue', 'information', 'progression', 'first_name', 'last_name', 'telephone']

    for x in range(len(person)):
        if person[x]:
            dict.setdefault(column_name[x], person[x])

    return dict

def define():
    session['counter'] = 0

def sum(num):
    num += 1
    return num

if __name__ == "__main__":
    app.run(debug=True)