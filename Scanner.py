import requests  # HTTP requests library
from urllib.parse import urljoin  # Safely join base URL with paths
from config import URLS_TO_CHECK, ROLES, HTTP_METHODS  # Configuration constants
from analyzer import analyze_with_llm  # LLM-based response analyzer
from concurrent.futures import ThreadPoolExecutor  # For parallel execution

# Logs in (with a specific role) and returns an authenticated session
def login(role, base_url):
    with requests.Session() as session:
        if role in ["user", "admin"]:
            login_url = urljoin(base_url, "/rest/user/login")
            response = session.post(login_url, json=ROLES[role])
            if response.status_code == 200:
                print(f"[+] Logged in as {role}")
            else:
                print(f"[-] Failed to log in as {role}")
        return session

# Sends an request to a specific endpoint, then it analyzes the response
def scan_endpoint(session, base_url, path, role, method):
    full_url = urljoin(base_url, path)
    try:
        response = session.request(method, full_url, timeout=600, allow_redirects=False)
        status = response.status_code

        # Analyze only if the response indicates potential access
        if status in [200, 201, 204]:
            context = f" Possible Broken Access Control vulnerability detected:::\n- URL: {full_url}\n- Role: {role}\n- HTTP Method: {method}\n- Status Code: {status}\n\nResponse:\n{response.text[:500]}\n"
            analysis = analyze_with_llm(context)
        else:
            analysis = f"No issues detected at {full_url} (Status: {status})"

        return {
            "url": full_url,
            "role": role,
            "method": method,
            "status": status,
            "analysis": analysis
        }

    except Exception as e:
        # Handle request errors gracefully
        return {
            "url": full_url,
            "role": role,
            "method": method,
            "status": "Error",
            "analysis": f" Error: {str(e)}"
        }

# Main function to check all endpoints for all roles and methods
def check_endpoints(base_url):
    results = []
    with ThreadPoolExecutor(max_workers=5) as executor:
        for role in ROLES:
            session = login(role, base_url)
            futures = [
                executor.submit(scan_endpoint, session, base_url, path, role, method)
                for path in URLS_TO_CHECK
                for method in HTTP_METHODS
            ]
            for future in futures:
                results.append(future.result())
    return results
