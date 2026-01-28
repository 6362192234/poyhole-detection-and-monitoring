# Pothole Mapping and Route Planning System - User Guide

## 🎯 Overview

This system extends the pothole detection app with intelligent route planning capabilities. It maps potholes on OpenStreetMap, detects road segments with multiple potholes ("series"), and suggests alternative routes that avoid damaged roads.

---

## ✨ New Features

### 1. **Data Export**
Export pothole data in multiple formats:
- **JSON**: Complete data with metadata
- **CSV**: Spreadsheet-friendly format
- **OSM XML**: OpenStreetMap-compatible format for visualization

**Usage:**
```
GET /api/export/potholes?format=json
GET /api/export/potholes?format=csv
GET /api/export/potholes?format=osm
```

### 2. **Pothole Series Detection**
Automatically identifies road segments with multiple consecutive potholes:
- Groups potholes by road name
- Detects series of 3+ potholes within 200 meters
- Stores bad segments in Firestore for route planning

**Usage:**
```
GET /api/bad-segments
POST /api/bad-segments/refresh
```

### 3. **Smart Route Planning**
Interactive route planner with pothole avoidance:
- Enter source and destination (address or GPS coordinates)
- View all potholes on the map (color-coded by severity)
- Get original route and safe alternative route
- See detailed comparison and recommendations

**Access:** Navigate to `http://localhost:5000/route-planner`

---

## 🚀 Quick Start

### Step 1: Start the Flask App

```bash
cd "c:\Users\dhanu\Downloads\pothole-2 (2)\pothole-2\pothole-2"
python app.py
```

The app will start at `http://127.0.0.1:5000`

### Step 2: Access Route Planner

1. Open browser and go to: `http://127.0.0.1:5000/route-planner`
2. You'll see an interactive map with all detected potholes

### Step 3: Plan a Route

**Method 1: Using Addresses**
1. Enter start location: "MG Road, Bangalore"
2. Enter end location: "Residency Road, Bangalore"
3. Click "Plan Route"

**Method 2: Using GPS Coordinates**
1. Enter start: "12.9716, 77.5946"
2. Enter end: "12.9352, 77.6245"
3. Click "Plan Route"

**Method 3: Click on Map**
1. Click in "Start Location" field
2. Click on map to set start point
3. Click in "End Location" field
4. Click on map to set end point
5. Click "Plan Route"

### Step 4: View Results

The system will show:
- **Original Route** (blue line): Direct route from A to B
- **Alternative Route** (green dashed line): Safer route avoiding bad segments
- **Bad Segments** (red circles): Areas with pothole series
- **Potholes** (colored dots): Individual potholes by severity
- **Recommendation**: Explanation of which route to take and why

---

## 📊 API Endpoints

### Export Potholes
```http
GET /api/export/potholes?format=json
```
**Parameters:**
- `format`: `json` | `csv` | `osm`

**Response:** Pothole data in requested format

---

### Get Bad Segments
```http
GET /api/bad-segments
```
**Response:**
```json
{
  "bad_segments": [...],
  "statistics": {
    "total_reports": 150,
    "bad_road_segments": 5,
    "potholes_in_series": 27
  },
  "total_segments": 5
}
```

---

### Refresh Bad Segments
```http
POST /api/bad-segments/refresh
```
**Response:**
```json
{
  "message": "Refreshed 5 bad road segments",
  "segments_count": 5
}
```

---

### Plan Route
```http
POST /api/route/plan
Content-Type: application/json

{
  "start": "MG Road, Bangalore",
  "end": "12.9352, 77.6245"
}
```

**Response:**
```json
{
  "original_route": {
    "distance_km": 5.2,
    "duration_minutes": 15,
    "coordinates": [...]
  },
  "alternative_route": {
    "distance_km": 6.1,
    "duration_minutes": 18,
    "coordinates": [...]
  },
  "bad_segments_detected": [...],
  "recommendation": {
    "message": "⚠️ Warning: MG Road has a series of 7 potholes (High severity)...",
    "severity": "recommended",
    "affected_roads": ["MG Road"],
    "total_potholes": 7
  }
}
```

---

### Get Pothole Locations
```http
GET /api/potholes/locations
```
**Response:**
```json
{
  "potholes": [
    {
      "id": "abc123",
      "lat": 12.9716,
      "lon": 77.5946,
      "severity": "High",
      "road": "MG Road",
      "detections": 5
    }
  ],
  "total": 25
}
```

---

## 🔧 Configuration

### Routing API Setup

The system uses OpenRouteService for routing. To use the full API:

1. Get a free API key from: https://openrouteservice.org/dev/#/signup
2. Add to `.env` file:
```
ORS_API_KEY=your_api_key_here
```

**Note:** Without an API key, the system uses mock routing (straight-line distance). This is fine for testing but won't provide accurate road-based routes.

### Series Detection Parameters

You can customize pothole series detection in `export_utils.py`:

```python
def detect_pothole_series(
    reports: List[Dict], 
    distance_threshold: float = 200,  # meters between potholes
    min_potholes: int = 3              # minimum potholes to form series
)
```

---

## 🎨 Map Legend

| Symbol | Meaning |
|--------|---------|
| 🔴 Red Dot | High Severity Pothole |
| 🟠 Orange Dot | Medium Severity Pothole |
| 🔵 Blue Dot | Low Severity Pothole |
| 🟢 Green Marker | Start Point |
| 🔴 Red Marker | End Point |
| 🔵 Blue Line | Original Route |
| 🟢 Green Dashed Line | Safe Alternative |
| 🔴 Red Circle | Bad Road Segment |

---

## 📱 Usage Examples

### Example 1: Export Data for Analysis
```bash
# Download pothole data as CSV
curl http://localhost:5000/api/export/potholes?format=csv > potholes.csv

# Download as OSM XML for mapping tools
curl http://localhost:5000/api/export/potholes?format=osm > potholes.osm
```

### Example 2: Check Bad Segments
```bash
# Get current bad segments
curl http://localhost:5000/api/bad-segments

# Refresh detection after new reports
curl -X POST http://localhost:5000/api/bad-segments/refresh
```

### Example 3: API Route Planning
```bash
curl -X POST http://localhost:5000/api/route/plan \
  -H "Content-Type: application/json" \
  -d '{
    "start": "12.9716, 77.5946",
    "end": "12.9352, 77.6245"
  }'
```

---

## 🐛 Troubleshooting

### No potholes showing on map
- Check if you have pothole reports in Firebase
- Visit `/admin` to see all reports
- Upload some pothole images with GPS to populate data

### Route planning not working
- Ensure both start and end locations are entered
- Check browser console for errors (F12)
- Verify internet connection (needed for geocoding and tiles)

### "Could not geocode address" error
- Use more specific addresses
- Try using GPS coordinates instead
- Check if OpenStreetMap Nominatim service is accessible

### Alternative route same as original
- May indicate no bad segments detected on the route
- Or bad segments unavoidable without major detour
- Check recommendation message for details

---

## 🔐 Security Notes

### OSM Data Export
The OSM XML export is meant for **visualization only**. To upload to public OpenStreetMap:
1. Follow OSM community guidelines
2. Verify data accuracy
3. Use proper changeset tags
4. Review OSM data contribution policies

### API Rate Limits
- OpenStreetMap Nominatim: Max 1 request/second
- OpenRouteService free tier: 2,000 requests/day
- Consider implementing caching for production use

---

## 📈 Future Enhancements

Potential improvements:
- Real-time pothole updates via WebSocket
- Historical route analysis
- Pothole severity prediction
- Integration with Google Maps API
- Mobile app version
- Community reporting features
- Administrative notifications for bad segments

---

## 📄 File Structure

```
pothole-2/
├── app.py                      # Main Flask app (updated with new routes)
├── export_utils.py            # NEW: Data export and series detection
├── route_planner.py           # NEW: Routing logic
├── templates/
│   ├── route_planner.html    # NEW: Route planner interface
│   ├── admin.html
│   └── index.html
├── static/
│   ├── route_planner.css     # NEW: Route planner styles
│   ├── route_planner.js      # NEW: Map and routing JavaScript
│   └── admin.css
├── exports/                   # NEW: Directory for exported files
├── models/
│   └── best.pt
└── uploads/
```

---

## 💡 Tips

- **Best Results:** Upload potholes with accurate GPS data
- **Series Detection:** Runs automatically when accessing bad segments API
- **Map View:** Zoom in to see individual potholes clearly
- **Export Data:** Use JSON format for complete metadata
- **Route Comparison:** Consider both distance and time factors

---

## 🆘 Support

For issues or questions:
1. Check the Flask app logs in the terminal
2. Open browser Developer Tools (F12) for frontend errors
3. Verify all dependencies are installed
4. Ensure Firebase credentials are correctly configured

---

**Last Updated:** 2026-01-20
**Version:** 2.0.0
