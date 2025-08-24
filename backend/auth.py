from flask_restx import Api,Resource,Namespace,fields
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from model import User

auth_ns = Namespace('auth',description="A namespace for authentication")

signup_model = auth_ns.model("SignUp", {
    "username": fields.String(),
    "email": fields.String(),
    "password": fields.String(),
})

login_model = auth_ns.model("Login", {
    "username": fields.String(),
    "password": fields.String(),
})

# ---------- Auth ----------
@auth_ns.route('/signup')
class SignUp(Resource):
    @auth_ns.expect(signup_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')

        # Check if user exists
        if User.query.filter_by(username=username).first():
            return {"message": "User already exists"}, 400

        new_user = User(
            username=username,
            email=email,
            password=generate_password_hash(password)
        )
        new_user.save()
        return {"message": "User created successfully"}, 201


@auth_ns.route('/login')
class Login(Resource):
    @auth_ns.expect(login_model)
    def post(self):
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')

        db_user = User.query.filter_by(username=username).first()
        if db_user and check_password_hash(db_user.password, password):
            access_token = create_access_token(identity=db_user.id)
            refresh_token = create_refresh_token(identity=db_user.id)
            return {
                "message": "Login successful",
                "access_token": access_token,
                "refresh_token": refresh_token
            }, 200

        return {"message": "Invalid username or password"}, 401