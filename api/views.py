from django.shortcuts import get_object_or_404
from rest_framework.views import Response, status
from rest_framework.decorators import api_view

from av_parser.settings import DEBUG
from .tasks import create_stat_and_top
from .models import Item, ItemHistory, Ad
from .serializers import ItemSerializer, ItemHistorySerializer, AdSerializer


@api_view(['POST'])
def add(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        query = serializer.validated_data['query']
        location = serializer.validated_data['location']
        obj, created = Item.objects.get_or_create(query=query,
                                                  location=location)
        if created:
            create_stat_and_top.delay(item=obj.id)
        return Response(obj.id, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def stat(request):
    queryset = ItemHistory.objects.all()
    pk: int = request.GET.get('id')
    start: int = request.GET.get('start')
    stop: int = request.GET.get('stop')
    if pk:
        item = get_object_or_404(Item, id=pk)
        queryset = item.history.all()
    if start:
        queryset = queryset.filter(timestamp__gte=start)
    if stop:
        queryset = queryset.filter(timestamp__lte=stop)
    serializer = ItemHistorySerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
def top(request):
    queryset = Ad.objects.all()
    pk: int = request.GET.get('id')
    if pk:
        item = get_object_or_404(Item, id=pk)
        queryset = item.ads.all()
    serializer = AdSerializer(queryset, many=True)
    return Response(serializer.data, status=status.HTTP_200_OK)
