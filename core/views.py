from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAuthenticatedOrReadOnly
from rest_framework import status, generics, mixins
from rest_framework.decorators import api_view, APIView, permission_classes
from .models import Post
from .serializers import PostSerializer
# , CommentSerializer
from django.shortcuts import get_object_or_404
from accounts.serializer import CurrentUserPostSerializer
from .permissions import ReadOnly, AuthorOrReadOnly
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import request
from .models import User
from drf_yasg.utils import swagger_auto_schema

# Create your views here.


@api_view(http_method_names=['GET', 'POST'])
@permission_classes([AllowAny])
def homepage(request: Request):

    if request.method == 'POST':
        data = request.data
        response = {'message': 'Hello world', 'data': data}
        return Response(data=response, status=status.HTTP_201_CREATED)
    response = {'message': 'Hello world'}
    return Response(data=response, status=status.HTTP_200_OK)


class PostListCreateView(generics.GenericAPIView,
                         mixins.ListModelMixin,
                         mixins.CreateModelMixin,
                         ):

    parser_classes = [MultiPartParser, FormParser]
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
    queryset = Post.objects.all()

    def perform_create(self, serializer, format=None):
        user = self.request.user
        serializer.save(author=user)
        return super().perform_create(serializer)

        # GET ALL POST

    @swagger_auto_schema(
        operation_summary='List all Post',
        operation_description='This Returns List of all Post with Descending Dates'
    )
    def get(self, request: Request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.order_by('-created_at')
        return queryset

    @swagger_auto_schema(
        operation_summary='Create a New Post',
        operation_description='Create a New Post with this endpoint'
    )
    def post(self, request: Request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class PostRetrieveUpdateDeleteView(generics.GenericAPIView,
                                   mixins.RetrieveModelMixin,
                                   mixins.UpdateModelMixin,
                                   mixins.DestroyModelMixin,):

    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [AuthorOrReadOnly]

    @swagger_auto_schema(
        operation_summary='Get Post By ID',
        operation_description='Get individual Post by ID with this endpoint'
    )
    def get(self, request: Request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Update Individual Post',
        operation_description='Update Individual Post With this Endpoint'
    )
    def put(self, request: Request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    @swagger_auto_schema(
        operation_summary='Delete Individual Post',
        operation_description='Delete Individual Post With this Endpoint'
    )
    def delete(self, request: Request, *args, **kwargs):

        return self.destroy(request, *args, **kwargs)


@api_view(http_method_names=['GET'])
@permission_classes([IsAuthenticated])
def get_post_for_current_user(request: Request):
    user = request.user

    serializer = CurrentUserPostSerializer(
        instance=user, context={"request": request})

    return Response(data=serializer.data, status=status.HTTP_200_OK)


class ListPOstForAuthor(generics.GenericAPIView, mixins.ListModelMixin):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = []

    def get_queryset(self):

        username = self.request.query_params.get('username') or None

        queryset = Post.objects.all()

        if username is not None:
            return Post.objects.filter(author__username=username)

        return queryset

    @swagger_auto_schema(
        operation_summary='List Post For Author',
        operation_description='Get post for Author With this Endpoint'
    )
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class PostLikeView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        operation_summary=' Post Like',
        operation_description='Post Like Endpoint'
    )
    def put(self, request, *args, **kwargs):
        post = self.get_object()
        user = request.user
        if user in post.likes.all():
            post.likes.remove(user)
        else:
            post.likes.add(user)
        serializer = self.get_serializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


'''
class CommentListCreateView(generics.ListCreateAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class CommentRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]
'''
