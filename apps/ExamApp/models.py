from django.db import models
from datetime import *
from django.contrib import messages
import bcrypt
from datetime import datetime, timedelta

import re	# the regex module

class BlogManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        # curr_date = str((datetime.now() - timedelta(weeks=260)))

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = ("Invalid email address!")
        if len(postData['first_name']) < 2:
            errors["first_name"] = "First name should be at least 2 characters"
        if len(postData['last_name']) < 2:
            errors["last_name"] = "Last name should be at least 2 characters"
        if len(postData['password']) < 2:
            errors["password"] = "Password should be at least 8 characters"
        # if postData['birth_date']:
        #     if datetime.strptime(postData['birth_date'], "%Y-%m-%d") > datetime(year=2007, month=1, day=1):
        #         errors["birth_date"] = "BirthDate should be in the past"
        # else: 
        #     errors["birth_date"] = "BirthDate cant be blank"
        # if datetime.strptime(postData['birth_date'], "%Y-%m-%d") < datetime.today():
        #     errors["birth_date"] = "BirthDate should be in the past"

        if User.objects.filter(email=postData['email']):
            errors["email"] = "email is taken"
        if (postData['password']) != (postData['password_confirm']):
            errors["password"] = "Password's should match"
        return errors

    def loginValid(self, request):
        theuser = User.objects.filter(email=request.POST['email']) 
        if theuser: 
            logged_user = theuser[0] 
            if not bcrypt.checkpw(request.POST['password'].encode(), logged_user.password.encode()):
                messages.error(request, "Invalid password")
            else:
                return True
        messages.error(request, "Invalid email")
        return False

    def book_add_valid(self, request):
        errors = {}
        if len(request.POST['itemName']) < 3:
            errors["itemName"] = "Must have a Title"
        if len(request.POST['descriptionName']) < 3:
            errors["descriptionName"] = "Description should be at least 5 characters"
        return errors



class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(max_length=254)
    password = models.CharField(max_length=255)
    password_confirm = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()   

    def __repr__(self):
        return f"<User object: {self.first_name} {self.last_name}({self.id})>"

class Item(models.Model):
    item = models.CharField(max_length=255)
    desc = models.TextField()
    uploaded_by = models.ForeignKey(User, related_name="items_uploaded")
    granted = models.BooleanField(default=False)
    users_who_fav = models.ManyToManyField(User, related_name="items_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = BlogManager()  

    def __repr__(self):
        return f"<Item object: {self.title} {self.desc}({self.id})>"


        
# this_book = Books.objects.get(id=5)	# retrieve an instance of a book
# this_author = Authors.objects.get(id=5)	# retrieve an instance of a publisher
                        # {% endfor %}     {% for user in users %}
#                            <form action='/favorite' method="POST">
#         {% csrf_token %}
#             <input class="btn btn-primary float-right" type="submit" value="Like">
#             <input type="hidden" name="book_liked_id"value={{books.id}}>
#     </form>

# # # this_author.books.add(this_book)	
# <form action="/books/addingauthortobook" method="POST">
# {% csrf_token %}
# <label for="exampleFormControlSelect1">Choose an Author:</label>
# <input type="hidden" name="hiddenValue" value={{book.id}} >
# <br>
# <select class="form-control" id="exampleFormControlSelect1" name="selectBook" >
#         {% for book in remainingauthors %}
#         <option value= {{author.id}}> {{author.first_name}}</option>
#         {% endfor %}
        
# #         </select>
# # <br>          <!-- <div class="control-group">
#                 <!-- Birth Date -->
#                 <label class="control-label"  for="birth_date">Birthdate</label>
#                 <div class="controls">
#                   <input type="date" id="birth_date" name="birth_date" placeholder="" class="input-xlarge">
#                 </div>
#               </div> -->
# <button type="submit" class="btn btn-primary mb-2">Submit</button>
# </form>