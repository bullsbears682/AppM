#!/usr/bin/env python3
"""
DevCost - Real-Time Development Cost Analytics
A working prototype that analyzes git repositories to show development costs
"""

from flask import Flask, render_template, jsonify, request
import subprocess
import json
import os
from datetime import datetime, timedelta
import re
from collections import defaultdict, Counter
import sqlite3

app = Flask(__name__)

class DevCostAnalyzer:
    def __init__(self):
        self.hourly_rate = 75  # Default developer hourly rate
        self.setup_database()
    
    def setup_database(self):
        """Initialize SQLite database for caching analysis data"""
        conn = sqlite3.connect('devcost.db')
        cursor = conn.cursor()
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS commits (
                hash TEXT PRIMARY KEY,
                author TEXT,
                date TEXT,
                message TEXT,
                files_changed INTEGER,
                insertions INTEGER,
                deletions INTEGER,
                estimated_hours REAL,
                cost REAL
            )
        ''')
        
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS features (
                name TEXT PRIMARY KEY,
                total_commits INTEGER,
                total_hours REAL,
                total_cost REAL,
                status TEXT,
                created_date TEXT
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def get_git_log(self, days=30):
        """Get git commit data for analysis"""
        try:
            # Get detailed commit information
            cmd = [
                'git', 'log', 
                f'--since="{days} days ago"',
                '--pretty=format:%H|%an|%ai|%s',
                '--numstat'
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, cwd='.')
            return result.stdout
        except Exception as e:
            return f"Error: {str(e)}"
    
    def parse_git_data(self, git_output):
        """Parse git log output into structured data"""
        commits = []
        lines = git_output.split('\n')
        
        current_commit = None
        
        for line in lines:
            if '|' in line and len(line.split('|')) == 4:
                # New commit line
                if current_commit:
                    commits.append(current_commit)
                
                parts = line.split('|')
                current_commit = {
                    'hash': parts[0],
                    'author': parts[1],
                    'date': parts[2],
                    'message': parts[3],
                    'files': [],
                    'insertions': 0,
                    'deletions': 0
                }
            elif line.strip() and current_commit and '\t' in line:
                # File change line
                parts = line.split('\t')
                if len(parts) >= 3:
                    try:
                        insertions = int(parts[0]) if parts[0] != '-' else 0
                        deletions = int(parts[1]) if parts[1] != '-' else 0
                        filename = parts[2]
                        
                        current_commit['files'].append({
                            'name': filename,
                            'insertions': insertions,
                            'deletions': deletions
                        })
                        current_commit['insertions'] += insertions
                        current_commit['deletions'] += deletions
                    except ValueError:
                        pass
        
        if current_commit:
            commits.append(current_commit)
        
        return commits
    
    def estimate_commit_time(self, commit):
        """Estimate time spent on a commit based on changes"""
        base_time = 0.5  # Minimum 30 minutes per commit
        
        # Factor in lines of code
        lines_changed = commit['insertions'] + commit['deletions']
        code_time = lines_changed * 0.02  # 1.2 minutes per line on average
        
        # Factor in number of files
        file_complexity = len(commit['files']) * 0.25
        
        # Factor in commit message complexity (feature vs bug fix)
        message_lower = commit['message'].lower()
        if any(word in message_lower for word in ['fix', 'bug', 'error', 'issue']):
            complexity_multiplier = 1.5  # Bug fixes take longer
        elif any(word in message_lower for word in ['feat', 'feature', 'add', 'implement']):
            complexity_multiplier = 1.2  # New features
        elif any(word in message_lower for word in ['refactor', 'cleanup', 'optimize']):
            complexity_multiplier = 1.3  # Refactoring
        else:
            complexity_multiplier = 1.0
        
        total_time = (base_time + code_time + file_complexity) * complexity_multiplier
        
        # Cap at reasonable limits
        return min(max(total_time, 0.25), 8.0)  # Between 15 minutes and 8 hours
    
    def categorize_commit(self, commit):
        """Categorize commit into feature/bug/maintenance"""
        message = commit['message'].lower()
        
        if any(word in message for word in ['fix', 'bug', 'error', 'issue', 'hotfix']):
            return 'Bug Fix'
        elif any(word in message for word in ['feat', 'feature', 'add', 'implement', 'new']):
            return 'Feature'
        elif any(word in message for word in ['refactor', 'cleanup', 'optimize', 'improve']):
            return 'Refactoring'
        elif any(word in message for word in ['test', 'spec', 'coverage']):
            return 'Testing'
        elif any(word in message for word in ['doc', 'readme', 'comment']):
            return 'Documentation'
        else:
            return 'Maintenance'
    
    def analyze_repository(self, days=30):
        """Perform complete repository analysis"""
        git_output = self.get_git_log(days)
        commits = self.parse_git_data(git_output)
        
        analysis = {
            'total_commits': len(commits),
            'total_hours': 0,
            'total_cost': 0,
            'commits_by_author': defaultdict(list),
            'commits_by_category': defaultdict(list),
            'daily_activity': defaultdict(lambda: {'commits': 0, 'hours': 0, 'cost': 0}),
            'file_hotspots': Counter(),
            'commit_details': []
        }
        
        for commit in commits:
            estimated_hours = self.estimate_commit_time(commit)
            estimated_cost = estimated_hours * self.hourly_rate
            category = self.categorize_commit(commit)
            
            # Update totals
            analysis['total_hours'] += estimated_hours
            analysis['total_cost'] += estimated_cost
            
            # Group by author
            analysis['commits_by_author'][commit['author']].append({
                'commit': commit,
                'hours': estimated_hours,
                'cost': estimated_cost,
                'category': category
            })
            
            # Group by category
            analysis['commits_by_category'][category].append({
                'commit': commit,
                'hours': estimated_hours,
                'cost': estimated_cost
            })
            
            # Daily activity
            date = commit['date'][:10]  # YYYY-MM-DD
            analysis['daily_activity'][date]['commits'] += 1
            analysis['daily_activity'][date]['hours'] += estimated_hours
            analysis['daily_activity'][date]['cost'] += estimated_cost
            
            # File hotspots
            for file_info in commit['files']:
                analysis['file_hotspots'][file_info['name']] += 1
            
            # Detailed commit info
            analysis['commit_details'].append({
                'hash': commit['hash'][:8],
                'author': commit['author'],
                'date': commit['date'],
                'message': commit['message'],
                'category': category,
                'files_changed': len(commit['files']),
                'lines_changed': commit['insertions'] + commit['deletions'],
                'estimated_hours': round(estimated_hours, 2),
                'estimated_cost': round(estimated_cost, 2)
            })
        
        return analysis

# Initialize analyzer
analyzer = DevCostAnalyzer()

@app.route('/')
def dashboard():
    """Main dashboard page"""
    return render_template('dashboard.html')

@app.route('/api/analysis')
def get_analysis():
    """API endpoint for repository analysis"""
    days = request.args.get('days', 30, type=int)
    analysis = analyzer.analyze_repository(days)
    
    # Convert defaultdicts to regular dicts for JSON serialization
    result = {
        'total_commits': analysis['total_commits'],
        'total_hours': round(analysis['total_hours'], 2),
        'total_cost': round(analysis['total_cost'], 2),
        'avg_cost_per_commit': round(analysis['total_cost'] / max(analysis['total_commits'], 1), 2),
        'commits_by_author': dict(analysis['commits_by_author']),
        'commits_by_category': {k: len(v) for k, v in analysis['commits_by_category'].items()},
        'category_costs': {k: round(sum(item['cost'] for item in v), 2) 
                          for k, v in analysis['commits_by_category'].items()},
        'daily_activity': dict(analysis['daily_activity']),
        'file_hotspots': dict(analysis['file_hotspots'].most_common(10)),
        'commit_details': analysis['commit_details'][-20:],  # Last 20 commits
        'hourly_rate': analyzer.hourly_rate
    }
    
    return jsonify(result)

@app.route('/api/settings', methods=['POST'])
def update_settings():
    """Update analysis settings"""
    data = request.json
    if 'hourly_rate' in data:
        analyzer.hourly_rate = float(data['hourly_rate'])
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)