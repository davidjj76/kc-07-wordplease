from django.conf import settings

MAX_IMAGE_WIDTH = getattr(settings, 'MAX_IMAGE_WIDTH', 1800)
THUMBNAIL_SIZES = getattr(settings, 'THUMBNAIL_SIZES', (1200, 800, 400, 200))
