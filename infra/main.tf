terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = "~> 3.0"
    }
  }
  
  backend "azurerm" {
    resource_group_name  = "rg-ls-lab-azure-cv01" 
    storage_account_name = "saazurecv01"
    container_name       = "tfstate"
    key                  = "cloud-resume.tfstate"
  }
}

provider "azurerm" {
  features {}
}

# Input Variables
variable "resource_group_name" { type = string }
variable "location"            { type = string }
variable "storage_account_name" { type = string }
variable "function_app_name"   { type = string }
variable "cosmos_db_endpoint"  { type = string }
variable "cosmos_db_key"       { type = string }
variable "database_name"       { type = string }
variable "container_name"      { type = string }

# 1. Resource Group
resource "azurerm_resource_group" "rg" {
  name     = var.resource_group_name
  location = var.location
}

# 2. Storage Account (for Static Website)
resource "azurerm_storage_account" "storage" {
  name                     = var.storage_account_name
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"

  static_website {
    index_document     = "index.html"
    error_404_document = "404.html"
  }

  tags = {
    environment = "cloud-resume-challenge"
  }
}

# 3. Storage Account for Function App (Required by Azure Functions)
resource "azurerm_storage_account" "func_storage" {
  name                     = "${var.function_app_name}stor"
  resource_group_name      = azurerm_resource_group.rg.name
  location                 = azurerm_resource_group.rg.location
  account_tier             = "Standard"
  account_replication_type = "LRS"
}

# 4. App Service Plan (Consumption Plan)
resource "azurerm_service_plan" "plan" {
  name                = "${var.function_app_name}-plan"
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  os_type             = "Linux"
  sku_name            = "Y1" # Y1 = Consumption Plan
}

# 5. Function App (Updated for AzureRM v3)
resource "azurerm_linux_function_app" "func" {
  name                = var.function_app_name
  resource_group_name = azurerm_resource_group.rg.name
  location            = azurerm_resource_group.rg.location
  storage_account_name       = azurerm_storage_account.func_storage.name
  storage_account_access_key = azurerm_storage_account.func_storage.primary_access_key
  service_plan_id            = azurerm_service_plan.plan.id

  site_config {
    application_stack {
      python_version = "3.12"
    }
    
    cors {
      allowed_origins = ["*"]
    }
  }

  app_settings = {
    "COSMOS_ENDPOINT"      = var.cosmos_db_endpoint
    "COSMOS_KEY"           = var.cosmos_db_key
    "DATABASE_NAME"        = var.database_name
    "APP_CONTAINER_NAME"   = var.container_name
    "FUNCTIONS_WORKER_RUNTIME" = "python"
    "WEBSITE_CONTENTAZUREFILE" = azurerm_storage_account.func_storage.name
    "WEBSITE_CONTENTSHARE"     = lower(var.function_app_name)
    "WEBSITE_RUN_FROM_PACKAGE"    = "0"
    "SCM_DO_BUILD_DURING_DEPLOYMENT" = "true"
  }

  tags = {
    environment = "cloud-resume-challenge"
  }
}

# Update output to use Storage Endpoint directly
output "cdn_endpoint_url" {
  # Use the static website endpoint of the Storage Account directly
  value = azurerm_storage_account.storage.primary_web_endpoint
  description = "The URL of your live resume site (via Storage Static Website)"
}

output "function_app_url" {
  value = "https://${azurerm_linux_function_app.func.default_hostname}/api/main"
  description = "The URL of your Azure Function"
}