from blog.api.serializers import CommentSerializer, PostSerializer, PostShareSerializer, PostFilterSerializer
from blog.models import Comment, Post, Notification
from rest_framework.generics import (
    ListCreateAPIView, DestroyAPIView, RetrieveUpdateAPIView,
    RetrieveAPIView, RetrieveDestroyAPIView
)
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth import get_user_model
from grammar.utils import get_user_form_jwt
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

User = get_user_model()


class NotificationsAPIView(ListCreateAPIView):
    serializer_class = NotificationSerializer

    @swagger_auto_schema(operation_summary="List notifications for a user")
    def get_queryset(self):
        return Notification.objects.filter(recipient=self.kwargs['userId'])

    @swagger_auto_schema(operation_summary="Create a notification")
    def perform_create(self, serializer):
        recipient_user = get_object_or_404(User, pk=self.kwargs['userId'])
        serializer.save(recipient=recipient_user, sender=self.request.user)


class NotificationRetrieveAPIView(RetrieveDestroyAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()


class CommentCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    @swagger_auto_schema(operation_summary="List comments for a post")
    def get_queryset(self):
        return Comment.objects.filter(postId=self.kwargs['post_id'])

    @swagger_auto_schema(operation_summary="Create a comment on a post")
    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(userId=self.request.user, postId=post)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        comment = serializer.instance

        recipient = None
        notif_type = None

        if comment.parentCommentId:
            recipient = comment.parentCommentId.userId
            notif_type = 'commented_comment'
        else:
            recipient = comment.postId.userId
            notif_type = 'reply'

        content = serializer.validated_data.get('content', '')
        tags = [word for word in content.split() if word.startswith('#')]

        response = {
            "commentId": serializer.instance.id,
            "message": "Comment created successfully",
        }

        if recipient and request.user != recipient:
            Notification.objects.create(
                recipient=recipient,
                sender=request.user,
                type=notif_type,
                commentId=comment,
            )

        return JsonResponse(response, safe=False, status=201)


class PostDeleteAPIView(DestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAdminUser]


class PostRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()


class PostShareRetrieveUpdateAPIView(RetrieveAPIView):
    serializer_class = PostShareSerializer
    queryset = Post.objects.all()


class PostCreateAPIView(ListCreateAPIView):
    serializer_class = PostFilterSerializer
    queryset = Post.objects.all()
    filter_backends = [OrderingFilter]
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    ordering_fields = ['created_date', 'like', 'comment_count']

    @swagger_auto_schema(operation_summary="List posts with advanced ordering")
    def get_queryset(self):
        ordering = self.request.query_params.get('ordering')

        base = Post.objects.annotate(comment_count=Count('comments'))

        if ordering:
            return base.order_by(ordering)

        likeslist = list(base.order_by('-like'))
        comment_countlist = list(base.order_by('-comment_count'))
        createdlist = list(base.order_by('-created_date'))

        finalList = []
        added = set()

        for i in range(len(base)):
            for source in [likeslist, comment_countlist, createdlist]:
                if i < len(source):
                    post = source[i]
                    if post.id not in added:
                        finalList.append(post)
                        added.add(post.id)

        return finalList

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        total = len(queryset)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response({
                "posts": serializer.data,
                "total": total
            })

        serializer = self.get_serializer(queryset, many=True)
        return Response({
            "posts": serializer.data,
            "total": total
        })

    @swagger_auto_schema(operation_summary="Create a new post")
    def create(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')

        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'message': 'Missing or Invalid Token'}, status=401)

        token = auth_header.split(' ')[1]
        user_data = get_user_form_jwt(token)

        if not user_data:
            return Response({"detail": "Invalid token"}, status=401)

        mutable_data = request.data.copy()
        mutable_data['userId'] = user_data['id']

        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response = {
            "postId": serializer.data['id'],
            "message": "Post created successfully",
            "tags": serializer.instance.tags,
            "shareLink": f"https://grammarazi.onrender.com/en/api/posts/{serializer.data['id']}"
        }

        return JsonResponse(response, safe=False, status=201)
