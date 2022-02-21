# Listing 5.31
TEMPLATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "templates")
TEMPLATES = [
    {
        'BACKEND':
                'django.template.backends.django.DjangoTemplates', 'DIRS': [TEMPLATE_DIR,],

