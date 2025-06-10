import requests  # For making HTTP requests to external APIs >> this is because it retrives it fro NVD API

# Fetches recent CVEs related to Broken Access Control from the NVD API
def fetch_related_cves(max_results=15):
    try:
        api_url = "https://services.nvd.nist.gov/rest/json/cves/2.0"

        # List of CWE IDs associated with Broken Access Control (based on OWASP 2021)
        broken_access_cwes = [
            "CWE-22", "CWE-23", "CWE-35", "CWE-59", "CWE-200", "CWE-201", "CWE-219",
            "CWE-264", "CWE-275", "CWE-276", "CWE-284", "CWE-285", "CWE-352", "CWE-359",
            "CWE-377", "CWE-402", "CWE-425", "CWE-441", "CWE-497", "CWE-538", "CWE-540",
            "CWE-548", "CWE-552", "CWE-566", "CWE-601", "CWE-639", "CWE-651", "CWE-668",
            "CWE-706", "CWE-862", "CWE-863", "CWE-913", "CWE-922", "CWE-1275"
        ]

        seen_ids = set()  # remove duplicate CVEs
        cves = []  # List to store formatted CVE entries

        # Loop through each CWE and fetch related CVEs
        for cwe_id in broken_access_cwes:
            params = {"cweId": cwe_id, "resultsPerPage": max_results}
            headers = {"User-Agent": "BrokenAccessScanner/1.0"}
            response = requests.get(api_url, params=params, headers=headers, timeout=15)
            response.raise_for_status()  # Raise error for bad responses
            data = response.json()

            # Extract CVE ID and description
            for item in data.get("vulnerabilities", []):
                cve = item.get("cve", {})
                cve_id = cve.get("id", "N/A")

                if cve_id in seen_ids:
                    continue   
                seen_ids.add(cve_id)

                # Get the description
                description = next(
                    (desc.get("value") for desc in cve.get("descriptions", []) if "value" in desc),
                    "No description available."
                )

                cves.append(f"- {cve_id}: {description}")

        return "\n".join(cves) if cves else "No relevant CVEs found."

    # errors handeling
    except requests.RequestException as req_err:
        return f"HTTP error: {str(req_err)}"
    except Exception as e:
        return f"Unexpected error: {str(e)}"
