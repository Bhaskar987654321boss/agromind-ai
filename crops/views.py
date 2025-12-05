from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import Crop, RecommendationLog, YieldLog, DiseaseLog
from ml_engine.recommendation import CropRecommender
from ml_engine.yield_prediction import YieldPredictor
from ml_engine.disease_prediction import predictor as disease_predictor

# PDF Generation
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import io
from datetime import datetime

# Initialize ML engines
recommender = CropRecommender()
yield_predictor = YieldPredictor()

@login_required
def recommend_crop(request):
    if request.method == 'POST':
        print("DEBUG: recommend_crop POST data:", request.POST)
        try:
            data = request.POST
            nitrogen = float(data.get('nitrogen'))
            phosphorus = float(data.get('phosphorus'))
            potassium = float(data.get('potassium'))
            temperature = float(data.get('temperature'))
            humidity = float(data.get('humidity'))
            ph = float(data.get('ph'))
            rainfall = float(data.get('rainfall'))
            
            # Optional fields
            soil_moisture = data.get('soil_moisture')
            print(f"DEBUG: Extra Recommendation Inputs - Soil Moisture: {soil_moisture}")
            
            recommendations = recommender.recommend(
                nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall
            )
            print("DEBUG: Recommendations:", recommendations)
            context = {
                'recommendations': recommendations,
                'nitrogen': nitrogen,
                'phosphorus': phosphorus,
                'potassium': potassium,
                'temperature': temperature,
                'humidity': humidity,
                'ph': ph,
                'rainfall': rainfall
            }
            
            # Save Log
            if request.user.is_authenticated:
                # Get top recommendation
                top_rec = recommendations[0]['crop'] if recommendations else "None"
                conf = recommendations[0]['confidence'] if recommendations else 0.0
                
                RecommendationLog.objects.create(
                    user=request.user,
                    nitrogen=nitrogen,
                    phosphorus=phosphorus,
                    potassium=potassium,
                    temperature=temperature,
                    humidity=humidity,
                    ph=ph,
                    rainfall=rainfall,
                    soil_moisture=str(soil_moisture) if soil_moisture else None,
                    recommended_crop=top_rec,
                    confidence=conf
                )

            return render(request, 'crops/recommend_result.html', context)
        except Exception as e:
            print("DEBUG: Error in recommend_crop:", e)
            return render(request, 'crops/recommend_form.html', {'error': str(e)})
            
    return render(request, 'crops/recommend_form.html')

@login_required
def download_recommendation_pdf(request):
    # Get parameters from GET request
    try:
        nitrogen = float(request.GET.get('nitrogen', 0))
        phosphorus = float(request.GET.get('phosphorus', 0))
        potassium = float(request.GET.get('potassium', 0))
        temperature = float(request.GET.get('temperature', 0))
        humidity = float(request.GET.get('humidity', 0))
        ph = float(request.GET.get('ph', 0))
        rainfall = float(request.GET.get('rainfall', 0))
        
        # Get recommendations again
        recommendations = recommender.recommend(
            nitrogen, phosphorus, potassium, temperature, humidity, ph, rainfall
        )
        
        # Create PDF
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        elements.append(Paragraph("Crop Recommendation Report", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Input Data
        elements.append(Paragraph("Soil and Weather Conditions:", styles['Heading2']))
        input_data = [
            ["Parameter", "Value"],
            ["Nitrogen", str(nitrogen)],
            ["Phosphorus", str(phosphorus)],
            ["Potassium", str(potassium)],
            ["Temperature", f"{temperature} C"],
            ["Humidity", f"{humidity} %"],
            ["pH", str(ph)],
            ["Rainfall", f"{rainfall} mm"]
        ]
        t = Table(input_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 24))
        
        # Recommendations
        elements.append(Paragraph("Recommended Crops:", styles['Heading2']))
        
        if recommendations:
            for rec in recommendations:
                crop_name = rec['crop']
                confidence = rec['confidence']
                elements.append(Paragraph(f"Crop: {crop_name} (Confidence: {confidence:.2f})", styles['Heading3']))
                
                # Measures for Farmers
                elements.append(Paragraph("Measures for Farmers:", styles['Heading4']))
                farmer_measures = get_farmer_measures(crop_name)
                for measure in farmer_measures:
                    elements.append(Paragraph(f"- {measure}", styles['Normal']))
                
                # Measures for Government
                elements.append(Paragraph("Measures for Government:", styles['Heading4']))
                gov_measures = get_gov_measures(crop_name)
                for measure in gov_measures:
                    elements.append(Paragraph(f"- {measure}", styles['Normal']))
                    
                elements.append(Spacer(1, 12))
        else:
            elements.append(Paragraph("No specific recommendations found based on the input data.", styles['Normal']))

        doc.build(elements)
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
        
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}")

def get_farmer_measures(crop):
    # Mock logic for measures
    common = [
        "Test soil regularly.",
        "Use organic fertilizers where possible.",
        "Ensure proper irrigation drainage."
    ]
    specific = {
        'rice': ["Maintain standing water level.", "Monitor for blast disease."],
        'maize': ["Ensure good drainage.", "Watch for stem borers."],
        'chickpea': ["Avoid waterlogging.", "Treat seeds before sowing."],
        'kidneybeans': ["Provide support for climbers.", "Harvest when pods are dry."],
        'pigeonpeas': ["Intercrop with cereals.", "Protect from pod borers."],
        'mothbeans': ["Drought tolerant, minimal irrigation needed.", "Harvest when pods turn yellow."],
        'mungbean': ["Short duration crop.", "Harvest before shattering."],
        'blackgram': ["Suitable for intercropping.", "Monitor for powdery mildew."],
        'lentil': ["Cool season crop.", "Avoid excessive moisture."],
        'pomegranate': ["Prune regularly.", "Control fruit borer."],
        'banana': ["Propping is required.", "Remove suckers regularly."],
        'mango': ["Prune for canopy management.", "Control fruit flies."],
        'grapes': ["Training and pruning is essential.", "Monitor for downy mildew."],
        'watermelon': ["Mulching helps conserve moisture.", "Harvest when tendril dries."],
        'muskmelon': ["Avoid wetting leaves.", "Harvest at full slip stage."],
        'apple': ["Requires chilling hours.", "Prune for better fruit quality."],
        'orange': ["Monitor for citrus greening.", "Prune dead wood."],
        'papaya': ["Avoid water stagnation.", "Monitor for viral diseases."],
        'coconut': ["Regular manuring is important.", "Control rhinoceros beetle."],
        'cotton': ["Monitor for bollworms.", "Use IPM strategies."],
        'jute': ["Retting requires clean water.", "Harvest at small pod stage."],
        'coffee': ["Shade management is crucial.", "Prune after harvest."]
    }
    return specific.get(crop.lower(), []) + common

def get_gov_measures(crop):
    # Mock logic for government measures
    common = [
        "Provide subsidies for seeds and fertilizers.",
        "Ensure availability of credit.",
        "Improve market access."
    ]
    specific = {
        'rice': ["Procure at MSP.", "Invest in irrigation infrastructure."],
        'wheat': ["Ensure timely procurement.", "Promote resistant varieties."],
        'cotton': ["Support pest management programs.", "Promote value addition."]
    }
    return specific.get(crop.lower(), []) + common


@login_required
def predict_yield(request):
    if request.method == 'POST':
        print("DEBUG: predict_yield POST data:", request.POST)
        try:
            crop_name = request.POST.get('crop')
            area = float(request.POST.get('area'))
            soil_type = request.POST.get('soil_type', 'Alluvial')
            rainfall = float(request.POST.get('rainfall', 100))
            temperature = float(request.POST.get('temperature', 25))
            
            # Optional fields
            fertilizer = float(request.POST.get('fertilizer', 0) or 0)
            irrigation = request.POST.get('irrigation', 'None')
            print(f"DEBUG: Extra Yield Inputs - Fertilizer: {fertilizer}, Irrigation: {irrigation}")
            
            prediction = yield_predictor.predict_yield(crop_name, area, soil_type, rainfall, temperature, fertilizer, irrigation)
            print("DEBUG: Prediction:", prediction)
            
            context = {
                'prediction': prediction,
                'crop': crop_name,
                'area': area,
                'soil_type': soil_type,
                'rainfall': rainfall,
                'temperature': temperature,
                'fertilizer': fertilizer,
                'irrigation': irrigation
            }
            
            # Save Log
            if request.user.is_authenticated:
                YieldLog.objects.create(
                    user=request.user,
                    crop_name=crop_name,
                    area=area,
                    soil_type=soil_type,
                    rainfall=rainfall,
                    temperature=temperature,
                    fertilizer=fertilizer,
                    irrigation=irrigation,
                    predicted_yield=prediction
                )
                
            return render(request, 'crops/yield_result.html', context)
        except Exception as e:
            print("DEBUG: Error in predict_yield:", e)
            return render(request, 'crops/yield_form.html', {'error': str(e)})
        
    crops = Crop.objects.all()
    return render(request, 'crops/yield_form.html', {'crops': crops})

@login_required
def download_yield_pdf(request):
    try:
        crop_name = request.GET.get('crop')
        area = float(request.GET.get('area', 0))
        soil_type = request.GET.get('soil_type', '')
        rainfall = float(request.GET.get('rainfall', 0))
        temperature = float(request.GET.get('temperature', 0))
        fertilizer = float(request.GET.get('fertilizer', 0))
        irrigation = request.GET.get('irrigation', '')
        
        prediction = yield_predictor.predict_yield(crop_name, area, soil_type, rainfall, temperature, fertilizer, irrigation)
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        elements.append(Paragraph("Yield Prediction Report", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        elements.append(Paragraph("Input Details:", styles['Heading2']))
        input_data = [
            ["Parameter", "Value"],
            ["Crop", crop_name],
            ["Area", f"{area} Hectares"],
            ["Soil Type", soil_type],
            ["Rainfall", f"{rainfall} mm"],
            ["Temperature", f"{temperature} C"],
            ["Fertilizer", f"{fertilizer} kg/ha"],
            ["Irrigation", irrigation]
        ]
        t = Table(input_data)
        t.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        elements.append(t)
        elements.append(Spacer(1, 24))
        
        elements.append(Paragraph("Predicted Yield:", styles['Heading2']))
        elements.append(Paragraph(f"{prediction} Quintals", styles['Heading1']))
        elements.append(Paragraph("This is an estimate based on historical data and current conditions.", styles['Normal']))
        
        doc.build(elements)
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
        
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}")

@login_required
def detect_disease(request):
    if request.method == 'POST':
        print("DEBUG: detect_disease POST data:", request.POST)
        print("DEBUG: detect_disease FILES data:", request.FILES)
        
        # Optional fields
        plant_age = request.POST.get('plant_age')
        affected_area = request.POST.get('affected_area')
        
        # Get crop name from either form
        crop_name = request.POST.get('crop_name') or request.POST.get('crop_name_symptoms')
        
        print(f"DEBUG: Extra Disease Inputs - Plant Age: {plant_age}, Affected Area: {affected_area}, Crop: {crop_name}")

        if 'image' in request.FILES:
            image = request.FILES['image']
            
            # Save the image temporarily
            from django.core.files.storage import FileSystemStorage
            fs = FileSystemStorage()
            filename = fs.save(image.name, image)
            file_path = fs.path(filename)
            
            print(f"DEBUG: Image saved to {file_path}")
            
            # Run prediction
            result = disease_predictor.predict_from_image(file_path, crop_name)
            
            # Save Log
            if request.user.is_authenticated:
                DiseaseLog.objects.create(
                    user=request.user,
                    crop_name=crop_name,
                    symptoms="Image Upload",
                    predicted_disease=result.get('disease', 'Unknown'),
                    confidence=result.get('confidence', 0.0)
                )
            
            # Pass crop name back to template
            result['crop_name'] = crop_name
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'status': 'success',
                    'result': result
                })
                
            return render(request, 'crops/disease_result.html', {'result': result})
            
        elif 'symptoms' in request.POST:
            symptoms = request.POST.get('symptoms')
            result = disease_predictor.predict_from_symptoms(symptoms, crop_name)
            
            # Save Log
            if request.user.is_authenticated:
                DiseaseLog.objects.create(
                    user=request.user,
                    crop_name=crop_name,
                    symptoms=symptoms,
                    predicted_disease=result.get('disease', 'Unknown'),
                    confidence=result.get('confidence', 0.0)
                )
            
            # Pass crop name back to template
            result['crop_name'] = crop_name
            return render(request, 'crops/disease_result.html', {'result': result})
            
    return render(request, 'crops/disease_form.html')

@login_required
def download_disease_pdf(request):
    try:
        disease = request.GET.get('disease', 'Unknown')
        confidence = float(request.GET.get('confidence', 0))
        description = request.GET.get('description', '')
        treatment = request.GET.get('treatment', '')
        crop_name = request.GET.get('crop_name', '')
        
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # Title
        elements.append(Paragraph("Disease Detection Report", styles['Title']))
        elements.append(Spacer(1, 12))
        elements.append(Paragraph(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M')}", styles['Normal']))
        elements.append(Spacer(1, 24))
        
        # Result
        elements.append(Paragraph("Analysis Result:", styles['Heading2']))
        if crop_name:
            elements.append(Paragraph(f"Crop: {crop_name}", styles['Heading3']))
            
        elements.append(Paragraph(f"Detected Disease: {disease}", styles['Heading3']))
        elements.append(Paragraph(f"Confidence Level: {confidence:.2f}", styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Description
        elements.append(Paragraph("Description:", styles['Heading3']))
        elements.append(Paragraph(description, styles['Normal']))
        elements.append(Spacer(1, 12))
        
        # Treatment
        elements.append(Paragraph("Recommended Treatment & Precautions:", styles['Heading3']))
        # Split treatment by period or newlines if possible, otherwise just paragraph
        elements.append(Paragraph(treatment, styles['Normal']))
        
        elements.append(Spacer(1, 24))
        elements.append(Paragraph("Disclaimer: This is an AI-based prediction. Please consult an agricultural expert for confirmation.", styles['Italic']))
        
        doc.build(elements)
        buffer.seek(0)
        return HttpResponse(buffer, content_type='application/pdf')
        
    except Exception as e:
        return HttpResponse(f"Error generating PDF: {str(e)}")
