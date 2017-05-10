import os

import sys
from PIL import Image
from celery import shared_task

from blogs.settings import MAX_IMAGE_WIDTH, THUMBNAIL_SIZES


@shared_task
def resize_thumbnails_update_post_image(post_id):
    from blogs.models import Post

    try:
        post = Post.objects.get(pk=post_id)
        original_image_path = post.image.path
        new_image_name = '{0}/{1}.{2}'.format(post.get_relative_image_folder(), str(post.pk), post.get_image_extension())
        new_image_path = '{0}/{1}.{2}'.format(post.get_absolute_image_folder(), str(post.pk), post.get_image_extension())

        img = Image.open(original_image_path)
        (width, height) = img.size
        if width > MAX_IMAGE_WIDTH:
            new_height = int(MAX_IMAGE_WIDTH * height / width)
            new_img = img.resize((MAX_IMAGE_WIDTH, new_height))
            new_img.save(new_image_path)

        for size in THUMBNAIL_SIZES:
            tn_img = img.copy()
            tn_img.thumbnail((size, int(size * height / width)))
            tn_img.save('{0}/{1}_{2}.{3}'.format(
                post.get_absolute_image_folder(),
                str(post.pk),
                str(size),
                post.get_image_extension()))

        post.image.name = new_image_name
        post.save()

        os.remove(original_image_path)

    except Post.DoesNotExist:
        print('Post {0} does not exist'.format(post_id))

    except:
        print('Unexpected error:', sys.exc_info()[0])