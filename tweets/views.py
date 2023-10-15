from django.shortcuts import render, redirect
from django.http import HttpResponse, Http404, JsonResponse
from .models import Tweet
from .forms import TweetForm
from .serializers import TweetSerializer, TweetActionSerializer, TweetCreateSerializer
from django.utils.http import url_has_allowed_host_and_scheme
from django.conf import settings

from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication

ALLOWED_HOSTS = settings.ALLOWED_HOSTS


def home_view(request):
    #return HttpResponse(f"<h3> Hello </h3>")\
    return render(request, "pages/home.html", context={}, status=200)

@api_view(['GET'])
def tweet_list_view(request, *args, **kwargs):
    tweetlist = Tweet.objects.all()
    serializer = TweetSerializer(tweetlist, many=True)
    return Response(serializer.data, status=200)

@api_view(['GET'])
def tweet_detail_view(request, tweet_id, *args, **kwargs):
    tweet = Tweet.objects.filter(id=tweet_id)

    if not tweet.exists():
        return Response({}, status=404)
    obj = tweet.first()
    serializer = TweetSerializer(obj)
    return Response(serializer.data, status=200)

@api_view(['POST'])
#@authentication_classes([SessionAuthentication])
@permission_classes([IsAuthenticated])
def tweet_create_view(request, *args, **kwargs):
    serializer = TweetCreateSerializer(data=request.data)
    if serializer.is_valid(raise_exception=True):
        serializer.save(user=request.user)
        return Response(serializer.data, status=201)
    return Response({}, status=400)

@api_view(['DELETE','POST'])
@permission_classes([IsAuthenticated])
def tweet_delete_view(request, tweet_id, *args, **kwargs):
    tweet = Tweet.objects.filter(id=tweet_id)
    if not tweet.exists():
        return Response({}, status=404)
    tweet = tweet.filter(user=request.user)
    if not tweet.exists():
        return Response({"message": "You Cannot Delete This Tweet"}, status=401)#unauthorized
    obj = tweet.first()
    obj.delete()
    return Response({"message" : "Tweet Deleted"}, status=200)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def tweet_action_view(request, *args, **kwargs):
    '''
    id is required
    Actions Like , unLike , Retweet
    '''

    serializer = TweetActionSerializer(data=request.data)
    if serializer.is_valid(raise_exception = True):
        data = serializer.validated_data
        tweetId = data.get("id")
        action = data.get("action")
        content = data.get("content")
        tweet = Tweet.objects.filter(id=tweetId)
        if not tweet.exists():
            return Response({}, status=404)
        obj = tweet.first()
        if action == 'unlike':
            obj.likes.remove(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'like':
            obj.likes.add(request.user)
            serializer = TweetSerializer(obj)
            return Response(serializer.data, status=200)
        elif action == 'retweet':
            newTweet = Tweet.objects.create(
                user = request.user,
                parent= obj,
                content = content
            )
            serializer = TweetSerializer(newTweet)
            return Response(serializer.data, status=201)
    return Response({}, status=200)


def tweet_create_view_pure_django(request, *args, **kwargs):
    user = request.user
    if not user.is_authenticated:
        user = None
        if is_ajax_call(request):
            return JsonResponse({}, status=401)
        return redirect(settings.LOGIN_URL)
    form = TweetForm(request.POST or None)
    next_url = request.POST.get("next") or None
    if form.is_valid():
        obj = form.save(commit=False)
        obj.user = user
        obj.save()
        if is_ajax_call(request):
            return JsonResponse(obj.serialize(), status = 201) # 201 - created Items
        
        if next_url != None and url_has_allowed_host_and_scheme(next_url,ALLOWED_HOSTS):
            return redirect(next_url)
        form = TweetForm()
    if form.errors:
        return JsonResponse(form.errors, status=400)
    return render(request, 'components/form.html', context={"form":form})

def tweet_list_view_pure_django(request, *args, **kwargs):
    tweetlist = Tweet.objects.all()
    tweets_list = [x.serialize() for x in tweetlist]
    data = {
        "isUser": False,
        "response": tweets_list
    }
    return JsonResponse(data)

def tweet_detail_view_pure_django(request, tweet_id, *args, **kwargs):
    tweetData = { 
        "id": tweet_id
    }
    try:
        obj = Tweet.objects.get(id = tweet_id)
        tweetData['content'] = obj.content
        status = 200
    except:
        tweetData['message'] = f'{tweet_id} -  Not Found'
        status = 404
    return JsonResponse(tweetData, status=status)

def is_ajax_call(request):
    return request.headers.get('X-Requested-With') == 'XMLHttpRequest'