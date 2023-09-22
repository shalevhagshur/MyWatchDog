import os
import time
import requests
import logging
import win32serviceutil
import win32service
import win32event
import servicemanager
import sys
import datetime

class WebsiteWatcher(win32serviceutil.ServiceFramework):
    # Windows service configuration
    _svc_name_ = "WebStalkerService"
    _svc_display_name_ = "Web Stalker Service"

    def __init__(self, args):
        win32serviceutil.ServiceFramework.__init__(self, args)
        self.hWaitStop = win32event.CreateEvent(None, 0, 0, None)
        self.is_alive = True
        # Initialize the logger for logging website status
        self.logger = self.setup_logger()

    def SvcStop(self):
        # Handle service stop request
        self.ReportServiceStatus(win32service.SERVICE_STOP_PENDING)
        win32event.SetEvent(self.hWaitStop)
        self.is_alive = False

    def SvcDoRun(self):
        # Log service start
        servicemanager.LogMsg(servicemanager.EVENTLOG_INFORMATION_TYPE,
                              servicemanager.PYS_SERVICE_STARTED,
                              (self._svc_name_, ''))
        while self.is_alive:
            self.main()

    def setup_logger(self):
        # Set up the logger for recording website status
        logger = logging.getLogger('WebsiteWatcher')
        logger.setLevel(logging.INFO)
        log_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'website_watcher.log')
        
        try:
            handler = logging.FileHandler(log_file_path)
        except IOError as e:
            # Handle any file-related errors here
            print(f"Error creating log file: {e}")
            handler = None
        
        if handler:
            formatter = logging.Formatter('%(asctime)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        
        return logger


    def check_website(self, url):
        try:
            # Send a GET request to the website
            response = requests.get(url)

            # Check if the website responded with a success status code (e.g., 200)
            if response.status_code == 200:
                return True
        except Exception:
            pass
        return False

    def main(self):
        website_url = "https://server.pro/"  # Change this to the URL you want to monitor
        is_website_up = False

        while self.is_alive:
            # Check if the website is up
            new_is_website_up = self.check_website(website_url)

            if new_is_website_up:
                # If the website is up, but it was previously down, log its status and set the last_log_time
                if not is_website_up:
                    self.logger.info(f"Website {website_url} is up and running.")
                    last_log_time = datetime.datetime.now()
                # If it's been an hour since the last log, log its status
                elif (datetime.datetime.now() - last_log_time).total_seconds() >= 3600:
                    self.logger.info(f"Website {website_url} is still up and running.")
                    last_log_time = datetime.datetime.now()
            else:
                # Log that the website has fallen with the current timestamp
                self.logger.error(f"Website {website_url} has fallen at {datetime.datetime.now()}")
                last_log_time = datetime.datetime.now()

            # Update the is_website_up flag
            is_website_up = new_is_website_up

            # Sleep for 3 minutes before checking again
            time.sleep(180)  # Sleep for 3 minutes

if __name__ == '__main__':
    if len(sys.argv) == 2 and sys.argv[1] == 'stop':
        # Check if the 'stop' argument is provided and stop the service
        win32serviceutil.StopService('WebStalkerService')
    else:
        # Otherwise, start the service as usual
        win32serviceutil.HandleCommandLine(WebsiteWatcher)