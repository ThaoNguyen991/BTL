from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


# Create your models here.
class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)

class BaseModel(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True
        ordering = ['id']

class Category(BaseModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class House(BaseModel):
    address = models.CharField(max_length=100)
    description = RichTextField(null=True)
    image = models.ImageField(upload_to="houses/%Y/%m")
    category = models.ForeignKey(Category, on_delete=models.RESTRICT)
    numbers = models.ManyToManyField('Number')

    def __str__(self):
        return self.address

    class Meta:
        unique_together = ('address', 'category')


class Room(BaseModel):
    roomname = models.CharField(max_length=50)
    description = RichTextField(null=True)
    image = models.ImageField(upload_to="rooms/%Y/%m")
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    numbers = models.ManyToManyField('Number')
    def __str__(self):
        return self.roomname

class Number(BaseModel):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Interaction(BaseModel):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)

    class Meta:
        abstract = True

class Comment(Interaction):
    content = models.CharField(max_length=255)

class Like(Interaction):
    liked = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'room')

class Rating(Interaction):
    rate = models.SmallIntegerField(default=0)