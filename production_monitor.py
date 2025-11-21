"""
Production Monitoring System
Author: [Your Name]
Description: Monitors website health, response times, and sends alerts
"""

import requests  # For making HTTP requests to check services
import time     # For adding delays between checks
import json     # For handling JSON data (if needed for APIs)
from datetime import datetime  # For timestamping events

class ProductionMonitor:
    """
    A production monitoring system that checks service health and sends alerts
    This is like having a security guard for your websites and APIs
    """
    
    def __init__(self, services_to_monitor):
        """
        Initialize the monitoring system with a list of services to watch
        
        Args:
            services_to_monitor (list): List of URLs to monitor
                Example: ["https://google.com", "https://github.com"]
        """
        # Store the list of services we need to monitor
        self.services = services_to_monitor
        
        # Keep history of all health checks for reporting
        self.health_history = []
        
        # Count how many alerts we've sent
        self.alert_count = 0
        
        # Track overall statistics
        self.stats = {
            "total_checks": 0,
            "healthy_checks": 0,
            "error_checks": 0,
            "start_time": datetime.now()
        }
    
    def check_service_health(self, service_url):
        """
        Check if a single service is healthy by making an HTTP request
        """
        try:
            start_time = time.time()
            response = requests.get(service_url, timeout=10)
            response_time = (time.time() - start_time) * 1000
            self.stats["total_checks"] += 1

            if response.status_code == 200:
                self.stats["healthy_checks"] += 1
                return {
                    "status": "🟢 HEALTHY",
                    "response_time": round(response_time, 2),
                    "status_code": response.status_code,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            else:
                self.stats["error_checks"] += 1
                return {
                    "status": "🟡 WARNING",
                    "response_time": round(response_time, 2),
                    "status_code": response.status_code,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "error": f"HTTP Error: {response.status_code}"
                }
                
        except requests.exceptions.Timeout:
            self.stats["error_checks"] += 1
            return {
                "status": "🔴 TIMEOUT",
                "response_time": 10000,
                "status_code": 0,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error": "Request timed out after 10 seconds"
            }
            
        except requests.exceptions.ConnectionError:
            self.stats["error_checks"] += 1
            return {
                "status": "🔴 CONNECTION ERROR",
                "response_time": 0,
                "status_code": 0,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error": "Cannot connect to service - check network/DNS"
            }
            
        except Exception as e:
            self.stats["error_checks"] += 1
            return {
                "status": "🔴 ERROR",
                "response_time": 0,
                "status_code": 0,
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "error": f"Unexpected error: {str(e)}"
            }
    
    def send_alert(self, service_url, health_status):
        """
        Send an alert when a service has problems
        """
        self.alert_count += 1
        
        alert_message = f"""
        🚨 PRODUCTION ALERT #{self.alert_count}
        📍 Service: {service_url}
        🕒 Time: {health_status['timestamp']}
        📊 Status: {health_status['status']}
        ⏱️ Response Time: {health_status.get('response_time', 'N/A')}ms
        ❌ Error: {health_status.get('error', 'Unknown error')}
        """
        
        print(alert_message)
        
        self.health_history.append({
            "service": service_url,
            "alert": alert_message,
            "timestamp": health_status['timestamp'],
            "alert_number": self.alert_count
        })
    
    def generate_health_report(self):
        """
        Generate health report for all services
        """
        print("\n" + "="*60)
        print("📊 PRODUCTION HEALTH REPORT")
        print("="*60)
        
        healthy_count = 0
        total_services = len(self.services)
        
        for service_url in self.services:
            health_status = self.check_service_health(service_url)
            
            print(f"\n🔍 {service_url}")
            print(f"   Status: {health_status['status']}")
            print(f"   Response Time: {health_status.get('response_time', 'N/A')}ms")
            print(f"   Time: {health_status['timestamp']}")
            
            if health_status['status'] == "🟢 HEALTHY":
                healthy_count += 1
            else:
                self.send_alert(service_url, health_status)
        
        health_percentage = (healthy_count / total_services) * 100
        
        print(f"\n📈 SUMMARY STATISTICS:")
        print(f"   ✅ Healthy Services: {healthy_count}/{total_services}")
        print(f"   📊 Health Percentage: {health_percentage:.1f}%")
        print(f"   🚨 Total Alerts Sent: {self.alert_count}")
        print(f"   📅 Monitoring Since: {self.stats['start_time'].strftime('%Y-%m-%d %H:%M:%S')}")
        
        return health_percentage
    
    def start_continuous_monitoring(self, check_interval=60):
        """
        Start continuous monitoring loop
        """
        print("🚀 STARTING PRODUCTION MONITORING SYSTEM")
        print(f"📡 Monitoring {len(self.services)} services")
        print(f"⏰ Check interval: Every {check_interval} seconds")
        print("="*60)
        
        check_cycle = 0
        
        try:
            while True:
                check_cycle += 1
                print(f"\n🔄 CHECK CYCLE #{check_cycle}")
                print(f"🕒 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
                
                health_percentage = self.generate_health_report()
                
                if health_percentage < 50:
                    urgent_alert = f"""
                    🚨🚨 CRITICAL ALERT!
                    📉 Less than 50% of services are healthy!
                    📊 Current Health: {health_percentage:.1f}%
                    ⚠️ Immediate attention required!
                    """
                    print(urgent_alert)
                
                print(f"\n⏳ Waiting {check_interval} seconds for next check...")
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n🛑 MONITORING STOPPED")
            print("📈 Final Statistics:")
            print(f"   Total check cycles: {check_cycle}")
            print(f"   Total alerts sent: {self.alert_count}")
            print(f"   Total health checks: {self.stats['total_checks']}")
            print(f"   Healthy checks: {self.stats['healthy_checks']}")
            print(f"   Error checks: {self.stats['error_checks']}")
    
    def export_report(self, filename="monitoring_report.txt"):
        """
        Export monitoring history to file
        """
        with open(filename, 'w') as file:
            file.write("PRODUCTION MONITORING REPORT\n")
            file.write("=" * 50 + "\n")
            file.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
            file.write(f"Total Alerts: {self.alert_count}\n")
            file.write(f"Total Checks: {self.stats['total_checks']}\n\n")
            
            for alert in self.health_history:
                file.write(alert['alert'] + "\n")
                file.write("-" * 50 + "\n")
        
        print(f"📄 Report exported to: {filename}")


if __name__ == "__main__":
    services_to_monitor = [
        "https://www.google.com",
        "https://www.github.com",
        "https://www.youtube.com",
        "https://httpstat.us/500",
        "https://httpstat.us/404",
        "http://this-domain-does-not-exist-12345.com"
    ]
    
    print("Initializing Production Monitoring System...")
    monitor = ProductionMonitor(services_to_monitor)
    monitor.start_continuous_monitoring(check_interval=30)
