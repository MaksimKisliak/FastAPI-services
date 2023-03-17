"""
This script is responsible for processing payment and inventory related messages from Redis streams.
"""

from inventory.main import redis
import time


# Payment consumer setup
payment_key = 'refund_order'
payment_group = 'payment-group'
payment_consumer = 'payment-consumer'

# Inventory consumer setup
inventory_key = 'order_completed'
inventory_group = 'inventory-group'
inventory_consumer = 'inventory-consumer'


def create_group(stream_key, group_name):
    """
    Create a consumer group for a given stream.

    Args:
        stream_key (str): The Redis stream key.
        group_name (str): The name of the consumer group.

    Returns:
        None
    """
    try:
        redis.xgroup_create(stream_key, group_name, mkstream=True)
    except Exception as e:
        if "BUSYGROUP" not in str(e):
            print(f"Error creating group: {str(e)}")
        else:
            print('Group already exists!')


create_group(payment_key, payment_group)
create_group(inventory_key, inventory_group)


def read_stream(group, consumer, key):
    """
    Read messages from a Redis stream.

    Args:
        group (str): The name of the consumer group.
        consumer (str): The name of the consumer.
        key (str): The Redis stream key.

    Returns:
        list: A list of tuples, where each tuple represents a message.
    """
    while True:
        try:
            return redis.xreadgroup(group, consumer, streams={key: '>'}, count=1)
        except Exception as e:
            print(f"Error reading stream: {str(e)}")
            time.sleep(1)


def process_payment(results):
    """
    Process payment messages from the Redis stream.

    Args:
        results (list): A list of tuples, where each tuple represents a message.

    Returns:
        None
    """
    if not results:
        return

    for result in results:
        obj = result[1][0][1]
        try:
            order_pk = obj['pk']
            order_key = f':payment.main.Order:{order_pk}'
            order_data = redis.hgetall(order_key)
            if order_data:
                redis.hmset(order_key, {"status": str("refunded").encode()})
                print(f"Refunded order: {obj['pk']}")
                redis.xack(payment_key, payment_group, result[1][0][0])
        except Exception as e:
            print(f"Error refunding order: {str(e)}")


def process_inventory(results):
    """
    Process inventory messages from the Redis stream.

    Args:
        results (list): A list of tuples, where each tuple represents a message.

    Returns:
        None
    """
    if not results:
        return

    for result in results:
        obj = result[1][0][1]
        product_id = obj['product_id']
        product_key = f':inventory.main.Product:{product_id}'
        product_data = redis.hgetall(product_key)
        if product_data:
            quantity = int(obj['quantity'])
            product_quantity = int(product_data['quantity'])
            if product_quantity >= quantity:
                redis.hmset(product_key, {'quantity': str(product_quantity - quantity).encode()})
                print(f"Updated product: {product_id}")
                redis.xack(inventory_key, inventory_group, result[1][0][0])
            else:
                print(f"Insufficient inventory for product: {product_id}")
                redis.xadd('refund_order', obj, '*')
        else:
            print(f"Product not found with ID: {product_id}")
            redis.xadd('refund_order', obj, '*')


while True:
    payment_results = read_stream(payment_group, payment_consumer, payment_key)
    process_payment(payment_results)

    inventory_results = read_stream(inventory_group, inventory_consumer, inventory_key)
    process_inventory(inventory_results)

    time.sleep(1)


# This script has two main functions: `process_payment` and `process_inventory` that process payment
# and inventory related messages from Redis streams respectively. The `create_group` function is used
# to create a consumer group for a given stream. The `read_stream` function is used to read messages
# from a Redis stream.
#
# The script has the following variables:
# - `payment_key`: the key of the Redis stream where payment messages are sent.
# - `payment_group`: the name of the consumer group for payment messages.
# - `payment_consumer`: the name of the payment consumer.
# - `inventory_key`: the key of the Redis stream where inventory messages are sent.
# - `inventory_group`: the name of the consumer group for inventory messages.
# - `inventory_consumer`: the name of the inventory consumer.
#
# The `process_payment` function processes payment messages from the Redis stream. It loops through each message in
# the `results` list and refunds the corresponding order by setting its status to "refunded" in Redis. It then
# acknowledges the message by calling `redis.xack`.
#
# The `process_inventory` function processes inventory messages from the Redis stream. It loops through each message
# in the `results` list and updates the corresponding product's quantity in Redis if there is sufficient inventory.
# If there is not enough inventory, it adds the message to the `refund_order` stream by calling `redis.xadd`.
#
# The `read_stream` function continuously reads messages from a Redis stream. It returns a list of tuples,
# where each tuple represents a message. The `while` loop at the end of the script continuously reads payment and
# inventory messages from their respective streams using the `read_stream` function, and processes them using the
# `process_payment` and `process_inventory` functions, respectively. It then sleeps for 1 second before starting
# the loop again.
