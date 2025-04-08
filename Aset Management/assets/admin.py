import csv
import openpyxl
from io import BytesIO
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.contrib import admin
from .models import Asset, Spesifikasi

class SpesifikasiInline(admin.StackedInline):
    model = Spesifikasi
    extra = 1  # Menampilkan form tambahan untuk spesifikasi dalam admin

class SpesifikasiPrinterInline(admin.StackedInline):
    model = Spesifikasi
    extra = 1
    fields = ['jenis_tinta', 'resolusi_cetak', 'kecepatan_cetak']

class AssetAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kategori', 'lokasi', 'tanggal_pembelian', 'status')
    
    def get_inlines(self, request, obj=None):
        """Menampilkan form spesifikasi sesuai kategori asset"""
        if obj and obj.kategori == "Printer":
            return [SpesifikasiPrinterInline]
        return []

# Fungsi Export ke CSV
def export_to_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="assets.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['ID', 'Nama', 'Kategori', 'Tanggal Pembelian', 'Status'])
    
    for asset in queryset:
        writer.writerow([asset.id, asset.nama, asset.kategori, asset.tanggal_pembelian, asset.status])

    return response

export_to_csv.short_description = "Export to CSV"

# Fungsi Export ke Excel
def export_to_excel(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="assets.xlsx"'
    
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.append(['ID', 'Nama', 'Kategori', 'Tanggal Pembelian', 'Status'])
    
    for asset in queryset:
        sheet.append([asset.id, asset.nama, asset.kategori, asset.tanggal_pembelian, asset.status])

    # Menyimpan ke BytesIO agar bisa dikirim ke response
    output = BytesIO()
    workbook.save(output)
    output.seek(0)

    response.write(output.getvalue())
    return response

export_to_excel.short_description = "Export to Excel"

# Fungsi Export ke PDF
def export_to_pdf(modeladmin, request, queryset):
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="assets.pdf"'
    
    pdf = canvas.Canvas(response)
    pdf.drawString(100, 800, "Daftar Aset")

    y = 780
    for asset in queryset:
        pdf.drawString(100, y, f"{asset.id} - {asset.nama} ({asset.kategori}) - {asset.tanggal_pembelian} - {asset.status}")
        y -= 20

    pdf.save()
    return response

export_to_pdf.short_description = "Export to PDF"

# Custom Admin dengan Export
class AssetAdmin(admin.ModelAdmin):
    list_display = ('nama', 'kategori', 'tanggal_pembelian', 'status')
    inlines = [SpesifikasiInline]
    actions = [export_to_csv, export_to_excel, export_to_pdf]

admin.site.register(Asset, AssetAdmin)