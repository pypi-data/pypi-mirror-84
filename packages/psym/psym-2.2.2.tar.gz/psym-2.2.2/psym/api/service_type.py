#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.

from typing import Iterator, List, Mapping, Optional

from psym.client import SymphonyClient
from psym.common.cache import SERVICE_TYPES
from psym.common.data_class import (
    PropertyDefinition,
    PropertyValue,
    ServiceEndpointDefinition,
    ServiceType,
)
from psym.common.data_enum import Entity
from psym.common.data_format import (
    format_to_property_type_inputs,
    format_to_service_type,
)

from .._utils import get_graphql_property_type_inputs
from ..exceptions import EntityNotFoundError
from ..graphql.input.service_type_create_data import ServiceTypeCreateData
from ..graphql.input.service_type_edit_data import (
    ServiceEndpointDefinitionInput,
    ServiceTypeEditData,
)
from ..graphql.mutation.add_service_type import AddServiceTypeMutation
from ..graphql.mutation.edit_service_type import EditServiceTypeMutation
from ..graphql.mutation.remove_service import RemoveServiceMutation
from ..graphql.mutation.remove_service_type import RemoveServiceTypeMutation
from ..graphql.query.service_type_services import ServiceTypeServicesQuery
from ..graphql.query.service_types import ServiceTypesQuery


def _populate_service_types(client: SymphonyClient) -> None:
    service_types = ServiceTypesQuery.execute(client)
    if not service_types:
        return
    edges = service_types.edges
    for edge in edges:
        node = edge.node
        if node is not None:
            SERVICE_TYPES[node.name] = format_to_service_type(
                service_type_fragment=node
            )


def add_service_type(
    client: SymphonyClient,
    name: str,
    has_customer: bool,
    properties: Optional[List[PropertyDefinition]],
    endpoint_definitions: Optional[List[ServiceEndpointDefinition]],
) -> ServiceType:
    """This function creates new service type.

    :param name: Service type name
    :type name: str
    :param has_customer: Flag for customer existance
    :type has_customer: bool
    :param properties: Property definitions list
    :type properties: List[ :class:`~psym.common.data_class.PropertyDefinition` ], optional
    :param endpoint_definitions: Service endpoint definitions list
    :type endpoint_definitions: List[ :class:`~psym.common.data_class.ServiceEndpointDefinition` ], optional

    :raises:
        FailedOperationException: Internal symphony error

    :return: ServiceType object
    :rtype: :class:`~psym.common.data_class.ServiceType`

    **Example**

    .. code-block:: python

        service_type = client.add_service_type(
            client=self.client,
            name="Internet Access",
            has_customer=True,
            properties=[
                PropertyDefinition(
                    property_name="Service Package",
                    property_kind=PropertyKind.string,
                    default_raw_value="Public 5G",
                    is_fixed=False,
                ),
                PropertyDefinition(
                    property_name="Address Family",
                    property_kind=PropertyKind.string,
                    default_raw_value=None,
                    is_fixed=False,
                ),
            ],
        )
    """

    formated_property_types = None
    if properties is not None:
        formated_property_types = format_to_property_type_inputs(data=properties)
    definition_inputs = []
    if endpoint_definitions:
        for endpoint in endpoint_definitions:
            definition_inputs.append(
                ServiceEndpointDefinitionInput(
                    name=endpoint.name,
                    role=endpoint.role,
                    index=endpoint.endpoint_definition_index,
                    equipmentTypeID=endpoint.equipment_type_id,
                )
            )
    result = AddServiceTypeMutation.execute(
        client,
        data=ServiceTypeCreateData(
            name=name,
            hasCustomer=has_customer,
            properties=formated_property_types,
            endpoints=definition_inputs,
        ),
    )
    service_type = format_to_service_type(service_type_fragment=result)
    SERVICE_TYPES[name] = service_type
    return service_type


def get_service_types(client: SymphonyClient) -> Iterator[ServiceType]:
    """Get the iterator of service types

    :raises:
        FailedOperationException: Internal symphony error

    :return: ServiceType Iterator
    :rtype: Iterator[ :class:`~psym.common.data_class.ServiceType` ]

    **Example**

    .. code-block:: python

        service_types = client.get_service_types()
        for service_type in service_types:
            print(service_type.name, service_type.description)
    """
    result = ServiceTypesQuery.execute(client)
    if result is None:
        return
    for edge in result.edges:
        node = edge.node
        if node is not None:
            yield format_to_service_type(service_type_fragment=node)


def get_service_type(client: SymphonyClient, service_type_id: str) -> ServiceType:
    """Get service type by ID.

    :param service_type_id: Service type ID
    :type service_type_id: str

    :raises:
        :class:`~psym.exceptions.EntityNotFoundError`: Service type with id=`service_type_id` does not found

    :return: ServiceType object
    :rtype: :class:`~psym.common.data_class.ServiceType`

    **Example**

    .. code-block:: python

        service_type = client.get_service_type(
            service_type_id="12345",
        )
    """
    for _, service_type in SERVICE_TYPES.items():
        if service_type.id == service_type_id:
            return service_type

    raise EntityNotFoundError(entity=Entity.ServiceType, entity_id=service_type_id)


def add_property_types_to_service_type(
    client: SymphonyClient,
    service_type_id: str,
    new_properties: List[PropertyDefinition],
) -> ServiceType:
    """This function adds new property types to existing service type.

    :param service_type_id: Existing service type ID
    :type service_type_id: str
    :param new_properties: List of property definitions
    :type new_properties: List[ :class:`~psym.common.data_class.PropertyDefinition` ]

    :raises:
        FailedOperationException: Internal symphony error

    :return: LocationType object
    :rtype: :class:`~psym.common.data_class.LocationType`

    **Example**

    .. code-block:: python

        service_type = client.add_property_types_to_service_type(
            service_type_id="12345678",
            new_properties=[
                PropertyDefinition(
                    property_name="Contact",
                    property_kind=PropertyKind.string,
                    default_raw_value=None,
                    is_fixed=True
                )
            ],
        )
    """
    service_type = get_service_type(client=client, service_type_id=service_type_id)
    new_property_type_inputs = format_to_property_type_inputs(data=new_properties)
    result = EditServiceTypeMutation.execute(
        client,
        ServiceTypeEditData(
            id=service_type.id,
            name=service_type.name,
            hasCustomer=service_type.has_customer,
            properties=new_property_type_inputs,
            endpoints=[],
        ),
    )
    edited = format_to_service_type(service_type_fragment=result)
    SERVICE_TYPES.pop(service_type.name)
    SERVICE_TYPES[edited.name] = edited
    return edited


def edit_service_type(
    client: SymphonyClient,
    service_type: ServiceType,
    new_name: Optional[str] = None,
    new_has_customer: Optional[bool] = None,
    new_properties: Optional[Mapping[str, PropertyValue]] = None,
    new_endpoints: Optional[List[ServiceEndpointDefinition]] = None,
) -> ServiceType:
    """Edit existing service type by ID.

    :param service_type: ServiceType object
    :type service_type: :class:`~psym.common.data_class.ServiceType`
    :param new_name: Service type name
    :type new_name: str, optional
    :param new_has_customer: Flag for customer existance
    :type new_has_customer: bool, optional
    :param new_properties: Property definitions list
    :type new_properties: List[ :class:`~psym.common.data_class.PropertyDefinition` ], optional
    :param new_endpoints: Service endpont definitions list
    :type new_endpoints: List[ :class:`~psym.common.data_class.ServiceEndpointDefinition` ], optional

    :raises:
        :class:`~psym.exceptions.EntityNotFoundError`: Service type with id=`service_type_id` does not found

    :return: ServiceType object
    :rtype: :class:`~psym.common.data_class.ServiceType`

    **Example**

    .. code-block:: python

        service_type = client.edit_service_type(
            service_type=service_type,
            new_name="new service type name",
            new_properties={"existing property name": "new value"},
            new_endpoints=[
                ServiceEndpointDefinition(
                    id="endpoint_def_id",
                    name="endpoint_def_name",
                    role="endpoint_def_role",
                    index=1,
                ),
            ],
        )
    """
    new_name = service_type.name if new_name is None else new_name
    new_has_customer = (
        service_type.has_customer if new_has_customer is None else new_has_customer
    )

    new_property_type_inputs = []
    if new_properties:
        property_types = SERVICE_TYPES[service_type.name].property_types
        new_property_type_inputs = get_graphql_property_type_inputs(
            property_types, new_properties
        )

    new_endpoints_definition_inputs = []
    if new_endpoints:
        for endpoint in new_endpoints:
            new_endpoints_definition_inputs.append(
                ServiceEndpointDefinitionInput(
                    name=endpoint.name,
                    role=endpoint.role,
                    index=endpoint.endpoint_definition_index,
                    equipmentTypeID=endpoint.equipment_type_id,
                )
            )

    result = EditServiceTypeMutation.execute(
        client,
        ServiceTypeEditData(
            id=service_type.id,
            name=new_name,
            hasCustomer=new_has_customer,
            properties=new_property_type_inputs,
            endpoints=new_endpoints_definition_inputs,
        ),
    )
    service_type = format_to_service_type(service_type_fragment=result)
    SERVICE_TYPES[service_type.name] = service_type
    return service_type


def delete_service_type(client: SymphonyClient, service_type: ServiceType) -> None:
    """This function deletes an service type.
    It gets the requested service type ID

    :param service_type: ServiceType object
    :type service_type: :class:`~psym.common.data_class.ServiceType`

    :rtype: None

    **Example**

    .. code-block:: python

        client.delete_service_type(service_type_id=service_type.id)
    """
    RemoveServiceTypeMutation.execute(client, id=service_type.id)
    del SERVICE_TYPES[service_type.name]


def delete_service_type_with_services(
    client: SymphonyClient, service_type: ServiceType
) -> None:
    """Delete service type with existing services.

    :param service_type: ServiceType object
    :type service_type: :class:`~psym.common.data_class.ServiceType`

    :raises:
        :class:`~psym.exceptions.EntityNotFoundError`: Service type does not exist

    :rtype: None

    **Example**

    .. code-block:: python

        client.delete_service_type_with_services(service_type=service_type)
    """
    service_type_with_services = ServiceTypeServicesQuery.execute(
        client, id=service_type.id
    )
    if not service_type_with_services:
        raise EntityNotFoundError(entity=Entity.ServiceType, entity_id=service_type.id)
    services = service_type_with_services.services
    for service in services:
        RemoveServiceMutation.execute(client, id=service.id)
    RemoveServiceTypeMutation.execute(client, id=service_type.id)
    del SERVICE_TYPES[service_type.name]
