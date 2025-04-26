from django.db import models

class datas(models.Model):
    name= models.CharField(max_length=100)
    contact = models.CharField(max_length=15)
    email= models.EmailField()
    date= models.DateField()
    time= models.TimeField(max_length=100)
    concern= models.TextField()