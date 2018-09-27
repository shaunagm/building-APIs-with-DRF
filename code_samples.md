This document contains the code samples displayed after each segment of the training.

# 1. Creating a Serializer

In `serializers.py`:

```python
from rest_framework import serializers

class ArticleSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField(max_length=100)
    content = serializers.CharField(max_length=5000, required=False, allow_blank=True)
    datetime_created = serializers.DateTimeField(read_only=True)
    published = serializers.BooleanField()
    datetime_published = serializers.DateTimeField(allow_null=True)

    def create(self, validated_data):
        return Article.objects.create(**validated_data)

    def update(self, instance, validated_data):
    	instance.title = validated_data.get('title', instance.title)
    	instance.content = validated_data.get('content', instance.content)
    	instance.published = validated_data.get('published', instance.published)
    	instance.datetime_published = validated_data.get('datetime_published', instance.datetime_published)
    	instance.save()
    	return instance   
```

Using the serializer in the shell:

```python
from blog.models import Article
from blog.serializers import ArticleSerializer
article1 = Article.objects.first()
serialized_article = ArticleSerializer(article1)
```

You should now be able to access the serialized data using `serialized_article.data`.

Rendering the data:

```python
from rest_framework.renderers import JSONRenderer
rendered_data = JSONRenderer().render(serialized_article.data)
```

Parsing data back into the database:

```python
from django.utils.six import BytesIO
new_content = rendered_data
stream = BytesIO(new_content)
from rest_framework.parsers import JSONParser
data = JSONParser().parse(stream)
serializer = ArticleSerializer(data=data, many=True)
serializer.is_valid()
serializer.save()
```

# 2. Creating a Model Serializer

In `serializers.py`:

```python
from .models import Article

class ArticleSerializer(serializers.ModelSerializer):

	class Meta:
    	model = Article
    	fields = ('id', 'title', 'content', 'datetime_created', 'published', 'datetime_published')
```

# 3. Creating a Basic API View

In `views.py`:

```python
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Article
from .serializers import ArticleSerializer

class ArticleList(APIView):

    def get(self, request):	
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
```

In `urls.py`:

```python
urlpatterns = [
	url(r'^articles$', views.ArticleList.as_view()),
]
```

# 4. More HTTP Methods - POST

In `views.py`:

```python
from rest_framework import status

class ArticleList(APIView):

    def get(self, request):	
        articles = Article.objects.all()
        serializer = ArticleSerializer(articles, many=True)
        return Response(serializer.data)
	
    def post(self, request):
        serializer = ArticleSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

# 5. More HTTP Methods - Put & Delete

In `urls.py`:

```python
urlpatterns = [
	url(r'^articles$', views.ArticleList.as_view()),
    url(r'^(?P<pk>[0-9]+)/$', views.ArticleDetail.as_view()),
]
```

In `views.py`:

```python
from django.http import Http404

class ArticleDetail(APIView):

    def get_object(self, pk):
        try:
            return Article.objects.get(pk=pk)
        except Article.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        article = self.get_object(pk)
        serializer = ArticleSerializer(article)
        return Response(serializer.data)

    def put(self, request, pk):
    	article = self.get_object(pk)
    	serializer = ArticleSerializer(article, data=request.data, partial=True)
    	if serializer.is_valid():
        	serializer.save()
        	return Response(serializer.data)
    	return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
    	article = self.get_object(pk)
    	article.delete()
    	return Response(status=status.HTTP_204_NO_CONTENT) 
```

# 6. Generic Views

In `views.py`:

```python
from rest_framework import generics

class ArticleList(generics.ListCreateAPIView):
	queryset = Article.objects.all()
	serializer_class = ArticleSerializer

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        print("We created an article with title: ", request.data['title'])
        return response

class ArticleList(generics.RetrieveUpdateDestroyAPIView):
	queryset = Article.objects.all()
	serializer_class = ArticleSerializer
```

# 7. Viewsets

In `views.py`:

```python
import datetime
from rest_framework import viewsets

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer

    def create(self, request):
        response = super().create(request)
        print("We created an article with title: ", request.data['title'])
        return response

    @action(methods=["put", "patch"], detail=True)
    def publish_article(self, request, pk=None):
        article = self.get_object()
        serializer = ArticleSerializer(data=request.data, partial=True)
        if serializer.is_valid() and serializer.validated_data['published'] == True:
            article.published = True
            article.datetime_published = datetime.datetime.now()
            article.save()
            return Response({'status': 'post published'})
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
```

In `urls.py`:

```python
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet, base_name='articles')
urlpatterns = router.urls
```

# 8. Building an Author API

In `serializers.py`:

```python
from .models import Article, Author

class AuthorSerializer(serializers.ModelSerializer):

    class Meta:

        model = Author
        fields = ('user', 'name', 'bio')
```

In `views.py`:

```python
from rest_framework import mixins

class AuthorViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, 
    mixins.UpdateModelMixin, mixins.DestroyModelMixin, viewsets.GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
```

In `urls.py`:

```python
router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet, base_name='articles')
router.register(r'authors', views.AuthorViewSet, base_name='authors')
urlpatterns = router.urls
```

# 9. Related Fields & Nested Serializers

In `serializers.py`:

```python
class AuthorSerializer(serializers.ModelSerializer):

    class Meta:
        model = Author
        fields = ('user', 'name', 'bio', 'article_set')

class ArticleSerializer(serializers.ModelSerializer):
    author = AuthorSerializer()

    class Meta:
        model = Article
        fields = ('id', 'title', 'content', 'datetime_created', 'published', 
            'datetime_published', 'author')

    def create(self, validated_data):
        author = Author.objects.create(**validated_data.pop('author'))
        article = Article.objects.create(author=author, **validated_data)
        return article
```

# 10. Requiring a Login

In `urls.py`:

```python
from django.conf.urls import include

router = DefaultRouter()
router.register(r'articles', views.ArticleViewSet, base_name='articles')
router.register(r'authors', views.AuthorViewSet, base_name='authors')
urlpatterns = router.urls

urlpatterns += [
    url(r'^api-auth/', include('rest_framework.urls')),
]
```

In `views.py`:

```python
from rest_framework import permissions

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    ...
```

# 11. Custom Permissions

In `permissions.py`:

```python
from rest_framework import permissions

class IsAuthorOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author.user == request.user
```

In `views.py`:

```python
from .permissions import IsAuthorOrReadOnly

class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly,)
```

# 12. Rate Limiting

In `settings.py`:

```python
REST_FRAMEWORK = {
    'DEFAULT_THROTTLE_CLASSES': (
        'rest_framework.throttling.AnonRateThrottle',
        'rest_framework.throttling.UserRateThrottle',
        'blog.throttles.BurstRateThrottle',
        'rest_framework.throttling.ScopedRateThrottle',
    ),
    'DEFAULT_THROTTLE_RATES': {
        'anon': '100/day',
        'user': '1000/day',
        'burst': '100/hour',
        'articles': '50/hour'
    }
}
```

In `throttles.py`:

```python
from rest_framework.throttling import UserRateThrottle

class BurstRateThrottle(UserRateThrottle):
    scope = 'burst'
```

In `views.py`:

```python
class ArticleViewSet(viewsets.ModelViewSet):
    queryset = Article.objects.all()
    serializer_class = ArticleSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsAuthorOrReadOnly)
    throttle_scope = 'articles'
```
