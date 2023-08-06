[![NPM version](https://badge.fury.io/js/cdk-gitlab.svg)](https://badge.fury.io/js/cdk-gitlab)
[![PyPI version](https://badge.fury.io/py/cdk-gitlab.svg)](https://badge.fury.io/py/cdk-gitlab)
![Release](https://github.com/pahud/cdk-gitlab/workflows/Release/badge.svg)

# cdk-gitlab

High level CDK construct to provision GitLab integrations with AWS

# Sample

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
from cdk_gitlab import Provider, FargateJobExecutor, FargateRunner, JobExecutorImage

provider = Provider(stack, "GitlabProvider", vpc=vpc)

# create a Amazon EKS cluster
provider.create_eks_cluster(stack, "GitlabEksCluster",
    vpc=vpc,
    version=eks.KubernetesVersion.V1_18
)

# create a default fargate runner with its job executor
provider.create_fargate_runner()

# alternatively, create the runner and the executor indivicually.
# first, create the executor
executor = FargateJobExecutor(stack, "JobExecutor",
    image=JobExecutorImage.DEBIAN
)

# second, create the runner with the task definition of the executor
FargateRunner(stack, "FargateRunner",
    vpc=vpc,
    executor={"task": executor.task_definition_arn}
)

# TBD - create Amazon EC2 runner for the GitLab
provider.create_ec2_runner(...)
```

# Deploy

```sh
cdk deploy -c GITLAB_REGISTRATION_TOKEN=<TOKEN>
```
