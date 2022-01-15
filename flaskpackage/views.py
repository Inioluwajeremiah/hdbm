from flask import Blueprint
from flask.json import jsonify
from flask import render_template, request, url_for, redirect
from flask_login import login_required, current_user
from sqlalchemy.sql.functions import user
from flaskpackage.models import HdbModel
import json
from . import db
from .models import HdbModel, AdminModel
views = Blueprint('views', __name__)


@views.route('/')
@login_required
def dataPage():
    # return redirect(request.url)
    allRecords = HdbModel.query.all()
    if not allRecords:
        # return render_template('main.html', allRecords = allRecords)
        return render_template('main.html', user=current_user)
    else:
        return render_template('main.html', allRecords=allRecords, user=current_user)


@views.route('/register', methods=['GET', 'POST'])
@login_required
def addNewStudents():
    if request.method == "POST":

        if request.form.get('register') == "Register":
            firstname = request.form.get('firstname').upper()
            lastname = request.form.get('lastname').upper()
            middlename = request.form.get('middlename').upper()
            department = request.form.get('department').upper()
            course = request.form.get('course').upper()
            level = request.form.get('level').upper()
            hallname = request.form.get('hallname').upper()
            blockname = request.form.get('blockname').upper()
            roomno = request.form.get('roomno')
            # date = request.form.get('date')
            # , date = date

            if not firstname or not lastname or not middlename or not department or not course or not level or not hallname or not blockname or not roomno:
                fill_fields = "Ensure you fill all fields"
                return render_template('register.html', user=current_user, fill_fields=fill_fields)

            else:
                # db.drop_all()
                # db.create_all()
                studentRecords = HdbModel(firstname=firstname, lastname=lastname, middlename=middlename,
                                          department=department, course=course, level=level, hallname=hallname,
                                          blockname=blockname, roomno=roomno)
                db.session.add(studentRecords)
                db.session.commit()

                smsg = firstname + ' ' + lastname + ' successfully registered'
                return render_template('register.html', smsg=smsg, user=current_user)
        else:
            return render_template('register.html', user=current_user)

    return render_template('register.html', user=current_user)


#   D E L E T E         B U T T O N
@views.route("/delrow", methods=['POST'])
def deleteRow():
    students_records = json.loads(request.data)
    row_id = students_records['row_id']
    deleteUser = HdbModel.query.get(row_id)
    if deleteUser:
        db.session.delete(deleteUser)
        db.session.commit()
    return jsonify({})
    # return redirect(request.url)
    # return render_template('main.html')


#  A D M I N     R E C O R D S
@views.route("/ad_records")
@login_required
def adminRecords():
    # return redirect(request.url)
    adminRecords = AdminModel.query.all()
    if not adminRecords:
        # return render_template('main.html', allRecords = allRecords)
        return render_template('adminRecord.html', user=current_user)
    else:
        return render_template('adminRecord.html', adminRecords=adminRecords, user=current_user)


#  S E A R C H
@views.route('/search', methods=['POST'])
def search():
    if request.method == "POST":
        if request.form.get('search') == 'Search':
            allRecords = HdbModel.query.all()
            searchvalue = request.form.get('search-text').upper()
            if not searchvalue:
                fill_fields = "Search field cannot be empty"
                return render_template('main.html', allRecords=allRecords, fill_fields=fill_fields, user=current_user)
            else:
                searchUsers = HdbModel.query.filter_by(
                    lastname=searchvalue)
                return render_template('search.html', searchUsers=searchUsers, user=current_user)
        return render_template('main.html', user=current_user)


@views.route("/forbidden", methods=['GET', 'POST'])
@login_required
def protected():
    return redirect(url_for('forbidden.html'))


#   E D I T

@views.route("/edit/<id>")
def editRecord(id):
    editRecord = HdbModel.query.filter_by(id=id).first()
    # return redirect(request.url)
    return render_template('update.html', edit_record=editRecord, user=current_user)


#  U P D A T E
@views.route("/update/<id>", methods=['POST'])
def updateRecord(id):

    if request.method == "POST":
        allRecords = HdbModel.query.all()
        if request.form.get('update') == "Update":
            firstname = request.form.get('ufirstname').upper()
            lastname = request.form.get('ulastname').upper()
            middlename = request.form.get('umiddlename').upper()
            department = request.form.get('udepartment').upper()
            course = request.form.get('ucourse').upper()
            level = request.form.get('ulevel').upper()
            hallname = request.form.get('uhallname').upper()
            blockname = request.form.get('ublockname').upper()
            roomno = request.form.get('uroomno')

            studentRecords = HdbModel(firstname=firstname, lastname=lastname, middlename=middlename,
                                      department=department, course=course, level=level, hallname=hallname,
                                      blockname=blockname, roomno=roomno)

            edit_record = HdbModel.query.filter_by(id=id).first()
            edit_record.firstname = firstname
            edit_record.lastname = lastname
            edit_record.middlename = middlename
            edit_record.department = department
            edit_record.level = level
            edit_record.course = course
            edit_record.hallname = hallname
            edit_record.blockname = blockname
            edit_record.roomno = roomno

            # db.session.add(studentRecords )
            db.session.commit()

        # smsg = firstname + ' ' + lastname + ' data has been successfully updated '
        # , smsg = smsg
            return render_template('main.html', allRecords=allRecords, user=current_user)
            # return redirect(url_for('dataPage'))

    return render_template('update.html', user=current_user)


# D E L E T E    ADMIN
@views.route("/delete/<id>")
def delete(id):
    deleteUser = AdminModel.query.filter_by(id=id).first()
    db.session.delete(deleteUser)
    db.session.commit()
    # return redirect(request.url)
    return redirect(url_for('views.adminRecords'))
