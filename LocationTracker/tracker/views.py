from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import LocationShare
import json
from django.utils import timezone


def create_link(request):
    location = LocationShare.objects.create()
    return JsonResponse({
        "link": request.build_absolute_uri(
            f"/share/{location.token}/"
        )
    })


def share_location(request, token):
    location = get_object_or_404(
        LocationShare, token=token
    )
    return render(
        request,
        'tracker/share_location.html',
        {'location': location}
    )


@require_POST
def save_location(request, token):
    location = get_object_or_404(
        LocationShare, token=token
    )

    try:
        data = json.loads(request.body)

        latitude = float(data['latitude'])
        longitude = float(data['longitude'])

        if not (-90 <= latitude <= 90):
            return JsonResponse({'error': 'Invalid latitude'}, status=400)

        if not (-180 <= longitude <= 180):
            return JsonResponse({'error': 'Invalid longitude'}, status=400)

        location.latitude = latitude
        location.longitude = longitude
        location.permission_granted = True
        location.updated_at = timezone.now()

        location.save()

        return JsonResponse({'status': 'success'})

    except (ValueError, KeyError, json.JSONDecodeError):
        return JsonResponse({'error': 'Invalid location data'}, status=400)


def dashboard(request):
    locations = LocationShare.objects.all().order_by('-updated_at')
    return render(
        request,
        'tracker/dashboard.html',
        {'locations': locations}
    )