from django.shortcuts import render, redirect
from . models import *
from . forms import *
from django.contrib.auth.models import User
from django.contrib.auth.models import Group
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . decorators import *
from tablib import Dataset
from . resources import *
from django.core.files.storage import FileSystemStorage
from datetime import datetime
import dateutil.parser
from .filters import JadwalFilter

# Create your views here.
@tolakhalaman_ini
def loginF(request):
  form = AuthenticationForm
  if request.method =='POST':
    username = request.POST.get('username')
    password = request.POST.get('password')
    cek_data = authenticate(request, username=username, password=password)
    if cek_data is not None:
      login(request, cek_data)
      return redirect('Admin')
    else:
      messages.error(request, 'Username atau Password anda salah')
      return redirect('loginU')
  else:
    Dewi = {
      'judul' : 'Jurnal Pengajar | LOGIN',
      'login': form,
    }
    return render(request, 'loren/login.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["pengajar"])
def profilGuru(request):
  hadir = Presensi.objects.filter(id_guru=request.user.id, hadir='H').exclude(foto_piket='tidak ada').count()
  izin = Presensi.objects.filter(id_guru=request.user.id, hadir='I').exclude(foto_piket='tidak ada').count()
  lambat = Presensi.objects.filter(id_guru=request.user.id, hadir='T').exclude(foto_piket='tidak ada').count()
  data = Guru.objects.get(user_id=request.user.id)
  sandi = request.POST.get('password')

  if sandi == "":
    if request.method == "POST":
      username = request.POST.get('username')
      user = User.objects.get(id=request.user.id)
      user.username=username
      user.save()

      id = request.POST.get('id_guru')
      nama = request.POST.get('nama')
      nip = request.POST.get('nip')
      hp = request.POST.get('hp')
      foto = request.POST.get('foto')
      userid = request.POST.get('user_id')

      data = Guru(
        id = id,
        nama = nama,
        nip = nip,
        hp = hp,
        foto = foto,
        user_id = userid,
      )

      data.save()
      return redirect('ProfilGuru')
  else:
    if request.method == "POST":
      username = request.POST.get("username")
      password1 = request.POST.get("password")
      password2 = request.POST.get("password2")

      if password1 != password2:
        messages.warning(request, "password tidak sama!")
        return redirect("ProfilGuru")

      user = User.objects.get(id=request.user.id)
      user.username=username
      user.set_password(password1)
      user.save()

      id = request.POST.get('id_guru')
      nama = request.POST.get('nama')
      nip = request.POST.get('nip')
      hp = request.POST.get('hp')
      foto = request.POST.get('foto')
      userid = request.POST.get('user_id')

      data = Guru(
      id = id,
      nama = nama,
      nip = nip,
      hp = hp,
      foto = foto,
      user_id = userid,
      )
      data.save()
      return redirect('ProfilGuru')
  Dewi = {
    'data'  : data,
    'hadir' : hadir,
    'izin' : izin,
    'lambat' : lambat,
  }
  return render(request, 'guru/profilGuru.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["pengajar"])
def jurnalMengajar(request):
  harini = datetime.today()
  hari = harini.strftime('%A')
  jadwal_pel = request.user.guru.jadwal_set.filter(hari=hari)
  Dewi = {
    'judul' : 'Jurnal Mengajar',
    'jadwalP': jadwal_pel,
    'cekhari': hari,
  }
  return render(request, 'guru/jurnalMengajar.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["pengajar"])
def rekap (request):
  rekap = Presensi.objects.all().exclude(foto_piket='tidak ada', id_piket='tidak ada')
  Dewi = {
    'judul' : 'Rekapan',
    'rekap' : rekap,
  }
  return render(request, 'guru/rekap.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["pengajar"])
def absenG (request, id):
  time = datetime.now().time()
  jl = Jadwal.objects.get(id=id)
  status =request.POST.get('hadir')

  if status == "I":
    if request.method == 'POST' and request.FILES['foto']:
      jadwal = request.POST.get('jadwal_id')
      guru = request.POST.get('id_guru')
      hadir = request.POST.get('hadir')
      capai = request.POST.get('pencapaian')

      file = request.FILES['foto']
      fs = FileSystemStorage()
      filename = fs.save(file.name, file)
      url = fs.url(filename)

      simpan = Presensi(
        hadir = hadir,
        foto_guru = url,
        pencapaian = capai,
        jadwal_id = jadwal,
        id_guru = guru,
      )
      simpan.save()
      return redirect('JurnalMengajar')
  else:
    if request.method == 'POST' and request.FILES['foto']:
      if time <= jl.jam:
        status = 'H'
        capai = request.POST.get('pencapaian')
        jadwal = request.POST.get('jadwal_id')
        guru = request.POST.get('id_guru')

        file = request.FILES['foto']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        url = fs.url(filename)

        simpan = Presensi(
          hadir = status,
          foto_guru = url,
          pencapaian = capai,
          jadwal_id = jadwal,
          id_guru = guru,
        )
        simpan.save()
        return redirect('JurnalMengajar')
      else: 
        # Terlambat (T)
        status = 'T'
        capai = request.POST.get('pencapaian')
        jadwal = request.POST.get('jadwal_id')
        guru = request.POST.get('id_guru')

        file = request.FILES['foto']
        fs = FileSystemStorage()
        filename = fs.save(file.name, file)
        url = fs.url(filename)

        simpan = Presensi(
          hadir = status,
          foto_guru = url,
          pencapaian = capai,
          jadwal_id = jadwal,
          id_guru = guru,
        )
        simpan.save()
        return redirect('JurnalMengajar')
  Dewi = {
    'judul':  'Absen Guru',
    'jadwal' : jl,
  }
  return render(request, 'guru/absen.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["piket"])
def profilPiket (request):
  belumdicek = Presensi.objects.filter(foto_piket='tidak ada', id_piket='tidak ada').count()
  data = Piket.objects.get(user_id=request.user.id)
  sandi = request.POST.get('password')

  if sandi == "":
    if request.method == "POST":
      username = request.POST.get('username')
      user = User.objects.get(id=request.user.id)
      user.username=username
      user.save()

      id = request.POST.get('id_piket')
      nama = request.POST.get('nama')
      nip = request.POST.get('nip')
      hp = request.POST.get('hp')
      foto = request.POST.get('foto')
      userid = request.POST.get('user_id')

      data = Piket(
        id = id,
        nama = nama,
        nip = nip,
        hp = hp,
        foto = foto,
        user_id = userid,
      )

      data.save()
      return redirect('ProfilPiket')
  else:
    if request.method == "POST":
      username = request.POST.get("username")
      password1 = request.POST.get("password")
      password2 = request.POST.get("password2")

      if password1 != password2:
        messages.warning(request, "password tidak sama!")
        return redirect("ProfilPiket")

      user = User.objects.get(id=request.user.id)
      user.username=username
      user.set_password(password1)
      user.save()

      id = request.POST.get('id_piket')
      nama = request.POST.get('nama')
      nip = request.POST.get('nip')
      hp = request.POST.get('hp')
      foto = request.POST.get('foto')
      userid = request.POST.get('user_id')

      data = Piket(
      id = id,
      nama = nama,
      nip = nip,
      hp = hp,
      foto = foto,
      user_id = userid,
      )
      data.save()
      return redirect('ProfilPiket')
  Dewi = {
    'data'  : data,
    'belum' : belumdicek,
  }
  return render(request, 'piket/profilPiket.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["piket"])
def Cekjurnal (request):
  cekjur = Presensi.objects.filter(foto_piket='tidak ada', id_piket='tidak ada')
  Dewi = {
    'judul' : 'Rekapan',
    'data' : cekjur,
  }
  return render(request, 'piket/cekJurnal.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["piket"])
def Dokumentasi (request):
  tanggal_absen = request.POST.get('tanggal_absen')
  tanggal = dateutil.parser.parse(tanggal_absen)

  if request.method == 'POST' and request.FILES['foto']:
    id = request.POST.get('id_absen')
    hadir = request.POST.get('hadir')
    foto_guru = request.POST.get('foto_guru')
    pencapaian = request.POST.get('pencapaian')
    jadwal_id = request.POST.get('jadwal_id')
    id_guru = request.POST.get('id_guru')
    id_piket = request.POST.get('id_piket')

    file = request.FILES['foto']
    fs = FileSystemStorage()
    filename = fs.save(id_guru+id_piket+tanggal_absen, file)
    url = fs.url(filename)

    simpan = Presensi(
      id = id,
      hadir = hadir,
      foto_guru = foto_guru,
      pencapaian = pencapaian,
      jadwal_id = jadwal_id,
      tanggal_absen = tanggal,
      id_guru = id_guru,
      foto_piket = url,
      id_piket = id_piket,
    )
    simpan.save()
    return redirect('CekJurnalMengajar')
  return render(request, 'piket/cekJurnal.html')

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["piket"])
def rekapPiket (request):
  rekap = Presensi.objects.all().exclude(foto_piket='tidak ada', id_piket='tidak ada')
  guru_piket = Piket.objects.get(user_id=request.user.id)
  Dewi = {
    'judul' : 'Rekapan',
    'rekap' : rekap,
    'piket' : guru_piket,
  }
  return render(request, 'piket/rekapPiket.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["wakakurikulum"])
def profilWaka (request):
  uPiket = User.objects.filter(groups='4').count()
  uGuru = User.objects.filter(groups='3').count()
  data = Waka.objects.get(user_id=request.user.id)
  sandi = request.POST.get('password')

  if sandi == "":
    if request.method == "POST":
      username = request.POST.get('username')
      user = User.objects.get(id=request.user.id)
      user.username=username
      user.save()

      id = request.POST.get('id_waka')
      nama = request.POST.get('nama')
      nip = request.POST.get('nip')
      hp = request.POST.get('hp')
      foto = request.POST.get('foto')
      userid = request.POST.get('user_id')

      data = Waka(
        id = id,
        nama = nama,
        nip = nip,
        hp = hp,
        foto = foto,
        user_id = userid,
      )

      data.save()
      return redirect('ProfilWaka')
  else:
    if request.method == "POST":
      username = request.POST.get("username")
      password1 = request.POST.get("password")
      password2 = request.POST.get("password2")

      if password1 != password2:
        messages.warning(request, "password tidak sama!")
        return redirect("ProfilWaka")

      user = User.objects.get(id=request.user.id)
      user.username=username
      user.set_password(password1)
      user.save()

      id = request.POST.get('id_waka')
      nama = request.POST.get('nama')
      nip = request.POST.get('nip')
      hp = request.POST.get('hp')
      foto = request.POST.get('foto')
      userid = request.POST.get('user_id')

      data = Waka(
      id = id,
      nama = nama,
      nip = nip,
      hp = hp,
      foto = foto,
      user_id = userid,
      )
      data.save()
      return redirect('ProfilWaka')
  Dewi = {
    'piket' : uPiket,
    'guru' : uGuru,
    'data'  : data,
  }
  return render(request, 'waka/profilwaka.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["wakakurikulum"])
def Penjadwalan (request):
  guru = Guru.objects.all()
  jadwal = Jadwal.objects.all()
  form = JadwalForm()
  filter_jadwal = JadwalFilter(request.GET, queryset=jadwal)
  jadwal=filter_jadwal.qs

  if request.method == 'POST':
    jadwal_r = JadwalResources()
    data = Dataset()
    jadwal_baru = request.FILES['file']
    imported_data = data.load(jadwal_baru.read(), format = 'xlsx')


    for data in imported_data:
      hari = data[0]
      jam = data[1]
      keterangan = data[2]
      kelas_id = data[3]
      guru_id = data[4]
      semester_id = data[5]
      tahun_pelajaran_id = data[6]
      guru = Guru.objects.get(id=guru_id)
      kelas = Kelas.objects.get(id=kelas_id)
      semester = Semester.objects.get(id=semester_id)
      tahun_pelajaran = Tahun_Pelajaran.objects.get(id=tahun_pelajaran_id)
      
      simpan = Jadwal(
        hari = hari,
        jam = jam,
        keterangan = keterangan,
        kelas = kelas,
        guru = guru,
        semester = semester,
        tahun_pelajaran = tahun_pelajaran
      )
      simpan.save()

      
  Dewi = {
    'judul' : 'Penjadwalan',
    'jadwalhtml' : jadwal,
    'guru' : guru,
    'form': form,
    'filter_jadwal': filter_jadwal,
  }
  return render(request, 'waka/penjadwalan.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["wakakurikulum"])
def TambahJ (request):
  form = JadwalForm()
  if request.method == "POST":
    simpan = JadwalForm(request.POST)
    if simpan.is_valid:
      simpan.save()
      messages.warning(request, "Data berhasil di tambahkan...")
      return redirect('Jadwal')
  Dewi = {
    'form' : form,
  }
  return render(request, 'waka/penjadwalan.html', Dewi)

  
@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["wakakurikulum"])
def idKode (request):
  tp = Tahun_Pelajaran.objects.all()
  s = Semester.objects.all()
  k = Kelas.objects.all()
  Dewi = {
    'tahun': tp,
    'semester': s,
    'kelas' : k,
  }
  return render(request, 'waka/idKode.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["wakakurikulum"])
def daftarGuru (request):
  dg = Guru.objects.all()
  dgp = Piket.objects.all()
  Dewi = {
    'judul' : 'Daftar pengajar dan guru piket',
    'dghtml': dg, 
    'dgphtml' : dgp, 
  }
  return render(request, 'waka/daftarguru.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["wakakurikulum"])
def absensiKinerja (request):
  rekap = Presensi.objects.all().exclude(foto_piket='tidak ada', id_piket='tidak ada')
  Dewi = {
    'judul' : 'Absensi Kinerja Guru',
    'kinerja' : rekap,
  }
  return render(request, 'waka/absensikinerja.html', Dewi)


@login_required(login_url='loginU')
@pilihan_login
def admiN (request):
  uAdmin = User.objects.filter(groups='1').count()
  uWaka = User.objects.filter(groups='2').count()
  uPiket = User.objects.filter(groups='4').count()
  uGuru = User.objects.filter(groups='3').count()
  Dewi = {
    'judul':  'admin | Jurnal-Pengajar',
    'admin' : uAdmin,
    'waka' : uWaka,
    'piket' : uPiket,
    'guru' : uGuru,
  }
  return render(request, 'admin/profiladmin.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def TambahP (request):
  #ambil dari database di model Guru
  gr = Guru.objects.all()
  #ambil dari form.py
  form = GuruForm()
  formGuru = GuruForm(request.POST)
  fotokosong = request.POST.get('foto')
  if fotokosong =='':
    if request.method == 'POST':
      username = request.POST.get("username")
      password1 = request.POST.get("password")
      password2 = request.POST.get("password2")

      if username == "":
          messages.warning(request, "Username Tidak Boleh Kosong")
          return redirect("tambahP")
      if password1 == "":
          messages.warning(request, "Password Tidak Boleh Kosong")
          return redirect("tambahP")
      if password2 == "":
          messages.warning(request, "Password2 Tidak Boleh Kosong")
          return redirect("tambahP")
      if User.objects.filter(username=username).first():
        messages.warning(request, "Username sudah ada.")
        return redirect("tambahP")
      if password1 != password2:
        messages.warning(request, "Password Tidak Sama")
        return redirect("tambahP")

      user = User.objects.create_user(username=username)
      user.set_password(password1)
      user.is_active = True
      user.save()

      addGroup = Group.objects.get(name="pengajar")
      user.groups.add(addGroup)

      formSimpanadminGuru = formGuru.save()
      formSimpanadminGuru.user = user
      formSimpanadminGuru.save()

      return redirect('tambahP')
  Dewi = {
    'judul':  'Admin | Tambah Guru',
    'guru' : form,
    'grhtml'   :  gr,
  }
  return render(request, 'admin/tambahguru.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def tahunakademik (request):
  #ambil dari database di model Guru
  tp = Tahun_Pelajaran.objects.all()
  s = Semester.objects.all()
  kls = Kelas.objects.all()
  # inputan tahun
  cekAktif = request.POST.get('aktif')
  if cekAktif == "1":
    if request.method == 'POST':
      tahunPelajaran = request.POST.get('tahunpelajaran')
      aktif = "1"

      simpan = Tahun_Pelajaran(
        tahun_pelajaran = tahunPelajaran,
        aktif = aktif,
      )
      simpan.save()
      return redirect('tahunAkademik')
  else:
    if request.method == 'POST':
      tahunPelajaran = request.POST.get('tahunpelajaran')
      aktif = "0"

      simpan = Tahun_Pelajaran(
        tahun_pelajaran = tahunPelajaran,
        aktif = aktif,
      )
      simpan.save()
      return redirect('tahunAkademik')
  Dewi = {
    'tahun' : tp,
    'Semester' : s,
    'kelas'   : kls
  }
  return render(request, 'admin/tahunAkademik.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def semester (request):
  #ambil dari database di model Guru
  s = Semester.objects.all()
  cekAktif = request.POST.get('aktif')
  if cekAktif == "1":
    if request.method == 'POST':
      semester = request.POST.get('semester')
      aktif = "1"

      simpan = Semester(
        nama_semester = semester,
        aktif = aktif,
      )
      simpan.save()
      return redirect('tahunAkademik')
  else:
    if request.method == 'POST':
      semester = request.POST.get('semester')
      aktif = "0"
    
      simpan = Semester(
        nama_semester = semester,
        aktif = aktif,
      )
      simpan.save()
      return redirect('tahunAkademik')
  Dewi = {
    'Semester' : s,
  }
  return render(request, 'admin/tahunAkademik.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def KelaS (request):
  kls = Kelas.objects.all()
  if request.method == 'POST':
    kelas = request.POST.get('kelas')

    if Kelas.objects.filter(kelas=kelas).first():
        messages.warning(request, "Kelas sudah ada.")
        return redirect("tahunAkademik")

    simpan = Kelas(
      kelas = kelas,
    )
    simpan.save()
    return redirect('tahunAkademik')
  Dewi = {
    'kelas' : kls,
  }
  return render(request, 'admin/tahunAkademik.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def piket (request):
  pk = Piket.objects.all()
  form = PiketForm()
  formPiket = PiketForm(request.POST)

  fotokosong = request.POST.get('foto')
  if fotokosong == '':
    if request.method == 'POST':
      username = request.POST.get("username")
      password1 = request.POST.get("password")
      password2 = request.POST.get("password2")

      if username == "":
          messages.warning(request, "Username Tidak Boleh Kosong")
          return redirect("Piket")
      if password1 == "":
          messages.warning(request, "Password Tidak Boleh Kosong")
          return redirect("Piket")
      if password2 == "":
          messages.warning(request, "Password2 Tidak Boleh Kosong")
          return redirect("Piket")
      if User.objects.filter(username=username).first():
        messages.warning(request, "Username sudah ada.")
        return redirect("Piket")
      if password1 != password2:
        messages.warning(request, "Password Tidak Sama")
        return redirect("Piket")

      user = User.objects.create_user(username=username)
      user.set_password(password1)
      user.is_active = True
      user.save()

      addGroup = Group.objects.get(name="piket")
      user.groups.add(addGroup)

      formSimpanadminPiket = formPiket.save()
      formSimpanadminPiket.user = user
      formSimpanadminPiket.save()

      return redirect('Piket')
  Dewi = {
    'judul':  'Tambah Piket',
    'piket': form,
    'pkhtml'   :  pk,
  }
  return render(request, 'admin/tambahpiket.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def waka (request):
  wk = Waka.objects.all()
  form = WakaForm()
  formWaka = WakaForm(request.POST)

  fotokosong = request.POST.get('foto')
  if fotokosong == '':
    if request.method == 'POST':
      username = request.POST.get("username")
      password1 = request.POST.get("password")
      password2 = request.POST.get("password2")

      if username == "":
          messages.warning(request, "Username Tidak Boleh Kosong")
          return redirect("Waka")
      if password1 == "":
          messages.warning(request, "Password Tidak Boleh Kosong")
          return redirect("Waka")
      if password2 == "":
          messages.warning(request, "Password2 Tidak Boleh Kosong")
          return redirect("Waka")
      if User.objects.filter(username=username).first():
        messages.warning(request, "Username sudah ada.")
        return redirect("Waka")
      if password1 != password2:
        messages.warning(request, "Password Tidak Sama")
        return redirect("Waka")

      user = User.objects.create_user(username=username)
      user.set_password(password1)
      user.is_active = True
      user.save()

      addGroup = Group.objects.get(name="wakakurikulum")
      user.groups.add(addGroup)

      formSimpanadminWaka = formWaka.save()
      formSimpanadminWaka.user = user
      formSimpanadminWaka.save()

      return redirect('Waka')
  Dewi = {
    'judul':  'Tambah Waka',
    'waka' : form,
    'wkhtml'   :  wk,
  }
  return render(request, 'admin/tambahwaka.html', Dewi)

def logouT (request):
  logout(request)
  return redirect('loginU')

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def editW (request, id):
  editW = Waka.objects.get(id=id)
  sandi = request.POST.get('password')

  if sandi == "":
    if request.method == "POST":
      username = request.POST.get('username')
      user = User.objects.get(id=editW.user.id)
      user.username=username
      user.save()

      nama = request.POST.get('nama')
      nip = request.POST.get('nip')
      hp = request.POST.get('hp')
      userid = request.POST.get('user_id')

      data = Waka(
        id = id,
        nama = nama,
        nip = nip,
        hp = hp,
        user_id = userid,
      )

      data.save()
      return redirect('Waka')
  else:
    if request.method == "POST":
      username = request.POST.get("username")
      password1 = request.POST.get("password")
      password2 = request.POST.get("password2")

      if password1 != password2:
        messages.warning(request, "password tidak sama!")
        return redirect("Waka")

      user = User.objects.get(id=editW.user.id)
      user.username=username
      user.set_password(password1)
      user.save()

      nama = request.POST.get('nama')
      nip = request.POST.get('nip')
      hp = request.POST.get('hp')
      userid = request.POST.get('user_id')

      data = Waka(
      id = id,
      nama = nama,
      nip = nip,
      hp = hp,
      user_id = userid,
      )
      data.save()
      return redirect('Waka')
  return render(request, 'admin/tambahwaka.html')

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def hapusW (request, id):
  if request.method == "POST":
    iduser = request.POST.get('user_id')
    hapusW = Waka.objects.filter(id=id)
    hapusW.delete()

    user = User.objects.get(id=iduser)
    user.delete()

  messages.warning(request, "Data berhasil di hapus")
  return redirect('Waka') 
  
# @login_required(login_url='loginU')
# @ijinkan_pengguna(yang_diizinkan=["admin"])
# def editT (request, id):
#   editT = Waka.objects.get(id=id)

#   if tahun == "":
#     if request.method == "POST":
#       tahunPejaran = request.POST.get('tahunpelajaran')
#       aktif  = request.POST.get('aktif')
      
#       data = Tahun_Pelajaran(
#       tahun_pelajaran = tahunPejaran,
#       aktif = aktif,
#       )
#       data.save()
#       return redirect('tahunAkademik')
#   else:
#     if request.method == "POST":
#       tahunPejaran = request.POST.get('tahunpelajaran')
#       aktif  = request.POST.get('aktif')
      
#       data = Tahun_Pelajaran(
#       tahun_pelajaran = tahunPejaran,
#       aktif = aktif,
#       )
#       simpan.save()
#       return redirect('tahunAkademik')
#   return render(request, 'admin/bstahunAkademik.html')

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def editK (request, id):
  editK = Kelas.objects.get(id=id)
  if request.method == 'POST':
    kelas = request.POST.get('kelas')
    edit = Kelas(
      id = id,
      kelas = kelas
    )
    edit.save()
    return redirect('tahunAkademik')
  Dewi = {
    'kelas' : editK
  }
  return render(request, 'admin/bstahunAkademik.html', Dewi)


@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def editTahun (request, id):
  editT = Tahun_Pelajaran.objects.get(id=id)
  cekAktif = request.POST.get('aktif')
  if cekAktif == "1":
    if request.method == 'POST':
      tahunPelajaran = request.POST.get('tahunpelajaran')
      aktif = "1"

      edit = Tahun_Pelajaran(
        id = id,
        tahun_pelajaran = tahunPelajaran,
        aktif = aktif,
      )
      edit.save()
      return redirect('tahunAkademik')
  else:
    if request.method == 'POST':
      tahunPelajaran = request.POST.get('tahunpelajaran')
      aktif = "0"

      edit = Tahun_Pelajaran(
        id = id,
        tahun_pelajaran = tahunPelajaran,
        aktif = aktif,
      )
      edit.save()
      return redirect('tahunAkademik')
  Dewi = {
    'tahun' : editT
  }
  return render(request, 'admin/bstahunAkademik.html', Dewi)
@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def editSemester (request, id):
  editS = Semester.objects.get(id=id)
  cekAktif = request.POST.get('aktif')
  if cekAktif == "1":
    if request.method == 'POST':
      semester = request.POST.get('semester')
      aktif = "1"

      edit = Semester(
        id = id,
        nama_semester = semester,
        aktif = aktif,
      )
      edit.save()
      return redirect('tahunAkademik')
  else:
    if request.method == 'POST':
      semester = request.POST.get('semester')
      aktif = "0"

      edit = Semester(
        id = id,
        nama_semester = semester,
        aktif = aktif,
      )
      edit.save()
      return redirect('tahunAkademik')
  Dewi = {
    'semester' : editS
  }
  return render(request, 'admin/bstahunAkademik.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def hapusT (request, id):
  if request.method == "POST":
    iduser = request.POST.get('user_id')
    hapusT = Tahun_Pelajaran.objects.filter(id=id)
    hapusT.delete()

    user = User.objects.get(id=iduser)
    user.delete()

  messages.warning(request, "Data berhasil di hapus")
  return redirect('tahunAkademik') 

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def editP (request, id):
  editP = Piket.objects.get(id=id)
  sandi = request.POST.get('password')

  if sandi == "":
    if request.method == "POST":
      username = request.POST.get('username')
      user = User.objects.get(id=editP.user.id)
      user.username=username
      user.save()

      nama = request.POST.get('nama')
      nip = request.POST.get('nip')
      hp = request.POST.get('hp')
      userid = request.POST.get('user_id')

      data = Piket(
        id = id,
        nama = nama,
        nip = nip,
        hp = hp,
        user_id = userid,
      )

      data.save()
      return redirect('Piket')
  else:
    if request.method == "POST":
      username = request.POST.get("username")
      password1 = request.POST.get("password")
      password2 = request.POST.get("password2")

      if password1 != password2:
        messages.warning(request, "password tidak sama!")
        return redirect("Piket")

      user = User.objects.get(id=editP.user.id)
      user.username=username
      user.set_password(password1)
      user.save()

      nama = request.POST.get('nama')
      nip = request.POST.get('nip')
      hp = request.POST.get('hp')
      userid = request.POST.get('user_id')

      data = Piket(
      id = id,
      nama = nama,
      nip = nip,
      hp = hp,
      user_id = userid,
      )
      data.save()
      return redirect('Piket')
  return render(request, 'admin/tambahpiket.html')


@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def hapusP (request, id):
  if request.method == "POST":
    iduser = request.POST.get('user_id')
    hapusP = Piket.objects.filter(id=id)
    hapusP.delete()

    user = User.objects.get(id=iduser)
    user.delete()

  messages.warning(request, "Data berhasil di hapus")
  return redirect('Piket') 
  
@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def editG (request, id):
  editG = Guru.objects.get(id=id)
  sandi = request.POST.get('password')

  if sandi == "":
    if request.method == "POST":
      username = request.POST.get('username')
      user = User.objects.get(id=editG.user.id)
      user.username=username
      user.save()

      nama = request.POST.get('nama')
      nip = request.POST.get('nip')
      hp = request.POST.get('hp')
      userid = request.POST.get('user_id')

      data = Guru(
        id = id,
        nama = nama,
        nip = nip,
        hp = hp,
        user_id = userid,
      )

      data.save()
      return redirect('tambahP')
  else:
    if request.method == "POST":
      username = request.POST.get("username")
      password1 = request.POST.get("password")
      password2 = request.POST.get("password2")

      if password1 != password2:
        messages.warning(request, "password tidak sama!")
        return redirect("tambahP")

      user = User.objects.get(id=editG.user.id)
      user.username=username
      user.set_password(password1)
      user.save()

      nama = request.POST.get('nama')
      nip = request.POST.get('nip')
      hp = request.POST.get('hp')
      userid = request.POST.get('user_id')

      data = Guru(
      id = id,
      nama = nama,
      nip = nip,
      hp = hp,
      user_id = userid,
      )
      data.save()
      return redirect('tambahP')
  return render(request, 'admin/tambahguru.html')

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["admin"])
def hapusG (request, id):
  if request.method == "POST":
    iduser = request.POST.get('user_id')
    hapusG = Guru.objects.filter(id=id)
    hapusG.delete()

    user = User.objects.get(id=iduser)
    user.delete()

  messages.warning(request, "Data berhasil di hapus")
  return redirect('tambahP') 
  
@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["wakakurikulum"])
def editJ (request, id):
  jadwal = Jadwal.objects.get(id=id)

  form = JadwalForm(instance=jadwal)
  if request.method == "POST":
    edit = JadwalForm(request.POST, instance=jadwal)
    if edit.is_valid:
      edit.save()
      messages.warning(request, "Data berhasil di edit")
      return redirect('Jadwal')
  Dewi = {
    'form' : form,
  }
  return render(request, 'waka/edit.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["wakakurikulum"])
def hapusJ (request, id):
  if request.method == "POST":
    hapusJ = Jadwal.objects.filter(id=id)
    hapusJ.delete()
  messages.warning(request, "Data berhasil di hapus")
  return redirect('Jadwal')

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["wakakurikulum"])
def uploadW (request):
  data = Waka.objects.get(user_id=request.user.id)
  if request.method == 'POST' and request.FILES['foto']:
    id = request.POST.get('id_waka')
    nama = request.POST.get('nama')
    nip = request.POST.get('nip')
    hp = request.POST.get('hp')
    userid = request.POST.get('user_id')

    file = request.FILES['foto']
    fs = FileSystemStorage()
    filename = fs.save(userid+hp+nip, file)
    url = fs.url(filename)

    simpan = Waka(
    id = id,
    nama = nama,
    nip = nip,
    hp = hp,
    user_id = userid,
    foto = url,
    )
    simpan.save()
    return redirect('ProfilWaka')
  Dewi = {
    'data'  : data,
  }
  return render(request, 'waka/profilwaka.html', Dewi)

@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["pengajar"])
def uploadG (request):
  data = Guru.objects.get(user_id=request.user.id)
  if request.method == 'POST' and request.FILES['foto']:
    id = request.POST.get('id_guru')
    nama = request.POST.get('nama')
    nip = request.POST.get('nip')
    hp = request.POST.get('hp')
    userid = request.POST.get('user_id')

    file = request.FILES['foto']
    fs = FileSystemStorage()
    filename = fs.save(userid+hp+nip, file)
    url = fs.url(filename)

    simpan = Guru(
    id = id,
    nama = nama,
    nip = nip,
    hp = hp,
    user_id = userid,
    foto = url,
    )
    simpan.save()
    return redirect('ProfilGuru')
  Dewi = {
    'data'  : data,
  }
  return render(request, 'guru/profilGuru.html', Dewi)
@login_required(login_url='loginU')
@ijinkan_pengguna(yang_diizinkan=["piket"])
def uploadP (request):
  data = Piket.objects.get(user_id=request.user.id)
  if request.method == 'POST' and request.FILES['foto']:
    id = request.POST.get('id_piket')
    nama = request.POST.get('nama')
    nip = request.POST.get('nip')
    hp = request.POST.get('hp')
    userid = request.POST.get('user_id')

    file = request.FILES['foto']
    fs = FileSystemStorage()
    filename = fs.save(userid+hp+nip, file)
    url = fs.url(filename)

    simpan = Piket(
    id = id,
    nama = nama,
    nip = nip,
    hp = hp,
    user_id = userid,
    foto = url,
    )
    simpan.save()
    return redirect('ProfilPiket')
  Dewi = {
    'data'  : data,
  }
  return render(request, 'piket/profilPiket.html', Dewi)
