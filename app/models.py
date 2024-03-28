from django.db import models
from django.contrib.auth.models import User


# user_student details
class StudentDetails(models.Model):
    username=models.CharField(max_length=120)
    email = models.CharField(max_length=120)
    wallet_balance = models.FloatField(default = 5000)
    status=models.IntegerField(default=1)
    user = models.ForeignKey(User,on_delete=models.CASCADE)

# bookdetails
class BookDetails(models.Model):
    name=models.CharField(max_length=128)
    book_code=models.IntegerField()
    author_name=models.CharField(max_length=128)
    date=models.DateField()
    status=models.CharField(max_length=128)
    amount=models.IntegerField()
    available_books = models.IntegerField()
    created_date=models.DateField()
    created_by=models.IntegerField()
    updated_date=models.DateField(null=True)
    updated_by=models.IntegerField(null=True)
    book_img = models.FileField(upload_to='image')


# booktransaction history
class Booktransferhistory(models.Model):
    student=models.ForeignKey(StudentDetails,on_delete=models.CASCADE)
    code=models.IntegerField()
    book_name=models.CharField(max_length=128)
    status = models.CharField(max_length = 20)
    created_at = models.DateTimeField(auto_now_add=True)


#user book details 
class UserBookDetails(models.Model):
    student=models.ForeignKey(StudentDetails,on_delete=models.CASCADE)
    books_quantity = models.IntegerField()
    updated_at = models.DateTimeField(auto_now_add=True)

#user bookstatus 
class UserBookStatus(models.Model):
    student=models.ForeignKey(StudentDetails,on_delete=models.CASCADE)
    book = models.ForeignKey(BookDetails,on_delete=models.CASCADE)
    status = models.IntegerField(default=1)

#cash_add transferhistory
class UserCash_history(models.Model):
    student=models.ForeignKey(StudentDetails,on_delete=models.CASCADE)
    student_name=models.CharField(max_length=30)
    amount=models.FloatField()
    date_time=models.DateTimeField(auto_now_add=True)
    deposited_by_admin=models.CharField(max_length=30)





# Create your models here.




