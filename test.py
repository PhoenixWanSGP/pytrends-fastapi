import requests

def test_individual_proxies():
    proxies = [
        "http://49.13.215.9:80",
        "http://47.88.31.196:8080",
        "http://5.75.200.249:80",
        "http://93.177.67.178:80",
        "http://198.49.68.80:80",
        "http://162.240.75.37:80",
        "http://20.235.159.154:80"
    ]

    for proxy in proxies:
        try:
            print(f"Testing proxy: {proxy}")
            response = requests.get('https://trends.google.com/trends/api/explore', proxies={'http': proxy, 'https': proxy}, verify=False)
            print(f"Proxy {proxy} works! Response: {response.status_code}")
            return proxy
        except requests.exceptions.ProxyError as e:
            print(f"Proxy {proxy} error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")

    return None

if __name__ == "__main__":
    working_proxy = test_individual_proxies()
    if working_proxy:
        print(f"Working proxy: {working_proxy}")
    else:
        print("No working proxies found.")
