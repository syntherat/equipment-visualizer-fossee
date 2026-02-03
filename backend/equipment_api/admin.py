from django.contrib import admin
from .models import Dataset, EquipmentData


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ['name', 'uploaded_at', 'uploaded_by', 'total_count']
    list_filter = ['uploaded_at', 'uploaded_by']
    search_fields = ['name']


@admin.register(EquipmentData)
class EquipmentDataAdmin(admin.ModelAdmin):
    list_display = ['equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature', 'dataset']
    list_filter = ['equipment_type', 'dataset']
    search_fields = ['equipment_name', 'equipment_type']
