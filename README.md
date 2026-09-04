# 📊 GitTrack — Student Activity Monitoring System

[![AWS](https://img.shields.io/badge/AWS-Serverless-orange)](https://aws.amazon.com/)
[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/)
[![DynamoDB](https://img.shields.io/badge/Database-DynamoDB-blue)](https://aws.amazon.com/dynamodb/)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

> **A serverless analytics platform for monitoring student coding activity, visualising team contributions, and helping instructors identify potential social loafing in software engineering projects.**

---

## 📖 Table of Contents

* [Project Overview](#-project-overview)
* [The Problem](#-the-problem)
* [The Solution](#-the-solution)
* [Architecture](#-architecture)
* [Tech Stack](#-tech-stack)
* [Features](#-features)
* [Data Flow](#-data-flow)
* [Prerequisites](#-prerequisites)
* [Installation & Setup](#-installation--setup)
* [Usage Guide](#-usage-guide)
* [API Documentation](#-api-documentation)
* [Dashboard](#-dashboard)
* [Project Structure](#-project-structure)
* [Testing](#-testing)
* [Deployment](#-deployment)
* [Security](#-security)
* [Cost Analysis](#-cost-analysis)
* [Development Process](#-development-process)
* [Challenges & Solutions](#-challenges--solutions)
* [Future Enhancements](#-future-enhancements)
* [Lessons Learned](#-lessons-learned)
* [Contributing](#-contributing)
* [License](#-license)
* [Contact](#-contact)
* [Acknowledgements](#-acknowledgements)

---

# 🎯 Project Overview

**GitTrack** is a serverless student activity monitoring system designed for team-based software engineering projects.

The system collects coding activity data, stores it in Amazon DynamoDB, exposes it through a REST API, and presents the information through an interactive web dashboard.

The goal is to give instructors a clearer, data-driven view of student participation in group projects.

### Key Objectives

* Monitor student coding activity.
* Track commits and merge requests.
* Store activity securely in a scalable database.
* Provide instructors with visual analytics.
* Reduce the amount of manual activity tracking.
* Help identify significant differences in team participation.
* Provide a foundation for future GitLab webhook integration.

---

# ⚠️ The Problem

Team-based software engineering projects can create challenges when contributions are unevenly distributed.

A common situation is that one or two students complete a large portion of the work while other team members contribute significantly less.

This can result in:

* Uneven workloads.
* Frustrated team members.
* Difficulty assessing individual contributions.
* Delayed intervention from instructors.
* Inequitable assessment.
* Time-consuming manual monitoring.

### Current Pain Points

| Problem                | Impact                                                               |
| ---------------------- | -------------------------------------------------------------------- |
| Manual data collection | Instructors spend time checking GitLab activity                      |
| Delayed detection      | Contribution problems may only become visible near project deadlines |
| Uneven contribution    | Some students carry a disproportionate amount of the workload        |
| Difficult assessment   | Individual contributions can be difficult to evaluate objectively    |
| Lack of visibility     | Instructors may not have a centralised view of team activity         |

---

# 💡 The Solution

GitTrack provides a centralised activity monitoring platform.

The application follows a serverless architecture:

```text
GitLab / Activity Source
        │
        ▼
   API Gateway
        │
        ▼
   AWS Lambda
        │
        ▼
   DynamoDB
        │
        ▼
   REST API
        │
        ▼
 S3 Dashboard
        │
        ▼
   Instructor
```

The system separates data ingestion, processing, storage, and presentation into independent components.

This makes the application easier to maintain and allows individual components to scale independently.

---

# 🏗️ Architecture

## High-Level Architecture

```text
┌─────────────────────────────────────────────────────────────┐
│                    GitLab Repository                        │
│                 Student Code & Activity                     │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     API Gateway                             │
│                                                             │
│              POST /activity                                 │
│              GET  /activity                                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────┐
│                     AWS Lambda                              │
│                                                             │
│   ┌─────────────────────┐   ┌──────────────────────────┐   │
│   │   save-activity     │   │      get-activity        │   │
│   │    POST Handler     │   │       GET Handler        │   │
│   └──────────┬──────────┘   └────────────┬─────────────┘   │
└──────────────┼───────────────────────────┼─────────────────┘
               │                           │
               └─────────────┬─────────────┘
                             │
                             ▼
                 ┌─────────────────────┐
                 │      DynamoDB       │
                 │                     │
                 │   StudentActivity   │
                 │                     │
                 │   student_id (PK)   │
                 │   timestamp (SK)    │
                 │   commits           │
                 │   merge_requests    │
                 │   project_id        │
                 └──────────┬──────────┘
                            │
                            ▼
                 ┌─────────────────────┐
                 │      S3 Bucket      │
                 │   Static Website    │
                 │                     │
                 │    index.html       │
                 │    style.css        │
                 │    app.js           │
                 └──────────┬──────────┘
                            │
                            ▼
                    ┌──────────────┐
                    │ User Browser  │
                    │  Dashboard    │
                    └──────────────┘
```

---

# 🛠️ Tech Stack

| Layer                     | Technology            | Purpose                      |
| ------------------------- | --------------------- | ---------------------------- |
| Programming Language      | Python 3.12           | Backend and utility scripts  |
| Compute                   | AWS Lambda            | Serverless application logic |
| API                       | Amazon API Gateway    | REST API endpoints           |
| Database                  | Amazon DynamoDB       | Student activity storage     |
| Frontend                  | HTML, CSS, JavaScript | Dashboard interface          |
| Visualisation             | Chart.js              | Activity charts              |
| Hosting                   | Amazon S3             | Static website hosting       |
| Monitoring                | AWS CloudWatch        | Logs and monitoring          |
| Cloud SDK                 | Boto3                 | Python integration with AWS  |
| Version Control           | Git / GitHub          | Source code management       |
| Activity Source           | GitLab                | Student repository activity  |
| Infrastructure Management | AWS CLI               | AWS resource management      |

---

# ✨ Features

## ✅ Implemented

| Feature               | Description                              | Status     |
| --------------------- | ---------------------------------------- | ---------- |
| Data ingestion        | Receive student activity through the API | ✅ Complete |
| DynamoDB storage      | Store activity records                   | ✅ Complete |
| Data retrieval        | Retrieve activity by student ID          | ✅ Complete |
| REST API              | POST and GET activity endpoints          | ✅ Complete |
| Dashboard             | Interactive activity dashboard           | ✅ Complete |
| Commit visualisation  | Bar chart showing commits                | ✅ Complete |
| Activity distribution | Doughnut chart                           | ✅ Complete |
| Student summary       | View total students and activity         | ✅ Complete |
| Student table         | View individual activity                 | ✅ Complete |
| Auto-refresh          | Dashboard refreshes periodically         | ✅ Complete |
| Mock data             | Generate test activity data              | ✅ Complete |
| AWS deployment        | Serverless infrastructure deployed       | ✅ Complete |

---

# 🔄 Data Flow

The application follows this sequence:

1. A user or activity source sends a `POST` request to API Gateway.
2. API Gateway triggers the `save-activity` Lambda function.
3. Lambda validates the request.
4. The activity record is saved to DynamoDB.
5. The dashboard sends a `GET` request to API Gateway.
6. API Gateway triggers the `get-activity` Lambda function.
7. Lambda queries DynamoDB.
8. The API returns the activity data.
9. The dashboard processes the response.
10. Chart.js visualises the activity for the instructor.

This flow separates data collection, processing, storage, and presentation.

---

# 📋 Prerequisites

## Required

Before running GitTrack, make sure you have:

* Python 3.12+
* Git
* AWS CLI v2
* An AWS account
* A GitHub account
* A GitLab account if using real GitLab data

## Recommended Tools

* VS Code
* Postman
* AWS Console
* GitLab

---

# 🚀 Installation & Setup

## 1. Clone the Repository

```bash
git clone https://github.com/precise18/GitTrack.git
cd GitTrack
```

---

## 2. Create a Python Virtual Environment

### Linux / macOS

```bash
python3 -m venv venv
source venv/bin/activate
```

### Windows

```bash
python -m venv venv
venv\Scripts\activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Configure Environment Variables

Create a `.env` file in the root directory:

```env
# GitLab Configuration
GITLAB_TOKEN=your_gitlab_token
GITLAB_PROJECT_ID=your_project_id
GITLAB_URL=https://gitlab.com
USE_MOCK_DATA=True

# AWS Configuration
AWS_DEFAULT_REGION=us-east-1

# API Configuration
API_URL=https://7ejkhfnocl.execute-api.us-east-1.amazonaws.com/prod

# Application Configuration
LOG_LEVEL=INFO
```

> ⚠️ **Security:** Never commit `.env` files, AWS credentials, or GitLab personal access tokens to GitHub.

---

# 🧪 Generate Mock Data

GitTrack includes mock data for development and testing.

Run:

```bash
python scripts/generate_mock_data.py
```

This generates sample student activity data that can be used without connecting to a live GitLab project.

---

# ▶️ Usage Guide

## Run Environment Tests

```bash
python scripts/test_setup.py
```

## Fetch Commits

```bash
python scripts/fetch_commits.py
```

## Test DynamoDB

```bash
PYTHONPATH="${PWD}:${PWD}/src" python scripts/test_dynamodb.py
```

---

# 📡 API Documentation

## Base URL

```text
https://7ejkhfnocl.execute-api.us-east-1.amazonaws.com/prod
```

---

## POST `/activity`

Stores student activity in DynamoDB.

### Request

```json
{
  "student_id": "Alice",
  "commits": 150,
  "merge_requests": 40,
  "project_id": "test123",
  "timestamp": "2026-09-04T12:14:00.769239Z"
}
```

### Request Fields

| Field            | Type    | Required | Description              |
| ---------------- | ------- | -------- | ------------------------ |
| `student_id`     | String  | Yes      | Student identifier       |
| `commits`        | Integer | No       | Number of commits        |
| `merge_requests` | Integer | No       | Number of merge requests |
| `project_id`     | String  | No       | Project identifier       |
| `timestamp`      | ISO8601 | No       | Activity timestamp       |

### Successful Response

```json
{
  "message": "Activity saved for Alice",
  "item": {
    "student_id": "Alice",
    "timestamp": "2026-09-04T12:14:00.769239Z",
    "commits": 150,
    "merge_requests": 40,
    "project_id": "test123"
  }
}
```

### Error Response

```json
{
  "error": "student_id is required"
}
```

---

# GET `/activity`

Retrieves student activity.

### Query Parameters

| Parameter    | Required | Default      | Description                |
| ------------ | -------- | ------------ | -------------------------- |
| `student_id` | No       | All students | Filter activity by student |
| `days`       | No       | 7            | Number of days to retrieve |

### Example

```bash
curl "https://7ejkhfnocl.execute-api.us-east-1.amazonaws.com/prod/activity?student_id=Alice"
```

### Example Response

```json
{
  "students": [
    {
      "student_id": "Alice",
      "timestamp": "2026-09-04T12:14:00.769239Z",
      "commits": 150,
      "merge_requests": 40,
      "project_id": "test123"
    }
  ],
  "count": 1,
  "query": {
    "student_id": "Alice",
    "days": 7
  }
}
```

---

# 📊 Dashboard

The GitTrack dashboard provides instructors with a visual overview of student activity.

### Dashboard URL

```text
http://gittrack-dashboard-1788526221.s3-website-us-east-1.amazonaws.com
```

## Dashboard Components

### Summary Cards

Displays:

* Total students
* Total commits
* Total merge requests
* Most active student

### Commits Chart

A bar chart showing the number of commits made by each student.

### Activity Distribution

A doughnut chart representing activity distribution across students.

### Student Activity Table

Displays:

| Student | Commits | Merge Requests | Total Activity |
| ------- | ------: | -------------: | -------------: |
| Alice   |     150 |             40 |            190 |
| Bob     |     100 |             25 |            125 |

### Auto Refresh

The dashboard automatically refreshes its data every 30 seconds.

---

# 📁 Project Structure

```text
GitTrack/
│
├── dashboard/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── src/
│   ├── __init__.py
│   ├── config.py
│   └── db.py
│
├── scripts/
│   ├── test_setup.py
│   ├── generate_mock_data.py
│   ├── fetch_commits.py
│   └── test_dynamodb.py
│
├── lambda/
│   ├── save_activity.py
│   └── get_activity.py
│
├── data/
│   └── mock_commits.json
│
├── docs/
│   ├── PROJECT_REPORT.md
│   └── GITLAB_SETUP.md
│
├── tests/
│
├── .env
├── .gitignore
├── requirements.txt
└── README.md
```

---

# 🧪 Testing

GitTrack was tested at multiple levels.

## Testing Strategy

| Test Type              | Tool              | Coverage                      |
| ---------------------- | ----------------- | ----------------------------- |
| Unit Testing           | Python `unittest` | Lambda functions              |
| Integration Testing    | AWS CLI           | API Gateway, Lambda, DynamoDB |
| End-to-End Testing     | cURL + Browser    | Complete application flow     |
| Performance Monitoring | CloudWatch        | Response times                |

## Test Results

| Component            | Pass Rate | Approx. Response Time |
| -------------------- | --------: | --------------------: |
| Save Activity Lambda |      100% |               ~250 ms |
| Get Activity Lambda  |      100% |               ~285 ms |
| API Gateway POST     |      100% |               ~300 ms |
| API Gateway GET      |      100% |               ~300 ms |
| Dashboard            |      100% |          ~500 ms load |

The documented testing process covers individual Lambda functions, AWS integration, the complete API-to-dashboard flow, and performance monitoring.

---

# 🔍 Sample Test Data

Example activity data used during testing:

| Student              | Commits | Merge Requests | Total |
| -------------------- | ------: | -------------: | ----: |
| StageUpdateTest      |     150 |             40 |   190 |
| APIGatewayFormatTest |     100 |             25 |   125 |
| APIGatewayTest       |      60 |             15 |    75 |
| DirectTest           |      50 |             10 |    60 |
| Alice Chen           |      16 |              6 |    22 |

---

# ☁️ AWS Deployment

GitTrack uses the following AWS services:

| Service     | Purpose                |
| ----------- | ---------------------- |
| AWS Lambda  | Serverless backend     |
| API Gateway | REST API               |
| DynamoDB    | Database               |
| S3          | Dashboard hosting      |
| CloudWatch  | Logging and monitoring |

---

## Create DynamoDB Table

```bash
aws dynamodb create-table \
    --table-name StudentActivity \
    --attribute-definitions \
        AttributeName=student_id,AttributeType=S \
        AttributeName=timestamp,AttributeType=S \
    --key-schema \
        AttributeName=student_id,KeyType=HASH \
        AttributeName=timestamp,KeyType=RANGE \
    --billing-mode PAY_PER_REQUEST \
    --region us-east-1
```

---

## Lambda Configuration

Create two Lambda functions:

```text
save-activity
get-activity
```

### Runtime

```text
Python 3.12
```

### Environment Variable

```text
TABLE_NAME=StudentActivity
```

---

## API Gateway

Configure the following routes:

| Method | Route       | Lambda          |
| ------ | ----------- | --------------- |
| POST   | `/activity` | `save-activity` |
| GET    | `/activity` | `get-activity`  |

CORS should be enabled for the dashboard.

---

# 🌐 Deploy Dashboard to S3

Create an S3 bucket:

```bash
aws s3api create-bucket \
    --bucket gittrack-dashboard-YOUR_ID \
    --region us-east-1
```

Enable static website hosting:

```bash
aws s3api put-bucket-website \
    --bucket gittrack-dashboard-YOUR_ID \
    --website-configuration '{
        "IndexDocument": {
            "Suffix": "index.html"
        },
        "ErrorDocument": {
            "Key": "index.html"
        }
    }'
```

Upload the dashboard:

```bash
aws s3 sync dashboard/ s3://gittrack-dashboard-YOUR_ID/
```

---

# 🔗 GitLab Integration

GitTrack is designed to integrate with GitLab activity.

## Personal Access Token

Create a GitLab Personal Access Token with the required read permissions.

Configure:

```env
GITLAB_TOKEN=your_personal_access_token
GITLAB_PROJECT_ID=your_project_id
GITLAB_URL=https://gitlab.com
```

Then run:

```bash
python scripts/fetch_commits.py
```

---

## GitLab Webhook

The planned webhook endpoint is:

```text
https://7ejkhfnocl.execute-api.us-east-1.amazonaws.com/prod/activity
```

Configure the GitLab webhook for:

```text
Trigger: Push Events
Content Type: application/json
```

The documented development process includes configuring API Gateway, CORS, the production stage, and testing the end-to-end flow.

---

# 🔐 Security

Security was considered throughout the project.

## IAM

The project uses separate roles for different responsibilities:

| Role                 | Purpose                   |
| -------------------- | ------------------------- |
| `GitTrack-Admin`     | Infrastructure management |
| `save-activity-role` | Activity data writing     |
| `get-activity-role`  | Activity data reading     |

## Security Practices

* MFA enabled.
* Root account not used for daily tasks.
* Environment variables used for configuration.
* `.env` excluded from version control.
* DynamoDB encryption at rest.
* CORS configured for the API.
* IAM permissions configured for AWS resources.
* Secrets are not stored directly in source code.

> **Production recommendation:** AWS IAM policies should be refined to follow strict least-privilege access rather than granting broad permissions such as `AmazonDynamoDBFullAccess`.

The project documentation records MFA, environment-variable usage, exclusion of `.env`, encryption at rest, and IAM practices as security measures.

---

# 💰 Cost Analysis

GitTrack was designed to operate using AWS Free Tier resources.

| Service     |   Documented Limit | Project Usage |
| ----------- | -----------------: | ------------: |
| Lambda      | 1,000,000 requests |         < 100 |
| DynamoDB    |      25 GB storage |        < 1 MB |
| API Gateway |    1,000,000 calls |         < 100 |
| S3          |       5 GB storage |        < 1 MB |
| CloudWatch  |          5 GB logs |        < 1 MB |

### Estimated Monthly Cost

```text
$0.00
```

The project also includes a zero-spend budget configuration and email notifications for cost monitoring.

> ⚠️ AWS Free Tier limits and pricing can change. Always verify current AWS pricing before deploying a production workload.

---

# 🛠️ Development Process

The project was developed incrementally.

## Phase 1 — Local Development & GitLab Setup

* Created Python virtual environment.
* Configured GitLab API integration.
* Generated mock data.
* Implemented commit fetching.

## Phase 2 — Serverless Backend

* Created DynamoDB table.
* Developed Lambda functions.
* Configured API Gateway.
* Implemented error handling.

## Phase 3 — API Integration

* Connected API Gateway to Lambda.
* Configured CORS.
* Deployed to the production stage.
* Tested the complete data flow.

## Phase 4 — Dashboard

* Built HTML/CSS/JavaScript interface.
* Integrated Chart.js.
* Connected dashboard to the API.
* Deployed dashboard to S3.
* Implemented automatic refresh.

---

# 🐛 Challenges & Solutions

| Challenge               | Solution                                   |
| ----------------------- | ------------------------------------------ |
| Python module imports   | Configured `sys.path` correctly            |
| DynamoDB permissions    | Configured appropriate IAM permissions     |
| API Gateway 500 errors  | Updated the deployment/stage configuration |
| DynamoDB Decimal values | Implemented a `DecimalEncoder` for JSON    |
| S3 website access       | Configured appropriate S3 access policies  |

These challenges and their documented solutions formed part of the project's development and troubleshooting process.

---

# 🚀 Future Enhancements

The current system provides a working foundation, with several improvements planned.

## High Priority

* [ ] Real-time GitLab webhook integration.
* [ ] Student authentication.
* [ ] Instructor authentication.
* [ ] Improved IAM least-privilege policies.

## Medium Priority

* [ ] Date-range filtering.
* [ ] Email notifications for unusually low activity.
* [ ] Improved analytics.
* [ ] Team-level comparisons.

## Low Priority

* [ ] CSV export.
* [ ] Advanced reporting.
* [ ] Historical activity trends.

## Architecture Improvements

* [ ] Implement Global Secondary Indexes (GSI).
* [ ] Add Amazon CloudFront.
* [ ] Implement caching.
* [ ] Add AWS Step Functions for workflows.
* [ ] Explore additional event-driven integrations.

The documented roadmap includes webhook integration, date filtering, email notifications, authentication, CSV export, GSIs, CloudFront, caching, and Step Functions.

---

# 📚 Lessons Learned

## Technical Lessons

### 1. AWS Lambda

Understanding Lambda event structures is essential when building serverless APIs.

### 2. API Gateway

API deployments and stages need to be managed carefully to ensure changes are available to clients.

### 3. DynamoDB

DynamoDB values may require special handling when serialising data to JSON.

### 4. Amazon S3

Static website hosting requires correct bucket configuration and access policies.

### 5. Python Project Structure

Correct module paths are important when executing Python scripts from different directories.

---

## Project Management Lessons

1. **Start small** — Build one component at a time.
2. **Test frequently** — Validate each component before integration.
3. **Use version control** — Commit changes regularly.
4. **Document as you go** — Documentation is easier when created alongside development.
5. **Monitor cloud costs** — Check AWS usage regularly.

The project's report identifies incremental development, frequent version-control commits, documentation, component-level testing, and cost awareness as key project-management lessons.

---

# 🎯 Project Outcomes

GitTrack successfully demonstrates a serverless architecture consisting of:

```text
API Gateway
     ↓
AWS Lambda
     ↓
DynamoDB
     ↓
REST API
     ↓
S3 Dashboard
```

### Achievements

* ✅ Functional serverless backend.
* ✅ Working POST endpoint.
* ✅ Working GET endpoint.
* ✅ DynamoDB data storage.
* ✅ Interactive dashboard.
* ✅ Chart-based visualisations.
* ✅ Automated dashboard refresh.
* ✅ Mock data generation.
* ✅ AWS deployment.
* ✅ Testing across multiple components.
* ✅ Cost monitoring.
* ✅ Comprehensive documentation.

---

# 🌍 Project Impact

### For Instructors

GitTrack can reduce the amount of time spent manually checking student activity and provide a centralised view of contribution data.

### For Students

The system can support greater transparency around team contributions and provide evidence that can inform discussions about workload distribution.

### For Institutions

The serverless architecture provides a lightweight foundation that can scale as the number of users and projects increases.

### Important Note

GitTrack should be used as a **supporting analytics tool**, not as the sole mechanism for determining a student's performance or contribution.

Commit counts alone do not capture the full value of software engineering work. Code reviews, design, debugging, documentation, testing, collaboration, and other contributions should also be considered.

---

# 🤝 Contributing

GitTrack is currently a personal learning and portfolio project, but feedback and suggestions are welcome.

### 1. Fork the Repository

```bash
git clone https://github.com/precise18/GitTrack.git
```

### 2. Create a Feature Branch

```bash
git checkout -b feature/AmazingFeature
```

### 3. Commit Your Changes

```bash
git add .
git commit -m "Add AmazingFeature"
```

### 4. Push Your Branch

```bash
git push origin feature/AmazingFeature
```

### 5. Open a Pull Request

Explain what you changed and why.

---

# 📄 License

This project is licensed under the **MIT License**.

See the [`LICENSE`](LICENSE) file for details.

---

# 📞 Contact

**Author:** Precise18

**GitHub:** [@precise18](https://github.com/precise18)

**Repository:**
https://github.com/precise18/GitTrack

**Live Dashboard:**
http://gittrack-dashboard-1788526221.s3-website-us-east-1.amazonaws.com

**API Base URL:**
https://7ejkhfnocl.execute-api.us-east-1.amazonaws.com/prod

---

# 🙏 Acknowledgements

Special thanks to the technologies and resources that made this project possible:

* [Amazon Web Services](https://aws.amazon.com/) — Cloud infrastructure.
* [AWS Lambda](https://aws.amazon.com/lambda/) — Serverless compute.
* [Amazon DynamoDB](https://aws.amazon.com/dynamodb/) — Database.
* [Amazon API Gateway](https://aws.amazon.com/api-gateway/) — API management.
* [Amazon S3](https://aws.amazon.com/s3/) — Static website hosting.
* [Chart.js](https://www.chartjs.org/) — Data visualisation.
* [GitLab](https://gitlab.com/) — Source repository and activity data.
* [Boto3](https://boto3.amazonaws.com/) — AWS SDK for Python.

---

# 📚 Additional Resources

* [AWS Lambda Documentation](https://docs.aws.amazon.com/lambda/)
* [Amazon API Gateway Documentation](https://docs.aws.amazon.com/apigateway/)
* [Amazon DynamoDB Documentation](https://docs.aws.amazon.com/dynamodb/)
* [AWS CLI Documentation](https://docs.aws.amazon.com/cli/)
* [GitLab API Documentation](https://docs.gitlab.com/ee/api/)
* [Chart.js Documentation](https://www.chartjs.org/docs/)
* [Boto3 Documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/index.html)

---

# 🎓 About the Project

**GitTrack** was developed as a technology learning and portfolio project during the **Horizon Academy of Technology bootcamp**.

The project demonstrates practical experience with:

* Python development
* REST API design
* Serverless architecture
* AWS Lambda
* Amazon DynamoDB
* API Gateway
* Amazon S3
* Cloud computing
* Git/GitHub
* GitLab APIs
* Data visualisation
* Testing and debugging
* Technical documentation

---

## 📊 GitTrack

> **"Tracking student contributions, one commit at a time."**

Built with ❤️ using Python and AWS.
