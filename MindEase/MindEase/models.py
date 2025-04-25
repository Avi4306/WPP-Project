from django.db import models

class datas(models.Model):
    name= models.CharField(max_length=100)
    email= models.CharField(max_length=100)
    date= models.CharField(max_length=100)
    time= models.CharField(max_length=100)
    concern= models.TextField()
    