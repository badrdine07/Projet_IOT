from rest_framework.decorators import api_view
from rest_framework import status, generics
from rest_framework.response import Response
from .models import Dht11
from .serializers import DHT11serialize
from datetime import datetime, timedelta
import pytz
import calendar  # Importer pour gérer les jours des mois

@api_view(['GET'])
def Dlist(request):
    # Get the 'timestamp' from the request
    timestamp = request.GET.get('timestamp', None)
    
    # Filter by timestamp if provided
    if timestamp:
        try:
            filtered_data = Dht11.objects.filter(timestamp=timestamp)
            if not filtered_data.exists():
                return Response({"message": "No data found for the provided timestamp."}, status=status.HTTP_404_NOT_FOUND)
        except ValueError:
            return Response({"message": "Invalid timestamp format."}, status=status.HTTP_400_BAD_REQUEST)
    else:
        filtered_data = Dht11.objects.all()  # Return all data if no timestamp is provided

    # Serialize the data
    data = DHT11serialize(filtered_data, many=True).data
    return Response({'data': data})

@api_view(['GET'])
def DlistByPeriod(request):
    # Get the period from the request
    period = request.GET.get('period', None)
    
    # Get the current date and time in UTC
    utc = pytz.UTC
    now = utc.localize(datetime.utcnow())

    # Initialize start_datetime
    start_datetime = None

    # Define the periods in hours
    if period == '6h':
        start_datetime = now - timedelta(hours=6)
    elif period == '12h':
        start_datetime = now - timedelta(hours=12)
    elif period == '24h':
        start_datetime = now - timedelta(hours=24)
    elif period == '72h':
        start_datetime = now - timedelta(hours=72)  # Corrected to 72 hours
    elif period == '168h':
        start_datetime = now - timedelta(hours=168)  # Corrected to 168 hours (7 days)
    else:
        return Response({"message": "Invalid period."}, status=status.HTTP_400_BAD_REQUEST)

    # Filter the data between start_datetime and now
    filtered_data = Dht11.objects.filter(timestamp__gte=start_datetime)

    if not filtered_data.exists():
        return Response({"message": "No data found for the provided period."}, status=status.HTTP_404_NOT_FOUND)

    # Serialize the data
    data = DHT11serialize(filtered_data, many=True).data
    return Response({'data': data})

@api_view(['GET'])
def DlistByDateRange(request):
    # Get the start and end dates from the request
    start_date_str = request.GET.get('start_date', None)
    end_date_str = request.GET.get('end_date', None)

    # Define UTC timezone
    utc = pytz.UTC

    # Initialize start_datetime and end_datetime
    start_datetime = None
    end_datetime = None

    # Check if start_date and end_date are provided in YYYY-MM format
    if start_date_str and end_date_str:
        try:
            # Parse start_date and end_date
            start_year, start_month = map(int, start_date_str.split('-'))
            end_year, end_month = map(int, end_date_str.split('-'))

            # Get the first day of the start month
            start_datetime = utc.localize(datetime(start_year, start_month, 1))

            # Get the last day of the end month
            last_day = calendar.monthrange(end_year, end_month)[1]
            end_datetime = utc.localize(datetime(end_year, end_month, last_day, 23, 59, 59))

        except ValueError:
            return Response({"message": "Invalid date format. Use YYYY-MM."}, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response({"message": "Specify both start_date and end_date in YYYY-MM format."}, status=status.HTTP_400_BAD_REQUEST)

    # Filter data between start_datetime and end_datetime
    filtered_data = Dht11.objects.filter(timestamp__gte=start_datetime, timestamp__lte=end_datetime)

    if not filtered_data.exists():
        return Response({"message": "No data found for the specified date range."}, status=status.HTTP_404_NOT_FOUND)

    # Serialize and return the data
    data = DHT11serialize(filtered_data, many=True).data
    return Response({'data': data})

class Dhtviews(generics.CreateAPIView):
    queryset = Dht11.objects.all()
    serializer_class = DHT11serialize
