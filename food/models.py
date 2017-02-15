from django.db import models

# Create your models here.
class Student_union_menu(models.Model):
	name=models.CharField(max_length=20,unique=True)
	price=models.CharField(max_length=10)

class Skyrounge_menu(models.Model):
	day=models.CharField(max_length=10, unique=True)
	lunch=models.TextField()
	dinner=models.TextField()

class kunja_menu(models.Model):
        day=models.CharField(max_length=10, unique=True)
        lunch=models.TextField()
        dinner=models.TextField()

class Woojung_menu(models.Model):
        day=models.CharField(max_length=10)
        menu=models.CharField(max_length=30)
        price=models.CharField(max_length=20)

class Woojung(models.Model):
	name=models.CharField(max_length=10, unique=True)
	running_time=models.CharField(max_length=20)
	menus=models.ManyToManyField(Woojung_menu, related_name="type")

