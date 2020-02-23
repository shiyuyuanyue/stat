import numpy
from django.test import TestCase

# Create your tests here.
import os
import django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "stocks_tools.settings")# project_name 项目名称
django.setup()

from tools.models import Tools



datas = Tools.objects.filter(code='601939')
list_data = []
for data in datas:
    list_data.append(data.close)
list01 = numpy.array(list_data).reshape(-1,1)
print(list01)
