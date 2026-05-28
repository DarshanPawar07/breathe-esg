from django.contrib import admin

from django.urls import path, include

from django.conf import settings

from django.conf.urls.static import (
    static
)

from django.http import JsonResponse


# ─────────────────────────────────────
# ROOT API CHECK
# ─────────────────────────────────────

def api_home(request):

    return JsonResponse({

        'message':
            'Breathe ESG API Running'
    })


# ─────────────────────────────────────
# URL PATTERNS
# ─────────────────────────────────────

urlpatterns = [

    # Admin

    path(
        'admin/',
        admin.site.urls
    ),

    # Root API check

    path(
        'api/',
        api_home
    ),

    # Core APIs

    path(
        'api/',
        include('core.urls')
    ),
]


# ─────────────────────────────────────
# MEDIA FILES
# ─────────────────────────────────────

urlpatterns += static(

    settings.MEDIA_URL,

    document_root=settings.MEDIA_ROOT
)

urlpatterns = [

    # ─────────────────────────────
    # ADMIN
    # ─────────────────────────────

    path(
        'admin/',
        admin.site.urls
    ),

    # ─────────────────────────────
    # ROOT API CHECK
    # ─────────────────────────────

    path(
        'api/',
        api_home
    ),

    # ─────────────────────────────
    # CORE APIs
    # ─────────────────────────────

    path(
        'api/',
        include('core.urls')
    ),
]


# ─────────────────────────────
# MEDIA FILES
# ─────────────────────────────

urlpatterns += static(

    settings.MEDIA_URL,

    document_root=settings.MEDIA_ROOT
)