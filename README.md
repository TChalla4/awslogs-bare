# AWSLogs

A simple command-line tool for browsing, searching, and analyzing AWS CloudWatch Logs. Requires Python3.7

## Installation

Install directly from your local directory:

```bash
pip install -e /path/to/your/awslogs-bare
```

Or if you have downloaded the repository:

```bash
cd /path/to/your/awslogs-bare
pip install .
```

## 🌐 AWS Region Configuration

You must specify an AWS region with all commands using one of these methods:

1. Command line parameter:
   ```bash
   --aws-region us-east-1
   ```

2. Environment variable:
   ```bash
   export AWS_REGION=us-east-1
   ```

All examples below assume you've configured the region using one of these methods.

## 🚀 Basic Commands

### List all Log Groups

```bash
awslogs groups
```

### List Streams in a Log Group

```bash
awslogs streams <GROUP_NAME>
```

### Get Logs from a Log Group (ALL Streams)

```bash
awslogs get <GROUP_NAME> ALL
```

### Get Logs from a Specific Stream

```bash
awslogs get <GROUP_NAME> '<STREAM_NAME>'
```

## 🧠 What is ALL?

In awslogs, when you use `ALL`:

* It automatically matches all streams inside a log group
* ✅ No need to know exact stream names
* ✅ Especially helpful for Lambda logs where streams are random per invocation

Example:

```bash
awslogs get /aws/lambda/my-function ALL --aws-region us-east-1
```

## 🕑 Time Filtering Options

You can filter logs by time using `--start` (or `-s`) and `--end` (or `-e`):

| Time Range | Example |
|------------|---------|
| Minutes | `--start='5m'` (5 minutes ago) |
| Hours | `--start='2h'` (2 hours ago) |
| Days | `--start='1d'` (1 day ago) |
| Weeks | `--start='3w'` (3 weeks ago) |
| Specific time | `--start='2025-04-24 12:00' --end='2025-04-24 14:00'` |

Time can be specified in multiple formats:

```bash
# Minutes
--start='2m'          # Events from 2 minutes ago
--start='5 minutes'   # Events from 5 minutes ago

# Hours
--start='1h'          # Events from 1 hour ago
--start='3 hours'     # Events from 3 hours ago

# Days
--start='2d'          # Events from 2 days ago
--start='1 day'       # Events from 1 day ago

# Weeks
--start='1w'          # Events from 1 week ago
--start='2 weeks'     # Events from 2 weeks ago

# Specific dates
--start='23/1/2025 12:00'             # Events after midday, Jan 23, 2025
--start='1/1/2025'                    # Events after midnight, Jan 1, 2025
--start='Sat Oct 11 17:13:46 UTC 2024' # Events after specific datetime
```

⏰ **Best Practice**: Always use a time filter to avoid pulling too much data!

## 🔍 Filter Pattern Options

You can use `--filter-pattern` to retrieve only logs that match a CloudWatch Logs Filter pattern.

### Basic Text Matching

```bash
# Search for error logs
awslogs get <GROUP_NAME> ALL --filter-pattern="ERROR" --start='1h'

# Search for multiple terms (OR condition)
awslogs get <GROUP_NAME> ALL --filter-pattern='"ERROR" || "WARN" || "INFO"' --start='1h'
```

### JSON Log Filtering

For JSON-formatted logs, use JSON filter patterns:

```bash
# Match a specific field value
awslogs get <GROUP_NAME> ALL --filter-pattern='{ $.level = "error" }' --start='1h'

# Match with wildcards
awslogs get <GROUP_NAME> ALL --filter-pattern='{ $.errorCode = "AccessDenied*" }' --start='1h'

# Match with IS NULL
awslogs get <GROUP_NAME> ALL --filter-pattern='{ $.responseTime IS NULL }' --start='1h'

# Match with NOT EXISTS
awslogs get <GROUP_NAME> ALL --filter-pattern='{ $.errorDetails NOT EXISTS }' --start='1h'
```

### Compound Expressions for JSON Logs

You can create more complex filters using compound expressions:

```bash
# Using AND (&&)
awslogs get <GROUP_NAME> ALL --filter-pattern='{ ($.statusCode = 500) && ($.service = "api") }' --start='1h'

# Using OR (||)
awslogs get <GROUP_NAME> ALL --filter-pattern='{ ($.statusCode = 400) || ($.statusCode = 500) }' --start='1h'

# Using both AND and OR with parentheses
awslogs get <GROUP_NAME> ALL --filter-pattern='{ ($.service = "api") && ($.statusCode = 500 || $.statusCode = 503) }' --start='1h'
```

### Space-Delimited Log Filtering

For space-delimited logs, use bracket notation and field positions:

```bash
# Match logs with specific IP range and status code
awslogs get <GROUP_NAME> ALL --filter-pattern='[ip=%127\.0\.0\.[1-9]%, user, username, timestamp, request, status_code = 404, bytes]' --start='1h'

# Using wildcards for request fields
awslogs get <GROUP_NAME> ALL --filter-pattern='[ip, user, username, timestamp, request =*.html*, status_code, bytes]' --start='1h'

# Using ellipsis (...) for unknown fields
awslogs get <GROUP_NAME> ALL --filter-pattern='[..., request, status_code = 404, bytes]' --start='1h'

# Using OR condition in space-delimited logs
awslogs get <GROUP_NAME> ALL --filter-pattern='[ip, user, username, timestamp, request, status_code = 404 || status_code = 410, bytes]' --start='1h'
```

### Pattern Matching by Word Position

Match terms by position using `w1`, `w2`, etc.:

```bash
# Match logs where first word is ERROR
awslogs get <GROUP_NAME> ALL --filter-pattern='[w1=ERROR, w2]' --start='1h'

# Match logs where first word is ERROR or WARNING
awslogs get <GROUP_NAME> ALL --filter-pattern='[w1=ERROR || w1=WARNING, w2]' --start='1h'

# Exclude terms - first word is NOT ERROR or WARNING
awslogs get <GROUP_NAME> ALL --filter-pattern='[w1!=ERROR && w1!=WARNING, w2]' --start='1h'
```

### Common Log Filtering Examples

```bash
# 1. Search for Log Levels
awslogs get <GROUP_NAME> ALL --filter-pattern='"ERROR" || "WARN" || "INFO"' --start='1h'

# 2. Search for AWS Service Errors
awslogs get <GROUP_NAME> ALL --filter-pattern='"AccessDeniedException" || "ThrottlingException" || "ResourceNotFoundException"' --start='1d'

# 3. Pull Lambda Execution REPORT Messages
awslogs get /aws/lambda/<FUNCTION_NAME> ALL --filter-pattern="[r=REPORT,...]" --start='30m'
```

## 🧹 JSON Field Extraction

If your logs are in JSON format, you can extract specific fields with `--query`:

```bash
# Show only message field
awslogs get <GROUP_NAME> ALL --query=message --start='1h'

# Show only errorCode field
awslogs get <GROUP_NAME> ALL --query=errorCode --start='1h'
```

## ☁️ AWS Authentication Options

You can provide AWS credentials in several ways:

1. Command line parameters:
   ```bash
   awslogs get <GROUP_NAME> ALL --aws-access-key-id XXXX --aws-secret-access-key YYYY
   ```

2. AWS CLI profiles:
   ```bash
   awslogs get <GROUP_NAME> ALL --profile my-profile
   ```

3. Environment variables:
   ```bash
   export AWS_ACCESS_KEY_ID=XXXX
   export AWS_SECRET_ACCESS_KEY=YYYY
   export AWS_REGION=us-east-1
   awslogs get <GROUP_NAME> ALL
   ```

4. Default credentials from AWS configuration

## 🔄 Working with Third-Party Endpoints

For tools like localstack, fakes3, or other services:

```bash
# Using command line parameter
awslogs get <GROUP_NAME> ALL --aws-endpoint-url http://localhost:4566

# Using environment variable
export AWS_ENDPOINT_URL=http://localhost:4566
awslogs get <GROUP_NAME> ALL
```

## 🌟 Coming Soon: --accounts Feature

We are developing a new `--accounts` option to:

* Run searches across multiple accounts automatically
* Handle role assumptions behind the scenes
* Eliminate the need for constant manual profile switching

🚀 Future troubleshooting will be even faster!

## 📢 Key Best Practices

* ✅ Always use a short time range (`--start=30m`, `--start=1h`) during active troubleshooting
* ✅ Use specific filter patterns to reduce data transfer
* ✅ For Lambda functions, use the `ALL` wildcard to capture all streams
* ✅ Refresh your credentials as needed when session tokens expire
* ✅ Use `--query` to extract only the fields you need from JSON logs

## 📚 Additional Resources

For more information about CloudWatch Logs filter patterns:
http://docs.aws.amazon.com/AmazonCloudWatch/latest/DeveloperGuide/FilterAndPatternSyntax.html