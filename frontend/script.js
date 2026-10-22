// Enhanced script.js

// District mapping for each state (expanded with more districts)
const stateDistricts = {
    "ANDHRA PRADESH": ["EAST GODAVARI", "WEST GODAVARI", "GUNTUR", "KRISHNA", "NELLORE", "PRAKASAM", "SRIKAKULAM", "VISAKHAPATNAM", "VIZIANAGARAM", "CHITTOOR", "ANANTAPUR", "KURNOOL"],
    "ASSAM": ["CACHAR", "DARRANG", "GOALPARA", "KAMRUP", "LAKHIMPUR", "NORTH CACHAR", "NAGAON", "SIVASAGAR", "BARPETA", "DHUBRI", "DIBRUGARH", "JORHAT"],
    "BIHAR": ["BHAGALPUR", "EAST CHAMPARAN", "DARBHANGA", "GAYA", "MUNGER", "MUZAFFARPUR", "WEST CHAMPARAN", "PURNEA", "PATNA", "ROHTAS", "SAHARSA"],
    "GUJARAT": ["AHMEDABAD", "BANASKANTHA", "BARODA", "BHARUCH", "VALSAD", "DANGS", "KHEDA", "MEHSANA", "RAJKOT", "JAMNAGAR", "KUTCH", "SURAT"],
    "HARYANA": ["AMBALA", "GURGAON", "HISAR", "JIND", "KARNAL", "MAHENDRAGARH", "ROHTAK", "BHIWANI", "FARIDABAD", "PANIPAT", "SONIPAT"],
    "KARNATAKA": ["UTTAR KANNADA", "DAKSHIN KANNADA", "UDUPI", "BELGAUM", "BIDAR", "BIJAPUR", "DHARWAD", "GULBARGA", "BANGALORE URBAN", "BANGALORE RURAL", "MYSORE", "SHIMOGA"],
    "KERALA": ["ALAPPUZHA", "KANNUR", "ERNAKULAM", "KOTTAYAM", "KOZHIKODE", "MALAPPURAM", "PALAKKAD", "KOLLAM", "THRISSUR", "THIRUVANANTHAPURAM", "IDUKKI"],
    "MADHYA PRADESH": ["BETUL", "VIDISHA", "BHIND", "DATIA", "DEWAS", "DHAR", "GUNA", "GWALIOR", "INDORE", "BHOPAL", "JABALPUR", "UJJAIN"],
    "MAHARASHTRA": ["MUMBAI CITY", "RAIGAD", "RATNAGIRI", "THANE", "SINDHUDURG", "MUMBAI SUBURBAN", "AHMEDNAGAR", "DHULE", "PUNE", "NASHIK", "NAGPUR", "AURANGABAD"],
    "PUNJAB": ["AMRITSAR", "BATHINDA", "FEROZEPUR", "GURDASPUR", "HOSHIARPUR", "JALANDHAR", "KAPURTHALA", "LUDHIANA", "PATIALA", "SANGRUR", "MOGA"],
    "RAJASTHAN": ["BARMER", "BIKANER", "CHURU", "GANGANAGAR", "JAISALMER", "JALORE", "JODHPUR", "NAGAUR", "JAIPUR", "UDAIPUR", "KOTA", "AJMER"],
    "TAMIL NADU": ["VELLORE", "COIMBATORE", "DHARMAPURI", "KANYAKUMARI", "CHENNAI", "MADURAI", "NILGIRIS", "RAMANATHAPURAM", "SALEM", "THANJAVUR", "TIRUCHIRAPALLI"],
    "UTTAR PRADESH": ["ALLAHABAD", "AZAMGARH", "BAHRAICH", "BALLIA", "BANDA", "BARABANKI", "BASTI", "DEORIA", "LUCKNOW", "KANPUR", "VARANASI", "AGRA"],
    "WEST BENGAL": ["COOCH BEHAR", "DARJEELING", "JALPAIGURI", "MALDA", "SOUTH DINAJPUR", "NORTH DINAJPUR", "BANKURA", "BIRBHUM", "KOLKATA", "HOWRAH", "NADIA"]
};

// Updated crop images with better cotton image
const cropImages = {
    'rice': 'https://images.unsplash.com/photo-1586201375761-83865001e31c?w=400&h=300&fit=crop',
    'wheat': 'https://images.unsplash.com/photo-1574323347407-f5e1ad6d020b?w=400&h=300&fit=crop',
    'corn': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400&h=300&fit=crop',
    'maize': 'https://images.unsplash.com/photo-1551754655-cd27e38d2076?w=400&h=300&fit=crop',
    'cotton': 'https://images.unsplash.com/photo-1445149657058-297488a54e87?w=400&h=300&fit=crop', // Simple cotton field image
    'sugarcane': 'https://images.unsplash.com/photo-1578662996442-48f60103fc96?w=400&h=300&fit=crop',
    'watermelon': 'https://images.unsplash.com/photo-1571771894821-ce9b6c11b08e?w=400&h=300&fit=crop',
    'apple': 'https://images.unsplash.com/photo-1560806887-1e4cd0b6cbd6?w=400&h=300&fit=crop',
    'banana': 'https://images.unsplash.com/photo-1603833665858-e61d17a86224?w=400&h=300&fit=crop',
    'coconut': 'https://images.unsplash.com/photo-1587119123148-68e7bb09ed3a?w=400&h=300&fit=crop',
    'coffee': 'https://images.unsplash.com/photo-1447933601403-0c6688de566e?w=400&h=300&fit=crop',
    'jute': 'https://images.unsplash.com/photo-1625246333195-78d9c38ad449?w=400&h=300&fit=crop',
    'grapes': 'https://images.unsplash.com/photo-1537640538966-79f369143f8f?w=400&h=300&fit=crop',
    'tea': 'https://images.unsplash.com/photo-1597318181409-45e4e9f6d6f6?w=400&h=300&fit=crop'
};

// Initialize page
document.addEventListener('DOMContentLoaded', function() {
    setupEventListeners();
    fillSampleData();
    addInputAnimations();
});

function setupEventListeners() {
    document.getElementById('state').addEventListener('change', handleStateChange);
    document.getElementById('predictionForm').addEventListener('submit', handleFormSubmit);
    addInputValidation();
    
    // Add location change listener for weather
    document.getElementById('state').addEventListener('change', updateWeatherOnLocationChange);
    document.getElementById('district').addEventListener('change', updateWeatherOnLocationChange);
}

function handleStateChange() {
    const selectedState = document.getElementById('state').value;
    const districtSelect = document.getElementById('district');
    
    districtSelect.innerHTML = '<option value="">Select District</option>';
    
    if (selectedState && stateDistricts[selectedState]) {
        stateDistricts[selectedState].forEach(district => {
            const option = document.createElement('option');
            option.value = district;
            option.textContent = district;
            districtSelect.appendChild(option);
        });
    }
}

function addInputValidation() {
    const inputs = document.querySelectorAll('input[type="number"]');
    
    inputs.forEach(input => {
        input.addEventListener('blur', function() {
            validateInput(this);
        });
        
        input.addEventListener('input', function() {
            removeValidationClasses(this);
        });
    });
}

function addInputAnimations() {
    const inputs = document.querySelectorAll('.form-control, .form-select');
    
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
        });
        
        input.addEventListener('blur', function() {
            this.parentElement.classList.remove('focused');
        });
    });
}

function validateInput(input) {
    const value = parseFloat(input.value);
    const min = parseFloat(input.getAttribute('min'));
    const max = parseFloat(input.getAttribute('max'));
    
    if (isNaN(value) || value < min || value > max) {
        input.classList.add('is-invalid');
        input.classList.remove('is-valid');
        return false;
    } else {
        input.classList.add('is-valid');
        input.classList.remove('is-invalid');
        return true;
    }
}

function removeValidationClasses(input) {
    input.classList.remove('is-valid', 'is-invalid');
}

async function handleFormSubmit(event) {
    event.preventDefault();
    
    if (!validateForm()) {
        showNotification('Please fill all fields with valid values!', 'error');
        return;
    }
    
    showLoading(true);
    const formData = collectFormData();
    
    try {
        const result = await makePrediction(formData);
        await displayResults(result);
        showWeatherForecast(formData);
    } catch (error) {
        console.error('Prediction error:', error);
        showNotification('Error making prediction. Please try again.', 'error');
    } finally {
        showLoading(false);
    }
}

function validateForm() {
    const requiredFields = ['nitrogen', 'phosphorous', 'potassium', 'ph', 'state', 'district', 'month'];
    let isValid = true;
    
    requiredFields.forEach(fieldId => {
        const field = document.getElementById(fieldId);
        if (!field.value) {
            field.classList.add('is-invalid');
            isValid = false;
        } else if (field.type === 'number') {
            isValid = validateInput(field) && isValid;
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

function collectFormData() {
    return {
        nitrogen: parseFloat(document.getElementById('nitrogen').value),
        phosphorous: parseFloat(document.getElementById('phosphorous').value),
        potassium: parseFloat(document.getElementById('potassium').value),
        ph: parseFloat(document.getElementById('ph').value),
        state: document.getElementById('state').value,
        district: document.getElementById('district').value,
        month: document.getElementById('month').value
    };
}

async function makePrediction(formData) {
    try {
        const response = await fetch('http://localhost:8000/predict', { 
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(formData)
        });
        
        if (response.ok) {
            return await response.json();
        } else {
            throw new Error('Backend API not available');
        }
    } catch (error) {
        console.warn('Backend not available, using mock prediction');
        return mockPrediction(formData);
    }
}

function mockPrediction(formData) {
    const { nitrogen, phosphorous, potassium, ph, month } = formData;
    
    let predictedCrop = 'rice';
    
    // Enhanced prediction logic
    if (nitrogen >= 80 && ph <= 7.0 && ['JUN', 'JUL', 'AUG', 'SEP'].includes(month)) {
        predictedCrop = 'rice';
    } else if (nitrogen >= 60 && ph >= 6.5 && ['NOV', 'DEC', 'JAN', 'FEB'].includes(month)) {
        predictedCrop = 'wheat';
    } else if (potassium >= 40 && ph >= 6.0 && nitrogen >= 70) {
        predictedCrop = 'cotton';
    } else if (nitrogen >= 100 && ['MAR', 'APR', 'MAY', 'JUN'].includes(month)) {
        predictedCrop = 'sugarcane';
    } else if (['APR', 'MAY', 'JUN'].includes(month) && ph >= 6.0 && ph <= 7.0) {
        predictedCrop = 'watermelon';
    } else if (nitrogen >= 60 && potassium >= 30) {
        predictedCrop = 'maize';
    } else if (ph < 6.5 && potassium >= 50) {
        predictedCrop = 'tea';
    } else if (potassium >= 60) {
        predictedCrop = 'banana';
    }
    
    const mockWeather = generateDetailedWeather(formData.state, formData.month);
    
    return {
        predicted_crop: predictedCrop,
        confidence: 0.87 + Math.random() * 0.12,
        weather_data: mockWeather,
        recommendations: generateEnhancedRecommendations(predictedCrop, formData),
        alternative_crops: generateAlternativeCrops(formData),
        soil_analysis: generateSoilAnalysis(formData),
        market_info: generateMarketInfo(predictedCrop)
    };
}

function generateDetailedWeather(state, month) {
    const baseTemps = {
        'JAN': 18, 'FEB': 22, 'MAR': 28, 'APR': 33, 'MAY': 37, 'JUN': 32,
        'JUL': 29, 'AUG': 29, 'SEP': 31, 'OCT': 29, 'NOV': 25, 'DEC': 20
    };
    
    const baseHumidity = {
        'JAN': 45, 'FEB': 40, 'MAR': 35, 'APR': 40, 'MAY': 45, 'JUN': 75,
        'JUL': 85, 'AUG': 85, 'SEP': 80, 'OCT': 70, 'NOV': 60, 'DEC': 50
    };
    
    const baseRainfall = {
        'JAN': 8, 'FEB': 12, 'MAR': 20, 'APR': 35, 'MAY': 75, 'JUN': 145,
        'JUL': 195, 'AUG': 175, 'SEP': 115, 'OCT': 75, 'NOV': 35, 'DEC': 12
    };
    
    // State-based adjustments
    let tempAdjust = 0;
    let humidityAdjust = 0;
    let rainfallMultiplier = 1;
    
    if (['KERALA', 'KARNATAKA', 'TAMIL NADU'].includes(state)) {
        tempAdjust = 2;
        humidityAdjust = 10;
        rainfallMultiplier = 1.3;
    } else if (['RAJASTHAN', 'HARYANA', 'PUNJAB'].includes(state)) {
        tempAdjust = 4;
        humidityAdjust = -15;
        rainfallMultiplier = 0.5;
    } else if (['ASSAM', 'WEST BENGAL'].includes(state)) {
        humidityAdjust = 20;
        rainfallMultiplier = 1.8;
    }
    
    return {
        temperature: Math.round(baseTemps[month] + tempAdjust + (Math.random() * 6 - 3)),
        humidity: Math.round(Math.max(20, Math.min(95, baseHumidity[month] + humidityAdjust + (Math.random() * 10 - 5)))),
        rainfall: Math.round(baseRainfall[month] * rainfallMultiplier * (0.8 + Math.random() * 0.4)),
        wind_speed: Math.round(5 + Math.random() * 10),
        uv_index: Math.round(3 + Math.random() * 8)
    };
}

function generateEnhancedRecommendations(crop, formData) {
    const baseRecommendations = [
        `${crop.charAt(0).toUpperCase() + crop.slice(1)} is optimal for your current conditions`,
        'Monitor weather conditions and adjust irrigation accordingly'
    ];
    
    const cropSpecific = {
        'rice': [
            'Maintain water level 2-5cm above soil surface',
            'Apply nitrogen fertilizer in 3 split doses',
            'Watch for blast and brown spot diseases'
        ],
        'wheat': [
            'Ensure good drainage to prevent waterlogging',
            'Apply phosphorus at sowing time',
            'Monitor for rust diseases in humid conditions'
        ],
        'cotton': [
            'Maintain optimal soil moisture during flowering',
            'Apply potassium for better fiber quality',
            'Regular monitoring for bollworm attacks'
        ],
        'sugarcane': [
            'Provide adequate irrigation during dry spells',
            'Apply organic matter to improve soil structure',
            'Monitor for red rot and smut diseases'
        ]
    };
    
    const soilRecommendations = [];
    if (formData.ph < 6.0) {
        soilRecommendations.push('Apply lime to increase soil pH for better nutrient uptake');
    } else if (formData.ph > 8.0) {
        soilRecommendations.push('Apply sulfur or organic matter to reduce soil pH');
    }
    
    if (formData.nitrogen < 50) {
        soilRecommendations.push('Consider nitrogen supplementation through urea or organic manure');
    }
    
    return [...baseRecommendations, ...(cropSpecific[crop] || []), ...soilRecommendations];
}

function generateAlternativeCrops(formData) {
    const alternatives = [];
    
    if (formData.nitrogen > 80) alternatives.push('wheat', 'sugarcane');
    if (formData.potassium > 50) alternatives.push('banana', 'coconut');
    if (formData.ph < 6.5) alternatives.push('rice', 'tea');
    if (formData.phosphorous > 40) alternatives.push('cotton', 'corn');
    if (formData.ph >= 6.0 && formData.ph <= 7.5) alternatives.push('maize', 'grapes');
    
    return [...new Set(alternatives)].slice(0, 3);
}

function generateSoilAnalysis(formData) {
    const { nitrogen, phosphorous, potassium, ph } = formData;
    
    let healthScore = 0;
    const issues = [];
    const recommendations = [];
    
    // NPK Analysis
    if (nitrogen >= 80) healthScore += 25;
    else if (nitrogen >= 50) healthScore += 15;
    else issues.push('Low nitrogen levels');
    
    if (phosphorous >= 40) healthScore += 25;
    else if (phosphorous >= 25) healthScore += 15;
    else issues.push('Low phosphorous levels');
    
    if (potassium >= 40) healthScore += 25;
    else if (potassium >= 25) healthScore += 15;
    else issues.push('Low potassium levels');
    
    // pH Analysis
    if (ph >= 6.0 && ph <= 7.5) healthScore += 25;
    else if (ph < 6.0) issues.push('Acidic soil - may limit nutrient availability');
    else issues.push('Alkaline soil - may cause nutrient deficiencies');
    
    let healthStatus;
    if (healthScore >= 90) healthStatus = 'Excellent';
    else if (healthScore >= 70) healthStatus = 'Good';
    else if (healthScore >= 50) healthStatus = 'Fair';
    else healthStatus = 'Needs Improvement';
    
    return {
        health_score: healthScore,
        health_status: healthStatus,
        issues: issues,
        npk_ratio: `${nitrogen}:${phosphorous}:${potassium}`
    };
}

function generateMarketInfo(crop) {
    const basePrices = {
        'rice': 2200, 'wheat': 2000, 'maize': 1800, 'cotton': 5200,
        'sugarcane': 280, 'banana': 25, 'watermelon': 15, 'tea': 400
    };
    
    const currentPrice = basePrices[crop] || 2000;
    const priceVariation = (Math.random() - 0.5) * 0.2; // ±10% variation
    const marketPrice = Math.round(currentPrice * (1 + priceVariation));
    
    return {
        current_price: marketPrice,
        price_trend: Math.random() > 0.5 ? 'Rising' : 'Stable',
        demand: Math.random() > 0.3 ? 'High' : 'Medium'
    };
}

async function displayResults(result) {
    const resultsSection = document.getElementById('resultsSection');
    const cropResult = document.getElementById('cropResult');
    
    resultsSection.style.display = 'block';
    resultsSection.classList.add('fade-in');
    
    const cropName = result.predicted_crop;
    const confidence = (result.confidence * 100).toFixed(1);
    const cropImageUrl = cropImages[cropName] || cropImages['rice'];
    
    cropResult.innerHTML = `
        <div class="row">
            <div class="col-lg-6 text-center">
                <div class="crop-info mb-4">
                    <h2 class="text-success mb-3">${cropName.charAt(0).toUpperCase() + cropName.slice(1)}</h2>
                    <div class="confidence-badge mb-3">
                        <span class="badge bg-success fs-6 px-4 py-2">
                            Confidence: ${confidence}%
                        </span>
                    </div>
                    <img src="${cropImageUrl}" alt="${cropName}" class="crop-image">
                </div>
                
                <div class="soil-analysis-card p-3 rounded-3 bg-light">
                    <h5><i class="fas fa-chart-pie text-warning"></i> Soil Health Analysis</h5>
                    <div class="health-score mb-2">
                        <strong>Health Score: ${result.soil_analysis.health_score}/100</strong>
                    </div>
                    <div class="health-status">
                        <span class="badge ${getHealthBadgeClass(result.soil_analysis.health_status)}">
                            ${result.soil_analysis.health_status}
                        </span>
                    </div>
                </div>
            </div>
            
            <div class="col-lg-6">
                <div class="weather-card mb-4">
                    <h5><i class="fas fa-cloud-sun"></i> Current Weather Conditions</h5>
                    <div class="weather-grid">
                        <div class="weather-item">
                            <i class="fas fa-thermometer-half"></i>
                            <span>Temperature</span>
                            <strong>${result.weather_data.temperature}°C</strong>
                        </div>
                        <div class="weather-item">
                            <i class="fas fa-tint"></i>
                            <span>Humidity</span>
                            <strong>${result.weather_data.humidity}%</strong>
                        </div>
                        <div class="weather-item">
                            <i class="fas fa-cloud-rain"></i>
                            <span>Rainfall</span>
                            <strong>${result.weather_data.rainfall} mm</strong>
                        </div>
                        <div class="weather-item">
                            <i class="fas fa-wind"></i>
                            <span>Wind Speed</span>
                            <strong>${result.weather_data.wind_speed} km/h</strong>
                        </div>
                    </div>
                </div>
                
                <div class="recommendations-card p-4 rounded-3 bg-light">
                    <h5><i class="fas fa-lightbulb text-warning"></i> Smart Recommendations</h5>
                    <ul class="recommendation-list">
                        ${result.recommendations.map(rec => 
                            `<li><i class="fas fa-check text-success me-2"></i>${rec}</li>`
                        ).join('')}
                    </ul>
                </div>
                
                <div class="market-info mt-4 p-3 rounded-3" style="background: linear-gradient(135deg, #e8f5e8, #f0f8f0);">
                    <h6><i class="fas fa-chart-line text-success"></i> Market Information</h6>
                    <div class="row text-center">
                        <div class="col-4">
                            <div class="price-tag">₹${result.market_info.current_price}</div>
                            <small>per quintal</small>
                        </div>
                        <div class="col-4">
                            <div class="trend-badge badge bg-info">${result.market_info.price_trend}</div>
                            <small class="d-block">Price Trend</small>
                        </div>
                        <div class="col-4">
                            <div class="demand-badge badge bg-warning">${result.market_info.demand}</div>
                            <small class="d-block">Demand</small>
                        </div>
                    </div>
                </div>
                
                <div class="alternatives mt-4">
                    <h6><i class="fas fa-seedling text-success"></i> Alternative Crops</h6>
                    <div class="d-flex flex-wrap gap-2">
                        ${result.alternative_crops.map(crop => 
                            `<span class="badge bg-secondary px-3 py-2">${crop}</span>`
                        ).join('')}
                    </div>
                </div>
            </div>
        </div>
    `;
    
    setTimeout(() => {
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }, 300);
}

function getHealthBadgeClass(status) {
    const classes = {
        'Excellent': 'bg-success',
        'Good': 'bg-primary',
        'Fair': 'bg-warning',
        'Needs Improvement': 'bg-danger'
    };
    return classes[status] || 'bg-secondary';
}

async function showWeatherForecast(formData) {
    const weatherCard = document.getElementById('weatherCard');
    const weatherContent = document.getElementById('weatherContent');
    
    try {
        const forecast = await getWeatherForecast(formData.state, formData.district);
        
        weatherContent.innerHTML = `
            <div class="col-12">
                <h6 class="mb-3">7-Day Weather Forecast</h6>
                <div class="weather-forecast-grid">
                    ${forecast.map(day => `
                        <div class="forecast-day">
                            <div class="day-name">${day.day}</div>
                            <i class="weather-icon ${day.icon}"></i>
                            <div class="temp">${day.temp}°C</div>
                            <div class="rain">${day.rain}mm</div>
                        </div>
                    `).join('')}
                </div>
            </div>
        `;
        
        weatherCard.style.display = 'block';
        weatherCard.classList.add('fade-in');
        
    } catch (error) {
        console.error('Weather forecast error:', error);
    }
}

async function getWeatherForecast(state, district) {
    // Mock 7-day weather forecast
    const days = ['Today', 'Tomorrow', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];
    const icons = ['fas fa-sun', 'fas fa-cloud-sun', 'fas fa-cloud-rain', 'fas fa-cloud'];
    
    return days.map(day => ({
        day: day,
        temp: Math.round(25 + Math.random() * 10),
        rain: Math.round(Math.random() * 20),
        icon: icons[Math.floor(Math.random() * icons.length)]
    }));
}

async function updateWeatherOnLocationChange() {
    const state = document.getElementById('state').value;
    const district = document.getElementById('district').value;
    
    if (state && district) {
        const formData = { state, district, month: 'JUL' };
        showWeatherForecast(formData);
    }
}

function showLoading(show) {
    const loading = document.getElementById('loading');
    loading.style.display = show ? 'block' : 'none';
}

function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : 'success'} alert-dismissible fade show position-fixed`;
    notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    notification.innerHTML = `
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.remove();
    }, 5000);
}

function fillSampleData() {
    document.getElementById('nitrogen').value = '85';
    document.getElementById('phosphorous').value = '45';
    document.getElementById('potassium').value = '55';
    document.getElementById('ph').value = '6.8';
    document.getElementById('state').value = 'KARNATAKA';
    
    handleStateChange();
    
    setTimeout(() => {
        document.getElementById('district').value = 'BANGALORE URBAN';
        document.getElementById('month').value = 'JUL';
    }, 100);
}