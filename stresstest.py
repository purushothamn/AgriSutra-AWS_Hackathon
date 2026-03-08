import threading
import time
import requests

# URL of your deployed Streamlit app (or local for testing)
TARGET_URL = "https://agrisutra-aws-hackathon-proto.streamlit.app/"

# CONFIGURATION
CONCURRENT_USERS = 5  # Number of simulated farmers asking questions at once
TEST_DURATION_SECONDS = 30

def simulate_user(user_id):
    print(f"User {user_id}: Starting session...")
    start_time = time.time()
    
    while time.time() - start_time < TEST_DURATION_SECONDS:
        try:
            # We simulate a GET request to the app. 
            # Note: For deep testing, use 'Locust' or 'Selenium', but this 
            # checks if the Streamlit server stays responsive under load.
            response = requests.get(TARGET_URL, timeout=10)
            status = "✅ Success" if response.status_code == 200 else f"❌ Error {response.status_code}"
            print(f"User {user_id}: {status} ({len(response.content)} bytes)")
        except Exception as e:
            print(f"User {user_id}: ⚠️ Connection Failed: {e}")
        
        time.sleep(2) # 2-second delay between "clicks"

threads = []
for i in range(CONCURRENT_USERS):
    t = threading.Thread(target=simulate_user, args=(i,))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

print("\n--- Stress Test Complete ---")