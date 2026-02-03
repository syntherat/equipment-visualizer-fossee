from django.db import models
from django.contrib.auth.models import User
import json


class Dataset(models.Model):
    # Stores metadata for each uploaded CSV dataset
    # Summary stats are pre-calculated to avoid expensive queries on every API call
    name = models.CharField(max_length=255)  # Original CSV filename
    uploaded_at = models.DateTimeField(auto_now_add=True)  # When dataset was created
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='datasets')  # Owner
    total_count = models.IntegerField(default=0)  # Total equipment records in this dataset
    avg_flowrate = models.FloatField(default=0.0)  # Pre-calculated for faster API response
    avg_pressure = models.FloatField(default=0.0)  # Pre-calculated for faster API response
    avg_temperature = models.FloatField(default=0.0)  # Pre-calculated for faster API response
    type_distribution = models.TextField(default='{}')  # Equipment type distribution as JSON
    
    class Meta:
        ordering = ['-uploaded_at']  # Show newest datasets first
    
    def __str__(self):
        return f"{self.name} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    def get_type_distribution(self):
        # Safely parse JSON string to dict, returns empty dict on error
        try:
            return json.loads(self.type_distribution)
        except:
            return {}
    
    def set_type_distribution(self, distribution_dict):
        # Convert dict to JSON string for database storage
        self.type_distribution = json.dumps(distribution_dict)


class EquipmentData(models.Model):
    # Individual equipment items from uploaded CSV
    # One record per row in the original CSV file
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name='equipment')  # Parent dataset
    equipment_name = models.CharField(max_length=255)  # Equipment identifier/name
    equipment_type = models.CharField(max_length=100)  # Type/category (Pump, Tank, Reactor, etc)
    flowrate = models.FloatField()  # Flowrate measurement value
    pressure = models.FloatField()  # Pressure measurement value
    temperature = models.FloatField()  # Temperature measurement value
    
    class Meta:
        ordering = ['equipment_name']  # Sort alphabetically for consistent display
    
    def __str__(self):
        return f"{self.equipment_name} ({self.equipment_type})"
