from django.db import models

# Create your models here.
class Chatter(models.Model):
	user_key=models.CharField(max_length=50, unique=True)
	next_chat_code=models.IntegerField(default=0)

	def set_next_chat_code(self, next_chat_code):
		self.next_chat_code=next_chat_code
		self.save()

class Chat(models.Model):
	content=models.TextField()
	user=models.ForeignKey(Chatter, related_name='chat')
	created_date = models.DateTimeField(auto_now_add=True, null=True)

	def __str__(self):
		return self.content+'-'+self.user.user_key

class kunja_menu(models.Model):
	day=models.CharField(max_length=10, unique=True)
	lunch=models.TextField()
	dinner=models.TextField()

	def __str__(self):
		return self.day

class Student_union_menu(models.Model):
	name=models.CharField(max_length=20,unique=True)
	price=models.CharField(max_length=10)
	popular=models.IntegerField(default=0)

	def __str__(self):
		return self.name

class Skyrounge_menu(models.Model):
	day=models.CharField(max_length=10, unique=True)
	lunch=models.TextField()
	dinner=models.TextField()

	def __str__(self):
		return self.day

class Woojung_menu(models.Model):
	day=models.CharField(max_length=10)
	menu=models.CharField(max_length=100)
	price=models.CharField(max_length=20)

	def __str__(self):
		return self.menu

class Woojung(models.Model):
	name=models.CharField(max_length=10, unique=True)
	running_time=models.CharField(max_length=20)
	menus=models.ManyToManyField(Woojung_menu, related_name="type")

	def __str__(self):
		return self.name
