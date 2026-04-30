import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE','sms_project.settings')
import django
django.setup()
from django.urls import get_resolver
resolver = get_resolver()
for p in resolver.url_patterns:
    print(p)
    try:
        print('  ->', list(p.url_patterns))
    except Exception:
        pass
