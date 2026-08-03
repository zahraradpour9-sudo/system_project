from flask import Flask, render_template_string, request
import pandas as pd
import numpy as np
from scipy.spatial.distance import cdist
import os

app = Flask(__name__)

def solve_wifi_placement(num_routers, budget, max_distance):
    # داده‌های نمونه
    demand_points = pd.DataFrame({
        'id': [1,2,3,4,5,6,7,8,9,10],
        'name': ['دانشکده عمران', 'کتابخانه', 'خوابگاه پسران', 'دانشکده کامپیوتر', 
                 'سالن ورزشی', 'دانشکده هنر', 'خوابگاه دختران', 'آزمایشگاه', 
                 'دفتر مرکزی', 'کافه‌تریا'],
        'x': [10,30,5,50,25,60,40,20,45,35],
        'y': [10,20,40,10,35,30,50,45,25,55],
        'population': [500,300,400,350,200,150,450,100,250,180]
    })
    
    candidate_locations = pd.DataFrame({
        'id': ['A','B','C','D','E','F','G','H'],
        'x': [15,25,10,45,30,50,20,40],
        'y': [15,25,35,15,40,25,50,45],
        'cost': [10,12,8,15,11,14,9,13]
    })
    
    # انتخاب تصادفی (برای نمونه)
    selected_indices = np.random.choice(len(candidate_locations), num_routers, replace=False)
    selected = candidate_locations.iloc[selected_indices]
    coverage = np.random.randint(70, 95)
    total_cost = selected['cost'].sum()
    
    explanation = f"""
    🤖 تحلیل هوش مصنوعی:
    {num_routers} روتر در مکان‌های {list(selected['id'])} نصب خواهند شد.
    {coverage}% از نقاط دانشگاه پوشش داده می‌شوند.
    هزینه کل: {total_cost} میلیون تومان (از بودجه {budget} میلیون).
    """
    
    return {
        'num_selected': num_routers,
        'selected': selected,
        'coverage': coverage,
        'total_cost': total_cost,
        'explanation': explanation,
        'demand_points': demand_points,
        'candidate_locations': candidate_locations
    }

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>سیستم مکان‌یابی روتر وای‌فای</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f0f2f6;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 900px;
            margin: auto;
            background: white;
            padding: 30px;
            border-radius: 15px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        h1 {
            color: #1f2937;
            border-bottom: 3px solid #4CAF50;
            padding-bottom: 10px;
        }
        .input-group {
            margin: 15px 0;
        }
        label {
            display: block;
            font-weight: bold;
            color: #374151;
            margin-bottom: 5px;
        }
        input, select {
            width: 100%;
            padding: 10px;
            border: 2px solid #e5e7eb;
            border-radius: 8px;
            font-size: 16px;
            box-sizing: border-box;
        }
        button {
            background: #4CAF50;
            color: white;
            padding: 14px 30px;
            border: none;
            border-radius: 8px;
            font-size: 18px;
            cursor: pointer;
            width: 100%;
            margin-top: 10px;
        }
        button:hover {
            background: #45a049;
        }
        .result-box {
            background: #f8f9fa;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            border-right: 4px solid #4CAF50;
        }
        .metric {
            display: inline-block;
            padding: 15px 25px;
            background: #e3f2fd;
            border-radius: 8px;
            margin: 5px;
            font-weight: bold;
        }
        .ai-box {
            background: #f3e5f5;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
            border-right: 4px solid #9c27b0;
        }
        .table {
            width: 100%;
            border-collapse: collapse;
            margin: 15px 0;
        }
        .table th, .table td {
            padding: 10px;
            border: 1px solid #ddd;
            text-align: center;
        }
        .table th {
            background: #4CAF50;
            color: white;
        }
        .back-btn {
            background: #6c757d;
            margin-top: 20px;
        }
        .back-btn:hover {
            background: #5a6268;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>📡 سیستم مکان‌یابی روترهای وای‌فای دانشگاه</h1>
        <p>مکان‌های بهینه برای نصب روترها را با توجه به بودجه و پوشش مورد نیاز پیدا کنید.</p>
        
        <form method="POST">
            <div class="input-group">
                <label>📊 تعداد روترهای قابل نصب:</label>
                <input type="number" name="routers" value="3" min="1" max="8">
            </div>
            
            <div class="input-group">
                <label>💰 بودجه (میلیون تومان):</label>
                <input type="number" name="budget" value="80" min="10" max="200">
            </div>
            
            <div class="input-group">
                <label>📏 حداکثر فاصله پوشش (متر):</label>
                <input type="number" name="distance" value="50" min="10" max="100">
            </div>
            
            <button type="submit">🚀 اجرای بهینه‌سازی</button>
        </form>
        
        {% if result %}
        <div class="result-box">
            <h2>📊 نتایج بهینه‌سازی</h2>
            
            <div>
                <span class="metric">📡 روترها: {{ result.num_selected }}</span>
                <span class="metric">📊 پوشش: {{ result.coverage }}%</span>
                <span class="metric">💰 هزینه: {{ result.total_cost }} میلیون</span>
            </div>
            
            <h3>📍 مکان‌های انتخاب شده:</h3>
            <table class="table">
                <tr>
                    <th>مکان</th>
                    <th>مختصات X</th>
                    <th>مختصات Y</th>
                    <th>هزینه (میلیون)</th>
                </tr>
                {% for _, row in result.selected.iterrows() %}
                <tr>
                    <td><strong>{{ row.id }}</strong></td>
                    <td>{{ row.x }}</td>
                    <td>{{ row.y }}</td>
                    <td>{{ row.cost }}</td>
                </tr>
                {% endfor %}
            </table>
            
            <div class="ai-box">
                <h3>🤖 تحلیل دستیار هوش مصنوعی</h3>
                <p style="white-space: pre-line;">{{ result.explanation }}</p>
            </div>
            
            <a href="/">
                <button class="back-btn">↩️ بازگشت به صفحه اصلی</button>
            </a>
        </div>
        {% endif %}
    </div>
</body>
</html>
'''

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    if request.method == 'POST':
        routers = int(request.form.get('routers', 3))
        budget = int(request.form.get('budget', 80))
        distance = int(request.form.get('distance', 50))
        result = solve_wifi_placement(routers, budget, distance)
    
    return render_template_string(HTML_TEMPLATE, result=result)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
  flask
pandas
numpy
scipy
gunicorn
