#!/usr/bin/env python3
"""
Healthcare System Monitoring
===========================
Comprehensive monitoring system for healthcare analytics platform.
Monitors system health, performance, and critical healthcare metrics.
"""

import psutil
import sqlite3
import time
import logging
import json
import asyncio
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import queue
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import requests

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class AlertSeverity(Enum):
    """Alert severity levels"""
    INFO = "info"
    WARNING = "warning"
    CRITICAL = "critical"
    EMERGENCY = "emergency"

class AlertType(Enum):
    """Alert types"""
    SYSTEM_HEALTH = "system_health"
    DATABASE = "database"
    API_PERFORMANCE = "api_performance"
    ML_MODEL = "ml_model"
    PATIENT_SAFETY = "patient_safety"
    DATA_QUALITY = "data_quality"
    SECURITY = "security"

@dataclass
class Alert:
    """Alert data structure"""
    id: str
    timestamp: str
    alert_type: AlertType
    severity: AlertSeverity
    title: str
    message: str
    source: str
    metadata: Dict[str, Any]
    acknowledged: bool = False
    resolved: bool = False

@dataclass
class SystemMetrics:
    """System metrics data structure"""
    timestamp: str
    cpu_percent: float
    memory_percent: float
    disk_percent: float
    network_io: Dict[str, int]
    database_connections: int
    api_requests_per_minute: int
    active_patients: int
    critical_alerts: int

class HealthcareSystemMonitor:
    """Healthcare system monitoring and alerting"""
    
    def __init__(self, config: Dict[str, Any]):
        """Initialize monitoring system"""
        self.config = config
        self.alerts_queue = queue.Queue()
        self.metrics_history = []
        self.alert_rules = self._load_alert_rules()
        self.monitoring_active = False
        self.monitor_thread = None
        
        # Database connection
        self.db_path = config.get('database_path', 'healthcare_data_streamlit.db')
        
        # Alert thresholds
        self.thresholds = {
            'cpu_percent': 80.0,
            'memory_percent': 85.0,
            'disk_percent': 90.0,
            'api_response_time': 5.0,
            'database_connections': 100,
            'critical_patients': 50
        }
        
        # Notification settings
        self.notification_config = config.get('notifications', {})
        
    def _load_alert_rules(self) -> List[Dict[str, Any]]:
        """Load alert rules from configuration"""
        return [
            {
                'name': 'High CPU Usage',
                'condition': lambda metrics: metrics.cpu_percent > self.thresholds['cpu_percent'],
                'severity': AlertSeverity.WARNING,
                'type': AlertType.SYSTEM_HEALTH
            },
            {
                'name': 'High Memory Usage',
                'condition': lambda metrics: metrics.memory_percent > self.thresholds['memory_percent'],
                'severity': AlertSeverity.WARNING,
                'type': AlertType.SYSTEM_HEALTH
            },
            {
                'name': 'Disk Space Critical',
                'condition': lambda metrics: metrics.disk_percent > self.thresholds['disk_percent'],
                'severity': AlertSeverity.CRITICAL,
                'type': AlertType.SYSTEM_HEALTH
            },
            {
                'name': 'Too Many Database Connections',
                'condition': lambda metrics: metrics.database_connections > self.thresholds['database_connections'],
                'severity': AlertSeverity.WARNING,
                'type': AlertType.DATABASE
            },
            {
                'name': 'High Number of Critical Patients',
                'condition': lambda metrics: metrics.critical_alerts > self.thresholds['critical_patients'],
                'severity': AlertSeverity.EMERGENCY,
                'type': AlertType.PATIENT_SAFETY
            }
        ]
    
    def collect_system_metrics(self) -> SystemMetrics:
        """Collect current system metrics"""
        try:
            # System metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network_io = psutil.net_io_counters()._asdict()
            
            # Database metrics
            db_connections = self._get_database_connections()
            active_patients = self._get_active_patients()
            critical_alerts = self._get_critical_alerts()
            
            # API metrics (simplified)
            api_requests = self._get_api_requests_count()
            
            return SystemMetrics(
                timestamp=datetime.now().isoformat(),
                cpu_percent=cpu_percent,
                memory_percent=memory.percent,
                disk_percent=disk.percent,
                network_io=network_io,
                database_connections=db_connections,
                api_requests_per_minute=api_requests,
                active_patients=active_patients,
                critical_alerts=critical_alerts
            )
            
        except Exception as e:
            logger.error(f"Error collecting system metrics: {e}")
            return None
    
    def _get_database_connections(self) -> int:
        """Get number of database connections"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            # SQLite doesn't have connection pooling like PostgreSQL
            # This is a simplified metric
            cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Error getting database connections: {e}")
            return 0
    
    def _get_active_patients(self) -> int:
        """Get number of active patients"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM patients WHERE status = 'Active'")
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Error getting active patients: {e}")
            return 0
    
    def _get_critical_alerts(self) -> int:
        """Get number of critical alerts"""
        try:
            conn = sqlite3.connect(self.db_path)
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM patients WHERE risk_level = 'Critical'")
            result = cursor.fetchone()
            conn.close()
            return result[0] if result else 0
        except Exception as e:
            logger.error(f"Error getting critical alerts: {e}")
            return 0
    
    def _get_api_requests_count(self) -> int:
        """Get API requests count (simplified)"""
        # In a real implementation, this would track actual API requests
        # For now, return a mock value
        return 0
    
    def check_alert_conditions(self, metrics: SystemMetrics) -> List[Alert]:
        """Check alert conditions against current metrics"""
        alerts = []
        
        for rule in self.alert_rules:
            try:
                if rule['condition'](metrics):
                    alert = Alert(
                        id=f"{rule['name']}_{int(time.time())}",
                        timestamp=datetime.now().isoformat(),
                        alert_type=rule['type'],
                        severity=rule['severity'],
                        title=rule['name'],
                        message=f"Alert triggered: {rule['name']}",
                        source="system_monitor",
                        metadata={
                            'cpu_percent': metrics.cpu_percent,
                            'memory_percent': metrics.memory_percent,
                            'disk_percent': metrics.disk_percent,
                            'active_patients': metrics.active_patients,
                            'critical_alerts': metrics.critical_alerts
                        }
                    )
                    alerts.append(alert)
            except Exception as e:
                logger.error(f"Error checking alert rule {rule['name']}: {e}")
        
        return alerts
    
    def send_alert(self, alert: Alert):
        """Send alert notification"""
        try:
            # Add to alerts queue
            self.alerts_queue.put(alert)
            
            # Log alert
            logger.warning(f"ALERT [{alert.severity.value.upper()}] {alert.title}: {alert.message}")
            
            # Send notifications
            self._send_email_notification(alert)
            self._send_slack_notification(alert)
            self._send_webhook_notification(alert)
            
        except Exception as e:
            logger.error(f"Error sending alert: {e}")
    
    def _send_email_notification(self, alert: Alert):
        """Send email notification"""
        if not self.notification_config.get('email', {}).get('enabled', False):
            return
        
        try:
            email_config = self.notification_config['email']
            smtp_server = email_config['smtp_server']
            smtp_port = email_config['smtp_port']
            username = email_config['username']
            password = email_config['password']
            to_addresses = email_config['to_addresses']
            
            msg = MIMEMultipart()
            msg['From'] = username
            msg['To'] = ', '.join(to_addresses)
            msg['Subject'] = f"[{alert.severity.value.upper()}] {alert.title}"
            
            body = f"""
            Healthcare System Alert
            
            Alert ID: {alert.id}
            Timestamp: {alert.timestamp}
            Severity: {alert.severity.value.upper()}
            Type: {alert.alert_type.value}
            
            Message: {alert.message}
            
            Metadata:
            {json.dumps(alert.metadata, indent=2)}
            """
            
            msg.attach(MIMEText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_server, smtp_port)
            server.starttls()
            server.login(username, password)
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email notification sent for alert {alert.id}")
            
        except Exception as e:
            logger.error(f"Error sending email notification: {e}")
    
    def _send_slack_notification(self, alert: Alert):
        """Send Slack notification"""
        if not self.notification_config.get('slack', {}).get('enabled', False):
            return
        
        try:
            slack_config = self.notification_config['slack']
            webhook_url = slack_config['webhook_url']
            
            color_map = {
                AlertSeverity.INFO: "good",
                AlertSeverity.WARNING: "warning",
                AlertSeverity.CRITICAL: "danger",
                AlertSeverity.EMERGENCY: "danger"
            }
            
            payload = {
                "attachments": [
                    {
                        "color": color_map.get(alert.severity, "warning"),
                        "title": alert.title,
                        "text": alert.message,
                        "fields": [
                            {"title": "Severity", "value": alert.severity.value.upper(), "short": True},
                            {"title": "Type", "value": alert.alert_type.value, "short": True},
                            {"title": "Timestamp", "value": alert.timestamp, "short": True}
                        ]
                    }
                ]
            }
            
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 200:
                logger.info(f"Slack notification sent for alert {alert.id}")
            else:
                logger.error(f"Slack notification failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error sending Slack notification: {e}")
    
    def _send_webhook_notification(self, alert: Alert):
        """Send webhook notification"""
        if not self.notification_config.get('webhook', {}).get('enabled', False):
            return
        
        try:
            webhook_config = self.notification_config['webhook']
            webhook_url = webhook_config['url']
            
            payload = {
                "alert_id": alert.id,
                "timestamp": alert.timestamp,
                "alert_type": alert.alert_type.value,
                "severity": alert.severity.value,
                "title": alert.title,
                "message": alert.message,
                "source": alert.source,
                "metadata": alert.metadata
            }
            
            response = requests.post(webhook_url, json=payload)
            if response.status_code == 200:
                logger.info(f"Webhook notification sent for alert {alert.id}")
            else:
                logger.error(f"Webhook notification failed: {response.status_code}")
                
        except Exception as e:
            logger.error(f"Error sending webhook notification: {e}")
    
    def start_monitoring(self):
        """Start monitoring system"""
        if self.monitoring_active:
            logger.warning("Monitoring is already active")
            return
        
        self.monitoring_active = True
        self.monitor_thread = threading.Thread(target=self._monitoring_loop, daemon=True)
        self.monitor_thread.start()
        logger.info("Healthcare system monitoring started")
    
    def stop_monitoring(self):
        """Stop monitoring system"""
        self.monitoring_active = False
        if self.monitor_thread:
            self.monitor_thread.join()
        logger.info("Healthcare system monitoring stopped")
    
    def _monitoring_loop(self):
        """Main monitoring loop"""
        while self.monitoring_active:
            try:
                # Collect metrics
                metrics = self.collect_system_metrics()
                if metrics:
                    # Store metrics history
                    self.metrics_history.append(metrics)
                    
                    # Keep only last 1000 metrics
                    if len(self.metrics_history) > 1000:
                        self.metrics_history = self.metrics_history[-1000:]
                    
                    # Check alert conditions
                    alerts = self.check_alert_conditions(metrics)
                    
                    # Send alerts
                    for alert in alerts:
                        self.send_alert(alert)
                
                # Wait before next check
                time.sleep(30)  # Check every 30 seconds
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                time.sleep(60)  # Wait longer on error
    
    def get_system_status(self) -> Dict[str, Any]:
        """Get current system status"""
        try:
            metrics = self.collect_system_metrics()
            if not metrics:
                return {"status": "error", "message": "Failed to collect metrics"}
            
            # Determine overall status
            status = "healthy"
            if metrics.cpu_percent > 90 or metrics.memory_percent > 95 or metrics.disk_percent > 95:
                status = "critical"
            elif metrics.cpu_percent > 80 or metrics.memory_percent > 85 or metrics.disk_percent > 90:
                status = "warning"
            
            return {
                "status": status,
                "timestamp": metrics.timestamp,
                "metrics": asdict(metrics),
                "alerts_count": self.alerts_queue.qsize(),
                "monitoring_active": self.monitoring_active
            }
            
        except Exception as e:
            logger.error(f"Error getting system status: {e}")
            return {"status": "error", "message": str(e)}
    
    def get_alerts(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent alerts"""
        alerts = []
        temp_queue = queue.Queue()
        
        # Get alerts from queue
        while not self.alerts_queue.empty():
            alert = self.alerts_queue.get()
            alerts.append(asdict(alert))
            temp_queue.put(alert)
        
        # Put alerts back in queue
        while not temp_queue.empty():
            self.alerts_queue.put(temp_queue.get())
        
        return alerts[-limit:]  # Return last N alerts
    
    def acknowledge_alert(self, alert_id: str) -> bool:
        """Acknowledge an alert"""
        # In a real implementation, this would update a database
        # For now, just log the acknowledgment
        logger.info(f"Alert {alert_id} acknowledged")
        return True
    
    def resolve_alert(self, alert_id: str) -> bool:
        """Resolve an alert"""
        # In a real implementation, this would update a database
        # For now, just log the resolution
        logger.info(f"Alert {alert_id} resolved")
        return True

# Configuration for monitoring
MONITORING_CONFIG = {
    'database_path': 'healthcare_data_streamlit.db',
    'notifications': {
        'email': {
            'enabled': False,
            'smtp_server': 'smtp.gmail.com',
            'smtp_port': 587,
            'username': 'your-email@gmail.com',
            'password': 'your-password',
            'to_addresses': ['admin@healthcare.com']
        },
        'slack': {
            'enabled': False,
            'webhook_url': 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK'
        },
        'webhook': {
            'enabled': False,
            'url': 'https://your-webhook-url.com/alerts'
        }
    }
}

# Global monitor instance
monitor = HealthcareSystemMonitor(MONITORING_CONFIG)

def start_healthcare_monitoring():
    """Start healthcare system monitoring"""
    monitor.start_monitoring()
    return monitor

def stop_healthcare_monitoring():
    """Stop healthcare system monitoring"""
    monitor.stop_monitoring()

def get_healthcare_system_status():
    """Get healthcare system status"""
    return monitor.get_system_status()

def get_healthcare_alerts():
    """Get healthcare alerts"""
    return monitor.get_alerts()

if __name__ == "__main__":
    # Example usage
    monitor = start_healthcare_monitoring()
    
    try:
        # Keep running
        while True:
            time.sleep(60)
            status = get_healthcare_system_status()
            print(f"System Status: {status['status']}")
            
    except KeyboardInterrupt:
        print("Stopping monitoring...")
        stop_healthcare_monitoring()
