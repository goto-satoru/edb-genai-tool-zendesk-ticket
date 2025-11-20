# ZenDesk Tools

## create .venv and dependent 

```
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Archive the Tool to zip file

```
zip -r ../zendesk_requests_tool.zip . -x "*.git*" -x "*__pycache__*" -x "*.venv/lib/python*/site-packages/*"
```
