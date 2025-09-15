import os
import subprocess
import time
import configparser
import tempfile
import getpass
import logging
from datetime import datetime
from fastapi import FastAPI, Form, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, FileResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="TestAutothon2025 Platform", version="1.0.0")

execution_status = {}

COMMON_COMPONENTS = {
    'UI Tests': 'ui_testrunner.py',
    'Mobile Tests': 'mob_testrunner.py',
    'Parallel Run': 'all_testrunner.py'
}

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECTS_CONFIG = {
    'TestAutothon2824': {
        'path': WORKSPACE_DIR,
        'name': 'TestAutothon2025 Automation Framework',
        'components': COMMON_COMPONENTS
    }
}

# Load HTML template
with open('ui_template.html', 'r', encoding='utf-8') as f:
    HTML_TEMPLATE = f.read()

@app.get("/", response_class=HTMLResponse)
async def index():
    return HTML_TEMPLATE

@app.get("/api/projects")
async def get_projects():
    projects = {}
    for project_id, config in PROJECTS_CONFIG.items():
        if os.path.exists(config.get('path', '')):
            projects[project_id] = {
                'name': config['name'],
                'components': list(COMMON_COMPONENTS.keys())
            }
    return projects

@app.post("/api/execute")
async def execute_automation(
    background_tasks: BackgroundTasks,
    project: str = Form(...),
    environment: str = Form(...),
    component: str = Form(...),
    team_name: str = Form(...),
    browser: str = Form(...),
    headless: str = Form(...)
):
    if project not in PROJECTS_CONFIG:
        raise HTTPException(status_code=400, detail="Invalid project")
    
    job_id = f"job_{int(time.time())}"
    
    # Create user directory
    user_dirs = create_user_directory(job_id)
    
    execution_status[job_id] = {
        'status': 'running',
        'logs': [f'> Starting {component}...'],
        'start_time': datetime.now(),
        'project': project,
        'component': component,
        'user_dir': user_dirs['user_dir'],
        'config_dir': user_dirs['config_dir']
    }
    
    background_tasks.add_task(run_component, job_id, project, component, environment, team_name, browser, headless)
    return {'status': 'started', 'job_id': job_id}

def create_user_directory(job_id):
    """Create user-specific directory structure"""
    username = getpass.getuser()
    temp_base = tempfile.gettempdir()
    user_dir = os.path.join(temp_base, username)
    
    # Create directory structure
    config_dir = os.path.join(user_dir, 'Configurations')
    os.makedirs(config_dir, exist_ok=True)
    
    return {
        'user_dir': user_dir,
        'config_dir': config_dir
    }

def create_config_file(config_dir, environment, team_name, browser, headless):
    config = configparser.ConfigParser()
    
    config['commonInfo'] = {
        'environment': environment,
        'team_name': team_name,
        'browser': browser,
        'headless': headless,
        'OR_Testenv': 'Configurations//OR.csv',
        'application_url': 'https://facebook.com/'
    }
    
    config_path = os.path.join(config_dir, 'config.ini')
    
    with open(config_path, 'w') as configfile:
        config.write(configfile)
    
    return config_path

def cleanup_user_directory(user_dir, job_id):
    """Clean up entire user directory after execution"""
    try:
        if user_dir and os.path.exists(user_dir):
            import shutil
            shutil.rmtree(user_dir)
            logger.info(f'Cleaned up user directory: {user_dir}')
            execution_status[job_id]['logs'].append('> User directory cleaned up')
    except Exception as e:
        logger.error(f'Error cleaning up user directory: {str(e)}')

def run_component(job_id, project, component, environment, team_name, browser, headless):
    try:
        project_path = PROJECTS_CONFIG[project]['path']
        execution_status[job_id]['logs'].append(f'> Project path: {project_path}')
        
        # Create config.ini file in user directory
        config_dir = execution_status[job_id]['config_dir']
        config_path = create_config_file(config_dir, environment, team_name, browser, headless)
        execution_status[job_id]['logs'].append(f'> Created config file: {config_path}')
        
        # Copy config to project Configurations folder
        project_config_dir = os.path.join(project_path, 'Configurations')
        os.makedirs(project_config_dir, exist_ok=True)
        import shutil
        shutil.copy2(config_path, os.path.join(project_config_dir, 'config.ini'))
        execution_status[job_id]['logs'].append('> Copied config to project folder')
        
        # Clean old reports
        import shutil
        reports_path = os.path.join(project_path, 'Outputs', 'Reports')
        if os.path.exists(reports_path):
            for file in os.listdir(reports_path):
                if file.endswith('.html'):
                    os.remove(os.path.join(reports_path, file))
        execution_status[job_id]['logs'].append('> Cleaned old reports')
        
        # Execute component
        script_path = COMMON_COMPONENTS.get(component)
        if not script_path:
            execution_status[job_id]['logs'].append(f'> Component not found: {component}')
            execution_status[job_id]['status'] = 'failed'
            return
        
        execution_status[job_id]['logs'].append(f'> Executing {component}...')
        
        cmd = f'python {script_path}'
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, 
                                 text=True, cwd=project_path, shell=True)
        stdout, stderr = process.communicate()
        
        if stdout:
            for line in stdout.strip().split('\n'):
                execution_status[job_id]['logs'].append(f'> {line}')
        
        if process.returncode == 0:
            execution_status[job_id]['logs'].append(f'> ✅ {component} completed successfully')
            execution_status[job_id]['status'] = 'completed'
        else:
            execution_status[job_id]['logs'].append(f'> ❌ Error: {stderr}')
            execution_status[job_id]['status'] = 'failed'
        
        execution_status[job_id]['end_time'] = datetime.now()
        
        # Clean up user directory
        user_dir = execution_status[job_id].get('user_dir')
        if user_dir:
            cleanup_user_directory(user_dir, job_id)
        
    except Exception as e:
        execution_status[job_id]['logs'].append(f'> ❌ Error: {str(e)}')
        execution_status[job_id]['status'] = 'failed'
        execution_status[job_id]['end_time'] = datetime.now()
        
        # Clean up user directory on error
        user_dir = execution_status[job_id].get('user_dir')
        if user_dir:
            cleanup_user_directory(user_dir, job_id)

@app.get("/api/status/{job_id}")
async def get_status(job_id: str):
    if job_id in execution_status:
        return execution_status[job_id]
    else:
        raise HTTPException(status_code=404, detail="Job not found")

@app.get("/api/reports")
async def get_reports():
    """Get latest reports from completed jobs"""
    reports = []
    
    # Clean up old completed jobs (older than 1 hour)
    current_time = datetime.now()
    jobs_to_cleanup = []
    
    for job_id, job_data in execution_status.items():
        if job_data.get('status') == 'completed' and job_data.get('end_time'):
            time_diff = current_time - job_data['end_time']
            if time_diff.total_seconds() > 3600:  # 1 hour
                jobs_to_cleanup.append(job_id)
    
    for job_id in jobs_to_cleanup:
        job_data = execution_status.pop(job_id, {})
        user_dir = job_data.get('user_dir')
        if user_dir:
            cleanup_user_directory(user_dir, job_id)

    # Component-specific report paths
    COMPONENT_PATHS = {
        'UI Tests': 'Outputs/Reports',
        'Mobile Tests': 'Outputs/Reports',
        'Parallel Run': 'Outputs/Reports'
    }

    for job_id, job_data in execution_status.items():
        if job_data.get('status') == 'completed':
            project_id = job_data.get('project')
            component = job_data.get('component', '')

            if project_id and project_id in PROJECTS_CONFIG:
                project_path = PROJECTS_CONFIG[project_id]['path']
                job_start_time = job_data.get('start_time')

                report_subpath = COMPONENT_PATHS.get(component, 'Reports')
                report_path = os.path.join(project_path, report_subpath)

                if os.path.exists(report_path):
                    for file in os.listdir(report_path):
                        if file.endswith(('.html', '.csv', '.txt', '.xlsx')):
                            file_path = os.path.join(report_path, file)
                            file_time = datetime.fromtimestamp(os.path.getmtime(file_path))

                            if job_start_time and file_time >= job_start_time:
                                duplicate = any(r['filename'] == file and r['project'] == project_id for r in reports)
                                if not duplicate:
                                    reports.append({
                                        'type': f'{component} Report',
                                        'filename': file,
                                        'path': file_path,
                                        'project': project_id,
                                        'icon': '📊'
                                    })

    return reports

@app.get("/api/download/{filepath:path}")
async def download_file(filepath: str):
    """Download a report file"""
    try:
        if os.path.exists(filepath) and os.path.isfile(filepath):
            return FileResponse(filepath, filename=os.path.basename(filepath))
        else:
            raise HTTPException(status_code=404, detail="File not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    try:
        import uvicorn
        uvicorn.run(app, host='127.0.0.1', port=9000)
    except ImportError:
        print('uvicorn not found. Install with: pip install uvicorn')
