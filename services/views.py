import django_filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, status, permissions, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from .models import Payment
from .serializers import PaymentSerializer, PaymentStatusSerializer
from django.contrib.auth import get_user_model

User = get_user_model()


class PaymentFilter(django_filters.FilterSet):
    created_at = django_filters.DateFilter(field_name='created_at', lookup_expr='date')
    status = django_filters.ChoiceFilter(choices=Payment.STATUS_CHOICES)
    amount = django_filters.NumberFilter()

    class Meta:
        model = Payment
        fields = ['amount', 'status', 'created_at']


class PaymentViewSet(mixins.ListModelMixin, mixins.CreateModelMixin,
                     mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Payment.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = PaymentFilter

    def get_permissions(self):
        if self.action in ('list', 'retrieve'):
            return permissions.IsAuthenticated(),
        return permissions.AllowAny(),

    def get_serializer_class(self):
        if self.action in ('status', 'cansel'):
            return PaymentStatusSerializer
        return PaymentSerializer

    @action(detail=True, methods=['get'])
    def status(self, request, pk=None):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'status': payment.status})

    @action(detail=True, methods=['post'])
    def cancel(self, request, pk=None):
        try:
            payment = Payment.objects.get(pk=pk)
        except Payment.DoesNotExist:
            return Response({'error': 'Payment not found'}, status=status.HTTP_404_NOT_FOUND)
        if payment.status not in ['completed', 'cancelled']:
            payment.status = 'cancelled'
            payment.save()
            return Response({'status': 'Payment cancelled'}, status=status.HTTP_200_OK)
        return Response({'error': 'Cannot cancel this payment'}, status=status.HTTP_400_BAD_REQUEST)
