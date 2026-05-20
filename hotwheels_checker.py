import requests
import time

BOT_TOKEN = "8846238134:AAHf6gtt_t3dU8nc_QlxPUGj9Vffq4radU0"
CHAT_ID = "8100056937"

def check_blinkit():
    url = "https://blinkit.com/v1/layout/search"
    params = {
        "offset": 0,
        "limit": 20,
        "actual_query": "hot wheels",
        "q": "hot wheels",
        "search_type": "type_to_search",
    }
    headers = {
        "App_client": "consumer_web",
        "App_version": "1010101010",
        "Access_token": "v2::4f765593-b536-49a1-88ce-a8f4d24eed6c",
        "Auth_key": "c761ec3633c22afad934fb17a66385c1c06c5472b4898b866b7306186d0bb477",
        "Device_id": "66012084bb7d5e9d",
        "Lat": "12.9837487",
        "Lon": "77.63924580000001",
        "Cookie": "gr_1_deviceId=a70542c4-3dae-4ceb-abc9-5bd0fd949d59; gr_1_locality=3; city=Bangalore",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
        "Accept": "*/*",
        "Origin": "https://blinkit.com",
        "Referer": "https://blinkit.com/s/?q=hot%20wheels",
    }
    response = requests.post(url, params=params, headers=headers)
    data = response.json()

    products = {}
    for snippet in data.get("response", {}).get("snippets", []):
        d = snippet.get("data", {})
        product_id = d.get("product_id")
        name = d.get("name", {}).get("text") or d.get("display_name", {}).get("text")
        state = d.get("product_state")
        if product_id and name and state == "available":
            link = f"https://blinkit.com/prn/{name.lower().replace(' ', '-')}/prid/{product_id}"
            products[product_id] = {"name": name, "link": link}
    return products

def send_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    requests.post(url, json={"chat_id": CHAT_ID, "text": message, "disable_web_page_preview": True})

known_ids = set()
first_run = True

while True:
    try:
        products = check_blinkit()
        current_ids = set(products.keys())

        if first_run:
            known_ids = current_ids
            first_run = False
            print(f"Started. Tracking {len(known_ids)} items.")
        else:
            new_ids = current_ids - known_ids
            if new_ids:
                for pid in new_ids:
                    p = products[pid]
                    send_telegram(f"🚗 New Hot Wheels on Blinkit!\n{p['name']}\n{p['link']}")
                    print(f"New item: {p['name']}")
                known_ids = current_ids
            else:
                print(f"Checked — {len(current_ids)} items, no new ones")
    except Exception as e:
        print(f"Error: {e}")
    time.sleep(60)