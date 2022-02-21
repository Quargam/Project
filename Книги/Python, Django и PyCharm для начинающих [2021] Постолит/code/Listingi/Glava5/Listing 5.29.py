# Listing 5.29
TEMPLATE_DIR = os.path.join(BASE_DIR, "templates")

TEMPLATES = [
    {
        'BACKEND':
              'django.template.backends.django.DjangoTemplates', 'DIRS': [TEMPLATE_DIR, ],