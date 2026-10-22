# backend/main.py - Enhanced version with Gemini AI integration

from fastapi import FastAPI, HTTPException, File, UploadFile, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import numpy as np
import logging
import json
import os
import google.generativeai as genai
from PIL import Image
import io
import base64
from typing import List, Dict, Optional
import aiofiles
import uuid
from datetime import datetime
import random

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini AI
GEMINI_API_KEY = "AIzaSyAEaM0g-BSk9vCgxhidXX51ZHmo3Vy2Luc"
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-pro-vision')

# Create FastAPI app
app = FastAPI(
    title="AgriSmart AI Platform",
    description="Complete agricultural platform with crop prediction, weather, disease detection, and store",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files for uploaded images
os.makedirs("uploads", exist_ok=True)
os.makedirs("data", exist_ok=True)
app.mount("/uploads", StaticFiles(directory="uploads"), name="uploads")

# Pydantic Models
class CropPredictionRequest(BaseModel):
    nitrogen: float
    phosphorous: float
    potassium: float
    ph: float
    state: str
    district: str
    month: str

class WeatherData(BaseModel):
    temperature: float
    humidity: float
    rainfall: float
    wind_speed: float
    uv_index: float

class SoilAnalysis(BaseModel):
    health_score: int
    health_status: str
    issues: List[str]
    npk_ratio: str

class MarketInfo(BaseModel):
    current_price: int
    price_trend: str
    demand: str

class CropPredictionResponse(BaseModel):
    predicted_crop: str
    confidence: float
    weather_data: WeatherData
    recommendations: List[str]
    alternative_crops: List[str]
    soil_analysis: SoilAnalysis
    market_info: MarketInfo

class DiseaseSymptom(BaseModel):
    symptoms: List[str]
    treatment: List[str]
    prevention: List[str]

class DiseaseDetectionResponse(BaseModel):
    disease: Dict
    additional_info: Dict

class Product(BaseModel):
    id: int
    name: str
    price: float
    category: str
    description: str
    image_url: str
    rating: float
    stock: int

class WeatherForecastDay(BaseModel):
    day: str
    temperature: int
    condition: str
    rain_chance: int
    humidity: int

# Store data initialization
def initialize_store_data():
    """Initialize store with agricultural products"""
    products = [
        {
            "id": 1, "name": "Premium Rice Seeds", "price": 450.0, "category": "Seeds",
            "description": "High-yielding basmati rice seeds, disease resistant",
            "image_url": "https://images.unsplash.com/photo-1586201375761-83865001e31c?w=300&h=200&fit=crop",
            "rating": 4.5, "stock": 100
        },
        {
            "id": 2, "name": "Wheat Seeds (HD-2967)", "price": 380.0, "category": "Seeds",
            "description": "Drought-resistant wheat variety with high protein content",
            "image_url": "https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=300&h=200&fit=crop",
            "rating": 4.7, "stock": 85
        },
        {
            "id": 3, "name": "Organic Neem Pesticide", "price": 245.0, "category": "Pesticides",
            "description": "100% organic neem-based pesticide, safe for all crops",
            "image_url": "https://images.unsplash.com/photo-1416879595882-3373a0480b5b?w=300&h=200&fit=crop",
            "rating": 4.3, "stock": 150
        },
        {
            "id": 4, "name": "NPK Fertilizer (19:19:19)", "price": 890.0, "category": "Fertilizers",
            "description": "Balanced NPK fertilizer for all crops, 50kg bag",
            "image_url": "https://images.unsplash.com/photo-1560493676-04071c5f467b?w=300&h=200&fit=crop",
            "rating": 4.6, "stock": 75
        },
        {
            "id": 5, "name": "Drip Irrigation Kit", "price": 2850.0, "category": "Equipment",
            "description": "Complete drip irrigation system for 1 acre",
            "image_url": "https://images.unsplash.com/photo-1574483750165-3d6b1e9e3b84?w=300&h=200&fit=crop",
            "rating": 4.8, "stock": 25
        },
        {
            "id": 6, "name": "Cotton Seeds (Bt Cotton)", "price": 950.0, "category": "Seeds",
            "description": "Genetically modified cotton seeds with pest resistance",
            "image_url": "https://images.unsplash.com/photo-1445149657058-297488a54e87?w=300&h=200&fit=crop",
            "rating": 4.4, "stock": 60
        },
        {
            "id": 7, "name": "Fungicide Spray", "price": 325.0, "category": "Pesticides",
            "description": "Broad-spectrum fungicide for disease prevention",
            "image_url": "https://images.unsplash.com/photo-1584464491033-06628f3a6b7b?w=300&h=200&fit=crop",
            "rating": 4.2, "stock": 120
        },
        {
            "id": 8, "name": "Soil pH Meter", "price": 1250.0, "category": "Equipment",
            "description": "Digital soil pH and moisture meter",
            "image_url": "https://images.unsplash.com/photo-1530836369250-ef72a3f5cda8?w=300&h=200&fit=crop",
            "rating": 4.5, "stock": 40
        }
    ]
    
    with open("data/products.json", "w") as f:
        json.dump(products, f, indent=2)
    
    return products

# Initialize store data
store_products = initialize_store_data()

# API Routes

@app.get("/")
async def root():
    return {
        "message": "AgriSmart AI Platform API",
        "version": "2.0.0",
        "features": [
            "Crop Prediction with ML",
            "Weather Forecasting",
            "AI Disease Detection with Gemini",
            "Agricultural E-commerce Store"
        ]
    }

@app.post("/predict", response_model=CropPredictionResponse)
async def predict_crop(request: CropPredictionRequest):
    """Enhanced crop prediction with detailed analysis"""
    try:
        logger.info(f"Crop prediction request for {request.state}, {request.district}")
        
        # Make prediction using enhanced logic
        prediction_result = enhanced_crop_prediction(request)
        
        # Generate weather data
        weather = generate_detailed_weather(request.state, request.district, request.month)
        
        # Generate soil analysis
        soil_analysis = analyze_soil_conditions(request)
        
        # Generate market information
        market_info = get_market_information(prediction_result['crop'])
        
        # Generate recommendations
        recommendations = generate_smart_recommendations(
            prediction_result['crop'], request, weather, soil_analysis
        )
        
        # Generate alternatives
        alternatives = generate_crop_alternatives(request)
        
        response = CropPredictionResponse(
            predicted_crop=prediction_result['crop'],
            confidence=prediction_result['confidence'],
            weather_data=WeatherData(**weather),
            soil_analysis=SoilAnalysis(**soil_analysis),
            market_info=MarketInfo(**market_info),
            recommendations=recommendations,
            alternative_crops=alternatives
        )
        
        logger.info(f"Prediction successful: {prediction_result['crop']}")
        return response
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail="Error making prediction. Please try again")

def enhanced_crop_prediction(data: CropPredictionRequest) -> Dict:
    """Enhanced crop prediction logic with more parameters"""
    nitrogen, phosphorous, potassium, ph, month = data.nitrogen, data.phosphorous, data.potassium, data.ph, data.month
    
    # Calculate nutrient ratios
    npk_sum = nitrogen + phosphorous + potassium
    n_ratio = nitrogen / npk_sum if npk_sum > 0 else 0
    p_ratio = phosphorous / npk_sum if npk_sum > 0 else 0
    k_ratio = potassium / npk_sum if npk_sum > 0 else 0
    
    # Seasonal factors
    kharif_months = ['JUN', 'JUL', 'AUG', 'SEP']
    rabi_months = ['NOV', 'DEC', 'JAN', 'FEB']
    summer_months = ['MAR', 'APR', 'MAY']
    
    crop_scores = {}
    
    # Rice scoring
    rice_score = 0
    if month in kharif_months: rice_score += 30
    if nitrogen >= 80: rice_score += 25
    if ph <= 7.0: rice_score += 20
    if 5.5 <= ph <= 7.0: rice_score += 15
    crop_scores['rice'] = rice_score
    
    # Wheat scoring
    wheat_score = 0
    if month in rabi_months: wheat_score += 30
    if nitrogen >= 60: wheat_score += 20
    if ph >= 6.0: wheat_score += 20
    if phosphorous >= 40: wheat_score += 15
    crop_scores['wheat'] = wheat_score
    
    # Cotton scoring
    cotton_score = 0
    if month in kharif_months: cotton_score += 25
    if potassium >= 50: cotton_score += 30
    if nitrogen >= 70: cotton_score += 20
    if ph >= 5.8: cotton_score += 15
    crop_scores['cotton'] = cotton_score
    
    # Sugarcane scoring
    sugarcane_score = 0
    if month in ['MAR', 'APR', 'MAY', 'JUN']: sugarcane_score += 25
    if nitrogen >= 100: sugarcane_score += 35
    if potassium >= 60: sugarcane_score += 20
    crop_scores['sugarcane'] = sugarcane_score
    
    # Maize scoring
    maize_score = 0
    if month in kharif_months or month in summer_months: maize_score += 20
    if nitrogen >= 80: maize_score += 25
    if potassium >= 40: maize_score += 20
    if 6.0 <= ph <= 7.5: maize_score += 20
    crop_scores['maize'] = maize_score
    
    # Find best crop
    best_crop = max(crop_scores, key=crop_scores.get)
    max_score = crop_scores[best_crop]
    
    # Calculate confidence
    confidence = min(0.95, max(0.60, max_score / 100))
    
    return {
        'crop': best_crop,
        'confidence': confidence
    }

def generate_detailed_weather(state: str, district: str, month: str) -> Dict:
    """Generate detailed weather data with state-specific adjustments"""
    base_data = {
        'JAN': {'temp': 18, 'humidity': 45, 'rainfall': 8, 'wind': 8, 'uv': 4},
        'FEB': {'temp': 22, 'humidity': 40, 'rainfall': 12, 'wind': 9, 'uv': 5},
        'MAR': {'temp': 28, 'humidity': 35, 'rainfall': 20, 'wind': 10, 'uv': 7},
        'APR': {'temp': 33, 'humidity': 40, 'rainfall': 35, 'wind': 12, 'uv': 9},
        'MAY': {'temp': 37, 'humidity': 45, 'rainfall': 75, 'wind': 14, 'uv': 10},
        'JUN': {'temp': 32, 'humidity': 75, 'rainfall': 145, 'wind': 16, 'uv': 8},
        'JUL': {'temp': 29, 'humidity': 85, 'rainfall': 195, 'wind': 15, 'uv': 6},
        'AUG': {'temp': 29, 'humidity': 85, 'rainfall': 175, 'wind': 14, 'uv': 6},
        'SEP': {'temp': 31, 'humidity': 80, 'rainfall': 115, 'wind': 12, 'uv': 7},
        'OCT': {'temp': 29, 'humidity': 70, 'rainfall': 75, 'wind': 10, 'uv': 8},
        'NOV': {'temp': 25, 'humidity': 60, 'rainfall': 35, 'wind': 8, 'uv': 6},
        'DEC': {'temp': 20, 'humidity': 50, 'rainfall': 15, 'wind': 7, 'uv': 4}
    }
    
    data = base_data.get(month, base_data['JAN'])
    
    # State-specific adjustments
    state_adjustments = {
        'RAJASTHAN': {'temp': +3, 'humidity': -10, 'rainfall': -20},
        'KERALA': {'temp': +2, 'humidity': +15, 'rainfall': +50},
        'PUNJAB': {'temp': -2, 'humidity': -5, 'rainfall': -10},
        'MAHARASHTRA': {'temp': +1, 'humidity': +5, 'rainfall': +10},
        'TAMIL NADU': {'temp': +2, 'humidity': +10, 'rainfall': +20},
        'UTTAR PRADESH': {'temp': 0, 'humidity': 0, 'rainfall': 0}
    }
    
    adj = state_adjustments.get(state.upper(), {'temp': 0, 'humidity': 0, 'rainfall': 0})
    
    return {
        'temperature': max(5, data['temp'] + adj['temp'] + random.uniform(-2, 2)),
        'humidity': max(10, min(95, data['humidity'] + adj['humidity'] + random.uniform(-5, 5))),
        'rainfall': max(0, data['rainfall'] + adj['rainfall'] + random.uniform(-10, 10)),
        'wind_speed': data['wind'] + random.uniform(-2, 2),
        'uv_index': max(1, min(12, data['uv'] + random.uniform(-1, 1)))
    }

def analyze_soil_conditions(data: CropPredictionRequest) -> Dict:
    """Analyze soil health based on NPK and pH values"""
    nitrogen, phosphorous, potassium, ph = data.nitrogen, data.phosphorous, data.potassium, data.ph
    
    # Calculate health score
    health_score = 0
    issues = []
    
    # pH analysis
    if 6.0 <= ph <= 7.5:
        health_score += 25
    elif 5.5 <= ph < 6.0 or 7.5 < ph <= 8.0:
        health_score += 15
        issues.append("pH slightly out of optimal range")
    else:
        health_score += 5
        if ph < 5.5:
            issues.append("Soil too acidic - consider liming")
        else:
            issues.append("Soil too alkaline - consider sulfur addition")
    
    # Nitrogen analysis
    if nitrogen >= 80:
        health_score += 25
    elif nitrogen >= 60:
        health_score += 20
    elif nitrogen >= 40:
        health_score += 15
        issues.append("Low nitrogen levels - add organic matter")
    else:
        health_score += 5
        issues.append("Very low nitrogen - urgent fertilization needed")
    
    # Phosphorous analysis
    if phosphorous >= 40:
        health_score += 25
    elif phosphorous >= 25:
        health_score += 20
    elif phosphorous >= 15:
        health_score += 15
        issues.append("Moderate phosphorous deficiency")
    else:
        health_score += 5
        issues.append("Severe phosphorous deficiency")
    
    # Potassium analysis
    if potassium >= 50:
        health_score += 25
    elif potassium >= 35:
        health_score += 20
    elif potassium >= 20:
        health_score += 15
        issues.append("Low potassium levels")
    else:
        health_score += 5
        issues.append("Severe potassium deficiency")
    
    # Determine health status
    if health_score >= 80:
        health_status = "Excellent"
    elif health_score >= 70:
        health_status = "Good"
    elif health_score >= 60:
        health_status = "Fair"
    elif health_score >= 50:
        health_status = "Poor"
    else:
        health_status = "Critical"
    
    # Calculate NPK ratio
    total = nitrogen + phosphorous + potassium
    if total > 0:
        n_ratio = round(nitrogen / total * 100)
        p_ratio = round(phosphorous / total * 100)
        k_ratio = round(potassium / total * 100)
        npk_ratio = f"{n_ratio}:{p_ratio}:{k_ratio}"
    else:
        npk_ratio = "0:0:0"
    
    if not issues:
        issues = ["Soil conditions are optimal"]
    
    return {
        'health_score': health_score,
        'health_status': health_status,
        'issues': issues,
        'npk_ratio': npk_ratio
    }

def get_market_information(crop: str) -> Dict:
    """Generate market information for the predicted crop"""
    market_data = {
        'rice': {'base_price': 2500, 'trend': 'stable', 'demand': 'high'},
        'wheat': {'base_price': 2200, 'trend': 'rising', 'demand': 'high'},
        'cotton': {'base_price': 6500, 'trend': 'volatile', 'demand': 'moderate'},
        'sugarcane': {'base_price': 350, 'trend': 'stable', 'demand': 'high'},
        'maize': {'base_price': 2000, 'trend': 'rising', 'demand': 'moderate'}
    }
    
    base_data = market_data.get(crop, {'base_price': 2000, 'trend': 'stable', 'demand': 'moderate'})
    
    # Add some market volatility
    price_variation = random.uniform(-200, 300)
    current_price = int(base_data['base_price'] + price_variation)
    
    return {
        'current_price': current_price,
        'price_trend': base_data['trend'],
        'demand': base_data['demand']
    }

def generate_smart_recommendations(crop: str, data: CropPredictionRequest, weather: Dict, soil: Dict) -> List[str]:
    """Generate smart farming recommendations"""
    recommendations = []
    
    # Crop-specific recommendations
    crop_advice = {
        'rice': [
            "Maintain water levels at 2-5 cm during vegetative stage",
            "Apply nitrogen in 3 splits: 50% basal, 25% tillering, 25% panicle initiation",
            "Monitor for brown plant hopper and stem borer"
        ],
        'wheat': [
            "Sow at proper depth (5-6 cm) for optimal germination",
            "Apply first irrigation at crown root initiation stage",
            "Monitor for rust diseases during grain filling stage"
        ],
        'cotton': [
            "Maintain proper plant spacing (45x30 cm) for better boll development",
            "Apply potash during square formation stage",
            "Regular monitoring for bollworm and whitefly"
        ],
        'sugarcane': [
            "Plant sets at 45 cm spacing with proper soil contact",
            "Apply high nitrogen during grand growth period",
            "Earthing up at 90 and 120 days after planting"
        ],
        'maize': [
            "Plant at 60x20 cm spacing for optimal plant population",
            "Side-dress nitrogen at knee-high stage",
            "Monitor for fall armyworm during early growth"
        ]
    }
    
    recommendations.extend(crop_advice.get(crop, ["Follow standard agronomic practices"]))
    
    # Weather-based recommendations
    if weather['rainfall'] > 150:
        recommendations.append("Ensure proper drainage to prevent waterlogging")
    elif weather['rainfall'] < 50:
        recommendations.append("Plan irrigation schedule due to low rainfall prediction")
    
    if weather['temperature'] > 35:
        recommendations.append("Consider shade nets or mulching to protect from heat stress")
    
    # Soil-based recommendations
    if soil['health_score'] < 60:
        recommendations.append("Improve soil health with organic matter and balanced fertilization")
    
    if 'acidic' in ' '.join(soil['issues']):
        recommendations.append("Apply lime to correct soil acidity")
    
    if 'alkaline' in ' '.join(soil['issues']):
        recommendations.append("Apply gypsum or sulfur to reduce soil alkalinity")
    
    return recommendations

def generate_crop_alternatives(data: CropPredictionRequest) -> List[str]:
    """Generate alternative crop suggestions"""
    alternatives = []
    
    # Season-based alternatives
    kharif_crops = ['rice', 'cotton', 'sugarcane', 'maize', 'sorghum', 'pearl millet']
    rabi_crops = ['wheat', 'barley', 'chickpea', 'lentil', 'mustard', 'pea']
    summer_crops = ['maize', 'fodder crops', 'vegetables', 'groundnut']
    
    kharif_months = ['JUN', 'JUL', 'AUG', 'SEP']
    rabi_months = ['NOV', 'DEC', 'JAN', 'FEB']
    summer_months = ['MAR', 'APR', 'MAY']
    
    if data.month in kharif_months:
        alternatives.extend(random.sample(kharif_crops, min(3, len(kharif_crops))))
    elif data.month in rabi_months:
        alternatives.extend(random.sample(rabi_crops, min(3, len(rabi_crops))))
    else:
        alternatives.extend(random.sample(summer_crops, min(3, len(summer_crops))))
    
    # Remove duplicates and return up to 4 alternatives
    alternatives = list(set(alternatives))
    return alternatives[:4]

@app.post("/detect-disease")
async def detect_disease(file: UploadFile = File(...)):
    """AI-powered disease detection using Gemini Vision"""
    try:
        logger.info(f"Disease detection request for file: {file.filename}")
        
        # Validate file type
        if not file.content_type.startswith('image/'):
            raise HTTPException(status_code=400, detail="File must be an image")
        
        # Read and process image
        contents = await file.read()
        image = Image.open(io.BytesIO(contents))
        
        # Convert to RGB if needed
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        # Resize image if too large
        max_size = (1024, 1024)
        image.thumbnail(max_size, Image.Resampling.LANCZOS)
        
        # Save image for reference
        filename = f"disease_{uuid.uuid4().hex[:8]}.jpg"
        filepath = f"uploads/{filename}"
        image.save(filepath)
        
        # Analyze with Gemini
        prompt = """
        Analyze this plant image for diseases or health issues. Please provide:
        1. Disease identification (if any)
        2. Symptoms observed
        3. Confidence level
        4. Treatment recommendations
        5. Prevention measures
        6. Severity level (mild/moderate/severe)
        
        If no disease is detected, mention the plant appears healthy.
        Format your response as a detailed analysis for farmers.
        """
        
        response = model.generate_content([prompt, image])
        analysis = response.text
        
        # Parse the AI response into structured data
        disease_info = parse_disease_analysis(analysis)
        
        # Add image URL
        disease_info['image_url'] = f"/uploads/{filename}"
        disease_info['timestamp'] = datetime.now().isoformat()
        
        # Additional agricultural context
        additional_info = {
            'general_tips': [
                "Ensure proper plant spacing for air circulation",
                "Avoid overhead watering to reduce leaf wetness",
                "Remove infected plant debris regularly",
                "Rotate crops to break disease cycles"
            ],
            'when_to_spray': "Early morning or evening for better effectiveness",
            'monitoring_frequency': "Check plants every 2-3 days for early detection"
        }
        
        return DiseaseDetectionResponse(
            disease=disease_info,
            additional_info=additional_info
        )
        
    except Exception as e:
        logger.error(f"Disease detection error: {e}")
        raise HTTPException(status_code=500, detail=f"Analysis failed: {str(e)}")

def parse_disease_analysis(analysis: str) -> Dict:
    """Parse AI analysis into structured format"""
    # This is a simplified parser - in production, you'd want more sophisticated NLP
    lines = analysis.split('\n')
    
    result = {
        'name': 'Unknown',
        'confidence': 0.8,
        'severity': 'moderate',
        'symptoms': [],
        'treatment': [],
        'prevention': [],
        'description': analysis
    }
    
    # Extract key information using simple keyword matching
    analysis_lower = analysis.lower()
    
    # Common plant diseases
    diseases = ['blight', 'rust', 'mildew', 'spot', 'rot', 'wilt', 'mosaic', 'scab']
    for disease in diseases:
        if disease in analysis_lower:
            result['name'] = disease.title()
            break
    
    # Check if plant appears healthy
    if any(word in analysis_lower for word in ['healthy', 'no disease', 'appears normal']):
        result['name'] = 'Healthy Plant'
        result['severity'] = 'none'
        result['symptoms'] = ['Plant appears healthy with no visible disease symptoms']
        result['treatment'] = ['No treatment required - continue regular care']
        result['prevention'] = ['Maintain current good agricultural practices']
    
    # Extract symptoms (simplified)
    if 'symptom' in analysis_lower:
        result['symptoms'] = [
            'Visible symptoms detected in plant tissue',
            'Refer to full analysis for detailed symptom description'
        ]
    
    # Extract treatment recommendations
    if any(word in analysis_lower for word in ['spray', 'fungicide', 'treatment', 'apply']):
        result['treatment'] = [
            'Follow integrated pest management practices',
            'Consider appropriate fungicide or pesticide application',
            'Consult local agricultural extension for specific products'
        ]
    
    # Extract prevention measures
    result['prevention'] = [
        'Maintain proper plant spacing',
        'Ensure adequate drainage',
        'Use disease-resistant varieties when possible',
        'Practice crop rotation'
    ]
    
    return result

@app.get("/weather/{state}/{district}")
async def get_weather_forecast(state: str, district: str):
    """Get 7-day weather forecast for a location"""
    try:
        forecast = []
        days = ['Today', 'Tomorrow', 'Day 3', 'Day 4', 'Day 5', 'Day 6', 'Day 7']
        conditions = ['Sunny', 'Partly Cloudy', 'Cloudy', 'Rainy', 'Thunderstorm']
        
        base_temp = random.randint(25, 35)
        
        for i, day in enumerate(days):
            temp_variation = random.randint(-3, 5)
            forecast.append({
                'day': day,
                'temperature': base_temp + temp_variation,
                'condition': random.choice(conditions),
                'rain_chance': random.randint(10, 90),
                'humidity': random.randint(40, 85)
            })
        
        return {
            'location': f"{district}, {state}",
            'forecast': forecast,
            'last_updated': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Weather forecast error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Store API endpoints
@app.get("/store/products")
async def get_products(category: Optional[str] = None):
    """Get all products or filter by category"""
    try:
        with open("data/products.json", "r") as f:
            products = json.load(f)
        
        if category:
            products = [p for p in products if p['category'].lower() == category.lower()]
        
        return {
            'products': products,
            'total': len(products),
            'categories': list(set([p['category'] for p in products]))
        }
        
    except Exception as e:
        logger.error(f"Products fetch error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/store/products/{product_id}")
async def get_product(product_id: int):
    """Get a specific product by ID"""
    try:
        with open("data/products.json", "r") as f:
            products = json.load(f)
        
        product = next((p for p in products if p['id'] == product_id), None)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        
        return product
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Product fetch error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/store/categories")
async def get_categories():
    """Get all product categories"""
    try:
        with open("data/products.json", "r") as f:
            products = json.load(f)
        
        categories = list(set([p['category'] for p in products]))
        category_counts = {}
        
        for category in categories:
            count = len([p for p in products if p['category'] == category])
            category_counts[category] = count
        
        return {
            'categories': categories,
            'category_counts': category_counts
        }
        
    except Exception as e:
        logger.error(f"Categories fetch error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/store/search")
async def search_products(q: str, category: Optional[str] = None, min_price: Optional[float] = None, max_price: Optional[float] = None):
    """Search products with filters"""
    try:
        with open("data/products.json", "r") as f:
            products = json.load(f)
        
        # Filter by search query
        if q:
            products = [p for p in products if 
                       q.lower() in p['name'].lower() or 
                       q.lower() in p['description'].lower()]
        
        # Filter by category
        if category:
            products = [p for p in products if p['category'].lower() == category.lower()]
        
        # Filter by price range
        if min_price is not None:
            products = [p for p in products if p['price'] >= min_price]
        
        if max_price is not None:
            products = [p for p in products if p['price'] <= max_price]
        
        return {
            'products': products,
            'total': len(products),
            'query': q,
            'filters': {
                'category': category,
                'min_price': min_price,
                'max_price': max_price
            }
        }
        
    except Exception as e:
        logger.error(f"Product search error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

# Agricultural Knowledge Base
@app.get("/knowledge/crops/{crop_name}")
async def get_crop_info(crop_name: str):
    """Get detailed information about a specific crop"""
    crop_database = {
        'rice': {
            'name': 'Rice',
            'scientific_name': 'Oryza sativa',
            'season': 'Kharif',
            'duration': '120-150 days',
            'water_requirement': 'High (1000-1200mm)',
            'soil_type': 'Clay loam, well water retention',
            'ideal_ph': '5.5-7.0',
            'temperature': '20-35°C',
            'major_varieties': ['Basmati', 'IR64', 'Swarna', 'Sona Masuri'],
            'planting_tips': [
                'Transplant 21-25 days old seedlings',
                'Maintain 2-5cm water level',
                'Plant spacing: 20x15 cm'
            ],
            'fertilizer': {
                'nitrogen': '150-200 kg/ha',
                'phosphorous': '60-80 kg/ha',
                'potassium': '40-60 kg/ha'
            },
            'common_diseases': ['Blast', 'Brown Spot', 'Bacterial Blight'],
            'pests': ['Brown Plant Hopper', 'Stem Borer', 'Leaf Folder']
        },
        'wheat': {
            'name': 'Wheat',
            'scientific_name': 'Triticum aestivum',
            'season': 'Rabi',
            'duration': '120-150 days',
            'water_requirement': 'Medium (450-650mm)',
            'soil_type': 'Well-drained loamy soil',
            'ideal_ph': '6.0-7.5',
            'temperature': '15-25°C',
            'major_varieties': ['HD-2967', 'PBW-343', 'WH-147'],
            'planting_tips': [
                'Sow at 5-6 cm depth',
                'Row spacing: 18-23 cm',
                'Seed rate: 100-125 kg/ha'
            ],
            'fertilizer': {
                'nitrogen': '120-150 kg/ha',
                'phosphorous': '60 kg/ha',
                'potassium': '40 kg/ha'
            },
            'common_diseases': ['Rust', 'Smut', 'Bunt'],
            'pests': ['Aphids', 'Termites', 'Cut worms']
        },
        'cotton': {
            'name': 'Cotton',
            'scientific_name': 'Gossypium spp.',
            'season': 'Kharif',
            'duration': '180-200 days',
            'water_requirement': 'Medium (700-800mm)',
            'soil_type': 'Well-drained black cotton soil',
            'ideal_ph': '5.8-8.0',
            'temperature': '21-35°C',
            'major_varieties': ['Bt Cotton', 'Hybrid varieties'],
            'planting_tips': [
                'Plant spacing: 45x30 cm',
                'Sow 2-3 cm deep',
                'Ensure proper drainage'
            ],
            'fertilizer': {
                'nitrogen': '150-200 kg/ha',
                'phosphorous': '60-80 kg/ha',
                'potassium': '60-80 kg/ha'
            },
            'common_diseases': ['Fusarium Wilt', 'Verticillium Wilt', 'Bacterial Blight'],
            'pests': ['Bollworm', 'Whitefly', 'Thrips']
        }
    }
    
    crop_info = crop_database.get(crop_name.lower())
    if not crop_info:
        raise HTTPException(status_code=404, detail="Crop information not found")
    
    return crop_info

@app.get("/knowledge/diseases")
async def get_disease_info():
    """Get information about common plant diseases"""
    diseases = {
        'fungal': [
            {
                'name': 'Powdery Mildew',
                'symptoms': 'White powdery spots on leaves',
                'treatment': 'Fungicide spray, improve air circulation',
                'prevention': 'Avoid overhead watering, proper spacing'
            },
            {
                'name': 'Rust',
                'symptoms': 'Orange/brown pustules on leaves',
                'treatment': 'Copper-based fungicides',
                'prevention': 'Use resistant varieties, crop rotation'
            }
        ],
        'bacterial': [
            {
                'name': 'Bacterial Blight',
                'symptoms': 'Water-soaked lesions on leaves',
                'treatment': 'Copper spray, remove infected plants',
                'prevention': 'Use certified seeds, avoid mechanical damage'
            }
        ],
        'viral': [
            {
                'name': 'Mosaic Virus',
                'symptoms': 'Mottled yellow-green pattern on leaves',
                'treatment': 'No direct treatment, remove infected plants',
                'prevention': 'Control insect vectors, use virus-free seeds'
            }
        ]
    }
    
    return diseases

@app.get("/agricultural-tips")
async def get_agricultural_tips():
    """Get general agricultural tips and best practices"""
    tips = {
        'soil_management': [
            'Test soil pH and nutrient levels annually',
            'Add organic matter regularly to improve soil structure',
            'Practice crop rotation to maintain soil health',
            'Avoid excessive tillage to prevent soil erosion'
        ],
        'water_management': [
            'Use drip irrigation for water efficiency',
            'Mulch around plants to retain moisture',
            'Collect rainwater for irrigation during dry periods',
            'Monitor soil moisture before watering'
        ],
        'pest_management': [
            'Implement Integrated Pest Management (IPM)',
            'Encourage beneficial insects and natural predators',
            'Use pheromone traps for monitoring',
            'Apply pesticides only when threshold levels are reached'
        ],
        'crop_management': [
            'Select varieties suited to local climate and soil',
            'Follow recommended planting dates',
            'Maintain proper plant spacing for optimal growth',
            'Regular monitoring for early problem detection'
        ],
        'post_harvest': [
            'Harvest at optimal maturity for best quality',
            'Proper drying and storage to prevent losses',
            'Use appropriate packaging for different crops',
            'Maintain cold chain for perishable products'
        ]
    }
    
    return {
        'tips': tips,
        'seasonal_advice': {
            'monsoon': 'Ensure proper drainage, monitor for fungal diseases',
            'winter': 'Protect sensitive crops from frost, adjust irrigation',
            'summer': 'Increase irrigation frequency, use shade nets if needed',
            'pre_monsoon': 'Prepare fields, clean drainage channels'
        }
    }

# Market and Price Information
@app.get("/market/prices/{crop}")
async def get_market_prices(crop: str, state: Optional[str] = None):
    """Get current market prices for crops"""
    # This would typically connect to government APIs like eNAM
    # For demo purposes, we'll generate sample data
    
    base_prices = {
        'rice': 2500,
        'wheat': 2200,
        'cotton': 6500,
        'sugarcane': 350,
        'maize': 2000,
        'soybean': 4500,
        'onion': 2000,
        'potato': 1500,
        'tomato': 3000
    }
    
    base_price = base_prices.get(crop.lower(), 2000)
    
    # Generate price data for different markets
    markets = ['Delhi', 'Mumbai', 'Chennai', 'Kolkata', 'Bangalore', 'Hyderabad']
    if state:
        markets = [f"{state} Local Market", f"{state} Wholesale", f"{state} Retail"]
    
    price_data = []
    for market in markets:
        variation = random.uniform(-300, 500)
        price_data.append({
            'market': market,
            'price_per_quintal': int(base_price + variation),
            'date': datetime.now().strftime('%Y-%m-%d'),
            'trend': random.choice(['rising', 'falling', 'stable'])
        })
    
    return {
        'crop': crop.title(),
        'prices': price_data,
        'average_price': int(np.mean([p['price_per_quintal'] for p in price_data])),
        'last_updated': datetime.now().isoformat()
    }

# Fertilizer Calculator
class FertilizerRequest(BaseModel):
    crop: str
    area: float  # in hectares
    soil_test_n: Optional[float] = None
    soil_test_p: Optional[float] = None
    soil_test_k: Optional[float] = None
    target_yield: Optional[float] = None

@app.post("/calculate-fertilizer")
async def calculate_fertilizer(request: FertilizerRequest):
    """Calculate fertilizer requirements based on crop and soil test"""
    
    # Standard fertilizer requirements (kg/ha)
    fertilizer_requirements = {
        'rice': {'N': 150, 'P': 60, 'K': 40},
        'wheat': {'N': 120, 'P': 60, 'K': 40},
        'cotton': {'N': 150, 'P': 75, 'K': 75},
        'maize': {'N': 120, 'P': 60, 'K': 60},
        'sugarcane': {'N': 200, 'P': 80, 'K': 100}
    }
    
    crop_req = fertilizer_requirements.get(request.crop.lower(), 
                                         {'N': 100, 'P': 50, 'K': 50})
    
    # Adjust for soil test results if provided
    if request.soil_test_n:
        crop_req['N'] = max(0, crop_req['N'] - request.soil_test_n)
    if request.soil_test_p:
        crop_req['P'] = max(0, crop_req['P'] - request.soil_test_p)
    if request.soil_test_k:
        crop_req['K'] = max(0, crop_req['K'] - request.soil_test_k)
    
    # Calculate total requirements
    total_n = crop_req['N'] * request.area
    total_p = crop_req['P'] * request.area
    total_k = crop_req['K'] * request.area
    
    # Convert to common fertilizers
    urea_needed = total_n / 0.46  # Urea contains 46% N
    dap_needed = min(total_p / 0.46, total_n / 0.18)  # DAP contains 46% P2O5, 18% N
    mop_needed = total_k / 0.60  # MOP contains 60% K2O
    
    # Adjust for DAP's nitrogen contribution
    remaining_n = max(0, total_n - (dap_needed * 0.18))
    urea_for_remaining_n = remaining_n / 0.46
    
    return {
        'crop': request.crop.title(),
        'area': request.area,
        'nutrient_requirements': {
            'nitrogen': total_n,
            'phosphorus': total_p,
            'potassium': total_k
        },
        'fertilizer_recommendations': {
            'urea_kg': round(urea_for_remaining_n, 1),
            'dap_kg': round(dap_needed, 1),
            'mop_kg': round(mop_needed, 1)
        },
        'application_schedule': {
            'basal': '50% N, 100% P, 50% K at planting',
            'first_top_dress': '25% N at 30-35 days',
            'second_top_dress': '25% N + 50% K at 60-65 days'
        },
        'estimated_cost': {
            'urea': round(urea_for_remaining_n * 6, 2),  # ₹6 per kg
            'dap': round(dap_needed * 25, 2),  # ₹25 per kg
            'mop': round(mop_needed * 15, 2),  # ₹15 per kg
            'total': round((urea_for_remaining_n * 6) + (dap_needed * 25) + (mop_needed * 15), 2)
        }
    }

# Irrigation Calculator
class IrrigationRequest(BaseModel):
    crop: str
    area: float
    soil_type: str
    growth_stage: str
    days_since_rain: int
    temperature: float

@app.post("/calculate-irrigation")
async def calculate_irrigation(request: IrrigationRequest):
    """Calculate irrigation requirements"""
    
    # Base water requirements (mm/day) for different crops
    base_water_req = {
        'rice': 8.0,
        'wheat': 4.5,
        'cotton': 5.5,
        'maize': 5.0,
        'sugarcane': 7.0,
        'vegetables': 4.0
    }
    
    # Growth stage multipliers
    stage_multiplier = {
        'seedling': 0.7,
        'vegetative': 1.0,
        'flowering': 1.3,
        'maturity': 0.8
    }
    
    # Soil type multipliers (based on water holding capacity)
    soil_multiplier = {
        'sandy': 1.3,
        'loamy': 1.0,
        'clay': 0.8
    }
    
    crop_req = base_water_req.get(request.crop.lower(), 5.0)
    stage_mult = stage_multiplier.get(request.growth_stage.lower(), 1.0)
    soil_mult = soil_multiplier.get(request.soil_type.lower(), 1.0)
    
    # Temperature adjustment
    temp_mult = 1.0
    if request.temperature > 35:
        temp_mult = 1.2
    elif request.temperature < 20:
        temp_mult = 0.8
    
    daily_req_mm = crop_req * stage_mult * soil_mult * temp_mult
    
    # Calculate irrigation needed based on days since rain
    total_water_needed = daily_req_mm * request.days_since_rain
    
    # Convert to liters per hectare (1mm = 10,000 L/ha)
    water_per_ha = total_water_needed * 10000
    total_water_needed_area = water_per_ha * request.area
    
    return {
        'crop': request.crop.title(),
        'area': request.area,
        'daily_requirement_mm': round(daily_req_mm, 2),
        'total_water_needed': {
            'mm': round(total_water_needed, 1),
            'liters_per_hectare': round(water_per_ha, 0),
            'total_liters': round(total_water_needed_area, 0)
        },
        'irrigation_schedule': {
            'frequency': f"Every {max(1, int(15/daily_req_mm))} days",
            'duration_per_session': "2-4 hours depending on irrigation method",
            'best_time': "Early morning (6-8 AM) or evening (6-8 PM)"
        },
        'water_saving_tips': [
            'Use drip or sprinkler irrigation for better efficiency',
            'Mulch around plants to reduce evaporation',
            'Monitor soil moisture before irrigation',
            'Avoid irrigation during windy conditions'
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)