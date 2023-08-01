from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Guru(models.Model):
 user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
 nama = models.CharField(max_length=40, null=True, blank=True)
 nip = models.CharField(max_length=40, null=True, blank=True)
 hp = models.CharField(max_length=20, null=True, blank=True)
 foto = models.URLField(default='berkas/profil.png', max_length=250, blank=True, null=True)
 def __str__(self):
  return self.nama
 class Meta:
  verbose_name_plural = "Data Guru"

class Piket(models.Model):
 user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
 nama = models.CharField(max_length=40, null=True, blank=True)
 nip = models.CharField(max_length=40, null=True, blank=True)
 hp = models.CharField(max_length=20, null=True, blank=True)
 foto = models.URLField(default='berkas/profil.png', max_length=250, blank=True, null=True)
 def __str__(self):
  return self.nama
 class Meta:
  verbose_name_plural = "Data Piket"

class Waka(models.Model):
 user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)
 nama = models.CharField(max_length=40, null=True, blank=True)
 nip = models.CharField(max_length=40, null=True, blank=True)
 hp = models.CharField(max_length=20, null=True, blank=True)
 foto = models.URLField(default='berkas/profil.png', max_length=250, blank=True, null=True)

 def __str__(self):
  return self.nama
 class Meta:
  verbose_name_plural = "Data Waka"

class Tahun_Pelajaran(models.Model):
    tahun_pelajaran = models.CharField(max_length=10, null=True, blank=True)
    aktif = models.BooleanField(default=True)

    def __str__(self):
      return self.tahun_pelajaran


class Semester(models.Model):
    nama_semester = models.CharField(max_length=20, null=True, blank=True)
    aktif = models.BooleanField(default=True)
    
    def __str__(self):
      return self.nama_semester

class Kelas(models.Model):
    kelas = models.CharField(max_length=15, null=True, blank=True)
    
    def __str__(self):
      return self.kelas



class Jadwal(models.Model):
    HARI =(
      ('Monday', 'Senin'),
      ('Tuesday', 'Selasa'),
      ('Wednesday', 'Rabu'),
      ('Thursday', 'Kamis'),
      ('Friday', 'Jumat'),
    )

    KETERANGAN =(
      ('1', 'Jam Ke-1'),
      ('2', 'Jam Ke-2'),
      ('3', 'Jam Ke-3'),
      ('4', 'Jam Ke-4'),
      ('5', 'Jam Ke-5'),
      ('6', 'Jam Ke-6'),
      ('7', 'Jam Ke-7'),
      ('8', 'Jam Ke-8'),
    )
    
    hari = models.CharField(max_length=20, null=True, blank=True, choices=HARI)
    jam = models.TimeField(auto_now=False, auto_now_add=False)
    keterangan = models.CharField(max_length=50, null=True, blank=True, choices=KETERANGAN)
    kelas = models.ForeignKey("Kelas", null=True , on_delete=models.CASCADE)
    guru = models.ForeignKey("Guru", null=True, on_delete=models.CASCADE)
    tahun_pelajaran = models.ForeignKey("Tahun_Pelajaran", null=True, on_delete=models.CASCADE)
    semester = models.ForeignKey("Semester", null=True, on_delete=models.CASCADE)


class Presensi(models.Model):
  jadwal = models.ForeignKey("Jadwal", null=True , on_delete=models.CASCADE)
  id_guru = models.CharField(max_length=50, null=True, blank=True)
  hadir = models.CharField(max_length=20, null=True, blank=True)
  foto_guru = models.URLField(null=True, blank=True)
  pencapaian = models.CharField(max_length=500, null=True, blank=True)
  id_piket = models.CharField(default="tidak ada", max_length=50, null=True, blank=True)
  foto_piket = models.URLField(default="tidak ada", null=True, blank=True)
  tanggal_absen = models.DateTimeField(auto_now_add=True, null=True)



