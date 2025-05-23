from flask import Blueprint, jsonify
from config.database import get_pg_connection
import pandas as pd
import matplotlib.pyplot as plt

analytics_bp = Blueprint('analytics', __name__)

@analytics_bp.route('/analytics', methods=['GET'])
def analytics():
    conn = get_pg_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT question, COUNT(*) as count FROM queries GROUP BY question ORDER BY count DESC LIMIT 10")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    
    df = pd.DataFrame(data, columns=['question', 'count'])
    plt.figure(figsize=(10, 6))
    plt.bar(df['question'], df['count'])
    plt.xticks(rotation=45)
    plt.tight_layout()
    chart_path = 'static/query_trends.png'
    plt.savefig(chart_path)
    plt.close()
    
    return jsonify({'chartUrl': f'https://your-api-domain.com/{chart_path}'}), 200