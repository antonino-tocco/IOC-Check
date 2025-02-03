# IOC CHECK

## Description

This python script checks for the presence of known Indicators of Compromise (IoCs) in the data based on OTX Alienvault and VirusTotal.

## Before you start

Generate the API keys for OTX Alienvault and VirusTotal.

## Setup

1. Install the required libraries using the following command:
```pip install -r requirements.txt```

## Run

1. Run the script using the following command:
```python ioc_check.py --otx_api_key <OTX_API_KEY> --vt_api_key <VIRUS_TOTAL_API_KEY> --base_path <BASE_PATH> --network```

If running without the base path, the script will check for the IoCs recursively in the user home directory .

## Output

At the time of writing, the script will output in the console when an IoC is found in the data.

## Next Steps

1. Add more IoCs to the list.
2. Add more sources for IoCs.
3. Add more output options.
4. Add ability to scan network traffic for IoCs.

## References

1. [OTX Alienvault](https://otx.alienvault.com/)
2. [VirusTotal](https://www.virustotal.com/gui/home/upload)