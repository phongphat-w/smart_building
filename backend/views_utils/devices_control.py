from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from ..models import IoTDevice
from ..serializers import IoTDeviceSerializer

@api_view(["POST"])
def control_device(request, ):
    try:
        device = IoTDevice.objects.get(id=device_id)
        temperature = request.data.get("temperature")

        if temperature is not None:
            device.temperature = temperature
            device.save()

        serializer = IoTDeviceSerializer(device)
        return Response(serializer.data, status=status.HTTP_200_OK)

    except IoTDevice.DoesNotExist:
        return Response({"error": "Device not found"}, status=status.HTTP_404_NOT_FOUND)
