import datetime


def get_project_info():

    return {
        "project_name": "Smart AI Campus",
        "version": "1.0",
        "ai_modules": [
            "Face Detection",
            "Face Recognition",
            "Tracking Engine",
            "Behavior Detection",
            "Heatmap Analytics"
        ],
        "features": [
            "Live Camera Monitoring",
            "Unknown Person Alerts",
            "Movement Heatmap",
            "Behavior Analysis",
            "AI Dashboard"
        ],
        "release_date": str(datetime.date.today())
    }