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

import queue
import threading
from datetime import datetime
from typing import TYPE_CHECKING

from fabric.actor.core.apis.i_actor import ActorType
from fabric.actor.core.apis.i_delegation import IDelegation
from fabric.actor.core.delegation.broker_delegation_factory import BrokerDelegationFactory
from fabric.actor.core.delegation.delegation_factory import DelegationFactory
from fabric.actor.core.kernel.broker_reservation_factory import BrokerReservationFactory
from fabric.actor.core.kernel.client_reservation_factory import ClientReservationFactory
from fabric.actor.core.kernel.slice_factory import SliceFactory
from fabric.actor.core.manage.broker_management_object import BrokerManagementObject
from fabric.actor.core.manage.kafka.services.kafka_broker_service import KafkaBrokerService
from fabric.actor.core.proxies.kafka.services.broker_service import BrokerService
from fabric.actor.core.registry.actor_registry import ActorRegistrySingleton
from fabric.actor.core.time.term import Term
from fabric.actor.core.util.resource_data import ResourceData

if TYPE_CHECKING:
    from fabric.actor.core.apis.i_broker_proxy import IBrokerProxy
    from fabric.actor.core.apis.i_slice import ISlice
    from fabric.actor.core.apis.i_client_reservation import IClientReservation
    from fabric.actor.core.kernel.resource_set import ResourceSet
    from fabric.actor.core.util.id import ID
    from fabric.actor.core.apis.i_client_callback_proxy import IClientCallbackProxy
    from fabric.actor.core.apis.i_reservation import IReservation
    from fabric.actor.core.apis.i_broker_reservation import IBrokerReservation
    from fabric.actor.core.util.client import Client

from fabric.actor.core.apis.i_broker import IBroker
from fabric.actor.core.common.constants import Constants
from fabric.actor.core.core.actor import Actor
from fabric.actor.core.registry.peer_registry import PeerRegistry
from fabric.actor.core.time.actor_clock import ActorClock
from fabric.actor.core.util.reservation_set import ReservationSet
from fabric.actor.security.auth_token import AuthToken


class Broker(Actor, IBroker):
    """
    Broker offers the base for all broker actors.
    """
    def __init__(self, *, identity: AuthToken = None, clock: ActorClock = None):
        super().__init__(auth=identity, clock=clock)
        # Recovered reservations that need to obtain tickets (both server and client roles).
        self.ticketing = ReservationSet()
        # Recovered reservations that need to extend tickets (both server and client roles).
        self.extending = ReservationSet()
        # The peer registry.
        self.registry = PeerRegistry()
        # Initialization status.
        self.initialized = False
        self.type = ActorType.Broker

    def __getstate__(self):
        state = self.__dict__.copy()
        del state['recovered']
        del state['wrapper']
        del state['logger']
        del state['clock']
        del state['monitor']
        del state['current_cycle']
        del state['first_tick']
        del state['stopped']
        del state['initialized']
        del state['thread_lock']
        del state['thread']
        del state['timer_queue']
        del state['event_queue']
        del state['reservation_tracker']
        del state['subscription_id']
        del state['actor_main_lock']
        del state['closing']
        del state['message_service']

        del state['ticketing']
        del state['extending']
        del state['registry']
        return state

    def __setstate__(self, state):
        self.__dict__.update(state)

        self.recovered = False
        self.wrapper = None
        self.logger = None
        self.clock = None
        self.monitor = None
        self.current_cycle = -1
        self.first_tick = True
        self.stopped = False
        self.initialized = False
        self.thread = None
        self.thread_lock = threading.Lock()
        self.timer_queue = queue.Queue()
        self.event_queue = queue.Queue()
        self.reservation_tracker = None
        self.subscription_id = None
        self.actor_main_lock = threading.Condition()
        self.closing = ReservationSet()
        self.message_service = None

        self.ticketing = ReservationSet()
        self.extending = ReservationSet()
        self.registry = PeerRegistry()

    def actor_added(self):
        super().actor_added()
        self.registry.actor_added()

    def add_broker(self, *, broker: IBrokerProxy):
        self.registry.add_broker(broker=broker)

    def register_client_slice(self, *, slice:ISlice):
        self.wrapper.register_slice(slice_object=slice)

    def bid(self, *, cycle: int):
        """
        Bids for resources as dictated by the bidding policy for the current cycle.

        @param cycle cycle

        @throws Exception in case of error
        """
        candidates = None
        candidates = self.policy.formulate_bids(cycle=cycle)
        if candidates is not None:
            for reservation in candidates.get_ticketing().values():
                try:
                    self.wrapper.ticket(reservation=reservation, destination=self)
                except Exception as e:
                    self.logger.error("unexpected ticket failure for #{}".format(reservation.get_reservation_id()))

            for reservation in candidates.get_extending().values():
                try:
                    self.wrapper.extend_ticket(reservation=reservation)
                except Exception as e:
                    self.logger.error("unexpected extend failure for #{}".format(reservation.get_reservation_id()))

    def claim_client(self, *, reservation_id: ID = None, resources: ResourceSet = None,
                     slice_object: ISlice = None, broker: IBrokerProxy = None) -> IClientReservation:
        if reservation_id is None:
            raise Exception("Invalid arguments")

        if broker is None:
            broker = self.get_default_broker()

        if slice_object is None:
            slice_object = self.get_default_slice()
            if slice_object is None:
                slice_object = SliceFactory.create(slice_id=ID(), name=self.identity.get_name())
                slice_object.set_owner(owner=self.identity)
                slice_object.set_inventory(value=True)

        end = datetime.utcnow()
        end.replace(year=end.year + 30)
        term = Term(start=self.clock.cycle_start_date(cycle=0), end=end)

        reservation = ClientReservationFactory.create(rid=reservation_id, resources=resources, term=term,
                                                      slice_object=slice_object, broker=broker, actor=self)
        reservation.set_exported(exported=True)
        self.wrapper.ticket(reservation=reservation, destination=self)
        return reservation

    def reclaim_client(self, *, reservation_id: ID = None, resources: ResourceSet = None,
                       slice_object: ISlice = None, broker: IBrokerProxy = None,
                       caller: AuthToken = None) -> IClientReservation:
        if reservation_id is None:
            raise Exception("Invalid arguments")

        if broker is None:
            broker = self.get_default_broker()

        if slice_object is None:
            slice_object = self.get_default_slice()
            if slice_object is None:
                slice_object = SliceFactory.create(slice_id=ID(), name=self.identity.get_name())
                slice_object.set_owner(owner=self.identity)
                slice_object.set_inventory(value=True)

        end = datetime.utcnow()
        end.replace(year=end.year + 30)
        term = Term(start=self.clock.cycle_start_date(0), end=end)

        reservation = ClientReservationFactory.create(rid=reservation_id, resources=resources, term=term,
                                                      slice_object=slice_object, broker=broker, actor=self)
        reservation.set_exported(exported=True)

        protocol = reservation.get_broker().get_type()
        callback = ActorRegistrySingleton.get().get_callback(protocol=protocol, actor_name=self.get_name())
        if callback is None:
            raise Exception("Unsupported")

        reservation.prepare(callback=callback, logger=self.logger)
        reservation.validate_outgoing()
        self.wrapper.reclaim_request(reservation=reservation, caller=caller, callback=callback)

        return reservation

    def claim(self, *, reservation: IReservation, callback: IClientCallbackProxy, caller: AuthToken):
        if not self.is_recovered() or self.is_stopped():
            raise Exception("This actor cannot receive calls")
        self.wrapper.claim_request(reservation=reservation, caller=caller, callback=callback)

    def reclaim(self, *, reservation: IReservation, callback: IClientCallbackProxy, caller: AuthToken):
        if not self.is_recovered() or self.is_stopped():
            raise Exception("This actor cannot receive calls")
        self.wrapper.reclaim_request(reservation=reservation, caller=caller, callback=callback)

    def claim_delegation_client(self, *, delegation_id: str = None, slice_object: ISlice = None,
                                broker: IBrokerProxy = None, id_token:str = None) -> IDelegation:
        if delegation_id is None:
            raise Exception("Invalid arguments")

        if broker is None:
            broker = self.get_default_broker()

        if slice_object is None:
            slice_object = self.get_default_slice()
            if slice_object is None:
                slice_object = SliceFactory.create(slice_id=ID(), name=self.identity.get_name())
                slice_object.set_owner(owner=self.identity)
                slice_object.set_inventory(value=True)

        delegation = BrokerDelegationFactory.create(did=delegation_id, slice_id=slice_object.get_slice_id(),
                                                    broker=broker)
        delegation.set_exported(value=True)
        delegation.set_slice_object(slice_object=slice_object)

        self.wrapper.delegate(delegation=delegation, destination=self, id_token=id_token)
        return delegation

    def reclaim_delegation_client(self, *, delegation_id: str = None, slice_object: ISlice = None,
                                  broker: IBrokerProxy = None, id_token:str = None) -> IDelegation:
        if delegation_id is None:
            raise Exception("Invalid arguments")

        if broker is None:
            broker = self.get_default_broker()

        if slice_object is None:
            slice_object = self.get_default_slice()
            if slice_object is None:
                slice_object = SliceFactory.create(slice_id=ID(), name=self.identity.get_name())
                slice_object.set_owner(owner=self.identity)
                slice_object.set_inventory(value=True)

        delegation = BrokerDelegationFactory.create(did=delegation_id, slice_id=slice_object.get_slice_id(),
                                                    broker=broker)
        delegation.set_slice_object(slice_object=slice_object)
        delegation.set_exported(exported=True)

        callback = ActorRegistrySingleton.get().get_callback(protocol=Constants.ProtocolKafka,
                                                             actor_name=self.get_name())
        if callback is None:
            raise Exception("Unsupported")

        delegation.prepare(callback=callback, logger=self.logger)
        delegation.validate_outgoing()

        self.wrapper.reclaim_delegation_request(delegation=delegation, caller=broker, callback=callback,
                                                id_token=id_token)

        return delegation

    def claim_delegation(self, *, delegation: IDelegation, callback: IClientCallbackProxy, caller: AuthToken):
        if not self.is_recovered() or self.is_stopped():
            raise Exception("This actor cannot receive calls")
        self.wrapper.claim_delegation_request(delegation=delegation, caller=caller, callback=callback)

    def reclaim_delegation(self, *, delegation: IDelegation, callback: IClientCallbackProxy, caller: AuthToken):
        if not self.is_recovered() or self.is_stopped():
            raise Exception("This actor cannot receive calls")
        self.wrapper.reclaim_delegation_request(delegation=delegation, caller=caller, callback=callback)

    def close_expiring(self, *, cycle: int):
        """
        Closes all expiring reservations.
        @param cycle cycle
        """
        expired = self.policy.get_closing(cycle=cycle)
        if expired is not None:
            self.logger.info("Broker expiring for cycle {} = {}".format(cycle, expired))
            self.close_reservations(reservations=expired)

    def demand(self, *, rid: ID):
        if rid is None:
            raise Exception("Invalid arguments")
        reservation = self.get_reservation(rid=rid)
        if reservation is None:
            raise Exception("unknown reservation #{}".format(rid))

        self.policy.demand(reservation=reservation)
        reservation.set_policy(policy=self.policy)

    def donate_reservation(self, *, reservation: IClientReservation):
        self.policy.donate_reservation(reservation=reservation)

    def export(self, *, reservation: IBrokerReservation, resources: ResourceSet, term: Term, client: AuthToken) -> ID:
        if reservation is None:
            slice_object = SliceFactory.create(slice_id=ID(), name=client.get_name(), data=ResourceData())
            slice_object.set_client()
            reservation = BrokerReservationFactory.create(rid=ID(), resources=resources, term=term, slice_obj=slice_object)
            reservation.set_owner(owner=self.identity)

        self.wrapper.export(reservation=reservation, client=client)
        return reservation.get_reservation_id()

    def extend_ticket_client(self, *, reservation: IClientReservation):
        if not self.recovered:
            self.extending.add(reservation=reservation)
        else:
            self.wrapper.extend_ticket(reservation=reservation)

    def extend_tickets_client(self, *, rset: ReservationSet):
        for reservation in rset.values():
            try:
                if isinstance(reservation, IBrokerReservation):
                    self.extend_ticket_broker(reservation=reservation)
                elif isinstance(reservation, IClientReservation):
                    self.extend_ticket_client(reservation=reservation)
                else:
                    self.logger.warning("Reservation #{} cannot be ticketed".format(reservation.get_reservation_id()))
            except Exception as e:
                self.logger.error("Could not ticket for # {}".format(reservation.get_reservation_id()))

    def extend_ticket_broker(self, *, reservation: IBrokerReservation):
        if not self.recovered:
            self.extending.add(reservation=reservation)
        else:
            self.wrapper.extend_ticket_request(reservation=reservation, caller=reservation.get_client_auth_token(),
                                               compare_sequence_numbers=False)

    def extend_ticket(self, *, reservation: IReservation, caller: AuthToken):
        if not self.recovered or self.is_stopped():
            raise Exception("This actor cannot receive calls")
        self.wrapper.extend_ticket_request(reservation=reservation, caller=caller, compare_sequence_numbers=True)

    def get_broker(self, *, guid: ID) -> IBrokerProxy:
        return self.registry.get_broker(guid=guid)

    def get_brokers(self) -> list:
        return self.registry.get_brokers()

    def get_default_broker(self) -> IBrokerProxy:
        return self.registry.get_default_broker()

    def get_default_slice(self) -> ISlice:
        slice_list = self.get_inventory_slices()
        if slice_list is not None and len(slice_list) > 0:
            return slice_list[0]
        return None

    def initialize(self):
        if not self.initialized:
            super().initialize()
            self.registry.set_slices_plugin(plugin=self.plugin)
            self.registry.initialize()
            self.initialized = True

    def issue_delayed(self):
        super().issue_delayed()

        self.extend_tickets_client(rset=self.extending)
        self.extending.clear()

        self.tickets_client(rset=self.ticketing)
        self.ticketing.clear()

    def ticket_client(self, *, reservation: IClientReservation):
        if not self.recovered:
            self.ticketing.add(reservation=reservation)
        else:
            self.wrapper.ticket(reservation=reservation, destination=self)

    def tickets_client(self, *, rset: ReservationSet):
        for reservation in rset.values():
            try:
                if isinstance(reservation, IBrokerReservation):
                    self.ticket_broker(reservation=reservation)
                elif isinstance(reservation, IClientReservation):
                    self.ticket_client(reservation=reservation)
                else:
                    self.logger.warning("Reservation #{} cannot be ticketed".format(reservation.get_reservation_id()))
            except Exception as e:
                self.logger.error("Could not ticket for #{}".format(reservation.get_reservation_id()))

    def ticket_broker(self, *, reservation: IBrokerReservation):
        if not self.recovered:
            self.ticketing.add(reservation=reservation)
        else:
            self.wrapper.ticket_request(reservation=reservation, caller=reservation.get_client_auth_token(),
                                        callback=reservation.get_callback(), compare_seq_numbers=False)

    def ticket(self, *, reservation: IReservation, callback: IClientCallbackProxy, caller: AuthToken):
        if not self.is_recovered() or self.is_stopped():
            raise Exception("This actor cannot receive calls")

        self.wrapper.ticket_request(reservation=reservation, caller=caller, callback=callback, compare_seq_numbers=True)

    def relinquish(self, *, reservation: IReservation, caller: AuthToken):
        if not self.is_recovered() or self.is_stopped():
            raise Exception("This actor cannot receive calls")
        self.wrapper.relinquish_request(reservation=reservation, caller=caller)

    def tick_handler(self):
        self.policy.allocate(cycle=self.current_cycle)
        self.bid(cycle=self.current_cycle)
        self.close_expiring(cycle=self.current_cycle)

    def update_ticket(self, *, reservation: IReservation, update_data, caller: AuthToken):
        if not self.is_recovered() or self.is_stopped():
            raise Exception("This actor cannot receive calls")
        self.wrapper.update_ticket(reservation=reservation, update_data=update_data, caller=caller)

    def update_delegation(self, *, delegation: IDelegation, update_data, caller: AuthToken):
        if not self.is_recovered() or self.is_stopped():
            raise Exception("This actor cannot receive calls")
        self.wrapper.update_delegation(delegation=delegation, update_data=update_data, caller=caller)

    def register_client(self, *, client: Client):
        database = self.plugin.get_database()

        try:
            database.get_client(guid=client.get_guid())
        except Exception as e:
            raise Exception("Failed to check if client is present in the database {}".format(e))

        try:
            database.add_client(client=client)
        except Exception as e:
            raise Exception("Failed to add client to the database{}".format(e))

    def unregister_client(self, *, guid:ID):
        database = self.plugin.get_database()

        try:
            database.get_client(guid=guid)
        except Exception as e:
            raise Exception("Failed to check if client is present in the database {}".format(e))

        try:
            database.remove_client(guid=guid)
        except Exception as e:
            raise Exception("Failed to add client to the database{}".format(e))

    def get_client(self, *, guid: ID) -> Client:
        database = self.plugin.get_database()

        try:
            client_obj = database.get_client(guid=guid)
            return client_obj
        except Exception as e:
            raise Exception("Failed to check if client is present in the database {}".format(e))

        # TODO Restore

        return None

    def modify(self, *, reservation_id: ID, modify_properties: dict):
        return

    @staticmethod
    def get_management_object_class() -> str:
        return BrokerManagementObject.__name__

    @staticmethod
    def get_management_object_module() -> str:
        return BrokerManagementObject.__module__

    @staticmethod
    def get_kafka_service_class() -> str:
        return BrokerService.__name__

    @staticmethod
    def get_kafka_service_module() -> str:
        return BrokerService.__module__

    @staticmethod
    def get_mgmt_kafka_service_class() -> str:
        return KafkaBrokerService.__name__

    @staticmethod
    def get_mgmt_kafka_service_module() -> str:
        return KafkaBrokerService.__module__
