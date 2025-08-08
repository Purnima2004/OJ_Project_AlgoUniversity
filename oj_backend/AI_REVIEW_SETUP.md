# AI Review Feature Setup

## Overview
The AI Review feature uses Google's Gemini model to provide intelligent code analysis and feedback to users.

## Setup Instructions

### 1. Get Google API Key
1. Go to [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Sign in with your Google account
3. Click "Create API Key"
4. Copy the generated API key

### 2. Configure Environment Variable
Set your Google API key as an environment variable:

**Windows (PowerShell):**
```powershell
$env:GOOGLE_API_KEY="your-api-key-here"
```

**Windows (Command Prompt):**
```cmd
set GOOGLE_API_KEY=your-api-key-here
```

**Linux/Mac:**
```bash
export GOOGLE_API_KEY="your-api-key-here"
```

### 3. Alternative: Direct Configuration
If you prefer to set the API key directly in the code (not recommended for production), edit `auth_app/views.py` and replace:
```python
GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY', 'your-api-key-here')
```
with:
```python
GOOGLE_API_KEY = 'your-actual-api-key-here'
```

## Features
- **Code Quality Assessment**: Analyzes code structure and style
- **Algorithm Analysis**: Evaluates the chosen approach
- **Complexity Analysis**: Provides time and space complexity insights
- **Issue Detection**: Identifies potential problems and bugs
- **Improvement Suggestions**: Offers specific recommendations
- **Overall Rating**: Gives a comprehensive evaluation

## Usage
1. Write code in the editor
2. Click the "AI Review" button in the sidebar
3. Wait for the analysis to complete
4. Review the structured feedback in the modal

## Security Note
- Never commit your API key to version control
- Use environment variables for production deployments
- The API key is only used server-side and never exposed to the client 