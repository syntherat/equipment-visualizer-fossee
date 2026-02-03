from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Count
from django.views.decorators.csrf import csrf_exempt
from .models import Dataset, EquipmentData
from .serializers import DatasetSerializer, DatasetSummarySerializer, EquipmentDataSerializer
import pandas as pd
import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.units import inch
from django.http import HttpResponse
from datetime import datetime


def get_request_user(request):
    """Return authenticated user or a fallback demo user for dev mode."""
    user = getattr(request, 'user', None)
    if user and getattr(user, 'is_authenticated', False):
        return user
    demo_user, created = User.objects.get_or_create(username='demo')
    if created or demo_user.has_usable_password():
        demo_user.set_unusable_password()
        demo_user.save()
    return demo_user


@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def login_view(request):
    """Login endpoint"""
    username = request.data.get('username')
    password = request.data.get('password')
    
    if not username or not password:
        return Response({'error': 'Username and password required'}, status=status.HTTP_400_BAD_REQUEST)
    
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({
            'message': 'Login successful',
            'username': user.username,
            'user_id': user.id
        })
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def logout_view(request):
    """Logout endpoint"""
    logout(request)
    return Response({'message': 'Logout successful'})


@api_view(['POST'])
@csrf_exempt
@permission_classes([AllowAny])
def upload_csv(request):
    """Upload and process CSV file"""
    if 'file' not in request.FILES:
        return Response({'error': 'No file provided'}, status=status.HTTP_400_BAD_REQUEST)
    
    csv_file = request.FILES['file']
    
    # Validate file type
    if not csv_file.name.endswith('.csv'):
        return Response({'error': 'File must be a CSV'}, status=status.HTTP_400_BAD_REQUEST)
    
    try:
        # Read CSV with pandas
        df = pd.read_csv(csv_file)
        
        # Validate required columns
        required_columns = ['Equipment Name', 'Type', 'Flowrate', 'Pressure', 'Temperature']
        if not all(col in df.columns for col in required_columns):
            return Response({
                'error': f'CSV must contain columns: {", ".join(required_columns)}'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Calculate summary statistics
        total_count = len(df)
        avg_flowrate = df['Flowrate'].mean()
        avg_pressure = df['Pressure'].mean()
        avg_temperature = df['Temperature'].mean()
        type_distribution = df['Type'].value_counts().to_dict()
        
        # Create dataset
        user = get_request_user(request)
        dataset = Dataset.objects.create(
            name=csv_file.name,
            uploaded_by=user,
            total_count=total_count,
            avg_flowrate=avg_flowrate,
            avg_pressure=avg_pressure,
            avg_temperature=avg_temperature
        )
        dataset.set_type_distribution(type_distribution)
        dataset.save()
        
        # Create equipment records
        for _, row in df.iterrows():
            EquipmentData.objects.create(
                dataset=dataset,
                equipment_name=row['Equipment Name'],
                equipment_type=row['Type'],
                flowrate=row['Flowrate'],
                pressure=row['Pressure'],
                temperature=row['Temperature']
            )
        
        # Keep only last 5 datasets per user
        user_datasets = Dataset.objects.filter(uploaded_by=user)
        if user_datasets.count() > 5:
            datasets_to_delete = user_datasets[5:]
            for ds in datasets_to_delete:
                ds.delete()
        
        serializer = DatasetSerializer(dataset)
        return Response({
            'message': 'File uploaded successfully',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)
    
    except Exception as e:
        return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([AllowAny])
def get_summary(request, dataset_id):
    """Get summary for a specific dataset"""
    try:
        user = get_request_user(request)
        dataset = Dataset.objects.get(id=dataset_id, uploaded_by=user)
        serializer = DatasetSerializer(dataset)
        return Response(serializer.data)
    except Dataset.DoesNotExist:
        try:
            dataset = Dataset.objects.get(id=dataset_id)
            serializer = DatasetSerializer(dataset)
            return Response(serializer.data)
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def get_history(request):
    """Get last 5 datasets"""
    user = get_request_user(request)
    datasets = Dataset.objects.filter(uploaded_by=user)[:5]
    serializer = DatasetSummarySerializer(datasets, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def generate_pdf_report(request, dataset_id):
    """Generate PDF report for a dataset"""
    try:
        user = get_request_user(request)
        dataset = Dataset.objects.get(id=dataset_id, uploaded_by=user)
    except Dataset.DoesNotExist:
        try:
            dataset = Dataset.objects.get(id=dataset_id)
        except Dataset.DoesNotExist:
            return Response({'error': 'Dataset not found'}, status=status.HTTP_404_NOT_FOUND)
    
    # Create HTTP response with PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="report_{dataset.id}_{datetime.now().strftime("%Y%m%d")}.pdf"'
    
    # Create PDF
    doc = SimpleDocTemplate(response, pagesize=letter)
    elements = []
    styles = getSampleStyleSheet()
    
    # Title
    title = Paragraph(f"<b>Equipment Data Report</b>", styles['Title'])
    elements.append(title)
    elements.append(Spacer(1, 0.3*inch))
    
    # Dataset info
    info_text = f"""
    <b>Dataset:</b> {dataset.name}<br/>
    <b>Uploaded:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}<br/>
    <b>Uploaded by:</b> {dataset.uploaded_by.username}<br/>
    <b>Total Equipment:</b> {dataset.total_count}<br/>
    """
    info = Paragraph(info_text, styles['Normal'])
    elements.append(info)
    elements.append(Spacer(1, 0.3*inch))
    
    # Summary statistics
    summary_title = Paragraph("<b>Summary Statistics</b>", styles['Heading2'])
    elements.append(summary_title)
    elements.append(Spacer(1, 0.1*inch))
    
    summary_data = [
        ['Metric', 'Average Value'],
        ['Flowrate', f'{dataset.avg_flowrate:.2f}'],
        ['Pressure', f'{dataset.avg_pressure:.2f}'],
        ['Temperature', f'{dataset.avg_temperature:.2f}']
    ]
    
    summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
    summary_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(summary_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Type distribution
    dist_title = Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2'])
    elements.append(dist_title)
    elements.append(Spacer(1, 0.1*inch))
    
    type_dist = dataset.get_type_distribution()
    dist_data = [['Equipment Type', 'Count']]
    for eq_type, count in type_dist.items():
        dist_data.append([eq_type, str(count)])
    
    dist_table = Table(dist_data, colWidths=[3*inch, 2*inch])
    dist_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 12),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(dist_table)
    elements.append(Spacer(1, 0.3*inch))
    
    # Equipment details
    equipment_title = Paragraph("<b>Equipment Details</b>", styles['Heading2'])
    elements.append(equipment_title)
    elements.append(Spacer(1, 0.1*inch))
    
    equipment = dataset.equipment.all()
    eq_data = [['Name', 'Type', 'Flow', 'Press', 'Temp']]
    for eq in equipment[:20]:  # Limit to first 20 for PDF
        eq_data.append([
            eq.equipment_name[:20],
            eq.equipment_type[:15],
            f'{eq.flowrate:.1f}',
            f'{eq.pressure:.1f}',
            f'{eq.temperature:.1f}'
        ])
    
    eq_table = Table(eq_data, colWidths=[2*inch, 1.5*inch, 0.8*inch, 0.8*inch, 0.8*inch])
    eq_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 8),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))
    elements.append(eq_table)
    
    if dataset.total_count > 20:
        note = Paragraph(f"<i>Note: Showing first 20 of {dataset.total_count} equipment items</i>", styles['Normal'])
        elements.append(Spacer(1, 0.1*inch))
        elements.append(note)
    
    # Build PDF
    doc.build(elements)
    return response


@api_view(['GET'])
@csrf_exempt
@permission_classes([AllowAny])
def health_check(request):
    """Health check endpoint"""
    return Response({'status': 'ok', 'message': 'API is running'})
