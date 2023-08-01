from django.urls import path
from . import views

urlpatterns = [
    #login register
    path('', views.loginF, name='loginU'),
    path('logout', views.logouT, name='Logout'),
    # guru
    path('guru', views.profilGuru, name='ProfilGuru'),
    path('jurnal-mengajar', views.jurnalMengajar, name='JurnalMengajar'),
    path('rekapan', views.rekap, name='Rekap'),
    path('jurnal-pengajar/absen/<str:id>', views.absenG, name='AbsenG'),
    # guru piket
    path('piket', views.profilPiket, name='ProfilPiket'),
    path('cek-jurnal-mengajar', views.Cekjurnal, name='CekJurnalMengajar'),
    path('laporanbelajar', views.rekapPiket, name='RekapPiket'),
    path('cek-jurnal-Pengajar/dokumentasi', views.Dokumentasi, name='DokP'),
    # wakakurikulum
    path('wakakurikulum', views.profilWaka, name='ProfilWaka'),
    path('penjadwalan', views.Penjadwalan, name='Jadwal'),
    path('daftarguru', views.daftarGuru, name='DaftarGuru'),
    path('absensikinerja', views.absensiKinerja, name='AbsensiKinerja'),
    path('idkode', views.idKode, name='id_kode'),
    #admin
    path('superadmin', views.admiN, name='Admin'),
    path('tambah_pengajar', views.TambahP, name='tambahP'),
    path('tambah_piket', views.piket, name='Piket'),
    path('tambah_waka', views.waka, name='Waka'),
    path('tahun_akademik', views.tahunakademik, name='tahunAkademik'),
    path('semesteran', views.semester, name='Semester'),
    path('kelas', views.KelaS, name='KELAS'),
    #url.id admin
    path('edit_waka/<str:id>', views.editW, name='EditWaka'),
    path('hapus_waka/<str:id>', views.hapusW, name='HapusWaka'),
    path('edit_piket/<str:id>', views.editP, name='EditPiket'),
    path('hapus_piket/<str:id>', views.hapusP, name='HapusPiket'),
    path('edit_guru/<str:id>', views.editG, name='EditGuru'),
    path('hapus_guru/<str:id>', views.hapusG, name='HapusGuru'),
    path('edit_kelas/<str:id>', views.editK, name='EditKelas'),
    path('edit_tahun/<str:id>', views.editTahun, name='EditTahun'),
    path('edit_semester/<str:id>', views.editSemester, name='EditSemester'),
    #url.id wakakurikulum
    path('tambah_jadwal', views.TambahJ, name='tambahJadwal'),
    path('edit_jadwal/<str:id>', views.editJ, name='EditJadwal'),
    path('hapus_jadwal/<str:id>', views.hapusJ, name='HapusJadwal'),
    path('upload', views.uploadW, name='uploadprofilWaka'),
    path('uploadG', views.uploadG, name='uploadprofilGuru'),
    path('uploadP', views.uploadP, name='uploadprofilPiket'),
]