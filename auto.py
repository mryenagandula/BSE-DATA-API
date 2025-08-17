import schedule
import time
from exection import main

cronTimer = 15

def job():
    print("Job started... and current time is ", time.strftime("%Y-%m-%d %H:%M:%S"))
    print("Starting automation task...")
    main()
    print("Completed automation task.")

# Schedule the job every cronTimer minutes
schedule.every(cronTimer).minutes.do(job)

print(f"Scheduler started. Running every {cronTimer} minutes.")
while True:
    schedule.run_pending()
    time.sleep(1)