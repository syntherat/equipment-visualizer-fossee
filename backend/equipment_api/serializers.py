from rest_framework import serializers
from .models import Dataset, EquipmentData


class EquipmentDataSerializer(serializers.ModelSerializer):
    # Converts EquipmentData model instances to JSON for API responses
    class Meta:
        model = EquipmentData
        fields = ['id', 'equipment_name', 'equipment_type', 'flowrate', 'pressure', 'temperature']


class DatasetSerializer(serializers.ModelSerializer):
    # Full dataset serializer - includes all equipment records
    # Used when client needs complete data for a dataset
    equipment = EquipmentDataSerializer(many=True, read_only=True)  # Nested equipment list
    type_distribution = serializers.SerializerMethodField()  # Parse JSON to dict
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)  # Username string
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'uploaded_at', 'uploaded_by_username',
            'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'type_distribution', 'equipment'
        ]
    
    def get_type_distribution(self, obj):
        # Convert JSON string to dictionary for JSON response
        return obj.get_type_distribution()


class DatasetSummarySerializer(serializers.ModelSerializer):
    # Lightweight serializer without equipment details
    # Used for history list to reduce payload size
    type_distribution = serializers.SerializerMethodField()  # Parse JSON to dict
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    
    class Meta:
        model = Dataset
        fields = [
            'id', 'name', 'uploaded_at', 'uploaded_by_username',
            'total_count', 'avg_flowrate', 'avg_pressure', 'avg_temperature',
            'type_distribution'
        ]
    
    def get_type_distribution(self, obj):
        # Convert JSON string to dictionary for JSON response
        return obj.get_type_distribution()
