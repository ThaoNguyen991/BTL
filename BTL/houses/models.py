from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


class User(AbstractUser):
    avatar = CloudinaryField('avatar', null=True)


class BaseModel(models.Model):
    created_date = models.DateField(auto_now_add=True, null=True)
    updated_date = models.DateField(auto_now=True, null=True)
    active = models.BooleanField(default=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    name = models.CharField(max_length=50, null=False)

    def __str__(self):
        return self.name


class House(BaseModel):
    address = models.CharField(max_length=255, null=False)
    description = RichTextField()
    image = models.ImageField(upload_to='houses/%Y/%m')
    category = models.ForeignKey(Category, on_delete=models.RESTRICT, related_query_name='houses')
    numbers = models.ManyToManyField('Number')

    def __str__(self):
        return self.address

    class Meta:
        unique_together = ('address', 'category')


class Room(BaseModel):
    roomname = models.CharField(max_length=255, null=False)
    price =  models.CharField(max_length=255, null=False)
    content = RichTextField()
    image = models.ImageField(upload_to='rooms/%Y/%m')
    house = models.ForeignKey(House, on_delete=models.CASCADE)
    numbers = models.ManyToManyField('Number')

    class Meta:
        unique_together = ('roomname', 'house')


class Number(BaseModel):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Interaction(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False)

    class Meta:
        abstract = True


class Comment(Interaction):
    content = models.CharField(max_length=255, null=False)


class Like(Interaction):
    active = models.BooleanField(default=True)

    class Meta:
        unique_together = ('user', 'room')


class Rating(Interaction):
    rate = models.SmallIntegerField(default=0)
