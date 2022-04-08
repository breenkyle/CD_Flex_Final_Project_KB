# from contextlib import redirect_stderr
# # from xml.etree.ElementTree import QName

# from platformdirs import user_data_dir
from flask import render_template, redirect, session, flash, request
import re
from flask_app import app
from flask_app.models.user_model import User
from flask_app.models.moc_model import MOC
# from flask_bcrypt import Bcrypt


@app.route('/moc/new')
def new_moc():
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":session['user_id']
    }
    return render_template('new_moc.html', user = User.get_by_id(data))



@app.route('/create/moc',methods=['POST'])
def create_moc():
    if 'user_id' not in session:
        return redirect('/logout')
    if not MOC.moc_validate(request.form):
        return redirect('/moc/new')
    data = {
        "moc_name": request.form["moc_name"],
        "description": request.form["description"],
        "user_id": session["user_id"]

    }
    MOC.save(data)
    return redirect('/all_mocs')



@app.route('/edit/moc/<int:id>')
def edit_moc(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        "id":id
    }
    user_data ={
        "id":session['user_id']
    }
    return render_template("edit_moc.html", edit=MOC.get_one(data), user=User.get_by_id(user_data))


@app.route('/update/moc',methods=['POST'])
def update_moc():
    moc_id=request.form['id']
    if "user_id" not in session:
        return redirect('/logout')
    if not MOC.moc_validate(request.form):
        return redirect(f'/edit/moc/{moc_id}')
    data = {
        "moc_name": request.form["moc_name"],
        "description": request.form["description"],
        "id": session["id"]
    }
    MOC.update(data)
    return redirect('/all_mocs')


@app.route('/moc/<int:id>')
def one_moc(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    user_data = {
        "id":session['user_id']
    }

    return render_template("one_moc.html", moc = MOC.get_one(data), user = User.get_by_id(user_data))


@app.route('/destroy/moc/<int:id>')
def destroy_moc(id):
    if 'user_id' not in session:
        return redirect('/logout')
    data = {
        "id":id
    }
    MOC.destroy(data)
    return redirect('/all_mocs')