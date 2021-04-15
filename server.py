from flask import Flask,render_template,redirect,request
from mysqlconnection import connectToMySQL    # import the function that will return an instance of a connection

app = Flask(__name__)

@app.route('/')
def index():
    query = "SELECT * FROM users;"
    users = connectToMySQL('users').query_db(query)
    print(users)
    return render_template("index.html",all_users=users)
    

@app.route('/add_user', methods=["POST", "GET"])
def create_user():
    if request.form:
        query = "INSERT INTO users (first_name, last_name, email) VALUES (%(first_name)s, %(last_name)s, %(email)s)"
        data = {
            "first_name":request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email'],
        }
        user_id = connectToMySQL('users').query_db(query, data)
        print(user_id)
        return redirect(f"/display_user/{user_id}")
    else:
        return render_template("add_user.html")


@app.route('/delete_user/<int:user_id>', methods=["GET"])
def delete_user(user_id):
    query = "DELETE FROM users WHERE id = %(id)s;"
    data = {
        'id': user_id
    }

    users = connectToMySQL('users').query_db(query, data)
    return redirect("/")


@app.route('/edit_user/<int:user_id>', methods=["GET", "POST"])
def edit_user(user_id):
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {
        'id': user_id
    }
    users = connectToMySQL('users').query_db(query, data)
    return render_template("/edit_user.html", user=users[0])

    if request.form:
        query = "UPDATE users SET first_name=%(first_name)s, last_name=%(last_name)s, email=%(email)s WHERE id = %(id)s;"
        data = {
            'id': user_id,
            "first_name":request.form['first_name'],
            "last_name": request.form['last_name'],
            "email": request.form['email']
        }
        user_id = connectToMySQL('users').query_db(query, data)
        print(user_id)
        return redirect(f"/display_user/{user_id}")
    else:
        return render_template("/edit_user.html")


@app.route('/display_user/<int:user_id>')
def display_user(user_id):
    query = "SELECT * FROM users WHERE id = %(id)s;"
    data = {
        'id': user_id
    }
    users = connectToMySQL('users').query_db(query, data)
    return render_template("/display_user.html", users=users)


if __name__ == "__main__":
    app.run(debug=True)