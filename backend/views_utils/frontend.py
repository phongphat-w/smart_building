import json

from django.views.decorators.csrf import csrf_exempt
from prometheus_client import Counter
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

# Define a custom counter
component_render_counter = Counter("react_component_render_count", "React component render count", ["component"])

@csrf_exempt
@permission_classes([AllowAny])  # Allow any user to register
def record_metrics(request):
    if request.method == "POST":
        data = json.loads(request.body)
        component = data.get("component", "unknown")
        value = data.get("value", 1)
        # Increment Prometheus counter
        component_render_counter.labels(component=component).inc(value)
        return Response({"status": "success"})
    return Response({"error": "Invalid method"}, status=400)
