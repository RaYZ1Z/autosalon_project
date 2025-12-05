from django.shortcuts import render

# Create your views here.

from rest_framework import viewsets, permissions
from rest_framework.decorators import action
from rest_framework.response import Response


class CarViewSet(viewsets.ModelViewSet):
    queryset = Car.objects.filter(status='available')
    serializer_class = CarSerializer

    @action(detail=False, methods=['get'])
    def available(self, request):
        cars = self.get_queryset()
        serializer = self.get_serializer(cars, many=True)
        return Response(serializer.data)


class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_permissions(self):
        if self.action in ['create', 'list']:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]