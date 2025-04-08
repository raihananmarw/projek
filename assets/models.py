from django.db import models

class Asset(models.Model):
    nama = models.CharField(max_length=255, default="Nama Default")
    kategori = models.CharField(max_length=100)
    tanggal_pembelian = models.DateField()
    status = models.CharField(max_length=50)

    def __str__(self):
        return self.nama

class Spesifikasi(models.Model):
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE, related_name="spesifikasi")
    
    # Field untuk Printer
    jenis_tinta = models.CharField(max_length=50, blank=True, null=True)
    resolusi_cetak = models.CharField(max_length=50, blank=True, null=True)
    kecepatan_cetak = models.CharField(max_length=50, blank=True, null=True)

    # Field untuk PC
    prosesor = models.CharField(max_length=100, blank=True, null=True)
    ram = models.CharField(max_length=50, blank=True, null=True)
    penyimpanan = models.CharField(max_length=100, blank=True, null=True)
    
    # Field tambahan
    lain_lain = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Spesifikasi {self.asset.nama}"