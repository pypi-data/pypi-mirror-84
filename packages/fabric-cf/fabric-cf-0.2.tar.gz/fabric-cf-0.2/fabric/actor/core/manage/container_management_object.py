#!/usr/bin/env python3
# MIT License
#
# Copyright (c) 2020 FABRIC Testbed
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#
#
# Author: Komal Thareja (kthare10@renci.org)
from __future__ import annotations
from typing import TYPE_CHECKING

from fabric.actor.core.apis.i_actor import ActorType
from fabric.actor.core.common.constants import Constants, ErrorCodes
from fabric.actor.core.manage.converter import Converter
from fabric.actor.core.manage.management_object import ManagementObject
from fabric.actor.core.manage.proxy_protocol_descriptor import ProxyProtocolDescriptor
from fabric.actor.core.apis.i_management_object import IManagementObject
from fabric.message_bus.messages.result_proxy_avro import ResultProxyAvro
from fabric.actor.core.registry.actor_registry import ActorRegistrySingleton
from fabric.actor.core.util.id import ID
from fabric.message_bus.messages.result_actor_avro import ResultActorAvro
from fabric.message_bus.messages.result_avro import ResultAvro

if TYPE_CHECKING:
    from fabric.actor.core.apis.i_container_database import IContainerDatabase
    from fabric.actor.security.auth_token import AuthToken


class ContainerManagementObject(ManagementObject):
    def __init__(self):
        super().__init__()
        self.id = ID(id=Constants.ContainerManagmentObjectID)

    def register_protocols(self):
        from fabric.actor.core.manage.local.local_container import LocalContainer
        local = ProxyProtocolDescriptor(protocol=Constants.ProtocolLocal,
                                        proxy_class=LocalContainer.__name__,
                                        proxy_module=LocalContainer.__module__)

        from fabric.actor.core.manage.kafka.kafka_container import KafkaContainer
        kakfa = ProxyProtocolDescriptor(protocol=Constants.ProtocolKafka,
                                        proxy_class=KafkaContainer.__name__,
                                        proxy_module=KafkaContainer.__module__)

        self.proxies = []
        self.proxies.append(local)
        self.proxies.append(kakfa)

    def save(self) -> dict:
        properties = super().save()
        properties[Constants.PropertyClassName] = ContainerManagementObject.__name__
        properties[Constants.PropertyModuleName] = ContainerManagementObject.__module__

        return properties

    def get_container_management_database(self) -> IContainerDatabase:
        from fabric.actor.core.container.globals import GlobalsSingleton
        return GlobalsSingleton.get().get_container().get_database()

    def get_actors_from_registry(self, *, atype: int, user: AuthToken):
        result = []
        actors = ActorRegistrySingleton.get().get_actors()
        if actors is not None:
            for a in actors:
                if atype == ActorType.All.value or atype == a.get_type():
                    result.append(a)
        return result

    def get_actors(self, *, caller: AuthToken, id_token: str = None) -> ResultActorAvro:
        result = ResultActorAvro()
        result.status = ResultAvro()

        if caller is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            act_list = self.get_actors_from_registry(atype=ActorType.All.value, user=caller)
            result.result = Converter.fill_actors(act_list=act_list)
        except Exception as e:
            self.logger.error("get_actors {}".format(e))
            result.status.set_code(ErrorCodes.ErrorInternalError.value)
            result.status.set_message(ErrorCodes.ErrorInternalError.name)
            result.status = ManagementObject.set_exception_details(result=result.status, e=e)

        return result

    def get_actors_from_database(self, *, caller: AuthToken, id_token: str = None) -> ResultActorAvro:
        result = ResultActorAvro()
        result.status = ResultAvro()

        if caller is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            act_list = None
            try:
                act_list = self.get_container_management_database().get_actors()
            except Exception as e:
                self.logger.error("get_actors_from_database {}".format(e))
                result.status.set_code(ErrorCodes.ErrorDatabaseError.value)
                result.status.set_message(ErrorCodes.ErrorDatabaseError.name)
                result.status = ManagementObject.set_exception_details(result=result.status, e=e)
                return result

            if act_list is not None:
                result.result = Converter.fill_actors_from_db(act_list=act_list)

        except Exception as e:
            self.logger.error("get_actors_from_database {}".format(e))
            result.status.set_code(ErrorCodes.ErrorInternalError.value)
            result.status.set_message(ErrorCodes.ErrorInternalError.name)
            result.status = ManagementObject.set_exception_details(result=result.status, e=e)

        return result

    def get_actors_from_database_name_type_status(self, *, name: str, actor_type: int, status: int,
                                                  caller: AuthToken, id_token: str = None) -> ResultActorAvro:
        result = ResultActorAvro()
        result.status = ResultAvro()

        if caller is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            act_list = None
            try:
                act_list = self.get_container_management_database().get_actors(name=name, actor_type=actor_type)
            except Exception as e:
                self.logger.error("get_actors_from_database {}".format(e))
                result.status.set_code(ErrorCodes.ErrorDatabaseError.value)
                result.status.set_message(ErrorCodes.ErrorDatabaseError.name)
                result.status = ManagementObject.set_exception_details(result=result.status, e=e)
                return result

            if act_list is not None:
                result.result = Converter.fill_actors_from_db_status(act_list=act_list, status=status)

        except Exception as e:
            self.logger.error("get_actors_from_database {}".format(e))
            result.status.set_code(ErrorCodes.ErrorInternalError.value)
            result.status.set_message(ErrorCodes.ErrorInternalError.name)
            result.status = ManagementObject.set_exception_details(result=result.status, e=e)

        return result

    def get_controllers(self, *, caller: AuthToken, id_token: str = None) -> ResultActorAvro:
        result = ResultActorAvro()
        result.status = ResultAvro()

        if caller is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            act_list = self.get_actors_from_registry(atype=ActorType.Orchestrator.value, user=caller)
            result.result = Converter.fill_actors(act_list=act_list)
        except Exception as e:
            self.logger.error("get_controllers {}".format(e))
            result.status.set_code(ErrorCodes.ErrorInternalError.value)
            result.status.set_message(ErrorCodes.ErrorInternalError.name)
            result.status = ManagementObject.set_exception_details(result=result.status, e=e)

    def get_brokers(self, *, caller: AuthToken, id_token: str = None) -> ResultActorAvro:
        result = ResultActorAvro()
        result.status = ResultAvro()

        if caller is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            act_list = self.get_actors_from_registry(atype=ActorType.Broker.value, user=caller)
            result.result = Converter.fill_actors(act_list=act_list)
        except Exception as e:
            self.logger.error("get_brokers {}".format(e))
            result.status.set_code(ErrorCodes.ErrorInternalError.value)
            result.status.set_message(ErrorCodes.ErrorInternalError.name)
            result.status = ManagementObject.set_exception_details(result=result.status, e=e)

    def get_authorities(self, *, caller: AuthToken, id_token: str = None) -> ResultActorAvro:
        result = ResultActorAvro()
        result.status = ResultAvro()

        if caller is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            act_list = self.get_actors_from_registry(atype=ActorType.Authority.value, user=caller)
            result.result = Converter.fill_actors(act_list=act_list)
        except Exception as e:
            self.logger.error("get_authorities {}".format(e))
            result.status.set_code(ErrorCodes.ErrorInternalError.value)
            result.status.set_message(ErrorCodes.ErrorInternalError.name)
            result.status = ManagementObject.set_exception_details(result=result.status, e=e)

    def get_management_object(self, *, key: ID) -> IManagementObject:
        from fabric.actor.core.container.globals import GlobalsSingleton
        return GlobalsSingleton.get().get_container().get_management_object_manager().get_management_object(key=key)

    def get_broker_proxies(self, *, protocol: str, caller: AuthToken, id_token: str = None) -> ResultProxyAvro:
        result = ResultProxyAvro()
        result.status = ResultAvro()

        if caller is None or protocol is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            proxies = ActorRegistrySingleton.get().get_broker_proxies(protocol=protocol)
            result.result = Converter.fill_proxies(proxies=proxies)
        except Exception as e:
            self.logger.error("get_broker_proxies {}".format(e))
            result.status.set_code(ErrorCodes.ErrorInternalError.value)
            result.status.set_message(ErrorCodes.ErrorInternalError.name)
            result.status = ManagementObject.set_exception_details(result=result.status, e=e)

    def get_site_proxies(self, *, protocol: str, caller: AuthToken, id_token: str = None) -> ResultProxyAvro:
        result = ResultProxyAvro()
        result.status = ResultAvro()

        if caller is None or protocol is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            proxies = ActorRegistrySingleton.get().get_site_proxies(protocol=protocol)
            result.result = Converter.fill_proxies(proxies=proxies)
        except Exception as e:
            self.logger.error("get_site_proxies {}".format(e))
            result.status.set_code(ErrorCodes.ErrorInternalError.value)
            result.status.set_message(ErrorCodes.ErrorInternalError.name)
            result.status = ManagementObject.set_exception_details(result=result.status, e=e)

    def get_proxies_by_protocol(self, *, protocol: str, caller: AuthToken, id_token: str = None) -> ResultProxyAvro:
        result = ResultProxyAvro()
        result.status = ResultAvro()

        if caller is None or protocol is None:
            result.status.set_code(ErrorCodes.ErrorInvalidArguments.value)
            result.status.set_message(ErrorCodes.ErrorInvalidArguments.name)
            return result

        try:
            proxies = ActorRegistrySingleton.get().get_proxies(protocol=protocol)
            result.result = Converter.fill_proxies(proxies=proxies)
        except Exception as e:
            self.logger.error("get_proxies {}".format(e))
            result.status.set_code(ErrorCodes.ErrorInternalError.value)
            result.status.set_message(ErrorCodes.ErrorInternalError.name)
            result.status = ManagementObject.set_exception_details(result=result.status, e=e)
