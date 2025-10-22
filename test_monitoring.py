#!/usr/bin/env python3
"""
Healthcare Monitoring Test Script
================================
Test script for the Healthcare System Monitoring and Alerting system.
"""

import sys
import os
import time
import json
from datetime import datetime
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent / "src"))

from monitoring.system_monitor import (
    HealthcareSystemMonitor,
    MONITORING_CONFIG,
    AlertSeverity,
    AlertType
)

def test_system_monitor():
    """Test the HealthcareSystemMonitor"""
    print("🔍 Testing Healthcare System Monitor...")
    
    try:
        # Initialize monitor
        monitor = HealthcareSystemMonitor(MONITORING_CONFIG)
        print("✅ Monitor initialized successfully")
        
        # Test metrics collection
        print("📊 Testing metrics collection...")
        metrics = monitor.collect_system_metrics()
        
        if metrics:
            print("✅ Metrics collected successfully")
            print(f"   CPU: {metrics.cpu_percent:.1f}%")
            print(f"   Memory: {metrics.memory_percent:.1f}%")
            print(f"   Disk: {metrics.disk_percent:.1f}%")
            print(f"   Active Patients: {metrics.active_patients}")
            print(f"   Critical Alerts: {metrics.critical_alerts}")
        else:
            print("❌ Failed to collect metrics")
            return False
        
        # Test alert conditions
        print("🚨 Testing alert conditions...")
        alerts = monitor.check_alert_conditions(metrics)
        print(f"✅ Found {len(alerts)} alerts")
        
        for alert in alerts:
            print(f"   - {alert.title} ({alert.severity.value})")
        
        # Test system status
        print("📈 Testing system status...")
        status = monitor.get_system_status()
        print(f"✅ System status: {status.get('status', 'unknown')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing monitor: {e}")
        return False

def test_alert_system():
    """Test the alert system"""
    print("\n🚨 Testing Alert System...")
    
    try:
        monitor = HealthcareSystemMonitor(MONITORING_CONFIG)
        
        # Test alert creation
        from monitoring.system_monitor import Alert
        
        test_alert = Alert(
            id="test_alert_001",
            timestamp=datetime.now().isoformat(),
            alert_type=AlertType.SYSTEM_HEALTH,
            severity=AlertSeverity.WARNING,
            title="Test Alert",
            message="This is a test alert",
            source="test_script",
            metadata={"test": True}
        )
        
        print("✅ Test alert created")
        print(f"   ID: {test_alert.id}")
        print(f"   Type: {test_alert.alert_type.value}")
        print(f"   Severity: {test_alert.severity.value}")
        print(f"   Message: {test_alert.message}")
        
        # Test alert sending
        print("📤 Testing alert sending...")
        monitor.send_alert(test_alert)
        print("✅ Alert sent successfully")
        
        # Test alert retrieval
        print("📥 Testing alert retrieval...")
        alerts = monitor.get_alerts(limit=10)
        print(f"✅ Retrieved {len(alerts)} alerts")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing alert system: {e}")
        return False

def test_monitoring_dashboard():
    """Test the monitoring dashboard"""
    print("\n📊 Testing Monitoring Dashboard...")
    
    try:
        # Check if dashboard file exists
        dashboard_path = "dashboards/healthcare_monitoring_dashboard.py"
        if not os.path.exists(dashboard_path):
            print(f"❌ Dashboard file not found: {dashboard_path}")
            return False
        
        print("✅ Dashboard file exists")
        
        # Check dashboard imports
        import importlib.util
        spec = importlib.util.spec_from_file_location("monitoring_dashboard", dashboard_path)
        dashboard_module = importlib.util.module_from_spec(spec)
        
        try:
            spec.loader.exec_module(dashboard_module)
            print("✅ Dashboard imports successfully")
        except Exception as e:
            print(f"❌ Dashboard import error: {e}")
            return False
        
        print("✅ Monitoring dashboard is ready")
        return True
        
    except Exception as e:
        print(f"❌ Error testing dashboard: {e}")
        return False

def test_notification_system():
    """Test the notification system"""
    print("\n📧 Testing Notification System...")
    
    try:
        monitor = HealthcareSystemMonitor(MONITORING_CONFIG)
        
        # Test email configuration
        email_config = monitor.notification_config.get('email', {})
        print(f"📧 Email notifications: {'Enabled' if email_config.get('enabled') else 'Disabled'}")
        
        # Test Slack configuration
        slack_config = monitor.notification_config.get('slack', {})
        print(f"💬 Slack notifications: {'Enabled' if slack_config.get('enabled') else 'Disabled'}")
        
        # Test webhook configuration
        webhook_config = monitor.notification_config.get('webhook', {})
        print(f"🔗 Webhook notifications: {'Enabled' if webhook_config.get('enabled') else 'Disabled'}")
        
        print("✅ Notification system configured")
        return True
        
    except Exception as e:
        print(f"❌ Error testing notification system: {e}")
        return False

def test_monitoring_integration():
    """Test monitoring integration with healthcare system"""
    print("\n🔗 Testing Monitoring Integration...")
    
    try:
        # Test database connection
        monitor = HealthcareSystemMonitor(MONITORING_CONFIG)
        
        # Test database metrics
        db_connections = monitor._get_database_connections()
        active_patients = monitor._get_active_patients()
        critical_alerts = monitor._get_critical_alerts()
        
        print(f"✅ Database connections: {db_connections}")
        print(f"✅ Active patients: {active_patients}")
        print(f"✅ Critical alerts: {critical_alerts}")
        
        # Test API metrics
        api_requests = monitor._get_api_requests_count()
        print(f"✅ API requests: {api_requests}")
        
        print("✅ Monitoring integration working")
        return True
        
    except Exception as e:
        print(f"❌ Error testing monitoring integration: {e}")
        return False

def run_monitoring_demo():
    """Run a monitoring demonstration"""
    print("\n🎬 Running Monitoring Demonstration...")
    
    try:
        monitor = HealthcareSystemMonitor(MONITORING_CONFIG)
        
        print("🚀 Starting monitoring system...")
        monitor.start_monitoring()
        
        print("⏳ Monitoring for 30 seconds...")
        time.sleep(30)
        
        print("📊 Getting system status...")
        status = monitor.get_system_status()
        print(f"   Status: {status.get('status', 'unknown')}")
        print(f"   Monitoring Active: {status.get('monitoring_active', False)}")
        print(f"   Alerts Count: {status.get('alerts_count', 0)}")
        
        print("🚨 Getting alerts...")
        alerts = monitor.get_alerts(limit=5)
        print(f"   Found {len(alerts)} alerts")
        
        for alert in alerts:
            print(f"   - {alert.get('title', 'Unknown')} ({alert.get('severity', 'unknown')})")
        
        print("🛑 Stopping monitoring system...")
        monitor.stop_monitoring()
        
        print("✅ Monitoring demo completed")
        return True
        
    except Exception as e:
        print(f"❌ Error in monitoring demo: {e}")
        return False

def main():
    """Main test function"""
    print("🏥 Healthcare System Monitoring Test Suite")
    print("=" * 60)
    
    tests = [
        ("System Monitor", test_system_monitor),
        ("Alert System", test_alert_system),
        ("Monitoring Dashboard", test_monitoring_dashboard),
        ("Notification System", test_notification_system),
        ("Monitoring Integration", test_monitoring_integration),
        ("Monitoring Demo", run_monitoring_demo)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🧪 Running {test_name} test...")
        try:
            if test_func():
                print(f"✅ {test_name} test passed")
                passed += 1
            else:
                print(f"❌ {test_name} test failed")
        except Exception as e:
            print(f"❌ {test_name} test error: {e}")
    
    print("\n" + "=" * 60)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Monitoring system is ready.")
        print("\n🚀 To start monitoring:")
        print("   python start_monitoring.py")
        print("\n📊 To view monitoring dashboard:")
        print("   streamlit run dashboards/healthcare_monitoring_dashboard.py --server.port 8506")
    else:
        print("⚠️  Some tests failed. Please check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
