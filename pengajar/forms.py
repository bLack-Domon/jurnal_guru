from django import forms
from django.forms import ModelForm
from . models import *

class GuruForm(ModelForm):
 class Meta:
  model = Guru
  fields = ['nama', 'nip', 'hp']
  widgets = {
   'nama' : forms.TextInput(attrs={
    'required': True,
    'autofocus': True,
    'class': 'form-control mb-2',
    'placeholder' : 'Nama Lengkap'
   }),

   'nip': forms.TextInput(attrs={
    'required': True,
    'class': 'form-control mb-2',
    'placeholder': 'NISP'
   }),
   'hp': forms.TextInput(attrs={
    'required': True,
    'class': 'form-control mb-2',
    'placeholder': 'No.hp'
   })
  }
  label = {
   "nama": "Nama Lengkap",
   "nip": "Nip",
   "hp": "No.hp",
  }

class PiketForm(ModelForm):
 class Meta:
  model = Piket
  fields = ['nama', 'nip', 'hp']
  widgets = {
   'nama' : forms.TextInput(attrs={
    'required': True,
    'autofocus': True,
    'class': 'form-control mb-2',
    'placeholder' : 'Nama Lengkap'
   }),

   'nip': forms.TextInput(attrs={
    'required': True,
    'class': 'form-control mb-2',
    'placeholder': 'NISP'
   }),
   'hp': forms.TextInput(attrs={
    'required': True,
    'class': 'form-control mb-2',
    'placeholder': 'No.hp'
   })
  }
  label = {
   "nama": "Nama Lengkap",
   "nip": "Nip",
   "hp": "No.hp",
  }

class WakaForm(ModelForm):
 class Meta:
  model = Waka
  fields = ['nama', 'nip', 'hp']
  widgets = {
   'nama' : forms.TextInput(attrs={
    'required': True,
    'autofocus': True,
    'class': 'form-control mb-2',
    'placeholder' : 'Nama Lengkap'
   }),

   'nip': forms.TextInput(attrs={
    'required': True,
    'class': 'form-control mb-2',
    'placeholder': 'NISP'
   }),
   'hp': forms.TextInput(attrs={
    'required': True,
    'class': 'form-control mb-2',
    'placeholder': 'No.hp'
   })
  }
  label = {
   "nama": "Nama Lengkap",
   "nip": "Nip",
   "hp": "No.hp",
  }

class JadwalForm(ModelForm):
    class Meta:
      model = Jadwal
      fields = '__all__'
      widgets = {
        'hari': forms.Select(attrs={
        'required': True,
        'autofocus': True,
        'class': 'form-control mb-2',
        }),
        'jam': forms.TextInput(attrs={
        'required': True,
        'class': 'form-control mb-2',
        'type': 'time',
        }),
        'keterangan': forms.Select(attrs={
        'required': True,
        'class': 'form-control mb-2',
        }),
        'kelas': forms.Select(attrs={
        'required': True,
        'class': 'form-control mb-2',
        }),
        'guru': forms.Select(attrs={
        'required': True,
        'class': 'form-control mb-2',
        }),
        'tahun_pelajaran': forms.Select(attrs={
        'required': True,
        'class': 'form-control mb-2',
        }),
        'semester': forms.Select(attrs={
        'required': True,
        'class': 'form-control mb-2',
        }),
        
      }
      labels = {
        "hari" : "Hari",
        "jam" : "Jam Pelajaran",
        "keterangan" : "Keterangan Jam-ke",
        "kelas" : "Kelas",
        "guru" : "Nama Guru",
        "tahun pelajaran" : "Tahun Pelajaran",
        "Semester" : "Semester",
      }



