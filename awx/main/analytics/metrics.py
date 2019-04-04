import os
from datetime import datetime

from prometheus_client import (
    Gauge,
    Info,
    generate_latest
)

from django.contrib.sessions.models import Session

# Temporary Imports 
from django.db import connection
from django.db.models import Count
from django.conf import settings

from awx.conf.license import get_license
from awx.main.utils import (get_awx_version, get_ansible_version,
                            get_custom_venv_choices)
from awx.main import models
from awx.main.analytics.collectors import counts, instance_info
from django.contrib.sessions.models import Session
from awx.main.analytics import register


SYSTEM_INFO = Info('awx_system', 'AWX System Information')

ORG_COUNT = Gauge('awx_organizations', 'Number of organizations')
USER_COUNT = Gauge('awx_users', 'Number of users')
TEAM_COUNT = Gauge('awx_teams', 'Number of teams')
INV_COUNT = Gauge('awx_inventories', 'Number of inventories')
PROJ_COUNT = Gauge('awx_projects', 'Number of projects')
JT_COUNT = Gauge('awx_job_templates', 'Number of job templates')
WFJT_COUNT = Gauge('awx_workflow_job_templates', 'Number of workflow job templates')
HOST_COUNT = Gauge('awx_hosts', 'Number of hosts')
SCHEDULE_COUNT = Gauge('awx_schedules', 'Number of schedules')
INV_SCRIPT_COUNT = Gauge('awx_inventory_scripts', 'Number of invetory scripts')
TOTAL_SESSIONS = Gauge('awx_active_sessions', 'Number of active session')
CUSTOM_VENVS = Gauge('awx_custom_virtualenvs', 'Number of virtualenvs')
ACTIVE_USER_SESSIONS = Gauge('awx_active_user_sessions', 'Number of Tower users logged in')
RUNNING_JOBS = Gauge('awx_running_jobs', 'Number of running jobs on the Tower system')
ACTIVE_HOST_COUNT = Gauge('awx_active_hosts', 'Number of active hosts counting towards subscription count')

def metrics():
    license_info = get_license(show_key=False)
    SYSTEM_INFO.info({'system_uuid': settings.SYSTEM_UUID, 
                      'tower_url_base': settings.TOWER_URL_BASE,
                      'tower_version': get_awx_version(),
                      'ansible_version': get_ansible_version(),
                      'license_type': license_info.get('license_type', 'UNLICENSED'),
                      'free_instances': str(license_info.get('free instances', 0)),
                      'license_expiry': str(license_info.get('time_remaining', 0)),
                      'pendo_tracking': settings.PENDO_TRACKING_STATE,
                      'external_logger_enabled': str(settings.LOG_AGGREGATOR_ENABLED),
                      'external_logger_type': getattr(settings, 'LOG_AGGREGATOR_TYPE', 'None')})

    current_counts = counts(datetime.now()) 
    
    ORG_COUNT.set(current_counts['organization'])
    USER_COUNT.set(current_counts['user'])
    TEAM_COUNT.set(current_counts['team'])
    INV_COUNT.set(current_counts['inventory'])
    PROJ_COUNT.set(current_counts['project'])
    JT_COUNT.set(current_counts['job_template'])
    WFJT_COUNT.set(current_counts['workflow_job_template'])
    HOST_COUNT.set(current_counts['host'])
    SCHEDULE_COUNT.set(current_counts['schedule'])
    INV_SCRIPT_COUNT.set(current_counts['custom_inventory_script'])
    CUSTOM_VENVS.set(current_counts['custom_virtualenvs'])
    TOTAL_SESSIONS.set(current_counts['active_sessions'])
    ACTIVE_USER_SESSIONS.set(current_counts['active_user_sessions'])
    RUNNING_JOBS.set(current_counts['running_jobs'])
    ACTIVE_HOST_COUNT.set(current_counts['active_host_count'])


    return generate_latest()


__all__ = ['metrics']
