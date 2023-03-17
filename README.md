<h1>FastAPI Microservices - Products and Orders</h1>
<p>This repository contains a sample FastAPI application that demonstrates how to implement microservices for products and orders, using Redis for data storage and message streaming. The project is based on the Microservices with FastAPI – Full Course from freecodecamp.org (https://www.freecodecamp.org/news/how-to-create-microservices-with-fastapi/). The code has been slightly simplified, and additional comments have been added for clarity. The Redis stream's <code>.get()</code> method was replaced with <code>.hgetall()</code> to resolve issues, which resulted in a "DeprecationWarning: Redis.hmset() is deprecated. Use Redis.hset() instead". No front-end implementation is included, as the focus is on understanding the microservices concept.</p>
<h2>Architecture</h2>
<p>The architecture consists of two main components:</p>
<ol>
  <li>A FastAPI application that exposes API endpoints for products and orders.</li>
  <li>A script that processes payment and inventory messages from Redis streams.</li>
</ol>
<p>The FastAPI application provides a RESTful API for managing products and orders, while the script is responsible for handling payment processing and inventory management through Redis streams.</p>
<h3>FastAPI Application</h3>
<p>The FastAPI application contains the following API endpoints:</p>
<ol>
  <li><code>/products</code>: Get all products.</li>
  <li><code>/products</code>: Create a new product.</li>
  <li><code>/products/{pk}</code>: Get a specific product by its primary key.</li>
  <li><code>/products/{pk}</code>: Delete a specific product by its primary key.</li>
  <li><code>/orders/{pk}</code>: Get a specific order by its primary key.</li>
  <li><code>/orders</code>: Create a new order.</li>
</ol>
<h3>Redis Stream Processing</h3>
<p>The Redis stream processing script processes payment and inventory messages from Redis streams. It consists of two main parts:</p>
<ol>
  <li>Payment processing: Refunds orders if necessary and updates order status.</li>
  <li>Inventory processing: Updates product quantities based on completed orders and creates refund messages if there is insufficient inventory.</li>
</ol>
<h2>Real-Life Examples and Improvement Opportunities</h2>
<p>This architecture pattern reflects a simplified real-life example of microservices in action. However, there are some potential conflicts and areas for improvement:</p>
<ol>
  <li><strong>Error Handling:</strong> The current implementation lacks robust error handling. Adding proper error handling and logging will improve the reliability and maintainability of the system.</li>
  <li><strong>Scalability:</strong> The current implementation uses a single Redis instance for both data storage and message streaming. To improve scalability, it's recommended to separate these concerns and use different instances or technologies for data storage and message streaming.</li>
  <li><strong>Data Consistency:</strong> The system relies on Redis streams for data consistency. However, it may be beneficial to implement a more robust solution, such as using a distributed transaction manager or an event sourcing pattern to ensure data consistency across services.</li>
     </ol>