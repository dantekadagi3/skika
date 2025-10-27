function varargout = readme(action)
% README  Show or return the project's README embedded in this file
%
% Usage:
%   readme()            - print the embedded README to the command window
%   readme('show')      - same as readme()
%   txt = readme('get') - return README content as a char array
%
% This file contains an embedded copy of README.md between markers. That
% makes the README available to MATLAB even if the external README.md is
% missing. The function extracts the embedded block and either prints or
% returns it.

if nargin < 1 || isempty(action)
        action = 'show';
end
action = lower(action);

try
        txt = get_embedded_readme();
catch ME
        error('readme:ReadError', 'Failed to extract embedded README: %s', ME.message);
end

switch action
        case {'show','print'}
                fprintf('%s\n', txt);
        case {'get','return'}
                if nargout >= 1
                        varargout{1} = txt;
                else
                        fprintf('%s\n', txt);
                end
        otherwise
                error('readme:BadArg', 'Unknown action ''%s''. Use ''show'' or ''get''.', action);
end

end

function txt = get_embedded_readme()
% Read this .m file and extract the text between the README markers
fullpath = [mfilename('fullpath') '.m'];
s = fileread(fullpath);
startTag = '%%% README:START';
endTag   = '%%% README:END';
i1 = strfind(s, startTag);
i2 = strfind(s, endTag);
if isempty(i1) || isempty(i2) || i2 <= i1
        error('readme:NoEmbedded', 'Embedded README markers not found in %s', fullpath);
end
% Extract content between tags
txt = s(i1 + length(startTag) : i2 - 1);
% Remove leading newlines and carriage returns
if ~isempty(txt) && (txt(1) == char(10) || txt(1) == char(13))
        txt = regexprep(txt, '^\r?\n', '');
end
% Normalize CRLF -> LF
txt = strrep(txt, char(13), '');
end

% Embedded README (kept here for portability). Do not modify the markers
% unless you update the extraction code above.
%{
%%% README:START
Skika Backend - A Voice for Gatundu North
Overview
The Skika Backend System is the backbone of the Skika platform, powering USSD interactions, securely managing data, coordinating feedback between citizens and leaders, and ensuring transparency and accountability. It connects the frontend (USSD & Dashboard), database (PostgreSQL), and APIs (communication layer) to achieve these goals. The backend is designed for scalability, data security, and ease of integration.
Objectives

Receive and store reports from USSD users across Gatundu North.
Facilitate two-way communication between youth (citizens) and administrators (e.g., NG-CDF officers, local leaders).
Automate feedback loops using SMS notifications.
Ensure data integrity, privacy, and traceability for every interaction.

System Architecture (High-Level)
textUser (Phone)
     ↓
USSD Gateway (Africa's Talking)
     ↓
Django REST API
     ↓
PostgreSQL Database
     ↓
Admin Dashboard (React)
     ↓
SMS Notification (Africa's Talking)
Data Flow

User Dial: A citizen dials 45601# and selects an option (Report / Suggest / Track).
USSD Gateway Request: Africa's Talking forwards user input to the Skika backend via POST requests.
API Processing: Django REST API validates and stores the request, generating a reference code (e.g., SKK-2025-012).
Database Entry: The report is stored in PostgreSQL under status = "Received".
Dashboard Update: Admins can view, filter, and act on reports via the web dashboard.
Feedback Loop: Status changes trigger SMS updates to users.

Technology Stack







































LayerTechnologyPurposeBackend FrameworkDjango REST Framework (Python)Rapid API development, scalability, built-in authenticationDatabasePostgreSQLReliable, relational database supporting complex queriesUSSD/SMS IntegrationAfrica's Talking APIHandles incoming and outgoing USSD/SMS requestsHosting/DeploymentRender / RailwaySimple, scalable, and supports continuous deploymentAuthenticationJWT (JSON Web Tokens)Secures dashboard and API endpointsVersion ControlGitHubTeam collaboration and change tracking
Setup Instructions
Prerequisites

Python 3.8+
PostgreSQL
Redis (for caching)
Africa's Talking API credentials

Installation

Clone the repository:
bashgit clone https://github.com/yourusername/skika-backend.git
cd skika-backend

Create a virtual environment and activate it:
bashpython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

Install dependencies:
bashpip install -r requirements.txt

Configure environment variables in a .env file:
textSECRET_KEY=your_secret_key
DEBUG=True
DB_USER=your_db_user
DB_PASSWORD=your_db_password
AFRICASTALKING_USERNAME=your_africastalking_username
AFRICASTALKING_API_KEY=your_africastalking_api_key

Set up the database:
bashpython manage.py makemigrations
python manage.py migrate

Create a superuser:
bashpython manage.py createsuperuser

Run the development server:
bashpython manage.py runserver


API Documentation
All endpoints require JWT authentication for admin access or token-based authentication for USSD. Obtain a JWT token via /api/token/ using rest_framework_simplejwt.
1. User Management

Endpoint: POST /api/users/register/

Method: POST
Description: Register a new user.
Sample Input:
json{
    "phone_number": "+254712345678",
    "role": "citizen",
    "ward": "Ward1"
}

Sample Output (Success - 201 Created):
json{
    "id": 1,
    "phone_number": "+254712345678",
    "role": "citizen",
    "ward": "Ward1",
    "created_at": "2025-10-27T11:36:00Z"
}

Sample Output (Error - 400 Bad Request):
json{
    "phone_number": ["A user with this phone number already exists."]
}



Endpoint: GET /api/users/

Method: GET
Description: List all users (admin only).
Sample Input: None (requires JWT token in header)
Sample Output (Success - 200 OK):
json[
    {
        "id": 1,
        "phone_number": "+254712345678",
        "role": "citizen",
        "ward": "Ward1",
        "created_at": "2025-10-27T11:36:00Z"
    }
]




2. Report Management

Endpoint: POST /api/reports/

Method: POST
Description: Create a new report.
Sample Input:
json{
    "ward": "Ward1",
    "category": "Infrastructure",
    "description": "Road issue"
}

Sample Output (Success - 201 Created):
json{
    "id": 1,
    "ref_id": "SKK-2025-abc123",
    "user": 1,
    "ward": "Ward1",
    "category": "Infrastructure",
    "description": "Road issue",
    "status": "Received",
    "created_at": "2025-10-27T11:36:00Z",
    "updated_at": "2025-10-27T11:36:00Z",
    "audit_trail": "Initial creation at Mon Oct 27 11:36:00 2025"
}




Endpoint: POST /api/reports/{id}/update_status/

Method: POST
Description: Update report status.
Sample Input:
json{
    "status": "Under Review"
}

Sample Output (Success - 200 OK):
json{
    "status": "success"
}

Sample Output (Error - 400 Bad Request):
json{
    "error": "Invalid status"
}




Endpoint: POST /api/reports/ussd_menu/

Method: POST
Description: Handle USSD menu interactions.
Sample Input:
json{
    "sessionId": "session123",
    "text": "1 Test Issue"
}

Sample Output (Success - 200 OK):
json{
    "USSResponse": "END Report SKK-2025-xyz789 submitted"
}




3. Project Management

Endpoint: POST /api/projects/

Method: POST
Description: Create a new project.
Sample Input:
json{
    "name": "Road Project",
    "ward": "Ward1",
    "description": "New road construction"
}

Sample Output (Success - 201 Created):
json{
    "id": 1,
    "name": "Road Project",
    "ward": "Ward1",
    "description": "New road construction",
    "created_at": "2025-10-27T11:36:00Z"
}



4. Feedback Management

Endpoint: POST /api/feedback/

Method: POST
Description: Submit feedback for a report.
Sample Input:
json{
    "report": 1,
    "satisfaction": "Yes",
    "comments": "Good work"
}

Sample Output (Success - 201 Created):
json{
    "id": 1,
    "report": 1,
    "satisfaction": "Yes",
    "comments": "Good work",
    "created_at": "2025-10-27T11:36:00Z"
}



5. Analytics

Endpoint: GET /api/reports/sentiment_analysis/

Method: GET
Description: Retrieve sentiment analysis of report descriptions.
Sample Input: None (requires JWT token in header)
Sample Output (Success - 200 OK):
json{
    "1": 0.5,
    "2": -0.2
}




Testing
Run tests to verify API functionality:
bashpython manage.py test
Contributing

Fork the repository.
Create a new branch: git checkout -b feature-branch.
Commit changes: git commit -m "Add new feature".
Push to the branch: git push origin feature-branch.
Submit a pull request.

License
This project is licensed under the MIT License - see the LICENSE file for details.
Contact
For questions or support, contact the project maintainers at your-email@example.com.

Notes

Replace placeholders (e.g., yourusername, your_secret_key, your-email@example.com) with actual values.
The requirements.txt file should include all dependencies (e.g., django, djangorestframework, djangorestframework-simplejwt, psycopg2-binary, python-decouple, africastalking, django-redis, textblob).

%%% README:END
%}
