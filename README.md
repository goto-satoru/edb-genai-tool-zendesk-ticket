# EDB PGAI GenAI Builder sample Tool for ZenDesk ticketing

A Griptape-based tool for creating and managing ZenDesk customer support tickets programmatically. This tool provides a simple Python interface to interact with the ZenDesk API, enabling automated ticket creation through the Griptape framework.

## 🌟 Features

- **Easy Ticket Creation**: Create ZenDesk support tickets programmatically
- **Griptape Integration**: Built as a Griptape tool for seamless integration with AI agents
- **Environment-based Configuration**: Secure credential management using environment variables
- **Comprehensive Error Handling**: Robust error handling with detailed error messages
- **Simple API**: Clean, intuitive interface for ticket operations

## 📋 Prerequisites

- Python 3.12 or higher
- A ZenDesk account with API access
- ZenDesk API token (can be generated from your ZenDesk admin panel)

## 🚀 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/EnterpriseDB/cx-tam-genai-tool-zendesk-ticket.git tool_zendesk
   cd tool_zendesk
   ```

2. **Create a Python virtual environment**:
   ```bash
   python3.12 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**:
   
   Copy the sample environment file:
   ```bash
   cp dotenv-sample .env
   ```
   
   Edit `.env` with your ZenDesk credentials:
   ```
   ZenDesk_URL=https://your-subdomain.zendesk.com/api/v2
   ZenDesk_EMAIL=your_email@company.com
   ZenDesk_TOKEN=your_api_token_here
   ```

## 🔑 Getting ZenDesk API Credentials

1. **Log in to your ZenDesk account** as an administrator
2. Navigate to **Admin** → **Channels** → **API**
3. Enable **Token Access**
4. Click **Add API Token**
5. Provide a description (e.g., "Griptape Tool Access")
6. Copy the generated token and save it in your `.env` file

## 📖 Usage

### create a Tool zip file

```
zip -r ../zendesk_tool.zip . -x "*.git*" -x "*__pycache__*" -x "*.venv/lib/python*/site-packages/*"
```

### upload a zip file to Data Lake

in GenAI Builder, navigate to data Lake in the left pane, then click "Create Bucket" button
to create a new bucket (.eg. test)

then, upload the zendesk_tool.zip file to the created bucket

### Create a Tool with GenAI Builder

navigate to Tools in the left pane, then select "Griptape Tool from Data Lake", 

```
Name: ZenDesk
Data Lake 
Bucket ID: test
Asset Path: zendesk_tool.zip
Environment Variables
  ZENDESK_URL=https://enterprisedb-61235.zendesk.com/api/v2
  ZENDESK_EMAIL=your_email@company.com
  ZENDESK_TOKEN=ZWtXyzxyzxyzxyzxyzxyzxyzxyzxyzxyzxyzxyzxyz
```

click "Create" button at the bottom to complete.

### make a test of the Tool

Navigate to "POST /activities/new_ticket", click "Try it out", then edit value(payload) as below:

```
{
  "subject": "GenAI Builder Tool test",
  "description": "GenAI Builder Tool test",
  "requester_name": "a customer",
  "requester_email": "test@gmail.com"
}
```

click "Execute" to create a new ZenDesk ticket.


### Using the Test Script

A comprehensive test script is provided to verify your setup:

```bash
python test_tool.py
```

This script will:
- ✅ Validate environment variables
- ✅ Initialize the tool using `init_tool()`
- ✅ List available activities
- ✅ Create a test ticket
- ✅ Display the result

## 🛠️ Tool Configuration

The tool is configured via `tool_config.yaml`:

```yaml
version: 1.0
runtime: python3
runtime_version: 3.12
build:
  requirements_file: requirements.txt
run:
  tool_file: tool.py
  init_tool_file: tool.py
  init_tool_function: init_tool
```

## 📚 API Reference

### ZenDeskTool Class

#### Activity: `new_ticket`

Creates a new ZenDesk support ticket.

**Parameters**:
- `requester_name` (str): Name of the person requesting support
- `requester_email` (str): Email address of the requester
- `subject` (str): Ticket subject line
- `description` (str): Detailed description of the issue

**Returns**:
- `TextArtifact`: Success message with ticket ID
- `ErrorArtifact`: Error message if creation fails

**Example**:
```python
params = {
    "values": {
        "requester_name": "Jane Smith",
        "requester_email": "jane.smith@example.com",
        "subject": "Database performance issue",
        "description": "Queries are running slower than expected on production database."
    }
}
result = ZenDesk_tool.new_ticket(params)
```

## 🔧 Deployment to GenAI Builder

### Archive the Tool

Create a zip file for deployment:

```bash
zip -r ../ZenDesk_tool.zip . -x "*.git*" -x "*__pycache__*" -x "*.venv/lib/python*/site-packages/*"
```

### Upload to GenAI Builder

1. **Upload to Data Lake**: Upload the `ZenDesk_tool.zip` file to the Data Lake of GenAI Builder
2. **Create a Tool**: In the Tools section of GenAI Builder, create a new tool
3. **Configure the Tool**: Link the uploaded zip file to your new tool

### Testing in GenAI Builder

In the Test tab, make a POST call to `/activities/new_ticket` with the following payload:

```json
{
  "requester_name": "Test User",
  "requester_email": "test@example.com",
  "subject": "Test Ticket from GenAI Builder",
  "description": "This is a test ticket created through GenAI Builder."
}
```

## 🔒 Security Best Practices

1. **Never commit your `.env` file** to version control
2. **Use strong API tokens** and rotate them periodically
3. **Limit API token permissions** to only what's necessary
4. **Store credentials securely** in production environments (e.g., AWS Secrets Manager, Azure Key Vault)
5. **Exclude sensitive files** from deployment archives

## 🧪 Testing

Run the test script to verify your installation:

```bash
python3 test_tool.py
```

Expected output:
```
======================================================================
Testing tool.py via init_tool()
======================================================================

✓ Environment variables loaded
  ZenDesk_URL: https://your-subdomain.ZenDesk.com
  ZenDesk_EMAIL: your_email@company.com
  ZenDesk_TOKEN: ********************

Calling init_tool()...
✓ Tool initialized: <tool.ZenDeskTool object>
...
✅ Success:
   Ticket created successfully: ID #12345
======================================================================
```

## 📦 Dependencies

- **griptape** (>=1.2.1): Framework for building AI agents and tools
- **python-dotenv**: Environment variable management
- **schema**: Data validation
- **requests**: HTTP library for API calls

See `requirements.txt` for the complete list.

## 🐛 Troubleshooting

### Common Issues

**Issue**: "Missing required environment variable: ZenDesk_URL"
- **Solution**: Ensure your `.env` file exists and contains all required variables

**Issue**: "Error creating ticket: 401 - Unauthorized"
- **Solution**: Verify your API token is correct and has not expired

**Issue**: "Error creating ticket: 422 - Unprocessable Entity"
- **Solution**: Check that the requester email is valid and properly formatted

**Issue**: URL formatting errors
- **Solution**: The tool accepts URLs in multiple formats:
  - `https://subdomain.ZenDesk.com`
  - `subdomain.ZenDesk.com`
  - `subdomain`

## 🏗️ Project Structure

```
├── tool.py                 # Main tool implementation
├── tool_config.yaml        # Tool configuration for GenAI Builder
├── requirements.txt        # Python dependencies
├── dotenv-sample          # Sample environment variables file
├── test_init_tool.py      # Comprehensive test script
├── list_modules.py        # Module listing utility
└── README.md              # This file
```


## 👥 Authors

EnterpriseDB Corporation

## 🔗 Related Resources

- [ZenDesk API Documentation](https://developer.ZenDesk.com/api-reference/)
- [EDB Postgres AI AI Factory GenAI Builder Tools](https://www.enterprisedb.com/docs/edb-postgres-ai/latest/ai-factory/gen-ai/tools/)
- [Griptape Documentation](https://docs.griptape.ai/)

## 📞 Support

For issues or questions:
- Create an issue in this repository
- Contact the EDB Customer Experience team

---

**Note**: This tool is designed for use with EnterpriseDB's ZenDesk instance but can be adapted for any ZenDesk account.
