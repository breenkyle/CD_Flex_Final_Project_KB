# from contextlib import redirect_stderr
# # from xml.etree.ElementTree import QName

# from platformdirs import user_data_dir
from flask import render_template, redirect, session, flash, request
import re
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.set_model import Set
# from flask_bcrypt import Bcrypt


@app.route('/set/new')
def new_set():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_set.html', user = User.get_by_id(data))



@app.route('/create/set',methods=['POST'])
def create_set():
    if 'user_id' not in session:
        return redirect('/logout')
    if not Set.set_validate(request.form):
        return redirect('/set/new')
    data = {
        "set_name": request.form["set_name"],
        "description": request.form["description"],
        "user_id": session["user_id"]

    }
    Set.save(data)
    return redirect('/all_mocs')



@app.route('/edit/set/<int:id>')
def edit_set(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id":id
    }
    user_data ={
        "id":session['user_id']
    }
    return render_template("edit_set.html", edit=Set.get_one(data), user=User.get_by_id(user_data))


@app.route('/update/set',methods=['POST'])
def update_set():
    set_id=request.form['id']
    if "user_id" not in session:
        return redirect('/logout')
    if not Set.set_validate(request.form):
        return redirect(f'/edit/set/{set_id}')
    data = {
        "set_name": request.form["set_name"],
        "description": request.form["description"],
        "id": session["id"]
    }
    Set.update(data)
    return redirect('/all_sets')


@app.route('/set/<int:id>')
def one_set(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }

    return render_template("one_set.html", set = Set.get_one(data), user = User.get_by_id(user_data))


@app.route('/destroy/set/<int:id>')
def destroy_set(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    Set.destroy(data)
    return redirect('/all_sets')