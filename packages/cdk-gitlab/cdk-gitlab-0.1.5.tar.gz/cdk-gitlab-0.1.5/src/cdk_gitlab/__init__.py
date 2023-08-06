"""
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

# create the fargate runner
provider.create_fargate_runner()

# TBD - create Amazon EC2 runner for the GitLab
provider.create_ec2_runner(...)
```

# Deploy

```sh
cdk deploy -c GITLAB_REGISTRATION_TOKEN=<TOKEN>
```
"""
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.aws_ec2
import aws_cdk.aws_eks
import aws_cdk.aws_iam
import aws_cdk.aws_kms
import aws_cdk.aws_lambda
import aws_cdk.core


class Provider(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-gitlab.Provider",
):
    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
    ) -> None:
        """
        :param scope: -
        :param id: -
        :param vpc: 
        """
        props = ProviderProps(vpc=vpc)

        jsii.create(Provider, self, [scope, id, props])

    @jsii.member(jsii_name="createEksCluster")
    def create_eks_cluster(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        default_capacity: typing.Optional[jsii.Number] = None,
        default_capacity_instance: typing.Optional[aws_cdk.aws_ec2.InstanceType] = None,
        default_capacity_type: typing.Optional[aws_cdk.aws_eks.DefaultCapacityType] = None,
        kubectl_enabled: typing.Optional[builtins.bool] = None,
        secrets_encryption_key: typing.Optional[aws_cdk.aws_kms.IKey] = None,
        core_dns_compute_type: typing.Optional[aws_cdk.aws_eks.CoreDnsComputeType] = None,
        endpoint_access: typing.Optional[aws_cdk.aws_eks.EndpointAccess] = None,
        kubectl_environment: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        kubectl_layer: typing.Optional[aws_cdk.aws_lambda.ILayerVersion] = None,
        masters_role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        output_masters_role_arn: typing.Optional[builtins.bool] = None,
        version: aws_cdk.aws_eks.KubernetesVersion,
        cluster_name: typing.Optional[builtins.str] = None,
        output_cluster_name: typing.Optional[builtins.bool] = None,
        output_config_command: typing.Optional[builtins.bool] = None,
        role: typing.Optional[aws_cdk.aws_iam.IRole] = None,
        security_group: typing.Optional[aws_cdk.aws_ec2.ISecurityGroup] = None,
        vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None,
        vpc_subnets: typing.Optional[typing.List[aws_cdk.aws_ec2.SubnetSelection]] = None,
    ) -> aws_cdk.aws_eks.Cluster:
        """
        :param scope: -
        :param id: -
        :param default_capacity: (experimental) Number of instances to allocate as an initial capacity for this cluster. Instance type can be configured through ``defaultCapacityInstanceType``, which defaults to ``m5.large``. Use ``cluster.addAutoScalingGroupCapacity`` to add additional customized capacity. Set this to ``0`` is you wish to avoid the initial capacity allocation. Default: 2
        :param default_capacity_instance: (experimental) The instance type to use for the default capacity. This will only be taken into account if ``defaultCapacity`` is > 0. Default: m5.large
        :param default_capacity_type: (experimental) The default capacity type for the cluster. Default: NODEGROUP
        :param kubectl_enabled: (deprecated) NOT SUPPORTED: We no longer allow disabling kubectl-support. Setting this option to ``false`` will throw an error. To temporary allow you to retain existing clusters created with ``kubectlEnabled: false``, you can use ``eks.LegacyCluster`` class, which is a drop-in replacement for ``eks.Cluster`` with ``kubectlEnabled: false``. Bear in mind that this is a temporary workaround. We have plans to remove ``eks.LegacyCluster``. If you have a use case for using ``eks.LegacyCluster``, please add a comment here https://github.com/aws/aws-cdk/issues/9332 and let us know so we can make sure to continue to support your use case with ``eks.Cluster``. This issue also includes additional context into why this class is being removed. Default: true
        :param secrets_encryption_key: (experimental) KMS secret for envelope encryption for Kubernetes secrets. Default: - By default, Kubernetes stores all secret object data within etcd and all etcd volumes used by Amazon EKS are encrypted at the disk-level using AWS-Managed encryption keys.
        :param core_dns_compute_type: (experimental) Controls the "eks.amazonaws.com/compute-type" annotation in the CoreDNS configuration on your cluster to determine which compute type to use for CoreDNS. Default: CoreDnsComputeType.EC2 (for ``FargateCluster`` the default is FARGATE)
        :param endpoint_access: (experimental) Configure access to the Kubernetes API server endpoint.. Default: EndpointAccess.PUBLIC_AND_PRIVATE
        :param kubectl_environment: (experimental) Environment variables for the kubectl execution. Only relevant for kubectl enabled clusters. Default: - No environment variables.
        :param kubectl_layer: (experimental) An AWS Lambda Layer which includes ``kubectl``, Helm and the AWS CLI. By default, the provider will use the layer included in the "aws-lambda-layer-kubectl" SAR application which is available in all commercial regions. To deploy the layer locally, visit https://github.com/aws-samples/aws-lambda-layer-kubectl/blob/master/cdk/README.md for instructions on how to prepare the .zip file and then define it in your app as follows:: const layer = new lambda.LayerVersion(this, 'kubectl-layer', { code: lambda.Code.fromAsset(`${__dirname}/layer.zip`)), compatibleRuntimes: [lambda.Runtime.PROVIDED] }) Default: - the layer provided by the ``aws-lambda-layer-kubectl`` SAR app.
        :param masters_role: (experimental) An IAM role that will be added to the ``system:masters`` Kubernetes RBAC group. Default: - a role that assumable by anyone with permissions in the same account will automatically be defined
        :param output_masters_role_arn: (experimental) Determines whether a CloudFormation output with the ARN of the "masters" IAM role will be synthesized (if ``mastersRole`` is specified). Default: false
        :param version: (experimental) The Kubernetes version to run in the cluster.
        :param cluster_name: (experimental) Name for the cluster. Default: - Automatically generated name
        :param output_cluster_name: (experimental) Determines whether a CloudFormation output with the name of the cluster will be synthesized. Default: false
        :param output_config_command: (experimental) Determines whether a CloudFormation output with the ``aws eks update-kubeconfig`` command will be synthesized. This command will include the cluster name and, if applicable, the ARN of the masters IAM role. Default: true
        :param role: (experimental) Role that provides permissions for the Kubernetes control plane to make calls to AWS API operations on your behalf. Default: - A role is automatically created for you
        :param security_group: (experimental) Security Group to use for Control Plane ENIs. Default: - A security group is automatically created
        :param vpc: (experimental) The VPC in which to create the Cluster. Default: - a VPC with default configuration will be created and can be accessed through ``cluster.vpc``.
        :param vpc_subnets: (experimental) Where to place EKS Control Plane ENIs. If you want to create public load balancers, this must include public subnets. For example, to only select private subnets, supply the following:: vpcSubnets: [ { subnetType: ec2.SubnetType.Private } ] Default: - All public and private subnets
        """
        props = aws_cdk.aws_eks.ClusterProps(
            default_capacity=default_capacity,
            default_capacity_instance=default_capacity_instance,
            default_capacity_type=default_capacity_type,
            kubectl_enabled=kubectl_enabled,
            secrets_encryption_key=secrets_encryption_key,
            core_dns_compute_type=core_dns_compute_type,
            endpoint_access=endpoint_access,
            kubectl_environment=kubectl_environment,
            kubectl_layer=kubectl_layer,
            masters_role=masters_role,
            output_masters_role_arn=output_masters_role_arn,
            version=version,
            cluster_name=cluster_name,
            output_cluster_name=output_cluster_name,
            output_config_command=output_config_command,
            role=role,
            security_group=security_group,
            vpc=vpc,
            vpc_subnets=vpc_subnets,
        )

        return jsii.invoke(self, "createEksCluster", [scope, id, props])

    @jsii.member(jsii_name="createEksServiceRole")
    def create_eks_service_role(self) -> aws_cdk.aws_iam.Role:
        return jsii.invoke(self, "createEksServiceRole", [])

    @jsii.member(jsii_name="createFargateRunner")
    def create_fargate_runner(self) -> None:
        return jsii.invoke(self, "createFargateRunner", [])

    @jsii.member(jsii_name="createGitlabManagedEksRole")
    def create_gitlab_managed_eks_role(
        self,
        *,
        account_id: builtins.str,
        external_id: builtins.str,
    ) -> None:
        """
        :param account_id: 
        :param external_id: 
        """
        props = RoleProps(account_id=account_id, external_id=external_id)

        return jsii.invoke(self, "createGitlabManagedEksRole", [props])

    @jsii.member(jsii_name="createSecurityGroup")
    def create_security_group(self) -> aws_cdk.aws_ec2.SecurityGroup:
        return jsii.invoke(self, "createSecurityGroup", [])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="vpc")
    def vpc(self) -> aws_cdk.aws_ec2.IVpc:
        return jsii.get(self, "vpc")

    @builtins.property # type: ignore
    @jsii.member(jsii_name="gitlabEksRole")
    def gitlab_eks_role(self) -> typing.Optional[aws_cdk.aws_iam.IRole]:
        return jsii.get(self, "gitlabEksRole")

    @gitlab_eks_role.setter # type: ignore
    def gitlab_eks_role(self, value: typing.Optional[aws_cdk.aws_iam.IRole]) -> None:
        jsii.set(self, "gitlabEksRole", value)


@jsii.data_type(
    jsii_type="cdk-gitlab.ProviderProps",
    jsii_struct_bases=[],
    name_mapping={"vpc": "vpc"},
)
class ProviderProps:
    def __init__(self, *, vpc: typing.Optional[aws_cdk.aws_ec2.IVpc] = None) -> None:
        """
        :param vpc: 
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if vpc is not None:
            self._values["vpc"] = vpc

    @builtins.property
    def vpc(self) -> typing.Optional[aws_cdk.aws_ec2.IVpc]:
        result = self._values.get("vpc")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-gitlab.RoleProps",
    jsii_struct_bases=[],
    name_mapping={"account_id": "accountId", "external_id": "externalId"},
)
class RoleProps:
    def __init__(self, *, account_id: builtins.str, external_id: builtins.str) -> None:
        """
        :param account_id: 
        :param external_id: 
        """
        self._values: typing.Dict[str, typing.Any] = {
            "account_id": account_id,
            "external_id": external_id,
        }

    @builtins.property
    def account_id(self) -> builtins.str:
        result = self._values.get("account_id")
        assert result is not None, "Required property 'account_id' is missing"
        return result

    @builtins.property
    def external_id(self) -> builtins.str:
        result = self._values.get("external_id")
        assert result is not None, "Required property 'external_id' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Provider",
    "ProviderProps",
    "RoleProps",
]

publication.publish()
