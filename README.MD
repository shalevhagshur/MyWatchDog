# Website Watcher Windows Service

The Website Watcher Windows Service is a Python-based service that monitors a website's status. It periodically checks if a specified website is up and running. If the website is up, it logs a message indicating that it's operational. If the website is down, it logs an error message with the current timestamp.

## Important shit to know
 after stoping the service wait 3 minutes before reinstalling
 some websites block watchdog by blocking request so it wont work on themgit commit -m "first commit"J

## Installation

1. **Install Requirments**:

  run this in the terminal: pip install -r Requirements.txt
 

2. **Clone the Repository**:
   Clone this repository to your local machine or download the source code.

3. **Configure the Service**:
   - Open the `Watchdog.py` script in a text editor.
   - Modify the `website_url` variable to specify the URL of the website you want to monitor.

4. **Install the Windows Service**:
   Open a Command Prompt or PowerShell window as an administrator and navigate to the directory containing `Watchdog.py`. Install the service using the following command:

5. **Start and Manage the Service**:
- Start the service:
  ```
  py -m pywin32_system32 start WebStalkerService
  ```
- Stop the service:
  ```
  py -m pywin32_system32 stop WebStalkerService
  ```
- View the service status:
  ```
  py -m pywin32_system32 status WebStalkerService
  ```
- Uninstall the service
  ```
  py -m pywin32_system32 remove WebStalkerService
  ```

## Usage

Once the service is installed and running, it will periodically check the specified website's status and log the results in the `website_watcher.log` file located in the same directory as the script.

You can review the log file to monitor the website's status and timestamps.

## Customization

- You can customize the check interval (currently set to 3 minutes) by modifying the `time.sleep()` value in the `main` function.
- To change the log file location or format, you can modify the logger configuration in the `setup_logger` function.


## Acknowledgments

- This Windows service is created using the `pywin32` library.
- Website status checks are performed using the `requests` library.

Feel free to enhance and customize the service according to your specific requirements.
