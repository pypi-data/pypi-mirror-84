# UbiOps Base Connector

This repository contains a template library for implementing connectors in UbiOps. It includes basic functionality such
as mapping data, loading variables and retrying, and provides a structure to implement connectors as UbiOps deployments.

A connector based on this template should import this library and extend the `Connector` class it exposes. For a basic
functional connector only the `insert` method needs to be implemented.


## Implementation structure

A very simple output connector implementation based on this library could look like this:

```
from ubiops_connector import OutputConnector, ConnectorError, RecoverableConnectorError, retry


class Model(OutputConnector):

    @retry(attempts=3)
    def insert(self, data):
        # Your application code to write 'data' to your target data store goes here. In case of errors, you can raise
        # the ConnectorError exception to fail inserting, or raise the RecoverableConnectorError to use the retry
        # functionality.
        pass
```

Connectors will often have a state, such as a database connection that needs to be created once and then re-used between
inserts. In that case, you can create an `__init__` method, setup your connection there and then re-use the created
object in the `insert` method. Do not forget to call the `__init__` method of the base class if you override the
 `__init__`.

The Connectors repository on the UbiOps Github provides several working connectors that can be used as an example.
