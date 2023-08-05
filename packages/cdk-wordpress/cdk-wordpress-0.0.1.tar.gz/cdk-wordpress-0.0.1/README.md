# cdk-wordpress

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_wordpress import Ecs

wordpress = Ecs(stack, "WordPressEcs")

# Get WordPress endpoint
CfnOutput(stack, "Endpoint", value=wordpress.endpoint)
```

### To deploy

```bash
cdk deploy
```

### To destroy

```bash
cdk destroy
```
