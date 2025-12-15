import requests
import sys

BASE_URL = "http://127.0.0.1:5000/api"

def test_api():
    try:
        # 1. Get initial stats
        print("1. Getting initial stats...")
        res = requests.get(f"{BASE_URL}/stats")
        print(f"Status: {res.status_code}")
        if res.status_code != 200:
            print(f"Error Body: {res.text}")
        print(f"Stats: {res.json()}")
        
        # 2. Post positive comment
        print("\n2. Posting positive comment...")
        res = requests.post(f"{BASE_URL}/comments", json={"text": "I love this application, it is wonderful!"})
        data = res.json()
        print(f"Sentiment: {data['comment']['sentiment_score']}")
        if data['comment']['sentiment_score'] > 0:
            print("PASS: Detected positive sentiment")
        else:
            print("FAIL: Did not detect positive sentiment")

        # 3. Post negative comment
        print("\n3. Posting negative comment...")
        res = requests.post(f"{BASE_URL}/comments", json={"text": "This is a terrible and horrible mistake."})
        data = res.json()
        print(f"Sentiment: {data['comment']['sentiment_score']}")
        if data['comment']['sentiment_score'] < 0:
            print("PASS: Detected negative sentiment")
        else:
            print("FAIL: Did not detect negative sentiment")
            
        # 4. Check stats update
        print("\n4. Checking updated stats...")
        res = requests.get(f"{BASE_URL}/stats")
        print(f"Stats: {res.json()}")
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    test_api()
