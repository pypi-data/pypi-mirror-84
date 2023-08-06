"""
## AWS APIGatewayv2 Integrations

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development. They are subject to non-backward compatible changes or removal in any future version. These are not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be announced in the release notes. This means that while you may use them, you may need to update your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Table of Contents

* [Introduction](#introduction)
* [Private Integration](#private-integration)

## Introduction

Integrations connect a route to backend resources. HTTP APIs support Lambda proxy, AWS service, and HTTP proxy integrations. HTTP proxy integrations are also known as private integrations.

Currently the following integrations are supported by this construct library.

## Private Integration

Private integrations enable integrating an HTTP API route with private resources in a VPC, such as Application Load Balancers or
Amazon ECS container-based applications.  Using private integrations, resources in a VPC can be exposed for access by
clients outside of the VPC.

The following integrations are supported for private resources in a VPC.

### Application Load Balancer

The following code is a basic application load balancer private integration of HTTP API:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vpc = ec2.Vpc(stack, "VPC")
lb = elbv2.ALB(stack, "lb", vpc=vpc)
listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = HttpApi(stack, "HttpProxyPrivateApi",
    default_integration=HttpAlbIntegrationProps(
        listener=listener
    )
)
```

### Network Load Balancer

The following code is a basic network load balancer private integration of HTTP API:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vpc = ec2.Vpc(stack, "VPC")
lb = elbv2.NLB(stack, "lb", vpc=vpc)
listener = lb.add_listener("listener", port=80)
listener.add_targets("target",
    port=80
)

http_endpoint = HttpApi(stack, "HttpProxyPrivateApi",
    default_integration=HttpNlbIntegrationProps(
        listener=listener
    )
)
```

### Cloud Map Service Discovery

The following code is a basic discovery service private integration of HTTP API:

```python
# Example automatically generated without compilation. See https://github.com/aws/jsii/issues/826
vpc = ec2.Vpc(stack, "VPC")
vpc_link = VpcLink(stack, "VpcLink", vpc=vpc)
namespace = servicediscovery.PrivateDnsNamespace(stack, "Namespace",
    name="boobar.com",
    vpc=vpc
)
service = namespace.create_service("Service")

http_endpoint = HttpApi(stack, "HttpProxyPrivateApi",
    default_integration=HttpServiceDiscoveryIntegration(
        vpc_link=vpc_link,
        service=service
    )
)
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

import aws_cdk.aws_apigatewayv2
import aws_cdk.aws_elasticloadbalancingv2
import aws_cdk.aws_servicediscovery
import aws_cdk.core


@jsii.implements(aws_cdk.aws_apigatewayv2.IHttpRouteIntegration)
class HttpAlbIntegration(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpAlbIntegration",
):
    """(experimental) The Application Load Balancer integration resource for HTTP API.

    :stability: experimental
    """

    def __init__(
        self,
        *,
        listener: aws_cdk.aws_elasticloadbalancingv2.ApplicationListener,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        vpc_link: typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink] = None,
    ) -> None:
        """
        :param listener: (experimental) The listener to the application load balancer used for the integration.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        """
        props = HttpAlbIntegrationProps(
            listener=listener, method=method, vpc_link=vpc_link
        )

        jsii.create(HttpAlbIntegration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: aws_cdk.aws_apigatewayv2.IHttpRoute,
        scope: aws_cdk.core.Construct,
    ) -> aws_cdk.aws_apigatewayv2.HttpRouteIntegrationConfig:
        """(experimental) (experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        """
        options = aws_cdk.aws_apigatewayv2.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return jsii.invoke(self, "bind", [options])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> aws_cdk.aws_apigatewayv2.HttpConnectionType:
        """
        :stability: experimental
        """
        return jsii.get(self, "connectionType")

    @_connection_type.setter # type: ignore
    def _connection_type(
        self,
        value: aws_cdk.aws_apigatewayv2.HttpConnectionType,
    ) -> None:
        jsii.set(self, "connectionType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> aws_cdk.aws_apigatewayv2.HttpMethod:
        """
        :stability: experimental
        """
        return jsii.get(self, "httpMethod")

    @_http_method.setter # type: ignore
    def _http_method(self, value: aws_cdk.aws_apigatewayv2.HttpMethod) -> None:
        jsii.set(self, "httpMethod", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="integrationType")
    def _integration_type(self) -> aws_cdk.aws_apigatewayv2.HttpIntegrationType:
        """
        :stability: experimental
        """
        return jsii.get(self, "integrationType")

    @_integration_type.setter # type: ignore
    def _integration_type(
        self,
        value: aws_cdk.aws_apigatewayv2.HttpIntegrationType,
    ) -> None:
        jsii.set(self, "integrationType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(self) -> aws_cdk.aws_apigatewayv2.PayloadFormatVersion:
        """
        :stability: experimental
        """
        return jsii.get(self, "payloadFormatVersion")

    @_payload_format_version.setter # type: ignore
    def _payload_format_version(
        self,
        value: aws_cdk.aws_apigatewayv2.PayloadFormatVersion,
    ) -> None:
        jsii.set(self, "payloadFormatVersion", value)


@jsii.implements(aws_cdk.aws_apigatewayv2.IHttpRouteIntegration)
class HttpNlbIntegration(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpNlbIntegration",
):
    """(experimental) The Network Load Balancer integration resource for HTTP API.

    :stability: experimental
    """

    def __init__(
        self,
        *,
        listener: aws_cdk.aws_elasticloadbalancingv2.NetworkListener,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        vpc_link: typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink] = None,
    ) -> None:
        """
        :param listener: (experimental) The listener to the netwwork load balancer used for the integration.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        """
        props = HttpNlbIntegrationProps(
            listener=listener, method=method, vpc_link=vpc_link
        )

        jsii.create(HttpNlbIntegration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: aws_cdk.aws_apigatewayv2.IHttpRoute,
        scope: aws_cdk.core.Construct,
    ) -> aws_cdk.aws_apigatewayv2.HttpRouteIntegrationConfig:
        """(experimental) (experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        """
        options = aws_cdk.aws_apigatewayv2.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return jsii.invoke(self, "bind", [options])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> aws_cdk.aws_apigatewayv2.HttpConnectionType:
        """
        :stability: experimental
        """
        return jsii.get(self, "connectionType")

    @_connection_type.setter # type: ignore
    def _connection_type(
        self,
        value: aws_cdk.aws_apigatewayv2.HttpConnectionType,
    ) -> None:
        jsii.set(self, "connectionType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> aws_cdk.aws_apigatewayv2.HttpMethod:
        """
        :stability: experimental
        """
        return jsii.get(self, "httpMethod")

    @_http_method.setter # type: ignore
    def _http_method(self, value: aws_cdk.aws_apigatewayv2.HttpMethod) -> None:
        jsii.set(self, "httpMethod", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="integrationType")
    def _integration_type(self) -> aws_cdk.aws_apigatewayv2.HttpIntegrationType:
        """
        :stability: experimental
        """
        return jsii.get(self, "integrationType")

    @_integration_type.setter # type: ignore
    def _integration_type(
        self,
        value: aws_cdk.aws_apigatewayv2.HttpIntegrationType,
    ) -> None:
        jsii.set(self, "integrationType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(self) -> aws_cdk.aws_apigatewayv2.PayloadFormatVersion:
        """
        :stability: experimental
        """
        return jsii.get(self, "payloadFormatVersion")

    @_payload_format_version.setter # type: ignore
    def _payload_format_version(
        self,
        value: aws_cdk.aws_apigatewayv2.PayloadFormatVersion,
    ) -> None:
        jsii.set(self, "payloadFormatVersion", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpPrivateIntegrationOptions",
    jsii_struct_bases=[],
    name_mapping={"method": "method", "vpc_link": "vpcLink"},
)
class HttpPrivateIntegrationOptions:
    def __init__(
        self,
        *,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        vpc_link: typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink] = None,
    ) -> None:
        """(experimental) Base options for private integration.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {}
        if method is not None:
            self._values["method"] = method
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod]:
        """(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        """
        result = self._values.get("method")
        return result

    @builtins.property
    def vpc_link(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink]:
        """(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        """
        result = self._values.get("vpc_link")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpPrivateIntegrationOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.implements(aws_cdk.aws_apigatewayv2.IHttpRouteIntegration)
class HttpServiceDiscoveryIntegration(
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpServiceDiscoveryIntegration",
):
    """(experimental) The Service Discovery integration resource for HTTP API.

    :stability: experimental
    """

    def __init__(
        self,
        *,
        service: aws_cdk.aws_servicediscovery.Service,
        vpc_link: aws_cdk.aws_apigatewayv2.IVpcLink,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
    ) -> None:
        """
        :param service: (experimental) The discovery service used for the integration.
        :param vpc_link: (experimental) The vpc link to be used for the private integration.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY

        :stability: experimental
        """
        props = HttpServiceDiscoveryIntegrationProps(
            service=service, vpc_link=vpc_link, method=method
        )

        jsii.create(HttpServiceDiscoveryIntegration, self, [props])

    @jsii.member(jsii_name="bind")
    def bind(
        self,
        *,
        route: aws_cdk.aws_apigatewayv2.IHttpRoute,
        scope: aws_cdk.core.Construct,
    ) -> aws_cdk.aws_apigatewayv2.HttpRouteIntegrationConfig:
        """(experimental) (experimental) Bind this integration to the route.

        :param route: (experimental) The route to which this is being bound.
        :param scope: (experimental) The current scope in which the bind is occurring. If the ``HttpRouteIntegration`` being bound creates additional constructs, this will be used as their parent scope.

        :stability: experimental
        """
        _ = aws_cdk.aws_apigatewayv2.HttpRouteIntegrationBindOptions(
            route=route, scope=scope
        )

        return jsii.invoke(self, "bind", [_])

    @builtins.property # type: ignore
    @jsii.member(jsii_name="connectionType")
    def _connection_type(self) -> aws_cdk.aws_apigatewayv2.HttpConnectionType:
        """
        :stability: experimental
        """
        return jsii.get(self, "connectionType")

    @_connection_type.setter # type: ignore
    def _connection_type(
        self,
        value: aws_cdk.aws_apigatewayv2.HttpConnectionType,
    ) -> None:
        jsii.set(self, "connectionType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="httpMethod")
    def _http_method(self) -> aws_cdk.aws_apigatewayv2.HttpMethod:
        """
        :stability: experimental
        """
        return jsii.get(self, "httpMethod")

    @_http_method.setter # type: ignore
    def _http_method(self, value: aws_cdk.aws_apigatewayv2.HttpMethod) -> None:
        jsii.set(self, "httpMethod", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="integrationType")
    def _integration_type(self) -> aws_cdk.aws_apigatewayv2.HttpIntegrationType:
        """
        :stability: experimental
        """
        return jsii.get(self, "integrationType")

    @_integration_type.setter # type: ignore
    def _integration_type(
        self,
        value: aws_cdk.aws_apigatewayv2.HttpIntegrationType,
    ) -> None:
        jsii.set(self, "integrationType", value)

    @builtins.property # type: ignore
    @jsii.member(jsii_name="payloadFormatVersion")
    def _payload_format_version(self) -> aws_cdk.aws_apigatewayv2.PayloadFormatVersion:
        """
        :stability: experimental
        """
        return jsii.get(self, "payloadFormatVersion")

    @_payload_format_version.setter # type: ignore
    def _payload_format_version(
        self,
        value: aws_cdk.aws_apigatewayv2.PayloadFormatVersion,
    ) -> None:
        jsii.set(self, "payloadFormatVersion", value)


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpServiceDiscoveryIntegrationProps",
    jsii_struct_bases=[],
    name_mapping={"service": "service", "vpc_link": "vpcLink", "method": "method"},
)
class HttpServiceDiscoveryIntegrationProps:
    def __init__(
        self,
        *,
        service: aws_cdk.aws_servicediscovery.Service,
        vpc_link: aws_cdk.aws_apigatewayv2.IVpcLink,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
    ) -> None:
        """(experimental) Properties to initialize ``HttpServiceDiscoveryIntegration``.

        :param service: (experimental) The discovery service used for the integration.
        :param vpc_link: (experimental) The vpc link to be used for the private integration.
        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "service": service,
            "vpc_link": vpc_link,
        }
        if method is not None:
            self._values["method"] = method

    @builtins.property
    def service(self) -> aws_cdk.aws_servicediscovery.Service:
        """(experimental) The discovery service used for the integration.

        :stability: experimental
        """
        result = self._values.get("service")
        assert result is not None, "Required property 'service' is missing"
        return result

    @builtins.property
    def vpc_link(self) -> aws_cdk.aws_apigatewayv2.IVpcLink:
        """(experimental) The vpc link to be used for the private integration.

        :stability: experimental
        """
        result = self._values.get("vpc_link")
        assert result is not None, "Required property 'vpc_link' is missing"
        return result

    @builtins.property
    def method(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod]:
        """(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        """
        result = self._values.get("method")
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpServiceDiscoveryIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpAlbIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={"method": "method", "vpc_link": "vpcLink", "listener": "listener"},
)
class HttpAlbIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        vpc_link: typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink] = None,
        listener: aws_cdk.aws_elasticloadbalancingv2.ApplicationListener,
    ) -> None:
        """(experimental) Properties to initialize ``HttpAlbIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created
        :param listener: (experimental) The listener to the application load balancer used for the integration.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "listener": listener,
        }
        if method is not None:
            self._values["method"] = method
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod]:
        """(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        """
        result = self._values.get("method")
        return result

    @builtins.property
    def vpc_link(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink]:
        """(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        """
        result = self._values.get("vpc_link")
        return result

    @builtins.property
    def listener(self) -> aws_cdk.aws_elasticloadbalancingv2.ApplicationListener:
        """(experimental) The listener to the application load balancer used for the integration.

        :stability: experimental
        """
        result = self._values.get("listener")
        assert result is not None, "Required property 'listener' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpAlbIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="@aws-cdk/aws-apigatewayv2-integrations.HttpNlbIntegrationProps",
    jsii_struct_bases=[HttpPrivateIntegrationOptions],
    name_mapping={"method": "method", "vpc_link": "vpcLink", "listener": "listener"},
)
class HttpNlbIntegrationProps(HttpPrivateIntegrationOptions):
    def __init__(
        self,
        *,
        method: typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod] = None,
        vpc_link: typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink] = None,
        listener: aws_cdk.aws_elasticloadbalancingv2.NetworkListener,
    ) -> None:
        """(experimental) Properties to initialize ``HttpNlbIntegration``.

        :param method: (experimental) The HTTP method that must be used to invoke the underlying HTTP proxy. Default: HttpMethod.ANY
        :param vpc_link: (experimental) The vpc link to be used for the private integration. Default: - a new VpcLink is created
        :param listener: (experimental) The listener to the netwwork load balancer used for the integration.

        :stability: experimental
        """
        self._values: typing.Dict[str, typing.Any] = {
            "listener": listener,
        }
        if method is not None:
            self._values["method"] = method
        if vpc_link is not None:
            self._values["vpc_link"] = vpc_link

    @builtins.property
    def method(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.HttpMethod]:
        """(experimental) The HTTP method that must be used to invoke the underlying HTTP proxy.

        :default: HttpMethod.ANY

        :stability: experimental
        """
        result = self._values.get("method")
        return result

    @builtins.property
    def vpc_link(self) -> typing.Optional[aws_cdk.aws_apigatewayv2.IVpcLink]:
        """(experimental) The vpc link to be used for the private integration.

        :default: - a new VpcLink is created

        :stability: experimental
        """
        result = self._values.get("vpc_link")
        return result

    @builtins.property
    def listener(self) -> aws_cdk.aws_elasticloadbalancingv2.NetworkListener:
        """(experimental) The listener to the netwwork load balancer used for the integration.

        :stability: experimental
        """
        result = self._values.get("listener")
        assert result is not None, "Required property 'listener' is missing"
        return result

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "HttpNlbIntegrationProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "HttpAlbIntegration",
    "HttpAlbIntegrationProps",
    "HttpNlbIntegration",
    "HttpNlbIntegrationProps",
    "HttpPrivateIntegrationOptions",
    "HttpServiceDiscoveryIntegration",
    "HttpServiceDiscoveryIntegrationProps",
]

publication.publish()
