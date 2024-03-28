from django.shortcuts import render,redirect
from django.contrib import messages
from .form import CustomUserForm
# from app.form import CustomUserForm
from app.models import *
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login
from datetime import datetime, timedelta
from django.db import transaction

# home page
def home(request):
    return render(request,'index.html')

# user registration page
def signup(request):
    form=CustomUserForm()
    if request.method=='POST':
        form=CustomUserForm(request.POST)
        query_dict = request.POST
        username = query_dict.get('username')
        email =  query_dict.get('email')
        if form.is_valid():
            form.save() 
            admin_user = User.objects.filter(email=email).first()
            user_id = admin_user.id
            print(user_id)
            user_details = StudentDetails(username = username,email = email,user_id = user_id)
            user_details.save()
            messages.success(request,'Register successfull')
    return render(request,'student_register.html',{'form':form})

# user login
def studentlogin(request):
    print(1)
    if request.method=='POST':
        print(2)
        name=request.POST.get('Name')
        pwd=request.POST.get('Password')
        print(name)
        print(pwd)
        try:
            user=authenticate(request,username=name,password=pwd)
            print(user)
            if user is not None:
                print(2)
                login(request,user)
                print(3)
                user_id = request.user.id
            print(4)
            student=StudentDetails.objects.filter(user_id = user_id).first()
            print(student)
            print(5)
            if student.status==1:
                print(5.5)
                return redirect('take')
            else:
                print(6)
                messages.error(request,'User is Does not Active')
                return redirect ('userlogin')

        except:
            messages.error(request,'Username or Password Does not match')
            return redirect ('userlogin')
    return render(request,'student_login.html')


# admin login
def adminlogin(request):
    print(1)
    if request.method=='POST':
        print(2) 
        name=request.POST.get('Name')
        pwd=request.POST.get('Password')
        print(name)
        print(pwd)
        try:
            print(3)
            user=authenticate(request,username=name,password=pwd)
            print(user)
            print(4)
            if user is not None:
                print(5)
                login(request,user)
                print(6)
                return redirect('Bookdetails')
            else:
                print(7)
                messages.error(request,'Username or Password Does not match')
                return redirect ('admin_login')

        except:
            pass
    return render(request,'admin_login.html')

# bookdetails page for admin
def bookdetails(request):
    obj=BookDetails.objects.all()
    return render(request,'Bookdetails.html',{'obj':obj})

#user details in adminpage
def userdetails(request):
    obj=StudentDetails.objects.all()
    return render(request,'userdetails.html',{'obj':obj}) 

#useredit
def useredit(request,pk):
    obj=StudentDetails.objects.filter(id=pk).first()
    print(obj)
    return render(request,'user_edit.html',{'obj':obj})

#addcash
def addcash(request,pk):
    if request.method=='POST':
        amount=request.POST.get('cash')
        old_amount=StudentDetails.objects.filter(id=pk).first()
        amount=float(amount)
        old_amount.wallet_balance+=amount
        old_amount.save()
        print("amount added success")
        date = datetime.now().date()
        cash=UserCash_history(student_id=pk,student_name=old_amount.username,
                                amount=amount,date_time=date)
        cash.save()
        messages.success(request,'Amount Added Sucessfully')

        return redirect("useredit",pk)
        


            
#user book page
def take(request):
    return render(request,'take.html')

#user bookdetails page 
def lib(request):
    if request.method=='POST':
        if request.user.is_authenticated:
            user_id = request.user.id
            date = datetime.now().date()
            library=BookDetails.objects.create(name=request.POST.get('Name'),book_code=request.POST.get('Code'),author_name=request.POST.get('Author'),
                                            date=request.POST.get('Date'),status=request.POST.get('Status'),amount=request.POST.get('Amount'),
                                            created_date=date,created_by=user_id,available_books = request.POST.get('available_books'),
                                            book_img = request.FILES['updatebook'])
            return redirect("Bookdetails")
        else:
            return redirect("book")
    return render(request, 'book.html')

# admin book_update page
def updatebook(request,pk):
    obj=BookDetails.objects.get(id=pk)
    if request.method=='POST':
        library = BookDetails.objects.filter(id=pk).first()
        library.name = request.POST.get('Name')
        library.book_code = request.POST.get('Code')
        library.author_name = request.POST.get('Author')
        library.date = request.POST.get('Date')
        library.amount = request.POST.get('Amount')
        library.available_books = request.POST.get('available_books')
        library.status = request.POST.get('status')
        library.book_img = request.FILES['updatebook']
        date = datetime.now().date()
        library.updated_date = date
        library.save()
        messages.success(request,'successfully updated the book')
        return redirect('Bookdetails')
    return render(request,'updatebook.html',{'obj':obj})

# admin book_delete page
def deletebook(request,pk):
    obj=BookDetails.objects.filter(id=pk).delete()
    messages.success(request,'successfully deleted the book')
    return redirect('Bookdetails')

# user book take page
def take(request):
    obj = BookDetails.objects.all()
    if request.method=='POST':
        aa=request.POST.get('search')
        bb=request.POST.get('searchcode')
        if bb =='':
            obj  = BookDetails.objects.filter(name=aa)
            
        if aa == '':
            obj = BookDetails.objects.filter(book_code=bb)
        if aa != '' and bb != '':
             obj = BookDetails.objects.filter(book_code=bb,name =aa)

        
    return render(request,'take.html',{'obj':obj})


# user book taking and can be saved
@transaction.atomic()
def takebook(request,pk):
        if request.user.is_authenticated:
            user_id = request.user.id
            date = datetime.now().date()
            #Reduce amount in Useraccount
            book_id = pk
            book_details = BookDetails.objects.filter(id = book_id).first()
            if book_details.available_books != 0:
                book_name = book_details.name
                book_code = book_details.book_code
                book_price = book_details.amount
                book_quantity = book_details.available_books
                user_details = StudentDetails.objects.filter(user_id = user_id).first()
                #Amount Reduction
                user_amount = user_details.wallet_balance
                current_amount = user_amount - book_price
                user_details.wallet_balance = current_amount
                user_details.save()
                
                #Book History Registeration
                student = StudentDetails.objects.filter(user_id = user_id).first()
                student_id = student.id
                book_history = Booktransferhistory(student_id = student_id,code = book_code,
                                                    book_name = book_name,status = "Take")
                book_history.save()
                    
                #UserBookstatus Registeration
                status = UserBookStatus(student_id=student_id,book_id = book_id)
                status.save()

                #UserBookDetails Registeration
                user = UserBookDetails.objects.filter(student_id = student_id).first()
                if user is  None:
                    user_book_details = UserBookDetails(student_id = student_id,
                                                books_quantity = 1,updated_at = date)
                    user_book_details.save()
                else:
                    user_update = UserBookDetails.objects.filter(student_id = student_id).first()
                    books_quantity = user_update.books_quantity 
                    quantity = int(books_quantity) +1
                    user_update.books_quantity = quantity
                    user_update.save()

                #Books reduction in BookDetails
                book_details = BookDetails.objects.filter(id = book_id).first()
                quantity = book_details.available_books
                quantity-=1

                book_details.available_books = quantity
                if quantity == 0:
                    book_details.status = 'Unavailable'
                book_details.save()
                messages.success(request,'successfully taken the book')
            else:
                messages.error(request,'Sorry Books not Available in Stocks')
                print("No stocks")    
            return redirect('take')
 

#user book return page 
@transaction.atomic()
def retainbook(request,pk):
    if request.user.is_authenticated:
        user_id = request.user.id
        book_id = pk
        student = StudentDetails.objects.filter(user_id = user_id).first()
        student_id = student.id
        user_book = UserBookStatus.objects.filter(student_id=student_id,book_id=book_id).first()
        if user_book is not None:
            if user_book.status == 1:
                date = datetime.now().date()
                    
                #Details
                book_details = BookDetails.objects.filter(id = book_id).first()
                book_name = book_details.name
                book_code = book_details.book_code
                book_price = book_details.amount
                book_quantity = book_details.available_books

                #Book History Registeration
                student = StudentDetails.objects.filter(user_id = user_id).first()
                student_id = student.id
                book_history = Booktransferhistory(student_id = student_id,code = book_code,
                                                    book_name = book_name,status = "Return")
                book_history.save()

                # books reduction
                books_reduction = UserBookDetails.objects.filter(student_id = student_id).first()
                book_quantity = books_reduction.books_quantity
                quantity = book_quantity-1
                books_reduction.books_quantity = quantity
                books_reduction.save()

                #books updation
                book_details = BookDetails.objects.filter(id = book_id).first()
                quantity = book_details.available_books
                quantity+=1
                book_details.available_books = quantity
                if quantity !=0:
                    book_details.status = 'Available'
                book_details.save()
                user_book.status = 0
                user_book.delete()
                messages.success(request,"successfully return the book")
            else:
                messages.error(request,'you dont have book so you are not able to return')
                print("you dont have book so you are not able to return")

        else:
            messages.error(request,'please purchase book')
            print("please purchase book")
                
    return redirect('take')