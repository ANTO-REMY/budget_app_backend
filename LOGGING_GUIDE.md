# 📊 Enhanced API Logging Guide

## Overview
The Budgetter API now includes comprehensive request/response logging that displays detailed information in the CLI/terminal when testing endpoints through Postman or any HTTP client.

## Features

### 🔵 Request Logging
Every incoming request logs:
- **Method**: GET, POST, PUT, DELETE, etc.
- **URL**: Full request URL with parameters
- **IP Address**: Client IP address
- **Content-Type**: Request content type
- **User-Agent**: Client information (truncated)
- **Request Body**: JSON payload (for POST/PUT requests)
- **Sensitive Data Masking**: Passwords and tokens are automatically masked

### ✅ Response Logging
Every outgoing response logs:
- **Status Code**: HTTP status with descriptive text
- **Duration**: Request processing time in milliseconds
- **Content-Type**: Response content type
- **Content-Length**: Response size
- **Response Body**: JSON response (truncated if large)
- **Color-Coded Status**: Visual indicators for success/error

## Status Code Indicators

| Status Range | Emoji | Color | Description |
|-------------|-------|-------|-------------|
| 200-299 | ✅ | Green | SUCCESS |
| 300-399 | 🔄 | Green | REDIRECT |
| 400-499 | ⚠️ | Yellow | CLIENT ERROR |
| 500-599 | ❌ | Red | SERVER ERROR |

## Sample Log Output

### Successful GET Request
```
18:11:05 | INFO | 🔵 REQUEST START
18:11:05 | INFO |    Method: GET
18:11:05 | INFO |    URL: http://127.0.0.1:5000/api/categories/
18:11:05 | INFO |    IP: 127.0.0.1
18:11:05 | INFO |    Content-Type: None
18:11:05 | INFO |    User-Agent: python-requests/2.32.5...
18:11:05 | INFO | ✅ RESPONSE SUCCESS
18:11:05 | INFO |    Status: 200 OK
18:11:05 | INFO |    Duration: 45.2ms
18:11:05 | INFO |    Content-Type: application/json
18:11:05 | INFO |    Content-Length: 100
18:11:05 | INFO |    Response: {
  "data": {
    "categories": [],
    "total": 0
  },
  "message": "Success",
  "success": true
}
18:11:05 | INFO | 🔵 REQUEST END - Total: 45.2ms
18:11:05 | INFO | ================================================================================
```

### POST Request with JSON Body
```
18:12:03 | INFO | 🔵 REQUEST START
18:12:03 | INFO |    Method: POST
18:12:03 | INFO |    URL: http://127.0.0.1:5000/api/categories/
18:12:03 | INFO |    IP: 127.0.0.1
18:12:03 | INFO |    Content-Type: application/json
18:12:03 | INFO |    User-Agent: python-requests/2.32.5...
18:12:03 | INFO |    Body: {
  "name": "Test Category",
  "parent_id": null
}
18:12:03 | INFO | ✅ RESPONSE SUCCESS
18:12:03 | INFO |    Status: 201 CREATED
18:12:03 | INFO |    Duration: 78.9ms
18:12:03 | INFO |    Content-Type: application/json
18:12:03 | INFO |    Content-Length: 206
18:12:03 | INFO |    Response: {
  "data": {
    "category": {
      "id": 1,
      "name": "Test Category",
      "parent_id": null,
      "parent_name": null
    }
  },
  "message": "Category created successfully",
  "success": true
}
18:12:03 | INFO | 🔵 REQUEST END - Total: 78.9ms
18:12:03 | INFO | ================================================================================
```

### Error Response (400 Bad Request)
```
18:13:48 | INFO | 🔵 REQUEST START
18:13:48 | INFO |    Method: POST
18:13:48 | INFO |    URL: http://127.0.0.1:5000/api/categories/
18:13:48 | INFO |    IP: 127.0.0.1
18:13:48 | INFO |    Content-Type: application/json
18:13:48 | INFO |    User-Agent: python-requests/2.32.5...
18:13:48 | INFO |    Body: {
  "name": "",
  "parent_id": null
}
18:13:48 | WARNING | ⚠️ RESPONSE CLIENT ERROR
18:13:48 | WARNING |    Status: 400 BAD REQUEST
18:13:48 | WARNING |    Duration: 12.5ms
18:13:48 | WARNING |    Content-Type: application/json
18:13:48 | WARNING |    Content-Length: 85
18:13:48 | WARNING |    Response: {
  "message": "Category name is required",
  "success": false
}
18:13:48 | INFO | 🔵 REQUEST END - Total: 12.5ms
18:13:48 | INFO | ================================================================================
```

## Security Features

### Sensitive Data Masking
The following fields are automatically masked in logs:
- `password`
- `password_hash`
- `current_password`
- `new_password`
- `access_token`
- `refresh_token`

Example:
```json
{
  "email": "user@example.com",
  "password": "***MASKED***",
  "first_name": "John"
}
```

## Testing the Logging

### Option 1: Use Postman
1. Import the updated `postman/collection.json`
2. Make requests to any endpoint
3. Watch the detailed logs in your Flask terminal

### Option 2: Use the Test Script
```bash
python test_logging.py
```

### Option 3: Use curl/PowerShell
```powershell
Invoke-WebRequest -Uri "http://127.0.0.1:5000/api/categories/" -Method GET
```

## Benefits

1. **🔍 Debugging**: See exactly what requests are coming in and responses going out
2. **⏱️ Performance**: Monitor request processing times
3. **🛡️ Security**: Sensitive data is automatically masked
4. **📊 Monitoring**: Clear status indicators for success/error states
5. **🎨 Visual**: Color-coded logs for easy identification
6. **📝 Detailed**: Complete request/response information for troubleshooting

## Configuration

The logging is automatically enabled when you run the Flask app. No additional configuration needed!

```bash
python app.py
```

The logs will appear in your terminal/CLI in real-time as you make API requests.
