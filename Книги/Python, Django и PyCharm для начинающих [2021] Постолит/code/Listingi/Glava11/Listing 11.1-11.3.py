# Listing 11.1
# Чтение SECRET_KEY из переменной окружения
import os

SECRET_KEY = os.environ['SECRET_KEY']
# ИЛИ чтение ключа из файла
with open('/etc/secret_key.txt') as f:
    SECRET_KEY = f.read().strip()

# Listing 11.2
# SECURITY WARNING: keep the secret key used in production secret!
# SECRET_KEY = 'dhp40_!05cp071e9pd5e5+3_90fev*vq-obx^3^hv8cx0=l#!k'

import os

SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', 'cg#p$g+j9tax!#a3cup@1$8obt2_+&k3q+pmu)5%asj6yjpkag')

# Listing 11.3
# SECURITY WARNING: don't run with debug turned on in production!
# DEBUG = True
DEBUG = bool(os.environ.get('DJANGO_DEBUG', True))


