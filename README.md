# Louie - Azure CV
# ☁️ Cloud Resume Challenge - Azure Edition
![Static Badge](https://img.shields.io/badge/Azure-000000?style=flat-square&logo=icloud&logoColor=ffffff&color=2e5ff2)
 ![Static Badge](https://img.shields.io/badge/GitHub-000000?style=flat-square&logo=github&color=2e5ff2) ![Static Badge](https://img.shields.io/badge/Terraform-000000?style=flat-square&logo=terraform&logoColor=ffffff&color=2e5ff2) ![Static Badge](https://img.shields.io/badge/Python-000000?style=flat-square&logo=python&logoColor=ffffff&color=2e5ff2) ![Static Badge](https://img.shields.io/badge/Cloudflare-000000?style=flat-square&logo=cloudflare&logoColor=ffffff&color=2e5ff2)

A serverless, secure, and scalable personal resume website built on **Microsoft Azure**. This project demonstrates end-to-end cloud engineering skills, from Infrastructure as Code (IaC) to CI/CD automation and serverless backend integration.

## 🚀 Live Demo
- **Website:** https://www.louie.geek.nz/
- **Repository:** https://github.com/Louie-IT/azure-resume/

## 🏗️ Architecture Overview
<br/>
<img width="736" height="460" alt="architecture-diagram" src="https://github.com/user-attachments/assets/2aafaf25-2be8-4b7f-b15a-a58dac4fe105" />
<br/>

The solution follows a **Serverless** architecture:
1.  **Frontend:** Static HTML/JS hosted on **Azure Blob Storage**.
2.  **Backend:** **Azure Functions** (Python) handling visitor counting logic.
3.  **Database:** **Azure Cosmos DB** (NoSQL) for persistent storage.
4.  **Security:** **Cloudflare** for DNS, SSL/TLS termination, and DDoS protection.
5.  **Infrastructure:** Provisioned via **Terraform**.
6.  **Automation:** **GitHub Actions** for CI/CD pipelines.

## 🛠️ Tech Stack & Skills Demonstrated

| Category | Technology | Skills Demonstrated |
| :--- | :--- | :--- |
| **Infrastructure** | Terraform, Azure Resource Manager | IaC, Modular Design, State Management, Resource Provisioning |
| **Compute** | Azure Functions (Python) | Serverless Computing, Event-Driven Architecture, Local Build Deployment |
| **Storage** | Azure Blob Storage, Cosmos DB | Static Hosting, NoSQL Data Modeling, CRUD Operations |
| **Networking** | Cloudflare, DNS, CORS | Custom Domain Mapping, SSL/TLS Management, Security Headers |
| **DevOps** | GitHub Actions, YAML | CI/CD Pipelines, Conditional Triggers, Automated Deployment |
| **Security** | Managed Identities, RBAC | Least Privilege Principle, Secure Secrets Management |

## 📂 Project Structure

```text
.
├── .github/
│   └── workflows/
│       └── deploy.yml          # CI/CD Pipeline (Conditional Terraform & App Deploy)
├── infra/                      # Terraform Modules
│   ├── main.tf                 # Resource Definitions
│   ├── variables.tf            # Input Variables
│   └── outputs.tf              # Output Values
├── frontend/                   # Static Site Files
|   ├── css/                   
│   ├── index.html
│   └── main.js                 # Visitor Counter Logic
├── function-app/               # Azure Function Code
│   ├── __init__.py             # API Endpoint Logic
│   ├── requirements.txt        # Python Dependencies
|   ├── test_function.py        # Tests the visitor counter Azure Function logic       
│   └── function.json           # Function Configuration
└── README.md
```

## 🚀 Key Features & Challenges Solved
1. Infrastructure as Code (IaC)

    Provisioned the entire Azure environment (Resource Group, Storage, Function App, Cosmos DB) using Terraform.
    Ensured reproducibility and version control of infrastructure.

2. Intelligent CI/CD Pipeline

    Designed a conditional GitHub Actions workflow:
        Terraform Job: Only runs when infra/ files change or [tf] is in the commit message.
        Deploy Jobs: Run automatically for frontend/function updates.
    Implemented Local Build Strategy (pip install -t .) to overcome Azure Consumption Plan limitations with WEBSITE_RUN_FROM_PACKAGE, ensuring reliable dependency installation.

3. Serverless Backend & Database

    Built a Python Azure Function to handle HTTP requests.
    Integrated with Cosmos DB for atomic read/write operations to track visitor counts.
    Handled CORS configuration to allow secure communication between the static frontend and the API.

4. Cost-Effective Custom Domain & SSL

    Replaced potential costly Azure Front Door service with Cloudflare Free Tier.
    Configured DNS CNAME records and Full SSL mode to serve the site over HTTPS with a custom domain at zero additional cost.

## 🏃 Getting Started
### Prerequisites

    Azure Subscription
    Terraform CLI
    Python 3.9+
    GitHub Account

### Local Development

1. Clone the repo:

        git clone https://github.com/Louie-IT/azure-resume.git
        cd azure-resume

2. Setup Environment:

        cd function-app
        pip install -r requirements.txt

3. Run Locally:

        func start

### Deployment

Push to the main branch to trigger the GitHub Actions pipeline:

    git push origin main

> [!IMPORTANT]
> Add **[tf]** to your commit message if you need to update infrastructure.</br>

## 🔒 Security Best Practices

  * Secrets Management: Sensitive data (Keys, Connection Strings) stored in GitHub Secrets and injected as Environment Variables.
  * Least Privilege: Azure Function uses RBAC to access Cosmos DB and Storage.
  * Secure Transfer: Enforced HTTPS on Azure Storage and Cloudflare.</br>

## 📈 Metrics

  * Uptime: 99.9% (Azure SLA)
  * Latency: < 100ms (Global via Cloudflare Edge)
  * Cost: ~0−5/month (Free tiers utilized); ~$40/year (Domain registration/renewal)</br>

## 🤝 Contributing

This is a learning project. Feel free to fork and explore the codebase.</br>

## 📄 License

Project licensed under the MIT License.
