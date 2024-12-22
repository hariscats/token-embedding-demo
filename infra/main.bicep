@description('Location to deploy the resources.')
param location string = resourceGroup().location

@description('Name of the App Service plan.')
param appServicePlanName string = 'llmDemoAppServicePlan'

@description('Name of the Web App.')
param webAppName string = 'llmDemoWebApp'

@description('App Service Plan SKU Tier (Free, Basic, Standard, etc.)')
@allowed([
  'FREE'
  'BASIC'
  'STANDARD'
])
param skuTier string = 'BASIC'

@description('App Service Plan SKU name: F1 (Free), B1/B2/B3 (Basic), S1/S2/S3 (Standard).')
param skuName string = 'B1'

resource appServicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: appServicePlanName
  location: location
  sku: {
    name: skuName
    tier: skuTier
  }
}

resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: webAppName
  location: location
  kind: 'app,linux'
  properties: {
    serverFarmId: appServicePlan.id
    siteConfig: {
      linuxFxVersion: 'PYTHON|3.9'
    }
    reserved: true  // This enables Linux hosting
  }
}
