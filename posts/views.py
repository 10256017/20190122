from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action 
from rest_framework.permissions import IsAuthenticated #權限控制, SAFE_METHODS 
from rest_framework import status
from rest_framework import mixins

from .models import Post, Commit
from .permissions import IsCreatorOrReadOnly#, CanUpdateOrDeleteCommit
from .serializers import PostSerializer, CommitsSerializer #, CreatePostSerializer

#貼文
class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer #使用者用GET打進來會給他PostSerializer(只有讀，對資料庫沒有異動(安全))
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]  #只有登入者可以增加文章,只有所有者可以對自己的文章進行異動

    #複寫 get_serializer_class 把驗證欄位抽開
    #serializer擋下creator
    # def get_serializer_class(self):
    #     serializer = super().get_serializer_class()
    #     if self.request.method not in SAFE_METHODS:
    #         return CreatePostSerializer

    #     return serializer
    #與上方相同，但方法較複雜
    # def get_serializer(self, *args, **kwargs):
    #     if self.request.method in SAFE_METHODS:
    #         return CreatePostSerializer(*args, **kwargs)

    #     return super().get_serializer(*args, **kwargs)

    #建立文章
    def perform_create(self, serializer):
        serializer.save(creator = self.request.user) #在存檔之前，拿到目前登入的user

    def get_serializer_class(self):
        serializer = super().get_serializer_class()

        if self.action == 'commit':
            return CommitsSerializer

        if self.action == 'like':
            return Serializer

        return serializer

    #貼文按讚
    @action(['PATCH'], True, permission_classes=[IsAuthenticated])    #會產生 /posts/<pk>/like (url)
    def like(self, request, pk):
        post = self.get_object()    #用傳進來的pk去抓對應的物件,會擋下不存在的

        #對同一個user對同意篇文按讚多次會取消(第一次是讚,第二次是取消)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
        else:
            post.likes.add(request.user)

        serializer = self.get_serializer(post)  #資料傳輸都要經過序列化
        return Response(serializer.data)
    
    #留言
    @action(['POST'], True, permission_classes=[IsAuthenticated])
    def commit(self, request, pk):
        post = self.get_object()    #取得POST
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)   #驗證user送進來的資料合不合法，
        serializer.save(creator=self.request.user, post=post)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)    #回傳狀態

#留言
class CommitViewSet(mixins.UpdateModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.ReadOnlyModelViewSet):
    queryset = Commit.objects.all()
    serializer_class = CommitsSerializer 
    permission_classes = [IsAuthenticated, IsCreatorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(creator = self.request.user) 

    def get_serializer_class(self):
        serializer = super().get_serializer_class()
        
        if self.action == 'like':
            return Serializer

        return serializer

    #按讚
    @action(['PATCH'], True, permission_classes=[IsAuthenticated])
    def like(self, request, pk):
        commit = self.get_object()

        if request.user in commit.likes.all():
            commit.likes.remove(request.user)
        else:
            commit.likes.add(request.user)

        serializer = self.get_serializer(commit)  #資料傳輸都要經過序列化
        return Response(serializer.data)


