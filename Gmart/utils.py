from django.conf import settings
from django.core.cache import cache
from wagtail.images.models import Image
from wagtail.rich_text import RichText
from bs4 import BeautifulSoup

# from noorcapital.constants import FRONTEND_FOLDERS, API_URLS

def get_rich_text_content(content, request):   
    if not content:
        return None

    # Ensure content is a string
    if isinstance(content, RichText):
        content = str(content)

    if not request: 
        return content  # or raise an exception if request is required

    soup = BeautifulSoup(content, 'html.parser')
    for img_tag in soup.find_all('img'):
        src = img_tag.get('src')
        if src:
            img_tag['src'] = request.build_absolute_uri(src)

    return str(soup)

def get_image_rendition(image, rendition_spec, cache_timeout=3600):   
    if not image:
        return None
    
    if image.file.name.endswith('.gif'):
        full_url = settings.BASE_URL + image.file.url
        data = {
                "url": full_url,
                "full_url": full_url,
                "width": None,
                "height": None,
                "alt": image.title
            }
        return data
    cache_key = f"image_{image.id}_{rendition_spec}"
    data = cache.get(cache_key)
    # print(cache_key,"---data--------------------------------",cache_timeout)
    if not data:
        try:
                       
            rendition = image.get_rendition(rendition_spec) 
            full_url = settings.BASE_URL + rendition.url
            data = {
                "url": full_url,#rendition.url,
                "full_url": full_url,
                "width": rendition.width,
                "height": rendition.height,
                "alt": image.title
            }
            cache.set(cache_key, data, timeout=cache_timeout)  # Cache for specified timeout
        except Exception as e:
            print(f"Error generating image rendition ({rendition_spec}):", e)
            return None
    return data

# def get_frontend_folder(key):
#     for item in FRONTEND_FOLDERS:
#         if item[0] == key:
#             return item[1]
#     return None  # Return None if the key is not found