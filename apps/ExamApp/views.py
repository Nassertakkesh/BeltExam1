
from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt


def register(request):
    errors = User.objects.basic_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        password = request.POST['password']
        print(password)
        password_confirm = request.POST['password_confirm']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt()) 
        pw_hash_confirm = bcrypt.hashpw(password_confirm.encode(), bcrypt.gensalt()) 
        print(pw_hash)
        theuser = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], password=pw_hash, password_confirm=pw_hash_confirm, 
        email=request.POST['email']) 
        print("its working")
        logged_user = theuser 
        request.session['userid'] = logged_user.id
        return redirect('/wishes')
        
def login(request):
    if not User.objects.loginValid(request):
        return redirect('/')
    else:
        theuser = User.objects.filter(email=request.POST['email']) 
        if theuser: 
            logged_user = theuser[0] 
            request.session['userid'] = logged_user.id
            return redirect('/wishes')
        return redirect('/')

def index(request):
    if request.session.get("userid"):
        return redirect("/")
    return render(request,"ExamApp/index.html")

def presuccess(request):
    uid = request.session.get("userid")
    if not uid:
        return redirect("/")
    this_user = User.objects.get(id=uid)
    this= this_user.items_uploaded.all()
    this_user_items = this.exclude(granted=True)
    allitems = Item.objects.filter(granted=True)
    # this_item_like=
    # countlikes= Item.objects.users_who_fav.all().count()
    # not_this_user = User.objects"allotheritems":
    context = {
        "thisuser" : User.objects.get(id=uid),
        "youritems" : this_user_items,
        "this_user" : User.objects.get(id=uid),
        "allitems":allitems,
        "all": Item.objects.all(),

        
    }
    return render(request,"ExamApp/success.html",context)

#   "remainingauthors": Authors.objects.all().exclude(books__in=Books.objects.filter(id=int(id)))
    

def logout(request):
    del request.session['userid'] 
    return redirect("/")

################^^^^^^^^^^^THE ABOVE CODE IS FOR REGISTRATION AND LOGIN^^^^^^^^^^^^######################

def makewishhtml(request):
    uid = request.session.get("userid")
    if not uid:
        return redirect("/")
    return render(request,"ExamApp/new.html")

def makewish(request):
    uid = request.session.get("userid")
    if not uid:
        return redirect("/")
        
    errors = User.objects.book_add_valid(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    else:
        if request.session.get("userid"):
            this_user_session_id= request.session.get("userid")
            print(this_user_session_id)
            this_user_obj= User.objects.get(id= this_user_session_id)

            print(this_user_obj.first_name)
            # print(for key in )

            new_book_adding = Item.objects.create(item=request.POST["itemName"],desc=request.POST["descriptionName"],uploaded_by = this_user_obj)

            print(new_book_adding)
            # this_user = User.objects.get(id=this_user_session_id)
            # print(this_user)
            # new_book_adding.users_who_fav.add(this_user)
            return redirect ("/wishes")
        return render(request,"FavBooksApp/index.html")


def editwishhtml(request,id):
    uid = request.session.get("userid")
    if not uid:
        return redirect("/")
    this_item = Item.objects.get(id=id)
    context = {
        "userid": id,
        "iteminfo": this_item
    }
    return render(request,"ExamApp/edit.html",context)


def editwish(request,id):
    uid = request.session.get("userid")
    if not uid:
        return redirect("/")

    errors = User.objects.book_add_valid(request)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/edit/' + id)
    else:
        if request.session.get("userid"):
            this_user_session_id= request.session.get("userid")
            print(this_user_session_id)
            update_item_obj= Item.objects.get(id= id)
            print(update_item_obj.item)
            update_item_obj.item = request.POST['itemName']
            update_item_obj.desc = request.POST['descriptionName']
            update_item_obj.save()
            return redirect ("/wishes")
        return render(request,"FavBooksApp/index.html")


def delete(request,id):
    uid = request.session.get("userid")
    if not uid:
        return redirect("/")
    else:
        if request.session.get("userid"):
            this_user_session_id= request.session.get("userid")
            print(this_user_session_id)
            
            update_item_obj= Item.objects.get(id= id)
            print(update_item_obj.item)
            update_item_obj.delete() 
         

            return redirect ("/wishes")
        return render(request,"FavBooksApp/index.html")


def granted(request,id):
    uid = request.session.get("userid")
    if not uid:
        return redirect("/")
    else:
        this_user_session_id= request.session.get("userid")
        print(this_user_session_id)
        update_item_obj= Item.objects.get(id= id)
        print(update_item_obj.item)
        update_item_obj.granted = True
        update_item_obj.save()
        return redirect ("/wishes")

    return render(request,"ExamApp/edit.html")


def stats(request):
    uid = request.session.get("userid")
    if not uid:
        return redirect("/")
    this_user = User.objects.get(id=uid)
    this = this_user.items_uploaded.all()
    this_user_items = this.exclude(granted=True).count()
    granted = this.exclude(granted=False).count()
    allitems = Item.objects.filter(granted=True).count()

    # not_this_user = User.objects"allotheritems":
    context = {
        "thisuser" : User.objects.get(id=uid),
        "youritems" : this_user_items,
        "this_user" : User.objects.get(id=uid),
        "allitems":allitems,
        "granted": granted
        
    }
    return render(request,"ExamApp/stat.html",context)


def like(request,id):
    if request.session.get("userid"):
        the_item_being_liked= id
        this_user_session_id= request.session.get("userid")
        this_item = Item.objects.get(id=the_item_being_liked)
        this_user = User.objects.get(id=this_user_session_id)
        print(this_item)
        print(this_user)
        print(this_user_session_id)
        print(the_item_being_liked)
        this_item.users_who_fav.add(this_user)

        return redirect ("/wishes") 
    return render(request,"ExamApp/index.html")
