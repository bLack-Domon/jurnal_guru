import django_filters
from . models import *

class JadwalFilter(django_filters.FilterSet):
 tahun_pelajaran = django_filters.ModelChoiceFilter(
  queryset=Tahun_Pelajaran.objects.filter(aktif=True),
  field_name ='tahun_pelajaran',
  label= 'Tahun Pelajaran'
 )
 class Meta:
  model = Jadwal
  fields = ['tahun_pelajaran', 'semester']
