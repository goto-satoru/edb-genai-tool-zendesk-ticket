# ZenDesk Tools

this tool allows to create a new ticket.

## create .venv

```
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Archive the Tool to zip file

```
zip -r ../zendesk_tool.zip . -x "*.git*" -x "*__pycache__*" -x "*.venv/lib/python*/site-packages/*"
```

## upload the Data Lake of GenAI Builder

## create a Tool in Tools of GenAI Builder

### in Test tab, then make a POST call to /activities/new_ticket
