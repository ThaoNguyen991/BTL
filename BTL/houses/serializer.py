from houses.models import Category, House, Number, Room, User, Comment
from rest_framework import serializers


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class NumberSerializer(serializers.ModelSerializer):
    class Meta:
        model = Number
        fields = ['id', 'name']


class BaseSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField(source='image')
    numbers = NumberSerializer(many=True)

    def get_image(self, house):

        if house.image:
            request = self.context.get('request')
            if request:
                return request.build_absolute_uri('/static/%s' % house.image.name)
            return '/static/%s' % house.image.name


class HouseSerializer(BaseSerializer):
    class Meta:
        model = House
        fields = '__all__'


class RoomSerializer(BaseSerializer):
    class Meta:
        model = Room
        fields = ['id', 'roomname', 'price', 'image', 'numbers', 'content', 'created_date', 'updated_date']


class RoomDetailsSerializer(RoomSerializer):
    liked = serializers.SerializerMethodField()

    def get_liked(self, room):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return room.like_set.filter(active=True).exists()

    class Meta:
        model = RoomSerializer.Meta.model
        fields = RoomSerializer.Meta.fields + ['liked']


class UserSerialzier(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()

        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerialzier()

    class Meta:
        model = Comment
        fields = ['id', 'content', 'user']
