from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, mixins, status
from rest_framework.generics import ListCreateAPIView, UpdateAPIView
from rest_framework.parsers import JSONParser, MultiPartParser
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from drfapi import serializers
from drfapi.filters import OrderFilterView
from drfapi.models import Customer, Product, Order


# Create your views here.
class BaseApiView(mixins.RetrieveModelMixin, mixins.CreateModelMixin, mixins.UpdateModelMixin,
                  generics.GenericAPIView):
    pass


class CustomerListCreateAPIView(ListCreateAPIView):
    model = Customer
    permission_classes = (AllowAny,)
    serializer_classes = {}
    default_serializer_class = serializers.CustomerModelSerializer
    parser_classes = (JSONParser, MultiPartParser)

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method, self.default_serializer_class)

    def get(self, request, *args, **kwargs):
        self.queryset = self.model.objects.all().order_by('-created_at')
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CustomerUpdateAPIView(UpdateAPIView):
    queryset = Customer.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = serializers.CustomerModelSerializer
    parser_classes = (JSONParser, MultiPartParser)

    def put(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductListCreateAPIView(ListCreateAPIView):
    queryset = Product.objects.all().order_by('-created_at')
    serializer_class = serializers.ProductModelSerializer
    permission_classes = (AllowAny,)
    parser_classes = (JSONParser, MultiPartParser)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderListCreateAPIView(ListCreateAPIView):
    queryset = Order.objects.all().order_by('-created_at')
    permission_classes = (AllowAny,)
    serializer_classes = {
        'GET': serializers.ListAllOrderModelSerializer
    }
    default_serializer_class = serializers.OrderModelSerializer
    parser_classes = (JSONParser, MultiPartParser)
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = OrderFilterView

    def get_serializer_class(self):
        return self.serializer_classes.get(self.request.method, self.default_serializer_class)

    def get(self, request, *args, **kwargs):
        filter_queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(filter_queryset, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
