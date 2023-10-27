from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import csv

app = FastAPI()

@app.get('/')
def home():
    return 'welcome to my blog'

@app.get('/about/')
def about_page():
    return 'this is all about us'


@app.get('/contact_us/')
def contact_page():
    return 'call us on +234 (0)8129012386'

# CSV database file
csv_file = "blog_data.csv"

# User model
class User(BaseModel):
    id: int
    email: str
    username: str
    password: str

# Post model
class Post(BaseModel):
    title: str
    content: str


# Define authentication security
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Read users from CSV
def get_users():
    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        return [user for user in csv_reader]
    
# Read posts from CSV
def get_posts():
    with open(csv_file, mode='r') as file:
        csv_reader = csv.DictReader(file)
        return [post for post in csv_reader]

# Check if user exists
def get_user(username):
    users = get_users()
    for user in users:
        if user["username"] == username:
            return user
        
# Authenticate user
def authenticate_user(username, password):
    user = get_user(username)
    if user and user["password"] == password:
        return user

# Create user
def create_user(user):
    with open(csv_file, mode='a', newline='') as file:
        fieldnames = ['id', 'email', "username", "password"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(user.dict())

# Create post
def create_post(post):
    with open(csv_file, mode='a', newline='') as file:
        fieldnames = ["title", "content"]
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writerow(post.dict())


# Get all posts
@app.get("/posts/")
def read_posts(current_user: User = Depends(authenticate_user)):
    posts = get_posts()
    return posts

# Create a new post
@app.post("/posts/")
def create_new_post(post: Post, current_user: User = Depends(authenticate_user)):
    create_post(post)
    return post

# User registration
@app.post("/register/")
def register(user: User):
    existing_user = get_user(user.username)
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="User already exists")
    create_user(user)
    return user