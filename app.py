"""
NBA Performance Analytics Dashboard
Milestone 4 - End-to-End Web Application
Data Titans Team

This Flask application provides an interactive web interface for NBA player performance analytics,
integrating all algorithms developed in Milestones 2-3 with data visualization and user queries.
"""

from flask import Flask, render_template, request, jsonify
import pandas as pd
import json
import os
from pathlib import Path
import subprocess
import time

app = Flask(__name__)

# Global data storage
data_cache = {}

def load_data():
    """Load NBA data from JSONL file"""
    global data_cache

    if 'df' in data_cache:
        return data_cache['df']

    jsonl_file = Path("data/curated/nba_ready.jsonl")

    if not jsonl_file.exists():
        print("Warning: JSONL file not found. Running data processing pipeline...")
        try:
            # Run data processing scripts if data doesn't exist
            subprocess.run(["python", "scripts/01_reduce.py"], check=True)
            subprocess.run(["python", "scripts/02_cleanse.py"], check=True)
            subprocess.run(["python", "scripts/03_transform_to_jsonl.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"Error running data processing: {e}")
            return pd.DataFrame()

    try:
        data = []
        with open(jsonl_file, 'r', encoding='utf-8') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))

        df = pd.DataFrame(data)
        data_cache['df'] = df
        print(f"Loaded {len(df)} player records")
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def run_algorithm(script_name):
    """Run a Python algorithm script and capture output"""
    try:
        start_time = time.time()
        result = subprocess.run(["python", f"scripts/{script_name}"], capture_output=True, text=True, timeout=300)
        end_time = time.time()

        return {
            'success': result.returncode == 0,
            'output': result.stdout,
            'error': result.stderr,
            'execution_time': round(end_time - start_time, 2)
        }
    except subprocess.TimeoutExpired:
        return {'success': False, 'error': 'Algorithm timed out after 5 minutes'}
    except Exception as e:
        return {'success': False, 'error': str(e)}

@app.route('/')
def index():
    """Main dashboard page"""
    return render_template('index.html')

@app.route('/api/player_search')
def player_search():
    """Search for players by name"""
    query = request.args.get('q', '').lower()
    if not query:
        return jsonify([])

    df = load_data()
    if df.empty:
        return jsonify([])

    # Search players
    matches = df[df['player_name'].str.lower().str.contains(query)]
    results = []

    for _, player in matches.head(20).iterrows():  # Limit to 20 results
        results.append({
            'player_id': player['player_id'],
            'player_name': player['player_name'],
            'team': player['team'],
            'season': int(player['season']),
            'stats': player['stats']
        })

    return jsonify(results)

@app.route('/api/player_stats/<player_id>')
def player_stats(player_id):
    """Get detailed stats for a specific player"""
    df = load_data()
    if df.empty:
        return jsonify({'error': 'No data available'})

    # Find player across all seasons
    player_data = df[df['player_id'] == player_id]

    if player_data.empty:
        return jsonify({'error': 'Player not found'})

    # Prepare career stats
    career_stats = []
    for _, row in player_data.iterrows():
        career_stats.append({
            'season': int(row['season']),
            'team': row['team'],
            'stats': row['stats']
        })

    # Sort by season
    career_stats.sort(key=lambda x: x['season'])

    return jsonify({
        'player_name': player_data.iloc[0]['player_name'],
        'career_stats': career_stats
    })

@app.route('/api/team_analysis')
def team_analysis():
    """Get team performance analysis"""
    try:
        result = run_algorithm('09_team_performance_analysis.py')
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/player_efficiency')
def player_efficiency():
    """Get player efficiency rankings"""
    try:
        result = run_algorithm('08_player_efficiency_ranking.py')
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/correlations')
def correlations():
    """Get statistical correlations analysis"""
    try:
        result = run_algorithm('10_statistical_correlations.py')
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/run_clustering')
def run_clustering():
    """Run K-means clustering algorithm"""
    try:
        result = run_algorithm('05_player_clustering.py')
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/run_prediction')
def run_prediction():
    """Run linear regression prediction"""
    try:
        result = run_algorithm('06_performance_prediction.py')
        return jsonify(result)
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/scalability_test')
def scalability_test():
    """Run scalability performance tests"""
    try:
        import time
        import platform
        import os

        start_time = time.time()

        # Get system metrics
        df = load_data()
        data_size = len(df) if not df.empty else 0

        # Basic system info
        results = {
            'data_processing_time': round(time.time() - start_time, 2),
            'data_size': data_size,
            'system_info': {
                'os': platform.system(),
                'python_version': platform.python_version(),
                'cpu_count': os.cpu_count() or 'Unknown'
            },
            'performance_metrics': {
                'data_load_efficiency': f"{data_size / max(time.time() - start_time, 0.001):.0f} records/sec",
                'dataset_size': f"{data_size} player records"
            }
        }

        # Try to get detailed system info if psutil is available
        try:
            import psutil
            memory_info = psutil.virtual_memory()
            disk_info = psutil.disk_usage('/')

            results.update({
                'memory_usage': {
                    'total_gb': round(memory_info.total / (1024**3), 2),
                    'available_gb': round(memory_info.available / (1024**3), 2),
                    'percent_used': memory_info.percent
                },
                'disk_info': {
                    'total_gb': round(disk_info.total / (1024**3), 2),
                    'free_gb': round(disk_info.free / (1024**3), 2),
                    'percent_used': disk_info.percent
                },
                'performance_metrics': {
                    'data_load_efficiency': f"{data_size / max(time.time() - start_time, 0.001):.0f} records/sec",
                    'memory_efficiency': f"{data_size / max(memory_info.total / (1024**3), 1):.0f} records/GB",
                    'dataset_size': f"{data_size} player records"
                }
            })
        except ImportError:
            results['note'] = 'Detailed hardware metrics unavailable (psutil not installed)'
        except Exception as e:
            results['hardware_note'] = f'Hardware metrics partially unavailable: {str(e)}'

        return jsonify(results)

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/api/system_info')
def system_info():
    """Get system information for scalability documentation"""
    import platform
    import psutil

    try:
        info = {
            'os': platform.system(),
            'os_version': platform.version(),
            'python_version': platform.python_version(),
            'cpu_count': psutil.cpu_count(),
            'cpu_logical': psutil.cpu_count(logical=True),
            'memory_total': round(psutil.virtual_memory().total / (1024**3), 2),  # GB
            'memory_available': round(psutil.virtual_memory().available / (1024**3), 2),  # GB
            'disk_total': round(psutil.disk_usage('/').total / (1024**3), 2),  # GB
            'disk_free': round(psutil.disk_usage('/').free / (1024**3), 2)  # GB
        }
    except:
        # Fallback if psutil not available
        info = {
            'os': platform.system(),
            'python_version': platform.python_version(),
            'note': 'psutil not available for detailed hardware info'
        }

    return jsonify(info)

if __name__ == '__main__':
    print("Starting NBA Performance Analytics Dashboard...")
    print("Loading data...")
    load_data()
    print("Server starting on http://localhost:5000")
    print("Open your browser and go to: http://localhost:5000")
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
