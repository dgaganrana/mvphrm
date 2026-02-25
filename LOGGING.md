# Logging Architecture

This document describes the industry-standard logging setup for the MVPHRM project.

## Overview

The project implements structured JSON logging across both backend (FastAPI) and frontend (Next.js) to provide:
- **Structured context** for debugging and monitoring
- **Correlation IDs** to trace requests across services
- **Performance metrics** with request duration tracking
- **Centralized log aggregation** support

## Backend Logging (FastAPI)

### Setup

Located in `app/core/logging.py`, the backend uses:
- **python-json-logger**: Outputs logs in JSON format for easy parsing
- **Structured format**: All logs include timestamp, level, logger name, and custom context

### Configuration

Environment variables (in `.env`):
```bash
LOG_LEVEL=INFO           # DEBUG, INFO, WARNING, ERROR, CRITICAL
LOG_FORMAT=json          # json or text format
ENABLE_REQUEST_LOGGING=true
```

### Middleware

The `LoggingMiddleware` in `app/core/middleware.py`:
- Logs all HTTP requests with method, path, and query parameters
- Tracks request duration
- Generates/forwards correlation IDs (`X-Correlation-ID` header)
- Logs errors with full context

### Usage Examples

```python
from app.core.logging import app_logger, api_logger, db_logger

# Log different levels
app_logger.info("Application started")
api_logger.debug("Processing request", extra={"user_id": 123})
db_logger.error("Database connection failed", extra={"error": str(exc)})
```

### Log Structure

```json
{
  "timestamp": "2026-02-25T13:14:01.543Z",
  "level": "INFO",
  "logger": "mvphrm.api",
  "message": "Request completed",
  "correlation_id": "550e8400-e29b-41d4-a716-446655440000",
  "method": "GET",
  "path": "/employees/",
  "status_code": 200,
  "duration_ms": 42.5,
  "response_size": "1024"
}
```

## Frontend Logging (Next.js/React)

### Setup

Located in `src/lib/logger.ts`, the frontend uses:
- **Custom StructuredLogger**: Browser-compatible JSON logging
- **Session Storage**: Persists correlation ID across requests
- **Performance tracking**: Measures API request durations

### Configuration

Pass `minLevel` to constructor:
```typescript
const logger = new StructuredLogger("my.module", "debug"); // debug, info, warn, error
```

### Usage Examples

```typescript
import { appLogger, apiLogger, uiLogger } from "@/lib/logger";

// Log with context
appLogger.info("Component mounted", { component: "EmployeeList" });
apiLogger.debug("API request starting", { endpoint: "/employees/" });
uiLogger.warn("Form validation failed", { field: "email" });
```

### Correlation ID Tracking

Each frontend session gets a unique correlation ID:
```typescript
const correlationId = apiLogger.getCorrelationId();
// Use in API requests with X-Correlation-ID header
```

### Browser Console Output

Logs appear in browser console with structured format:
```
[INFO] mvphrm.api
{
  timestamp: "2026-02-25T13:14:01.543Z",
  level: "info",
  logger: "mvphrm.api",
  message: "API request completed",
  correlationId: "550e8400-e29b-41d4-a716-446655440000",
  method: "GET",
  endpoint: "/employees/",
  duration: 42.5
}
```

## API Integration

### Request/Response Flow

1. Frontend makes request with `X-Correlation-ID` header
2. Backend logs request with correlation ID
3. Backend processes and logs response/errors
4. Frontend logs success/failure with timing

### Available Loggers

**Backend:**
- `app_logger`: General application logs
- `api_logger`: HTTP request/response logs
- `db_logger`: Database operation logs (can be extended)

**Frontend:**
- `appLogger`: General application events
- `apiLogger`: API call logging
- `uiLogger`: UI component and interaction logs

## Best Practices

### Backend
1. Always include relevant context in `extra` parameter
2. Use appropriate log levels:
   - `DEBUG`: Detailed information for debugging
   - `INFO`: Important business events
   - `WARNING`: Potentially harmful situations
   - `ERROR`: Error events with stack traces
3. Log request IDs for traceability

### Frontend
1. Log API calls for debugging connectivity issues
2. Include correlation ID in all API requests
3. Log component lifecycle events in development
4. Use appropriate log levels to avoid noise in production

## Monitoring and Aggregation

The JSON log format enables easy integration with log aggregation services:
- **ELK Stack** (Elasticsearch, Logstash, Kibana)
- **Splunk**
- **DataDog**
- **New Relic**
- **CloudWatch** (AWS)

### Example Aggregation Setup

To send logs to aggregation service, add to:
1. Backend: Extend `LoggingMiddleware` with external handler
2. Frontend: Use `window.__sendLogs` to post logs to backend `/api/logs` endpoint

## Performance Considerations

- **Backend**: Minimal overhead with async logging
- **Frontend**: Logs sent asynchronously to avoid blocking UI
- **Correlation IDs**: Lightweight string tracking across requests
- **Production**: Adjust `LOG_LEVEL` to `INFO` or `WARNING` to reduce noise

## Troubleshooting

### No logs appearing
- Check `LOG_LEVEL` setting in `.env`
- Verify logger is initialized with `setup_logging()` (backend)
- Check browser console for frontend logs

### Missing correlation IDs
- Frontend generates on first request
- Verify `X-Correlation-ID` header is passed in requests
- Check middleware is added to FastAPI app

### Performance issues
- Reduce `LOG_LEVEL` to `INFO` or higher in production
- Implement log sampling for high-traffic endpoints
- Consider async log shipping to external service
