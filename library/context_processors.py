
# from .models import FooterContent

# def footer_data(request):
#     try:
#         # footer = FooterContent.objects.first()
#         footer = FooterContent.objects.get(id=1)
#     except FooterContent.DoesNotExist:
#         footer = None
#     return {'footer_data': footer}

from .models import FooterContent

def footer_data(request):
    footer = FooterContent.objects.first()  # only one footer
    return {'footer': footer}


# library/context_processors.py

# from .models import LibrarySetting

# def library_setting(request):
#     setting = LibrarySetting.objects.first()
#     return {'library_setting': setting}

from .models import LibrarySetting

def library_settings(request):
    try:
        settings = LibrarySetting.objects.first()
    except LibrarySetting.DoesNotExist:
        settings = None
    return {'library_settings': settings}

