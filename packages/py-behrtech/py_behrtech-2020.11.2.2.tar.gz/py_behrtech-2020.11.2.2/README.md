
![publish-pypi](https://github.com/matthewashley1/Fetch_BehrTech/workflows/publish-pypi/badge.svg)

# py_behrtech

A python wrapper for BehrTech's Mythings Central REST API. Currently supporting version 3.0.0

## Status

This package is a work in progress. Currently working to get all API endpoints implemented with checks on each returned status code.

### Endpoints Check List

##### Azure
- [ ] azurefunctionDelete
- [ ] azurefunctionFunctionIDDelete
- [ ] azurefunctionFunctionIDGet
- [ ] azurefunctionGet
- [ ] azurefunctionPost
- [ ] azurefunctionDelete
- [ ] azuremappingGet
- [ ] azuremappingMappingIDDelete
- [ ] azuremappingMappingIDGet
- [ ] azuremappingPost

##### Base Station
- [ ] systemBasestationBsEuiConfigGet
- [ ] systemBasestationBsEuiConfigPost
- [ ] systemBasestationBsEuiDelete
- [ ] systemBasestationBsEuiGet
- [ ] systemBasestationBsEuiPost

##### MQTT
- [ ] brokerBrokerIDDelete
- [ ] brokerBrokerIDGet
- [ ] brokerBrokerIDPost
- [ ] brokerDelete
- [ ] brokerGet
- [ ] brokerPost
- [ ] mqttmappingDelete
- [ ] mqttmappingGet
- [ ] mqttmappingPost
- [ ] mqttmappingMappingIDDelete
- [ ] mqttmappingMappingIDGet

##### Messages
- [ ] messagesDelete
- [x] messagesGet
- [ ] messagesPost

##### Nodes
- [ ] nodesDelete
- [ ] nodesEpEuiDelete
- [ ] nodesEpEuiGet
- [ ] nodesEpEuiTxdataDelete
- [ ] nodesEpEuiTxdataGet
- [ ] nodesEpEuiTxdataPost
- [ ] nodesGet
- [ ] nodesPost

##### Plugin
- [ ] pluginAcceptGet
- [ ] pluginAcceptPost
- [ ] pluginPluginNameArbitraryPathGet
- [ ] pluginPluginNameDelete
- [ ] pluginPluginNameGet
- [ ] pluginPluginNameMappingDelete
- [ ] pluginPluginNameMappingGet
- [ ] pluginPluginNameMappingPost
- [ ] pluginPluginNameMappingEpEuiDelete
- [ ] pluginRegisterGet

##### Sensor Models
- [ ] sensormodelsDelete
- [ ] sensormodelsGet
- [ ] sensormodelsPost
- [ ] sensormodelsSensorTypeDelete
- [ ] sensormodelsSensorTypeGet
- [ ] sensormodelsSensorTypePost

##### System
- [ ] authTicketGet
- [x] loginPost
- [ ] systemDatabasedumpGet
- [ ] systemDatabasedumpIdDelete
- [ ] systemDatabasedumpIdGet
- [ ] systemGet
- [ ] wsGet
 
## License

Fetch_BehrTech is released under the [MIT](https://opensource.org/licenses/MIT) license
