[![NPM version](https://badge.fury.io/js/cdk-gitlab.svg)](https://badge.fury.io/js/cdk-gitlab)
[![PyPI version](https://badge.fury.io/py/cdk-gitlab.svg)](https://badge.fury.io/py/cdk-gitlab)
![Release](https://github.com/pahud/cdk-gitlab/workflows/Release/badge.svg)

# cdk-gitlab

High level CDK construct to provision GitLab integrations with AWS

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
import cdk_gitlab as gl

provider = gl.Provider(stack, "GitlabProvider")

# create Amazon EKS cluster for the GitLab integration
provider.create_eks_cluster(stack, "GitlabEksCluster",
    version=eks.KubernetesVersion.V1_18
)

# TBD - create Amazon EC2 runner for the GitLab
provider.create_ec2_runner(...)

# TBD - create Fargate runner for the GitLab
provider.create_fargate_runner(...)
```
