"""
Main interface for lambda service type definitions.

Usage::

    ```python
    from mypy_boto3_lambda.type_defs import AccountLimitTypeDef

    data: AccountLimitTypeDef = {...}
    ```
"""
import sys
from datetime import datetime
from typing import IO, Any, Dict, List, Union

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict

__all__ = (
    "AccountLimitTypeDef",
    "AccountUsageTypeDef",
    "AliasConfigurationTypeDef",
    "AliasRoutingConfigurationTypeDef",
    "ConcurrencyTypeDef",
    "DeadLetterConfigTypeDef",
    "DestinationConfigTypeDef",
    "EnvironmentErrorTypeDef",
    "EnvironmentResponseTypeDef",
    "EventSourceMappingConfigurationTypeDef",
    "FileSystemConfigTypeDef",
    "FunctionCodeLocationTypeDef",
    "FunctionConfigurationTypeDef",
    "FunctionEventInvokeConfigTypeDef",
    "LayerTypeDef",
    "LayerVersionContentOutputTypeDef",
    "LayerVersionsListItemTypeDef",
    "LayersListItemTypeDef",
    "OnFailureTypeDef",
    "OnSuccessTypeDef",
    "ProvisionedConcurrencyConfigListItemTypeDef",
    "ResponseMetadata",
    "TracingConfigResponseTypeDef",
    "VpcConfigResponseTypeDef",
    "AddLayerVersionPermissionResponseTypeDef",
    "AddPermissionResponseTypeDef",
    "EnvironmentTypeDef",
    "FunctionCodeTypeDef",
    "GetAccountSettingsResponseTypeDef",
    "GetFunctionConcurrencyResponseTypeDef",
    "GetFunctionResponseTypeDef",
    "GetLayerVersionPolicyResponseTypeDef",
    "GetLayerVersionResponseTypeDef",
    "GetPolicyResponseTypeDef",
    "GetProvisionedConcurrencyConfigResponseTypeDef",
    "InvocationResponseTypeDef",
    "InvokeAsyncResponseTypeDef",
    "LayerVersionContentInputTypeDef",
    "ListAliasesResponseTypeDef",
    "ListEventSourceMappingsResponseTypeDef",
    "ListFunctionEventInvokeConfigsResponseTypeDef",
    "ListFunctionsResponseTypeDef",
    "ListLayerVersionsResponseTypeDef",
    "ListLayersResponseTypeDef",
    "ListProvisionedConcurrencyConfigsResponseTypeDef",
    "ListTagsResponseTypeDef",
    "ListVersionsByFunctionResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PublishLayerVersionResponseTypeDef",
    "PutProvisionedConcurrencyConfigResponseTypeDef",
    "TracingConfigTypeDef",
    "VpcConfigTypeDef",
    "WaiterConfigTypeDef",
)

AccountLimitTypeDef = TypedDict(
    "AccountLimitTypeDef",
    {
        "TotalCodeSize": int,
        "CodeSizeUnzipped": int,
        "CodeSizeZipped": int,
        "ConcurrentExecutions": int,
        "UnreservedConcurrentExecutions": int,
    },
    total=False,
)

AccountUsageTypeDef = TypedDict(
    "AccountUsageTypeDef", {"TotalCodeSize": int, "FunctionCount": int}, total=False
)

AliasConfigurationTypeDef = TypedDict(
    "AliasConfigurationTypeDef",
    {
        "AliasArn": str,
        "Name": str,
        "FunctionVersion": str,
        "Description": str,
        "RoutingConfig": "AliasRoutingConfigurationTypeDef",
        "RevisionId": str,
    },
    total=False,
)

AliasRoutingConfigurationTypeDef = TypedDict(
    "AliasRoutingConfigurationTypeDef", {"AdditionalVersionWeights": Dict[str, float]}, total=False
)

ConcurrencyTypeDef = TypedDict(
    "ConcurrencyTypeDef", {"ReservedConcurrentExecutions": int}, total=False
)

DeadLetterConfigTypeDef = TypedDict("DeadLetterConfigTypeDef", {"TargetArn": str}, total=False)

DestinationConfigTypeDef = TypedDict(
    "DestinationConfigTypeDef",
    {"OnSuccess": "OnSuccessTypeDef", "OnFailure": "OnFailureTypeDef"},
    total=False,
)

EnvironmentErrorTypeDef = TypedDict(
    "EnvironmentErrorTypeDef", {"ErrorCode": str, "Message": str}, total=False
)

EnvironmentResponseTypeDef = TypedDict(
    "EnvironmentResponseTypeDef",
    {"Variables": Dict[str, str], "Error": "EnvironmentErrorTypeDef"},
    total=False,
)

EventSourceMappingConfigurationTypeDef = TypedDict(
    "EventSourceMappingConfigurationTypeDef",
    {
        "UUID": str,
        "BatchSize": int,
        "MaximumBatchingWindowInSeconds": int,
        "ParallelizationFactor": int,
        "EventSourceArn": str,
        "FunctionArn": str,
        "LastModified": datetime,
        "LastProcessingResult": str,
        "State": str,
        "StateTransitionReason": str,
        "DestinationConfig": "DestinationConfigTypeDef",
        "Topics": List[str],
        "MaximumRecordAgeInSeconds": int,
        "BisectBatchOnFunctionError": bool,
        "MaximumRetryAttempts": int,
    },
    total=False,
)

FileSystemConfigTypeDef = TypedDict("FileSystemConfigTypeDef", {"Arn": str, "LocalMountPath": str})

FunctionCodeLocationTypeDef = TypedDict(
    "FunctionCodeLocationTypeDef", {"RepositoryType": str, "Location": str}, total=False
)

FunctionConfigurationTypeDef = TypedDict(
    "FunctionConfigurationTypeDef",
    {
        "FunctionName": str,
        "FunctionArn": str,
        "Runtime": Literal[
            "nodejs",
            "nodejs4.3",
            "nodejs6.10",
            "nodejs8.10",
            "nodejs10.x",
            "nodejs12.x",
            "java8",
            "java8.al2",
            "java11",
            "python2.7",
            "python3.6",
            "python3.7",
            "python3.8",
            "dotnetcore1.0",
            "dotnetcore2.0",
            "dotnetcore2.1",
            "dotnetcore3.1",
            "nodejs4.3-edge",
            "go1.x",
            "ruby2.5",
            "ruby2.7",
            "provided",
            "provided.al2",
        ],
        "Role": str,
        "Handler": str,
        "CodeSize": int,
        "Description": str,
        "Timeout": int,
        "MemorySize": int,
        "LastModified": str,
        "CodeSha256": str,
        "Version": str,
        "VpcConfig": "VpcConfigResponseTypeDef",
        "DeadLetterConfig": "DeadLetterConfigTypeDef",
        "Environment": "EnvironmentResponseTypeDef",
        "KMSKeyArn": str,
        "TracingConfig": "TracingConfigResponseTypeDef",
        "MasterArn": str,
        "RevisionId": str,
        "Layers": List["LayerTypeDef"],
        "State": Literal["Pending", "Active", "Inactive", "Failed"],
        "StateReason": str,
        "StateReasonCode": Literal[
            "Idle",
            "Creating",
            "Restoring",
            "EniLimitExceeded",
            "InsufficientRolePermissions",
            "InvalidConfiguration",
            "InternalError",
            "SubnetOutOfIPAddresses",
            "InvalidSubnet",
            "InvalidSecurityGroup",
        ],
        "LastUpdateStatus": Literal["Successful", "Failed", "InProgress"],
        "LastUpdateStatusReason": str,
        "LastUpdateStatusReasonCode": Literal[
            "EniLimitExceeded",
            "InsufficientRolePermissions",
            "InvalidConfiguration",
            "InternalError",
            "SubnetOutOfIPAddresses",
            "InvalidSubnet",
            "InvalidSecurityGroup",
        ],
        "FileSystemConfigs": List["FileSystemConfigTypeDef"],
    },
    total=False,
)

FunctionEventInvokeConfigTypeDef = TypedDict(
    "FunctionEventInvokeConfigTypeDef",
    {
        "LastModified": datetime,
        "FunctionArn": str,
        "MaximumRetryAttempts": int,
        "MaximumEventAgeInSeconds": int,
        "DestinationConfig": "DestinationConfigTypeDef",
    },
    total=False,
)

LayerTypeDef = TypedDict("LayerTypeDef", {"Arn": str, "CodeSize": int}, total=False)

LayerVersionContentOutputTypeDef = TypedDict(
    "LayerVersionContentOutputTypeDef",
    {"Location": str, "CodeSha256": str, "CodeSize": int, "ResponseMetadata": "ResponseMetadata"},
    total=False,
)

LayerVersionsListItemTypeDef = TypedDict(
    "LayerVersionsListItemTypeDef",
    {
        "LayerVersionArn": str,
        "Version": int,
        "Description": str,
        "CreatedDate": str,
        "CompatibleRuntimes": List[
            Literal[
                "nodejs",
                "nodejs4.3",
                "nodejs6.10",
                "nodejs8.10",
                "nodejs10.x",
                "nodejs12.x",
                "java8",
                "java8.al2",
                "java11",
                "python2.7",
                "python3.6",
                "python3.7",
                "python3.8",
                "dotnetcore1.0",
                "dotnetcore2.0",
                "dotnetcore2.1",
                "dotnetcore3.1",
                "nodejs4.3-edge",
                "go1.x",
                "ruby2.5",
                "ruby2.7",
                "provided",
                "provided.al2",
            ]
        ],
        "LicenseInfo": str,
    },
    total=False,
)

LayersListItemTypeDef = TypedDict(
    "LayersListItemTypeDef",
    {"LayerName": str, "LayerArn": str, "LatestMatchingVersion": "LayerVersionsListItemTypeDef"},
    total=False,
)

OnFailureTypeDef = TypedDict("OnFailureTypeDef", {"Destination": str}, total=False)

OnSuccessTypeDef = TypedDict("OnSuccessTypeDef", {"Destination": str}, total=False)

ProvisionedConcurrencyConfigListItemTypeDef = TypedDict(
    "ProvisionedConcurrencyConfigListItemTypeDef",
    {
        "FunctionArn": str,
        "RequestedProvisionedConcurrentExecutions": int,
        "AvailableProvisionedConcurrentExecutions": int,
        "AllocatedProvisionedConcurrentExecutions": int,
        "Status": Literal["IN_PROGRESS", "READY", "FAILED"],
        "StatusReason": str,
        "LastModified": str,
    },
    total=False,
)

ResponseMetadata = TypedDict(
    "ResponseMetadata",
    {
        "RequestId": str,
        "HostId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, Any],
        "RetryAttempts": int,
    },
)

TracingConfigResponseTypeDef = TypedDict(
    "TracingConfigResponseTypeDef", {"Mode": Literal["Active", "PassThrough"]}, total=False
)

VpcConfigResponseTypeDef = TypedDict(
    "VpcConfigResponseTypeDef",
    {"SubnetIds": List[str], "SecurityGroupIds": List[str], "VpcId": str},
    total=False,
)

AddLayerVersionPermissionResponseTypeDef = TypedDict(
    "AddLayerVersionPermissionResponseTypeDef", {"Statement": str, "RevisionId": str}, total=False
)

AddPermissionResponseTypeDef = TypedDict(
    "AddPermissionResponseTypeDef", {"Statement": str}, total=False
)

EnvironmentTypeDef = TypedDict("EnvironmentTypeDef", {"Variables": Dict[str, str]}, total=False)

FunctionCodeTypeDef = TypedDict(
    "FunctionCodeTypeDef",
    {"ZipFile": Union[bytes, IO[bytes]], "S3Bucket": str, "S3Key": str, "S3ObjectVersion": str},
    total=False,
)

GetAccountSettingsResponseTypeDef = TypedDict(
    "GetAccountSettingsResponseTypeDef",
    {"AccountLimit": "AccountLimitTypeDef", "AccountUsage": "AccountUsageTypeDef"},
    total=False,
)

GetFunctionConcurrencyResponseTypeDef = TypedDict(
    "GetFunctionConcurrencyResponseTypeDef", {"ReservedConcurrentExecutions": int}, total=False
)

GetFunctionResponseTypeDef = TypedDict(
    "GetFunctionResponseTypeDef",
    {
        "Configuration": "FunctionConfigurationTypeDef",
        "Code": "FunctionCodeLocationTypeDef",
        "Tags": Dict[str, str],
        "Concurrency": "ConcurrencyTypeDef",
    },
    total=False,
)

GetLayerVersionPolicyResponseTypeDef = TypedDict(
    "GetLayerVersionPolicyResponseTypeDef", {"Policy": str, "RevisionId": str}, total=False
)

GetLayerVersionResponseTypeDef = TypedDict(
    "GetLayerVersionResponseTypeDef",
    {
        "Content": "LayerVersionContentOutputTypeDef",
        "LayerArn": str,
        "LayerVersionArn": str,
        "Description": str,
        "CreatedDate": str,
        "Version": int,
        "CompatibleRuntimes": List[
            Literal[
                "nodejs",
                "nodejs4.3",
                "nodejs6.10",
                "nodejs8.10",
                "nodejs10.x",
                "nodejs12.x",
                "java8",
                "java8.al2",
                "java11",
                "python2.7",
                "python3.6",
                "python3.7",
                "python3.8",
                "dotnetcore1.0",
                "dotnetcore2.0",
                "dotnetcore2.1",
                "dotnetcore3.1",
                "nodejs4.3-edge",
                "go1.x",
                "ruby2.5",
                "ruby2.7",
                "provided",
                "provided.al2",
            ]
        ],
        "LicenseInfo": str,
    },
    total=False,
)

GetPolicyResponseTypeDef = TypedDict(
    "GetPolicyResponseTypeDef", {"Policy": str, "RevisionId": str}, total=False
)

GetProvisionedConcurrencyConfigResponseTypeDef = TypedDict(
    "GetProvisionedConcurrencyConfigResponseTypeDef",
    {
        "RequestedProvisionedConcurrentExecutions": int,
        "AvailableProvisionedConcurrentExecutions": int,
        "AllocatedProvisionedConcurrentExecutions": int,
        "Status": Literal["IN_PROGRESS", "READY", "FAILED"],
        "StatusReason": str,
        "LastModified": str,
    },
    total=False,
)

InvocationResponseTypeDef = TypedDict(
    "InvocationResponseTypeDef",
    {
        "StatusCode": int,
        "FunctionError": str,
        "LogResult": str,
        "Payload": IO[bytes],
        "ExecutedVersion": str,
    },
    total=False,
)

InvokeAsyncResponseTypeDef = TypedDict("InvokeAsyncResponseTypeDef", {"Status": int}, total=False)

LayerVersionContentInputTypeDef = TypedDict(
    "LayerVersionContentInputTypeDef",
    {"S3Bucket": str, "S3Key": str, "S3ObjectVersion": str, "ZipFile": Union[bytes, IO[bytes]]},
    total=False,
)

ListAliasesResponseTypeDef = TypedDict(
    "ListAliasesResponseTypeDef",
    {"NextMarker": str, "Aliases": List["AliasConfigurationTypeDef"]},
    total=False,
)

ListEventSourceMappingsResponseTypeDef = TypedDict(
    "ListEventSourceMappingsResponseTypeDef",
    {"NextMarker": str, "EventSourceMappings": List["EventSourceMappingConfigurationTypeDef"]},
    total=False,
)

ListFunctionEventInvokeConfigsResponseTypeDef = TypedDict(
    "ListFunctionEventInvokeConfigsResponseTypeDef",
    {"FunctionEventInvokeConfigs": List["FunctionEventInvokeConfigTypeDef"], "NextMarker": str},
    total=False,
)

ListFunctionsResponseTypeDef = TypedDict(
    "ListFunctionsResponseTypeDef",
    {"NextMarker": str, "Functions": List["FunctionConfigurationTypeDef"]},
    total=False,
)

ListLayerVersionsResponseTypeDef = TypedDict(
    "ListLayerVersionsResponseTypeDef",
    {"NextMarker": str, "LayerVersions": List["LayerVersionsListItemTypeDef"]},
    total=False,
)

ListLayersResponseTypeDef = TypedDict(
    "ListLayersResponseTypeDef",
    {"NextMarker": str, "Layers": List["LayersListItemTypeDef"]},
    total=False,
)

ListProvisionedConcurrencyConfigsResponseTypeDef = TypedDict(
    "ListProvisionedConcurrencyConfigsResponseTypeDef",
    {
        "ProvisionedConcurrencyConfigs": List["ProvisionedConcurrencyConfigListItemTypeDef"],
        "NextMarker": str,
    },
    total=False,
)

ListTagsResponseTypeDef = TypedDict(
    "ListTagsResponseTypeDef", {"Tags": Dict[str, str]}, total=False
)

ListVersionsByFunctionResponseTypeDef = TypedDict(
    "ListVersionsByFunctionResponseTypeDef",
    {"NextMarker": str, "Versions": List["FunctionConfigurationTypeDef"]},
    total=False,
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PublishLayerVersionResponseTypeDef = TypedDict(
    "PublishLayerVersionResponseTypeDef",
    {
        "Content": "LayerVersionContentOutputTypeDef",
        "LayerArn": str,
        "LayerVersionArn": str,
        "Description": str,
        "CreatedDate": str,
        "Version": int,
        "CompatibleRuntimes": List[
            Literal[
                "nodejs",
                "nodejs4.3",
                "nodejs6.10",
                "nodejs8.10",
                "nodejs10.x",
                "nodejs12.x",
                "java8",
                "java8.al2",
                "java11",
                "python2.7",
                "python3.6",
                "python3.7",
                "python3.8",
                "dotnetcore1.0",
                "dotnetcore2.0",
                "dotnetcore2.1",
                "dotnetcore3.1",
                "nodejs4.3-edge",
                "go1.x",
                "ruby2.5",
                "ruby2.7",
                "provided",
                "provided.al2",
            ]
        ],
        "LicenseInfo": str,
    },
    total=False,
)

PutProvisionedConcurrencyConfigResponseTypeDef = TypedDict(
    "PutProvisionedConcurrencyConfigResponseTypeDef",
    {
        "RequestedProvisionedConcurrentExecutions": int,
        "AvailableProvisionedConcurrentExecutions": int,
        "AllocatedProvisionedConcurrentExecutions": int,
        "Status": Literal["IN_PROGRESS", "READY", "FAILED"],
        "StatusReason": str,
        "LastModified": str,
    },
    total=False,
)

TracingConfigTypeDef = TypedDict(
    "TracingConfigTypeDef", {"Mode": Literal["Active", "PassThrough"]}, total=False
)

VpcConfigTypeDef = TypedDict(
    "VpcConfigTypeDef", {"SubnetIds": List[str], "SecurityGroupIds": List[str]}, total=False
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
