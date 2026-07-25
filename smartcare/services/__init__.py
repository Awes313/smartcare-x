"""
Business logic layer. Functions here are intentionally decoupled from
request/response handling — they take plain arguments (or model instances)
and return plain data or model instances, so routes stay thin and this
logic is unit-testable without a request context.
"""
