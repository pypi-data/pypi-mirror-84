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

import threading
import traceback
from typing import TYPE_CHECKING

from fabric.actor.core.common.constants import Constants
from fabric.actor.core.core.actor_identity import ActorIdentity
from fabric.actor.core.manage.messages.client_mng import ClientMng
from fabric.message_bus.messages.proxy_avro import ProxyAvro
from fabric.actor.core.util.id import ID
from fabric.message_bus.admin import AdminApi

if TYPE_CHECKING:
    from fabric.actor.core.apis.i_mgmt_actor import IMgmtActor
    from fabric.actor.core.apis.i_actor import IActor, ActorType


class RemoteActorCache:
    ActorName = "NAME"
    ActorGuid = "GUID"
    ActorLocation = "LOCATION"
    ActorProtocol = "PROTOCOL"
    ActorType = "TYPE"

    def __init__(self):
        self.cache = {}
        from fabric.actor.core.container.globals import GlobalsSingleton
        self.logger = GlobalsSingleton.get().get_logger()
        self.lock = threading.Lock()
        self.local_actor_guids = set()

    def known_guids(self) -> set:
        result = None
        try:
            self.lock.acquire()
            result = set()
            for k in self.cache.keys():
                result.add(k)
        finally:
            self.lock.release()
        return result

    def check_to_remove_entry(self, *, guid: ID):
        if guid is None:
            return

        try:
            self.lock.acquire()
            if guid in self.cache:
                value = self.cache[guid]
                if self.ActorLocation not in value:
                    self.cache.pop(guid)
        finally:
            self.lock.release()

    def add_cache_entry(self, *, guid: ID, entry: dict):
        if guid is None or entry is None:
            return

        try:
            self.lock.acquire()
            self.non_mt_cache_merge(guid=guid, entry=entry)
            self.local_actor_guids.add(guid)
        finally:
            self.lock.release()

    def add_partial_cache_entry(self, *, guid: ID, entry: dict):
        if guid is None or entry is None:
            return
        try:
            self.lock.acquire()
            self.non_mt_cache_merge(guid=guid, entry=entry)
        finally:
            self.lock.release()

    def non_mt_cache_merge(self, *, guid: ID, entry: dict):
        if guid not in self.cache:
            self.logger.debug("Inserting new entry for {}".format(guid))
            self.cache[guid] = entry
            return
        current = self.cache[guid]
        for k, v in entry.items():
            current[k] = v

        self.cache[guid] = current

    def get_cache_entry_copy(self, *, guid: ID) -> dict:
        try:
            self.lock.acquire()
            if guid in self.cache:
                ret_val = self.cache[guid]
                return ret_val
        finally:
            self.lock.release()
        return None

    def check_peer(self, *, from_mgmt_actor: IMgmtActor, from_guid: ID, to_mgmt_actor: IMgmtActor, to_guid: ID):
        self.logger.debug("from_mgmt_actor={} from_guid={} to_mgmt_actor={} to_guid={}".format(type(from_mgmt_actor),
                                                                                               from_guid,
                                                                                               type(to_mgmt_actor),
                                                                                               to_guid))
        try:
            if to_mgmt_actor is not None:
                client = to_mgmt_actor.get_client(guid=from_guid)
                if to_mgmt_actor.get_client(guid=from_guid) is not None:
                    self.logger.debug("Edge between {} and {} exists (client)".format(from_guid, to_guid))
                    return True

            elif from_mgmt_actor is not None:
                if from_mgmt_actor.get_broker(broker=to_guid) is not None:
                    self.logger.debug("Edge between {} and {} exists (broker)".format(from_guid, to_guid))
                    return True
        except Exception as e:
            raise Exception("Unable to cast actor {} or {} e={}".format(from_guid, to_guid, e))

        self.logger.debug("Edge between {} and {} does not exist".format(from_guid, to_guid))
        return False

    def establish_peer_private(self, *, from_mgmt_actor: IMgmtActor, from_guid: ID, to_mgmt_actor:IMgmtActor,
                               to_guid: ID) -> ClientMng:
        self.logger.debug("establish_peer_private IN")
        client = None
        from_map = self.get_cache_entry_copy(guid=from_guid)
        to_map = self.get_cache_entry_copy(guid=to_guid)

        if from_map is None:
            raise Exception("Actor {} does not have a registry cache entry".format(from_guid))

        if to_map is None:
            raise Exception("Actor {} does not have a registry cache entry".format(to_guid))

        if from_mgmt_actor is not None:
            self.logger.debug("From actor {} is local".format(from_mgmt_actor.get_name()))

            protocol = Constants.ProtocolLocal
            kafka_topic = None

            if self.ActorLocation in to_map:
                if self.ActorProtocol not in to_map:
                    raise Exception("Actor {} does not specify communications protocol (local/kafka)".format(to_map[self.ActorName]))

                protocol = to_map.get(self.ActorProtocol, None)
                kafka_topic = to_map[self.ActorLocation]
                self.logger.debug("Added To actor location (non-local) {}".format(to_map[self.ActorLocation]))

            identity = ActorIdentity(name=to_map[self.ActorName], guid=to_guid)

            if kafka_topic is not None:
                self.logger.debug("Kafka Topic is available, registering broker proxy")
                proxy = ProxyAvro()
                proxy.set_protocol(protocol)
                proxy.set_guid(str(identity.get_guid()))
                proxy.set_name(identity.get_name())
                proxy.set_type(to_map[self.ActorType])
                proxy.set_kafka_topic(kafka_topic)

                try:
                    if not from_mgmt_actor.add_broker(broker=proxy):
                        raise Exception("Could not register broker {}".format(from_mgmt_actor.get_last_error()))
                except Exception as e:
                    traceback.print_exc()
            else:
                self.logger.debug("Not adding broker to actor at this time because the remote actor actor kafka topic is not available")

            if to_mgmt_actor is not None:
                self.logger.debug("Creating a client for local to actor")
                client = ClientMng()
                client.set_name(name=from_mgmt_actor.get_name())
                client.set_guid(guid=str(from_mgmt_actor.get_guid()))
                try:
                    to_mgmt_actor.register_client(client=client, kafka_topic=kafka_topic)
                except Exception as e:
                    raise Exception("Could not register actor: {} as a client of actor: {} e= {}".format(client.get_name(), to_mgmt_actor.get_name(), e))
        else:
            # fromActor is remote: toActor must be local
            # no-need to create any proxies
            # we only need to register clients
            if to_mgmt_actor is None:
                raise Exception("Both peer endpoints are non local actors: {} {}".format(from_map[self.ActorName], to_map[self.ActorName]))

            if self.ActorGuid not in from_map:
                raise Exception("Missing guid for remote actor: {}".format(from_map[self.ActorName]))

            self.logger.debug("From actor was remote, to actor {} is local".format(to_mgmt_actor.get_name()))
            if self.ActorLocation in from_map:
                kafka_topic = from_map[self.ActorLocation]
                self.logger.debug("From actor has kafka topic")
                self.logger.debug("Creating client for from actor {}".format(from_map[self.ActorName]))
                client = ClientMng()
                client.set_name(name=from_map[self.ActorName])
                client.set_guid(guid=str(from_map[self.ActorGuid]))
                try:
                    to_mgmt_actor.register_client(client=client, kafka_topic=kafka_topic)
                except Exception as e:
                    raise Exception(
                        "Could not register actor: {} as a client of actor: {} e= {}".format(
                            client.get_name(), to_mgmt_actor.get_name(), e))
            else:
                self.logger.debug("Not adding client to actor at this time - remote actor topic not available")
        self.logger.debug("establish_peer_private OUT {}".format(client))
        return client

    def establish_peer(self, *, from_guid: ID, from_mgmt_actor: IMgmtActor, to_guid: ID,
                       to_mgmt_actor: IMgmtActor) -> ClientMng:
        self.logger.debug("establish_peer IN")
        client = None
        if from_guid is None or to_guid is None:
            self.logger.error("Cannot establish peer when either guid is not known")
            raise Exception("Cannot establish peer when either guid is not known")
        try:
            if not self.check_peer(from_mgmt_actor=from_mgmt_actor, from_guid=from_guid,
                                   to_mgmt_actor=to_mgmt_actor, to_guid=to_guid):

                client = self.establish_peer_private(from_mgmt_actor=from_mgmt_actor, from_guid=from_guid,
                                                     to_mgmt_actor=to_mgmt_actor, to_guid=to_guid)

                self.check_to_remove_entry(guid=from_guid)
                self.check_to_remove_entry(guid=to_guid)

                self.logger.debug("Peer established from {} to {}".format(from_guid, to_guid))

        except Exception as e:
            self.logger.error(traceback.format_exc())
            self.logger.error("Peer could not be established from {} to {} e:={}".format(from_guid, to_guid, e))
        self.logger.debug("establish_peer OUT {}".format(client))
        return client

    def check_topic_exists(self, *, topic: str) -> bool:
        api = AdminApi("localhost:9092")
        topic_list = api.list_topics()
        # check topic exists
        if topic_list is not None and topic in topic_list:
            return True
        return False

    def register_with_registry(self, *, actor: IActor):
        try:
            act_name = actor.get_name()
            act_type = actor.get_type()
            act_guid = actor.get_guid()

            from fabric.actor.core.container.globals import GlobalsSingleton
            kafka_topic = GlobalsSingleton.get().get_config().get_actor().get_kafka_topic()

            entry = {self.ActorName: act_name,
                     self.ActorGuid: act_guid,
                     self.ActorType: act_type.name,
                     self.ActorProtocol: Constants.ProtocolKafka,
                     self.ActorLocation: kafka_topic}

            self.add_cache_entry(guid=act_guid, entry=entry)
            # TODO start liveness thread
        except Exception as e:
            self.logger.debug("Could not register actor {} with lcoal registry".format(actor.get_name()))


class RemoteActorCacheSingleton:
    __instance = None

    def __init__(self):
        if self.__instance is not None:
            raise Exception("Singleton can't be created twice !")

    def get(self):
        """
        Actually create an instance
        """
        if self.__instance is None:
            self.__instance = RemoteActorCache()
        return self.__instance

    get = classmethod(get)