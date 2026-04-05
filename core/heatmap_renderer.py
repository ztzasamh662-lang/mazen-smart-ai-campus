import psycopg2
import numpy as np
import cv2
from config import DB_CONFIG

OUTPUT_PATH = "data/heatmap.png"
WIDTH = 1280
HEIGHT = 720


def generate_heatmap():

    conn = psycopg2.connect(**DB_CONFIG)
    cur = conn.cursor()

    # 👇 نجيب الحركة من recognition_logs
    cur.execute("""
        SELECT camera_id
        FROM recognition_logs
    """)

    rows = cur.fetchall()

    cur.close()
    conn.close()

    heatmap = np.zeros((HEIGHT, WIDTH), dtype=np.float32)

    # نحول camera_id → نقطة عشوائية (temporary mapping)
    for (camera_id,) in rows:

        # توزيع عشوائي مؤقت عشان يظهر heatmap
        x = int((camera_id * 300) % WIDTH)
        y = int((camera_id * 200) % HEIGHT)

        heatmap[y, x] += 1

    heatmap = cv2.GaussianBlur(heatmap, (51, 51), 0)

    heatmap = cv2.normalize(
        heatmap,
        None,
        0,
        255,
        cv2.NORM_MINMAX
    )

    heatmap = heatmap.astype(np.uint8)

    heatmap_color = cv2.applyColorMap(
        heatmap,
        cv2.COLORMAP_JET
    )

    cv2.imwrite(OUTPUT_PATH, heatmap_color)

    return OUTPUT_PATH