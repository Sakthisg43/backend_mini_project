from flask import Blueprint,request
user = Blueprint('user',__name__,url_prefix='/api/v1/users')
from config import db
from api.user.models import User

#api for user
@user.route('/create', methods = ['POST'])
def create_user():
        data = request.json
        name  = data['name']
        email = data['email']
        is_super_admin = data['is_super_admin']
        delete_permission = data['delete_permission']
        edit_permission = data['edit_permission']
        new_user = User(name=name, email=email, is_super_admin=is_super_admin, delete_permission=delete_permission, edit_permission=edit_permission)
        db.session.add(new_user)
        db.session.commit()
        return "User Created successfully"


@user.route("/edit/<_id>", methods=["PUT"])
def edit_user(_id):
    data_edit = request.get_json()
    get_user = User.query.get(_id)

    if data_edit.get('name'):
            get_user.name = data_edit['name']
    if data_edit.get('email'):
            get_user.email = data_edit['email']
    if data_edit.get('is_super_admin'): 
            get_user.is_super_admin = data_edit['is_super_admin'] 
    if data_edit.get('delete_permission'):
            get_user.delete_permission = data_edit['delete_permission']
    if data_edit.get('edit_permission'):
            get_user.edit_permission = data_edit['edit_permission']
            db.session.add(get_user)
            db.session.commit()
    return "User Edited successfully"













#     elif request.method == 'GET':
#         users = User.query.all()
#         results = [
#             {
#                 "name":user.name,
#                 "email":user.email, 
#                 "is_super_admin":user.is_super_admin,
#                 "delete_permission":user.delete_permission,
#                 "edit_permission":user.edit_permission,                 
#                 "password_hash":user.password_hash,
            
#             }
#                for user in users  ]

#         return {"Count : ":len(results),"User":results}



# @user.route('/users/<user_id>',methods=['GET'])
# def handle(user_id):
#     user = User.query.get_or_404(user_id)

#     if request.method == 'GET':
#         response = {
#             "name":user.name,
#             "email":user.email,
#             "is_super_admin":user.is_super_admin,
#             "Delete":user.delete_permission,
#             "Edit":user.edit_permission,
#             "password_hash":user.password_hash
#         }
#         return {"User":response}

#         '''
#         _id
#         token_created_time
#         is_logged_in
#         '''

        