from __future__ import absolute_import
from collections import namedtuple
import contextlib
from logging import getLogger

import pika.spec
from tornado import gen, locks

from .exchange import Exchange
from .message import IncomingMessage
from .common import BaseChannel
from . import tools
from .exceptions import QueueEmpty

LOGGER = getLogger(__name__)

ConsumerTag = str
DeclarationResult = namedtuple('DeclarationResult', ('message_count', 'consumer_count'))


class Queue(BaseChannel):
    """ AMQP queue abstraction """

    __slots__ = ('name', 'durable', 'exclusive', 'auto_delete', 'arguments', '_get_lock', '_channel', '__closing',
                 'declaration_result')

    def __init__(self, loop, future_store, channel, name, durable, exclusive, auto_delete, arguments):  # pylint: disable=too-many-arguments
        """
        :type loop: :class:`tornado.ioloop.IOLoop`
        :type future_store: :class:`topika.FutureStore`
        :type channel: :class:`pika.Channel`
        :type name: str
        :type durable: bool
        :type exclusive: bool
        :type auto_delete: bool
        :type arguments: dict
        """
        super(Queue, self).__init__(loop, future_store)

        self._channel = channel
        self.name = name or ''
        self.durable = durable
        self.exclusive = exclusive
        self.auto_delete = auto_delete
        self.arguments = arguments
        self.declaration_result = None  # type: DeclarationResult
        self._get_lock = locks.Lock()

    def __str__(self):
        return "%s" % self.name

    def __repr__(self):
        return "<Queue(%s): auto_delete=%s, durable=%s, exclusive=%s, arguments=%r>" % (
            self,
            self.auto_delete,
            self.durable,
            self.exclusive,
            self.arguments,
        )

    @BaseChannel._ensure_channel_is_open
    def declare(self, timeout=None, passive=False):
        """ Declare queue.

        :param timeout: execution timeout
        :type timeout: int
        :param passive: Only check to see if the queue exists.
        :type passive: bool
        :rtype: :class:`tornado.concurrent.Future`
        """

        LOGGER.debug("Declaring queue: %r", self)

        declare_future = self._create_future(timeout)

        self._channel.queue_declare(
            queue=self.name,
            passive=passive,
            durable=self.durable,
            exclusive=self.exclusive,
            auto_delete=self.auto_delete,
            arguments=self.arguments,
            callback=declare_future.set_result)

        def on_queue_declared(result):
            res = result.result()
            self.name = res.method.queue
            self.declaration_result = DeclarationResult(
                message_count=res.method.message_count,
                consumer_count=res.method.consumer_count,
            )

        declare_future.add_done_callback(on_queue_declared)

        return declare_future

    @BaseChannel._ensure_channel_is_open
    def bind(self, exchange, routing_key=None, arguments=None, timeout=None):
        """ A binding is a relationship between an exchange and a queue. This can be
        simply read as: the queue is interested in messages from this exchange.

        Bindings can take an extra routing_key parameter. To avoid the confusion
        with a basic_publish parameter we're going to call it a binding key.

        :param exchange: :class:`topika.exchange.Exchange` instance
        :type exchange: :class:`ExchangeType`
        :param routing_key: routing key
        :type routing_key: str
        :param arguments: additional arguments (will be passed to `pika`)
        :type arguments: dict or NoneType
        :param timeout: execution timeout
        :type timeout: int
        :raises tornado.gen.TimeoutError: when the binding timeout period has elapsed.
        :rtype: :class:`tornado.concurrent.Future`
        """
        LOGGER.debug("Binding queue %r: exchange=%r, routing_key=%r, arguments=%r", self, exchange, routing_key,
                     arguments)

        bind_future = self._create_future(timeout)

        self._channel.queue_bind(
            queue=self.name,
            exchange=Exchange._get_exchange_name(exchange),  # pylint: disable=protected-access
            routing_key=routing_key,
            arguments=arguments,
            callback=bind_future.set_result)

        return bind_future

    @BaseChannel._ensure_channel_is_open
    def unbind(self, exchange, routing_key, arguments=None, timeout=None):
        """ Remove binding from exchange for this :class:`Queue` instance

        :param exchange: :class:`topika.exchange.Exchange` instance
        :type exchange: :class:`ExchangeType`
        :param routing_key: routing key
        :type routing_key: str
        :param arguments: additional arguments (will be passed to `pika`)
        :type arguments: dict or NoneType
        :param timeout: execution timeout
        :type timeout: int
        :raises tornado.gen.TimeoutError: when the unbinding timeout period has elapsed.
        :rtype: :class:`tornado.concurrent.Future`
        """

        LOGGER.debug("Unbinding queue %r: exchange=%r, routing_key=%r, arguments=%r", self, exchange, routing_key,
                     arguments)

        unbind_future = self._create_future(timeout)

        self._channel.queue_unbind(
            queue=self.name,
            exchange=Exchange._get_exchange_name(exchange),  # pylint: disable=protected-access
            routing_key=routing_key,
            arguments=arguments,
            callback=unbind_future.set_result)

        return unbind_future

    @BaseChannel._ensure_channel_is_open
    @tools.coroutine
    def consume(self, callback, no_ack=False, exclusive=False, arguments=None, consumer_tag=None, timeout=None):  # pylint: disable=too-many-arguments
        """ Start to consuming the :class:`Queue`.

        :param timeout: :class:`tornado.gen.TimeoutError` will be raises when the
                        Future was not finished after this time.
        :param callback: Consuming callback. Could be a coroutine.
        :type callback: :class:`FunctionType`
        :param no_ack: if :class:`True` you don't need to call :func:`topika.message.IncomingMessage.ack`
        :type no_ack: bool
        :param exclusive: Makes this queue exclusive. Exclusive queues may only be accessed by the current
                          connection, and are deleted when that connection closes. Passive declaration of an
                          exclusive queue by other connections are not allowed.
        :type exclusive: bool
        :param arguments: extended arguments for pika
        :type arguments: Optional[dict]
        :param consumer_tag: optional consumer tag

        :raises tornado.gen.TimeoutError: when the consuming timeout period has elapsed.
        :rtype: class:`Generator[Any, None, ConsumerTag]`
        """

        LOGGER.debug("Start to consuming queue: %r", self)
        future = self._futures.create_future(timeout=timeout)

        def consumer(channel, envelope, properties, body):
            """
            :type channel: :class:`Channel`
            :type body: bytes
            """
            message = IncomingMessage(
                channel=channel,
                body=body,
                envelope=envelope,
                properties=properties,
                no_ack=no_ack,
            )

            if tools.iscoroutinepartial(callback):
                tools.create_task(callback(message))
            else:
                self.loop.add_callback(callback, message)

        consumer_tag = self._channel.basic_consume(
            queue=self.name,
            on_message_callback=consumer,
            auto_ack=no_ack,
            exclusive=exclusive,
            consumer_tag=consumer_tag,
            arguments=arguments,
            callback=future.set_result,
        )

        yield future

        raise gen.Return(consumer_tag)

    @BaseChannel._ensure_channel_is_open
    def cancel(self, consumer_tag, timeout=None):
        """ This method cancels a consumer. This does not affect already
        delivered messages, but it does mean the server will not send any more
        messages for that consumer. The client may receive an arbitrary number
        of messages in between sending the cancel method and receiving the
        cancel-ok reply. It may also be sent from the server to the client in
        the event of the consumer being unexpectedly cancelled (i.e. cancelled
        for any reason other than the server receiving the corresponding
        basic.cancel from the client). This allows clients to be notified of
        the loss of consumers due to events such as queue deletion.

        :param consumer_tag: consumer tag returned by :func:`~topika.Queue.consume`
        :type consumer_tag: :class:`ConsumerTag`
        :param timeout: execution timeout
        :type timeout: int or NoneType
        :return: Basic.CancelOk when operation completed successfully
        """
        cancel_future = self._create_future(timeout)
        self._channel.basic_cancel(consumer_tag=consumer_tag, callback=cancel_future.set_result)

        return cancel_future

    @BaseChannel._ensure_channel_is_open
    @gen.coroutine
    def get(self, no_ack=False, timeout=None, fail=True):
        """ Get message from the queue.

        :param no_ack: if :class:`True` you don't need to call
                       :func:`aio_pika.message.IncomingMessage.ack`
        :type no_ack: bool
        :param timeout: execution timeout
        :type timeout: int or NoneType
        :param fail: Should return :class:`None` instead of raise an
                     exception :class:`aio_pika.exceptions.QueueEmpty`.
        :type fail: bool
        :rtype: :class:`Generator[Any, None, Optional[IncomingMessage]]`
        """

        get_future = self._create_future(timeout)

        def _on_getempty(method_frame, *_a, **_kw):
            if fail:
                get_future.set_exception(QueueEmpty(method_frame))
            else:
                get_future.set_result(None)

        def _on_getok(channel, envelope, props, body):
            message = IncomingMessage(
                channel,
                envelope,
                props,
                body,
                no_ack=no_ack,
            )

            get_future.set_result(message)

        with (yield self._get_lock.acquire()), self._capture_empty(_on_getempty):
            LOGGER.debug("Awaiting message from queue: %r", self)

            self._channel.basic_get(queue=self.name, callback=_on_getok, auto_ack=no_ack)

            try:
                message = yield get_future
                raise gen.Return(message)
            finally:
                self._channel._on_getempty = None  # pylint: disable=protected-access

    @contextlib.contextmanager
    def _capture_empty(self, callback):
        """
        Capture an empty message from the queue.
        :param callback: The callback to call upon receiving the empty message
        """
        cancelled = False

        def callback_wrapper(frame):
            if not cancelled:
                callback(frame)

        self._channel.add_callback(callback_wrapper, (pika.spec.Basic.GetEmpty,), one_shot=True)
        try:
            yield
        finally:
            cancelled = True

    @BaseChannel._ensure_channel_is_open
    def purge(self, timeout=None):
        """ Purge all messages from the queue.

        :param timeout: execution timeout
        :rtype: :class:`tornado.concurrent.Future`
        """

        LOGGER.info("Purging queue: %r", self)

        purge_future = self._create_future(timeout)
        self._channel.queue_purge(queue=self.name, callback=purge_future.set_result)
        return purge_future

    @BaseChannel._ensure_channel_is_open
    def delete(self, if_unused=True, if_empty=True, timeout=None):
        """ Delete the queue.

        :param if_unused: Perform delete only when unused
        :param if_empty: Perform delete only when empty
        :param timeout: execution timeout
        :rtype: :class:`tornado.concurrent.Future`
        """

        LOGGER.info("Deleting %r", self)

        self._futures.reject_all(RuntimeError("Queue was deleted"))

        future = self._create_future(timeout)

        self._channel.queue_delete(queue=self.name, if_unused=if_unused, if_empty=if_empty, callback=future.set_result)

        return future

    # def __iter__(self) -> 'QueueIterator':
    #     """ Return the :class:`QueueIterator` which might be used with `async for` syntax
    #     before use it we are strongly recommended call :method:`set_qos` with argument `1`. """
    #     iterator = self.iterator()
    #     self.loop.add_callback(iterator.consume)
    #     return iterator
    #
    # @asyncio.coroutine
    # def __aiter__(self) -> 'QueueIterator':
    #     iterator = self.iterator()
    #     yield from iterator.consume()
    #     return iterator
    #
    # def iterator(self) -> 'QueueIterator':
    #     """ Returns an iterator for async for expression.
    #
    #     Full example:
    #
    #     .. code-block:: python
    #
    #         import aio_pika
    #
    #         async def main():
    #             connection = await aio_pika.connect()
    #
    #             async with connection:
    #                 channel = await connection.channel()
    #
    #                 queue = await channel.declare_queue('test')
    #
    #                 async with queue.iterator() as q:
    #                     async for message in q:
    #                         print(message.body)
    #
    #     When your program runs with run_forever the iterator will be closed
    #     in background. In this case the context processor for iterator might
    #     be skipped and the queue might be used in the "async for"
    #     expression directly.
    #
    #     .. code-block:: python
    #
    #         import aio_pika
    #
    #         async def main():
    #             connection = await aio_pika.connect()
    #
    #             async with connection:
    #                 channel = await connection.channel()
    #
    #                 queue = await channel.declare_queue('test')
    #
    #                 async for message in queue:
    #                     print(message.body)
    #
    #     :return: QueueIterator
    #     """
    #
    #     return QueueIterator(self)


#
# class QueueIterator:
#     def __init__(self, queue: Queue):
#         self._amqp_queue = queue
#         self._queue = asyncio.Queue(loop=self.loop)
#         self._consumer_tag = None
#
#     @property
#     def loop(self) -> asyncio.AbstractEventLoop:
#         return self._amqp_queue.loop
#
#     def on_message(self, message: IncomingMessage):
#         self._queue.put_nowait(message)
#
#     @asyncio.coroutine
#     def consume(self):
#         self._consumer_tag = yield from self._amqp_queue.consume(self.on_message)
#
#     @asyncio.coroutine
#     def _close(self):
#         yield from self._amqp_queue.cancel(self._consumer_tag)
#         self._consumer_tag = None
#
#         def get_msg():
#             try:
#                 return self._queue.get_nowait()
#             except asyncio.QueueEmpty:
#                 return
#
#         # Reject all messages
#         msg = get_msg()     # type: IncomingMessage
#         while msg:
#             msg.reject(requeue=True)
#             msg = get_msg()  # type: IncomingMessage
#
#     def close(self) -> asyncio.Future:
#         if not self._consumer_tag or self._amqp_queue._channel.is_closed:
#             f = asyncio.Future(loop=self.loop)
#             f.set_result(None)
#             return f
#
#         return self.loop.add_callback(self._close)
#
#     def __del__(self):
#         self.close()
#
#     def __iter__(self):
#         return self
#
#     __aiter__ = asyncio.coroutine(__iter__)
#
#     @asyncio.coroutine
#     def __next__(self) -> IncomingMessage:
#         try:
#             return (yield from self._queue.get())
#         except asyncio.CancelledError:
#             yield from self.close()
#             raise
#
#     @asyncio.coroutine
#     def __aenter__(self):
#         if self._consumer_tag is None:
#             yield from self.consume()
#         return self
#
#     @asyncio.coroutine
#     def __aexit__(self, exc_type, exc_val, exc_tb):
#         yield from self.close()
#
#     __anext__ = __next__

__all__ = 'Queue'
