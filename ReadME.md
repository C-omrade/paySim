# Payment and Transaction Processing Simulator

# Final Goal
A simulated payment platform with secure apis, transaction analytics, event-driven processing, and automated deployment

# Phase 1 -> Django Foundation 
Goal -> Build a payment backend before adding other services
Features to build
1. Merchant Registration records and simulated customer accounts
2. Create and retrieve payment transactions
3. Simulate payment success and failure
4. Track Payment status and timestamps
5. List and filter transactions
6. Create refunds as a later extension 

# Phase 2 -> Authentication and authorization
Goal -> Turn the API from an open application into a multi-merchant system
1. User authentication: login, logout, token valiation, jwt access, refresh tokens and password hashing
2. Let a merchent server call the payment api using a revocable key
3. Authorization 
seprate customer, merchant, and admin permissions.
One merchant should access his own details

# Phase 3 -> FastAPI for analytics and real time monitoring 
Goal -> Django remains responsible for core payment management. FastAPI provides analytics endpoints and a live transaction-monitoring interface 


flowchart TD
    C[Client] --> D[Django REST API]
    D --> P[(PostgreSQL)]
    C --> F[FastAPI Analytics API]
    F --> P
    F --> S[Analytics calculations]
    S --> C

# Phase 4 -> Message queues, and background processing
Goal: move slow or move independent work, out of the synchronous request path
Here comes the RabbitMQ and Celery 
Events to implement

- payment.created
- payment.processing
- payment.succeeded
- payment.failed
- refund.created
- refund.completed

Critical engineering concepts
- Retries with exponential backoff.
- Acknowledgements and dead-letter queues.
- Idempotent consumers that tolerate duplicate delivery.
- Transactional outbox for reliable event publication.
- Event IDs and correlation IDs for tracing.
- Monitoring queue depth and processing delays.

# Phase 5 — Financial correctness and resilience
Goal: Make the simulator behave like a robust financial system.
Add a double-entry ledger, refunds, idempotency, reconciliation, and concurrency testing.

# Phase 6 — Package everything with Docker
Goal: Make the whole project reproducible on another machine

# Phase 7 - CI/CD pipeline
Goal: Every code change is tested automatically and approved changes can be deployed consistently.