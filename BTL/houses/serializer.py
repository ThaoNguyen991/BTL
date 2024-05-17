from .models import Category, House, Room, Number, User, Comment
from rest_framework import serializers

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ['id', 'name']


class HouseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    nymbers = NumberSerializer(many=True)

    def get_image(self, obj):
        request = self.context.get('request')
        if obj.image:
            if request:
                return request.build_absolute_uri("/static/%s" % obj.image.name)
            return "/static/%s" % obj.image.name

    class Meta:
        model = House
        fields = '__all__'


class RoomSerializer(serializers.ModelSerializer):
    numbers = NumberSerializer(many=True)
    class Meta:
        model = Room
        fields = ['id', 'roomname', 'description', 'created_date', 'updated_date', 'image', 'numbers']

class RoomSerializeDetail(RoomSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, room):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return room.like_set.filter(liked=True, user=request.user).exists()

    class Meta:
        model = RoomSerializer.Meta.model
        fields = RoomSerializer.Meta.fields + ['liked']

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', 'password', 'avatar']

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content']