from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from rest_framework.generics import ListCreateAPIView, RetrieveDestroyAPIView, RetrieveUpdateAPIView, RetrieveAPIView, DestroyAPIView
from rest_framework.filters import OrderingFilter
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAdminUser
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response
from blog.models import Comment, Post, Notification
from blog.api.serializers import CommentSerializer, PostSerializer, PostShareSerializer, PostFilterSerializer, NotificationSerializer
from grammar.utils import get_user_data_from_user_service
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()

class NotificationsAPIView(ListCreateAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        user_id = self.kwargs['userId']
        return Notification.objects.filter(recipient_id=user_id)
    
    def perform_create(self, serializer):
        user_data = self._get_user_data_from_token()
        recipient_user = get_object_or_404(User, pk=self.kwargs['userId'])
        serializer.save(recipient=recipient_user, sender_id=user_data['id'])

    def _get_user_data_from_token(self):
        auth_header = self.request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed("Avtorizasiya başlığı tapılmadı")
        token = auth_header.split(' ')[1]
        user_data = get_user_data_from_user_service(token)
        if not user_data:
            raise AuthenticationFailed("Token etibarsızdır")
        return user_data

class NotificationRetrieveAPIView(RetrieveDestroyAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

class CommentCreateAPIView(ListCreateAPIView):
    serializer_class = CommentSerializer
    queryset = Comment.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(postId=self.kwargs['post_id'])
    
    def perform_create(self, serializer):
        user_data = self._get_user_data_from_token()
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        serializer.save(userId_id=user_data['id'], postId=post)
    
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
            "message": "Şərh uğurla yaradıldı",
        }
        
        if recipient and user_data['id'] != recipient.id:
            Notification.objects.create(
                recipient=recipient,
                sender_id=user_data['id'],
                type=notif_type,
                commentId=comment,
            )
        
        return JsonResponse(response, safe=False, status=201)

    def _get_user_data_from_token(self):
        auth_header = self.request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed("Avtorizasiya başlığı tapılmadı")
        token = auth_header.split(' ')[1]
        user_data = get_user_data_from_user_service(token)
        if not user_data:
            raise AuthenticationFailed("Token etibarsızdır")
        return user_data

class PostDeleteAPIView(DestroyAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAdminUser]

class PostRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        user_data = self._get_user_data_from_token()
        post = self.get_object()
        old_like = post.like
        updated_post = serializer.save()
        new_like = updated_post.like

        if user_data['id'] != post.userId.id and new_like > old_like:
            Notification.objects.create(
                recipient=post.userId,
                sender_id=user_data['id'],
                type='like',
                postId=post,
            )

    def _get_user_data_from_token(self):
        auth_header = self.request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed("Avtorizasiya başlığı tapılmadı")
        token = auth_header.split(' ')[1]
        user_data = get_user_data_from_user_service(token)
        if not user_data:
            raise AuthenticationFailed("Token etibarsızdır")
        return user_data

class PostShareRetrieveUpdateAPIView(RetrieveAPIView):
    serializer_class = PostShareSerializer
    queryset = Post.objects.all()
    permission_classes = [IsAuthenticatedOrReadOnly]

class PostCreateAPIView(ListCreateAPIView):
    serializer_class = PostFilterSerializer
    queryset = Post.objects.all()
    filter_backends = [OrderingFilter]
    pagination_class = LimitOffsetPagination
    permission_classes = [IsAuthenticatedOrReadOnly]
    ordering_fields = ['created_date', 'like', 'comment_count']

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

    def create(self, request, *args, **kwargs):
        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return Response({'message': 'Avtorizasiya başlığı tapılmadı və ya etibarsızdır'}, status=401)
        
        token = auth_header.split(' ')[1]
        user_data = get_user_data_from_user_service(token)

        if not user_data:
            return Response({"detail": "Token etibarsızdır"}, status=401)
        
        mutable_data = request.data.copy()
        mutable_data['userId'] = user_data['id']

        serializer = self.get_serializer(data=mutable_data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        response = {
            "postId": serializer.data['id'],
            "message": "Post uğurla yaradıldı",
            "tags": serializer.instance.tags,
            "shareLink": f"https://grammarazi.onrender.com/en/api/posts/{serializer.data['id']}" 
        }
        
        return JsonResponse(response, safe=False, status=201)

    def perform_create(self, serializer):
        user_data = self._get_user_data_from_token()
        serializer.save(userId_id=user_data['id'])

    def _get_user_data_from_token(self):
        auth_header = self.request.headers.get('Authorization', '')
        if not auth_header.startswith('Bearer '):
            raise AuthenticationFailed("Avtorizasiya başlığı tapılmadı")
        token = auth_header.split(' ')[1]
        user_data = get_user_data_from_user_service(token)
        if not user_data:
            raise AuthenticationFailed("Token etibarsızdır")
        return user_data