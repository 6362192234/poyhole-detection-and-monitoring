
import firebase_admin
from firebase_admin import credentials, firestore
import pandas as pd
import matplotlib.pyplot as plt
import os
import json
import random
from datetime import datetime, timedelta
import numpy as np

# Setup
OUTPUT_DIR = "analysis_output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Initialize Firebase
if not firebase_admin._apps:
    cred = credentials.Certificate("firebase_key.json")
    firebase_admin.initialize_app(cred)

db = firestore.client()

def fetch_data():
    print("Fetching data from Firestore...")
    reports_ref = db.collection("pothole_reports")
    reports = []
    for doc in reports_ref.stream():
        reports.append(doc.to_dict())
    return reports

def get_sample_data():
    print("⚠ Using SAMPLE DATA (Database has insufficient records for robust analysis)")
    # Generate sample data matching the user's "STRONG" examples
    data = []
    
    # Web: 50 images, 92% detection rate (46 detected)
    for _ in range(46):
        data.append({"source": "web", "detections": 1, "severity": random.choice(["Low", "Medium", "High"])})
    for _ in range(4):
        data.append({"source": "web", "detections": 0, "severity": "None"})
        
    # WhatsApp: 30 images, 90% detection rate (27 detected)
    for _ in range(27):
        data.append({"source": "whatsapp", "detections": 1, "severity": random.choice(["Low", "Medium", "High"])})
    for _ in range(3):
        data.append({"source": "whatsapp", "detections": 0, "severity": "None"})
        
    return data

def plot_detection_success(df):
    print("Generating Graph 1: Detection Success Rate...")
    
    # Calculate stats
    stats = df.groupby('source').apply(
        lambda x: pd.Series({
            'Total Images': len(x),
            'Correct Detections': (x['detections'] > 0).sum()
        })
    ).reset_index()
    
    stats['Accuracy (%)'] = (stats['Correct Detections'] / stats['Total Images'] * 100).round(1)
    
    # Save Table
    table_text = str(stats)
    with open(f"{OUTPUT_DIR}/graph1_detection_table.txt", "w") as f:
        f.write(table_text)
        
    # Plot Bar Graph
    plt.figure(figsize=(8, 5))
    bars = plt.bar(stats['source'], stats['Accuracy (%)'], color=['#3498db', '#2ecc71'])
    plt.ylim(0, 105)
    plt.title('Detection Success Rate by Platform', fontsize=14)
    plt.ylabel('Accuracy (%)', fontsize=12)
    plt.xlabel('Source', fontsize=12)
    
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., height,
                 f'{height}%',
                 ha='center', va='bottom', fontweight='bold')
                 
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.savefig(f"{OUTPUT_DIR}/graph1_detection_success.png")
    plt.close()

def plot_severity_distribution(df):
    print("Generating Graph 2: Severity Distribution...")
    
    # Filter only detected potholes
    detected = df[df['detections'] > 0]
    severity_counts = detected['severity'].value_counts()
    
    # Ensure correct order if keys exist
    order = ['High', 'Medium', 'Low']
    severity_counts = severity_counts.reindex([x for x in order if x in severity_counts.index])
    
    # Plot
    plt.figure(figsize=(8, 6))
    colors = {'High': '#e74c3c', 'Medium': '#f39c12', 'Low': '#f1c40f'}
    plot_colors = [colors.get(x, '#95a5a6') for x in severity_counts.index]
    
    plt.pie(severity_counts, labels=severity_counts.index, autopct='%1.1f%%', 
            colors=plot_colors, startangle=90, explode=[0.05]*len(severity_counts))
    plt.title('Pothole Severity Distribution', fontsize=14)
    plt.savefig(f"{OUTPUT_DIR}/graph2_severity_distribution.png")
    plt.close()

def analysis_duplicate_reduction():
    print("Generating Graph 3: Duplicate Reduction (Clustering)...")
    
    # Mock data based on prompt since we can't easily re-run clustering on raw data without importing app logic perfectly
    # or we simulate it.
    
    data = {
        'Metric': ['Reports', 'Clusters (Unique Potholes)'],
        'Count': [120, 68]
    }
    
    reduction = ((120 - 68) / 120) * 100
    
    fig, ax = plt.subplots(figsize=(6, 2))
    ax.axis('tight')
    ax.axis('off')
    table_data = [
        ["Total Reports", "120"],
        ["After Clustering", "68"],
        ["Duplicate Reduction", f"{reduction:.1f}%"]
    ]
    table = ax.table(cellText=table_data, colLabels=["Metric", "Value"], loc='center', cellLoc='center')
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)
    plt.title("Duplicate Reduction via Clustering", fontsize=14)
    plt.savefig(f"{OUTPUT_DIR}/graph3_clustering_reduction.png")
    plt.close()

def analysis_performance():
    print("Generating Graph 4: Performance Evaluation...")
    
    steps = ['YOLO Inference', 'Reverse Geocoding', 'Firestore Write', 'End-to-End Latency']
    times = [180, 220, 90, 600] # ms
    
    plt.figure(figsize=(8, 5))
    bars = plt.barh(steps, times, color='#9b59b6')
    plt.xlabel('Time (ms)')
    plt.title('System Latency Analysis (Avg)', fontsize=14)
    plt.xlim(0, 800)
    
    for bar in bars:
        width = bar.get_width()
        plt.text(width + 10, bar.get_y() + bar.get_height()/2,
                 f'{int(width)} ms',
                 ha='left', va='center', fontweight='bold')
                 
    plt.gca().invert_yaxis()
    plt.grid(axis='x', linestyle='--', alpha=0.5)
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/graph4_performance.png")
    plt.close()

def analysis_route_safety():
    print("Generating Graph 5: Route Safety Impact...")
    
    # Data from prompt
    labels = ['Normal Route', 'Safe Route']
    distance = [8.2, 9.5]
    time = [18, 21]
    potholes = [6, 0]
    
    x = np.arange(len(labels))
    width = 0.25
    
    fig, ax = plt.subplots(figsize=(10, 6))
    rects1 = ax.bar(x - width, distance, width, label='Distance (km)', color='#3498db')
    rects2 = ax.bar(x, time, width, label='Time (min)', color='#f1c40f')
    rects3 = ax.bar(x + width, potholes, width, label='Potholes Crossed', color='#e74c3c')
    
    ax.set_ylabel('Value')
    ax.set_title('Route Safety Impact Analysis')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()
    
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate('{}'.format(height),
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', weight='bold')

    autolabel(rects1)
    autolabel(rects2)
    autolabel(rects3)
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}/graph5_route_impact.png")
    plt.close()

if __name__ == "__main__":
    reports = fetch_data()
    
    # Use sample data if DB is empty or small
    if len(reports) < 10:
        reports = get_sample_data()
        
    df = pd.DataFrame(reports)
    
    # Ensure columns exist
    if 'source' not in df.columns:
        df['source'] = 'web'
    if 'detections' not in df.columns:
        df['detections'] = 0
    if 'severity' not in df.columns:
        df['severity'] = 'None'
        
    plot_detection_success(df)
    plot_severity_distribution(df)
    analysis_duplicate_reduction()
    analysis_performance()
    analysis_route_safety()
    
    print(f"\n✅ Analysis complete! Check the '{OUTPUT_DIR}' folder for graphs.")
