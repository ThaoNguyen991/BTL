from rest_framework import viewsets, generics, status, parsers, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from houses import serializer, paginator
from houses.models import Category, House, Room, User, Comment, Like
from houses import perms


class CategoryViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = serializer.CategorySerializer


class HouseViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = House.objects.filter(active=True).all()
    serializer_class = serializer.HouseSerializer
    pagination_class = paginator.HousePaginator

    def get_queryset(self):
        queries = self.queryset

        q = self.request.query_params.get("q")
        if q:
            queries = queries.filter(address__icontains=q)

        return queries

    @action(methods=['get'], detail=True)
    def rooms(self, request, pk):
        rooms = self.get_object().room_set.filter(active=True).all()

        return Response(serializer.RoomSerializer(rooms, many=True, context={'request': request}).data,
                        status=status.HTTP_200_OK)


class RoomViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = Room.objects.filter(active=True).all()
    serializer_class = serializer.RoomDetailsSerializer
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.action in ['add_comment', 'like']:
            return [permissions.IsAuthenticated()]

        return self.permission_classes

    @action(methods=['post'], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        c = Comment.objects.create(user=request.user, room=self.get_object(), content=request.data.get('content'))

        return Response(serializer.CommentSerializer(c).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='like', detail=True)
    def like(self, request, pk):
        like, created = Like.objects.get_or_create(user=request.user, room=self.get_object())
        if not created:
            like.active = not like.active
            like.save()

        return Response(serializer.RoomDetailsSerializer(self.get_object(), context={'request': request}).data, status=status.HTTP_200_OK)


class CommentViewSet(viewsets.ViewSet, generics.DestroyAPIView, generics.UpdateAPIView):
    queryset = Comment.objects.all()
    serializer_class = serializer.CommentSerializer
    permission_classes = [perms.OwnerAuthenticated]


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True).all()
    serializer_class = serializer.UserSerialzier
    parser_classes = [parsers.MultiPartParser]

    def get_permissions(self):
        if self.action.__eq__('current_user'):
            return [permissions.IsAuthenticated()]

        return [permissions.AllowAny()]

    @action(methods=['get'], url_path='current-user' ,url_name='current-user', detail=False)
    def current_user(self, request):
        return Response(serializer.UserSerialzier(request.user).data)

