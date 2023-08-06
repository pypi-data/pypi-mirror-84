from __future__ import absolute_import
from tornado import gen
from enum import Enum, unique
from logging import getLogger
from typing import Optional, Union

from pika.channel import Channel
from .common import BaseChannel, FutureStore
from .message import Message
from .tools import create_future

log = getLogger(__name__)

ExchangeType_ = Union['Exchange', str]


@unique
class ExchangeType(Enum):
    FANOUT = 'fanout'
    DIRECT = 'direct'
    TOPIC = 'topic'
    HEADERS = 'headers'
    X_DELAYED_MESSAGE = 'x-delayed-message'
    X_CONSISTENT_HASH = 'x-consistent-hash'


class Exchange(BaseChannel):
    """ Exchange abstraction """

    __slots__ = ('name', '__type', '__publish_method', 'arguments', 'durable', 'auto_delete', 'internal', 'passive',
                 '_channel')

    def __init__(self,
                 loop,
                 future_store,
                 channel,
                 publish_method,
                 name=None,
                 type=ExchangeType.DIRECT,
                 passive=False,
                 durable=False,
                 auto_delete=False,
                 internal=False,
                 arguments=None):
        """
        :type loop: :class:`tornado.ioloop.IOLoop`
        :type future_store: :class:`FutureStore`
        :type channel: :class:`Channel`
        :type name: str
        :type type: ExchangeType
        :type auto_delete: Optional[bool]
        :type durable: Optional[bool]
        :type internal: Optional[bool]
        :type passive: Optional[bool]
        :type arguments: dict or NoneType
        """
        super(Exchange, self).__init__(loop, future_store)

        if not arguments:
            arguments = {}

        self._channel = channel
        self.__publish_method = publish_method
        self.__type = type.value
        self.name = name
        self.auto_delete = auto_delete
        self.durable = durable
        self.internal = internal
        self.passive = passive
        self.arguments = arguments

    def __str__(self):
        return self.name

    def __repr__(self):
        return "<Exchange(%s): auto_delete=%s, durable=%s, arguments=%r)>" % (self, self.auto_delete, self.durable,
                                                                              self.arguments)

    @BaseChannel._ensure_channel_is_open
    def declare(self, timeout=None):
        """
        :type timeout: int
        """
        future = self._create_future(timeout=timeout)

        self._channel.exchange_declare(
            exchange=self.name,
            exchange_type=self.__type,
            passive=self.passive,
            durable=self.durable,
            auto_delete=self.auto_delete,
            internal=self.internal,
            arguments=self.arguments,
            callback=future.set_result)

        return future

    @staticmethod
    def _get_exchange_name(exchange):
        """
        :type exchange: ExchangeType_
        """
        if isinstance(exchange, Exchange):
            return exchange.name
        elif isinstance(exchange, str):
            return exchange
        else:
            raise ValueError('exchange argument must be an exchange instance or str')

    @BaseChannel._ensure_channel_is_open
    def bind(self, exchange, routing_key='', arguments=None, timeout=None):
        """ A binding can also be a relationship between two exchanges. This can be
        simply read as: this exchange is interested in messages from another exchange.

        Bindings can take an extra routing_key parameter. To avoid the confusion
        with a basic_publish parameter we're going to call it a binding key.

        .. code-block:: python

            client = await connect()

            routing_key = 'simple_routing_key'
            src_exchange_name = "source_exchange"
            dest_exchange_name = "destination_exchange"

            channel = await client.channel()
            src_exchange = await channel.declare_exchange(src_exchange_name, auto_delete=True)
            dest_exchange = await channel.declare_exchange(dest_exchange_name, auto_delete=True)
            queue = await channel.declare_queue(auto_delete=True)

            await queue.bind(dest_exchange, routing_key)
            await dest_exchange.bind(src_exchange, routing_key)

        :param exchange: :class:`topika.exchange.Exchange` instance
        :type exchange: ExchangeType_
        :param routing_key: routing key
        :type routing_key: str
        :param arguments: additional arguments (will be passed to `pika`)
        :param timeout: execution timeout
        :type timeout: int
        :rtype: :class:`tornado.concurrent.Future`
        """

        log.debug("Binding exchange %r to exchange %r, routing_key=%r, arguments=%r", self, exchange, routing_key,
                  arguments)

        f = self._create_future(timeout)

        self._channel.exchange_bind(
            destination=self.name,
            source=self._get_exchange_name(exchange),
            routing_key=routing_key,
            arguments=arguments,
            callback=f.set_result,
        )

        return f

    @BaseChannel._ensure_channel_is_open
    def unbind(self, exchange, routing_key='', arguments=None, timeout=None):
        """ Remove exchange-to-exchange binding for this :class:`Exchange` instance

        :param exchange: :class:`topika.exchange.Exchange` instance
        :type exchange: ExchangeType_
        :param routing_key: routing key
        :type routing_key: str
        :param arguments: additional arguments (will be passed to `pika`)
        :type arguments: dict
        :param timeout: execution timeout
        :type timeout: int
        :rtype: :class:`tornado.concurrent.Future`
        """

        log.debug("Unbinding exchange %r from exchange %r, routing_key=%r, arguments=%r", self, exchange, routing_key,
                  arguments)

        f = self._create_future(timeout)

        self._channel.exchange_unbind(
            destination=self.name,
            source=self._get_exchange_name(exchange),
            routing_key=routing_key,
            arguments=arguments,
            callback=f.set_result,
        )

        return f

    @BaseChannel._ensure_channel_is_open
    @gen.coroutine
    def publish(self, message, routing_key, mandatory=True):
        """ Publish the message to the queue. `topika` use `publisher confirms`_
        extension for message delivery.

        .. _publisher confirms: https://www.rabbitmq.com/confirms.html

        :type message: :class:`Message`
        """

        log.debug("Publishing message via exchange %s: %r", self, message)
        if self.internal:
            # Caught on the client side to prevent channel closure
            raise ValueError("cannot publish to internal exchange: '%s'!" % self.name)

        raise gen.Return((yield self.__publish_method(
            self.name,
            routing_key,
            message.body,
            properties=message.properties,
            mandatory=mandatory)))

    @BaseChannel._ensure_channel_is_open
    def delete(self, if_unused=False):
        """ Delete the queue

        :param if_unused: perform deletion when queue has no bindings.
        :rtype: :class:`tornado.concurrent.Future`
        """
        log.info("Deleting %r", self)
        self._futures.reject_all(RuntimeError("Exchange was deleted"))
        future = create_future(loop=self.loop)
        self._channel.exchange_delete(exchange=self.name, if_unused=if_unused, callback=future.set_result)
        return future


__all__ = ('Exchange',)
