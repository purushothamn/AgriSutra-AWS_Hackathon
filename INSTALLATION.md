# AgriSutra Installation Guide

This guide will help you set up the AgriSutra Farm Intelligence System on your local machine.

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.8 or higher**: Check with `python --version`
- **pip**: Python package installer (usually comes with Python)
- **Git**: For cloning the repository (optional)

## Step-by-Step Installation

### Step 1: Verify Project Structure

Run the verification script to ensure all files are in place:

```bash
python verify_setup.py
```

You should see "All checks passed (19/19)" message.

### Step 2: Create Virtual Environment and Install Dependencies

**On Windows:**
```bash
setup.bat
```

**On Linux/Mac:**
```bash
chmod +x setup.sh
./setup.sh
```

**Manual Installation (if scripts don't work):**
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate.bat
# On Linux/Mac:
source venv/bin/activate

# Upgrade pip
python -m pip install --upgrade pip

# Install dependencies
pip install -r requirements.txt
```

### Step 3: Configure AWS Credentials

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```

2. Edit `.env` file with your AWS credentials:
   ```
   AWS_REGION=us-east-1
   AWS_ACCESS_KEY_ID=your_access_key_here
   AWS_SECRET_ACCESS_KEY=your_secret_key_here
   S3_CACHE_BUCKET=agrisutra-cache
   DYNAMODB_TABLE=agrisutra-sessions
   WEATHER_API_KEY=your_openweathermap_api_key_here
   ```

3. **Getting AWS Credentials:**
   - Log in to AWS Console
   - Go to IAM → Users → Your User → Security Credentials
   - Create Access Key if you don't have one
   - Copy Access Key ID and Secret Access Key

4. **Required AWS Permissions:**
   Your AWS user needs permissions for:
   - AWS Bedrock (Claude 3 Haiku model access)
   - AWS Transcribe
   - AWS Polly
   - AWS S3 (optional, for caching)
   - AWS DynamoDB (optional, for session storage)

### Step 4: Verify Installation

Test that the configuration module loads correctly:

```bash
python -c "from agrisutra import config; print('✓ Config loaded'); print(f'Languages: {config.SUPPORTED_LANGUAGES}')"
```

You should see:
```
✓ Config loaded
Languages: ['hi', 'kn', 'ta']
```

### Step 5: Run Tests (Optional)

Verify everything works by running the test suite:

```bash
# Activate virtual environment first
# On Windows: venv\Scripts\activate.bat
# On Linux/Mac: source venv/bin/activate

# Run tests
pytest tests/unit/test_config.py -v
```

### Step 6: Start the Application

```bash
# Make sure virtual environment is activated
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## Troubleshooting

### Issue: "No module named 'boto3'"

**Solution:** Make sure you activated the virtual environment:
```bash
# On Windows:
venv\Scripts\activate.bat
# On Linux/Mac:
source venv/bin/activate
```

### Issue: "AWS credentials not found"

**Solution:** 
1. Check that `.env` file exists in the project root
2. Verify the credentials are correct
3. Ensure no extra spaces in the `.env` file

### Issue: "Permission denied" when running setup.sh

**Solution:** Make the script executable:
```bash
chmod +x setup.sh
./setup.sh
```

### Issue: Python version too old

**Solution:** Install Python 3.8 or higher:
- **Windows**: Download from [python.org](https://www.python.org/downloads/)
- **Linux**: `sudo apt-get install python3.8` (Ubuntu/Debian)
- **Mac**: `brew install python@3.8`

### Issue: "streamlit: command not found"

**Solution:** 
1. Activate virtual environment
2. Reinstall dependencies: `pip install -r requirements.txt`

## Verification Checklist

Before proceeding to development, verify:

- [ ] Virtual environment created and activated
- [ ] All dependencies installed (`pip list` shows boto3, streamlit, etc.)
- [ ] `.env` file configured with AWS credentials
- [ ] Config module imports successfully
- [ ] Tests pass (if running tests)
- [ ] Streamlit app starts without errors

## Next Steps

Once installation is complete:

1. Review the [README.md](README.md) for usage instructions
2. Check the [design document](.kiro/specs/agrisutra-farm-intelligence/design.md) for architecture details
3. Start implementing features according to the [tasks](.kiro/specs/agrisutra-farm-intelligence/tasks.md)

## Getting Help

If you encounter issues not covered here:

1. Check the [README.md](README.md) troubleshooting section
2. Review AWS service status at [status.aws.amazon.com](https://status.aws.amazon.com)
3. Verify your AWS account has Bedrock access enabled
4. Check Python and pip versions are compatible

## Environment Variables Reference

| Variable | Description | Required | Default |
|----------|-------------|----------|---------|
| AWS_REGION | AWS region for services | Yes | us-east-1 |
| AWS_ACCESS_KEY_ID | AWS access key | Yes | - |
| AWS_SECRET_ACCESS_KEY | AWS secret key | Yes | - |
| S3_CACHE_BUCKET | S3 bucket for caching | No | agrisutra-cache |
| DYNAMODB_TABLE | DynamoDB table name | No | agrisutra-sessions |
| WEATHER_API_KEY | OpenWeatherMap API key | No | - |

## Dependencies

The project uses the following main dependencies:

- **boto3**: AWS SDK for Python
- **streamlit**: Web UI framework
- **hypothesis**: Property-based testing
- **pytest**: Testing framework
- **moto**: AWS service mocking for tests
- **responses**: HTTP mocking for tests

See [requirements.txt](requirements.txt) for complete list with versions.
