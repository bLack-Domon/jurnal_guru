from django.http import HttpResponse
from django.shortcuts import redirect

def tolakhalaman_ini(fungsi_awal):
    def perubahan_halaman(request, *args, **kwargs):
        if request.user.is_authenticated:
           return redirect("Admin")
        else:
          return fungsi_awal(request, *args, **kwargs)
    return perubahan_halaman

def ijinkan_pengguna(yang_diizinkan=[]):
    def aturan(fungsi_awal):
        def perubahan_halaman(request, *args, **kwargs):
            group = None
            if request.user.groups.exists():
               group = request.user.groups.all()[0].name
            if group in yang_diizinkan:
              return fungsi_awal(request, *args, **kwargs)
            else:
              return redirect("block_access")
        return perubahan_halaman
    return aturan

def pilihan_login(fungsi_awal):
   def perubahan_halaman(request, *args, **kwargs):
      group = None
      if request.user.groups.exists():
         group = request.user.groups.all()[0].name
      if group == "wakakurikulum":
         return redirect("ProfilWaka")
      if group == "pengajar":
         return redirect("ProfilGuru")
      if group == "piket":
         return redirect("ProfilPiket")
      if group == "admin":
         return fungsi_awal(request, *args, **kwargs)
   return perubahan_halaman