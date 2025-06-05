param location string = resourceGroup().location
param backendName string = 'cost-optimizer-api'
param skuName string = 'B1'

resource servicePlan 'Microsoft.Web/serverfarms@2022-03-01' = {
  name: 'cost-optimizer-plan'
  location: location
  sku: {
    name: skuName
    tier: 'Basic'
  }
}

resource webApp 'Microsoft.Web/sites@2022-03-01' = {
  name: backendName
  location: location
  serverFarmId: servicePlan.id
  kind: 'app'
  properties: {
    httpsOnly: true
  }
}
