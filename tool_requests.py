from schema import Literal, Schema
import os
import requests
import base64
from griptape.artifacts import BaseArtifact, ErrorArtifact, TextArtifact
from griptape.tools import BaseTool
from griptape.utils.decorators import activity

class ZendeskTool(BaseTool):
         
    @activity(
        config={
            "description": "Create Zendesk customer support tickets",
            "schema": Schema(
                {
                    Literal("requester_name"): str,
                    Literal("requester_email"): str,
                    Literal("subject"): str,
                    Literal("description"): str,
                },
            ),
        },
    )
    def new_ticket(self, params: dict) -> BaseArtifact: 
        try:
            # Get Zendesk credentials from environment
            zendesk_url = os.environ['ZENDESK_URL']
            zendesk_email = os.environ['ZENDESK_EMAIL']
            zendesk_token = os.environ['ZENDESK_TOKEN']
            
            # Extract subdomain from URL
            # Handle formats like: https://subdomain.zendesk.com or subdomain.zendesk.com or just subdomain
            url_clean = zendesk_url.replace('https://', '').replace('http://', '').rstrip('/')
            subdomain = url_clean.split('.')[0]
            
            # Construct API URL
            api_url = f"https://{subdomain}.zendesk.com/api/v2/tickets.json"
            
            # Extract ticket details
            requester_name = params["values"]["requester_name"]
            requester_email = params["values"]["requester_email"]
            subject = params["values"]["subject"]
            description = params["values"]["description"]
            
            # Prepare ticket data
            ticket_data = {
                "ticket": {
                    "subject": subject,
                    "comment": {
                        "body": description
                    },
                    "requester": {
                        "name": requester_name,
                        "email": requester_email
                    }
                }
            }
            
            # Create authentication header
            credentials = f"{zendesk_email}/token:{zendesk_token}"
            encoded_credentials = base64.b64encode(credentials.encode('utf-8')).decode('utf-8')
            
            headers = {
                "Content-Type": "application/json",
                "Authorization": f"Basic {encoded_credentials}"
            }
            
            # Make API request
            response = requests.post(api_url, json=ticket_data, headers=headers)
            
            # Check if request was successful
            if response.status_code == 201:
                ticket_response = response.json()
                ticket_id = ticket_response['ticket']['id']
                return TextArtifact(f"Ticket created successfully: ID #{ticket_id}")
            else:
                return ErrorArtifact(f"Error creating ticket: {response.status_code} - {response.text}")
                
        except KeyError as e:
            return ErrorArtifact(f"Missing required environment variable: {e}")
        except requests.exceptions.RequestException as e:
            return ErrorArtifact(f"HTTP request error: {e}")
        except Exception as e:
            return ErrorArtifact(f"Error creating ticket: {e}")

def init_tool() -> ZendeskTool:
    return ZendeskTool()
