from django.db import models

# Create your models here.
class Chatter(models.Model):
	user_key=models.CharField(max_length=20, unique=True)
	next_chat_code=models.IntegerField(default=0)

	def set_next_chat_code(self, next_chat_code):
		self.next_chat_code=next_chat_code
		self.save()

class Chat(models.Model):
	content=models.TextField()
	user=models.ForeignKey(Chatter, related_name='chat')
	created_date = models.DateTimeField(auto_now_add=True, null=True)

class kunja_menu(models.Model):
	day=models.CharField(max_length=10, unique=True)
	lunch=models.TextField()
	dinner=models.TextField()

class Student_union_menu(models.Model):
	name=models.CharField(max_length=20,unique=True)
	price=models.CharField(max_length=10)
	popular=models.IntegerField(default=0)

class Skyrounge_menu(models.Model):
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