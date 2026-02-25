/**
 * Browser-based logger with structured JSON logging
 */

// Extend Window interface for custom properties
declare global {
  interface Window {
    __sendLogs?: boolean;
  }
}

type LogLevel = "debug" | "info" | "warn" | "error";

interface LogEntry {
  timestamp: string;
  level: LogLevel;
  logger: string;
  message: string;
  [key: string]: any;
}

const LOG_LEVEL_PRIORITY: Record<LogLevel, number> = {
  debug: 0,
  info: 1,
  warn: 2,
  error: 3,
};

class StructuredLogger {
  private name: string;
  private minLevel: LogLevel;
  private correlationId: string;

  constructor(name: string, minLevel: LogLevel = "info") {
    this.name = name;
    this.minLevel = minLevel;
    // Generate or get correlation ID from session storage
    this.correlationId =
      typeof window !== "undefined"
        ? sessionStorage.getItem("correlation-id") ||
          this.generateCorrelationId()
        : this.generateCorrelationId();
    if (typeof window !== "undefined") {
      sessionStorage.setItem("correlation-id", this.correlationId);
    }
  }

  private generateCorrelationId(): string {
    return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
  }

  private log(
    level: LogLevel,
    message: string,
    context?: Record<string, any>
  ): void {
    // Skip if level is below minimum
    if (
      LOG_LEVEL_PRIORITY[level] < LOG_LEVEL_PRIORITY[this.minLevel]
    ) {
      return;
    }

    const entry: LogEntry = {
      timestamp: new Date().toISOString(),
      level,
      logger: this.name,
      message,
      correlationId: this.correlationId,
      ...context,
    };

    // Send to console with appropriate method
    const consoleMethod: "log" | "debug" | "warn" | "error" = 
      level === "warn" ? "warn" : 
      level === "error" ? "error" : 
      level === "debug" ? "debug" : 
      "log";
    
    (console[consoleMethod] as any)(
      `[${entry.level.toUpperCase()}] ${entry.logger}`,
      entry
    );

    // Send to backend if provided
    if (typeof window !== "undefined" && window.__sendLogs) {
      this.sendToBackend(entry);
    }
  }

  private sendToBackend(entry: LogEntry): void {
    // Send logs asynchronously without blocking the application
    fetch("/api/logs", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(entry),
    }).catch(() => {
      // Fail silently to not impact application
    });
  }

  debug(message: string, context?: Record<string, any>): void {
    this.log("debug", message, context);
  }

  info(message: string, context?: Record<string, any>): void {
    this.log("info", message, context);
  }

  warn(message: string, context?: Record<string, any>): void {
    this.log("warn", message, context);
  }

  error(message: string, context?: Record<string, any>): void {
    this.log("error", message, context);
  }

  getCorrelationId(): string {
    return this.correlationId;
  }
}

// Export singleton instances
export const appLogger = new StructuredLogger("mvphrm.app");
export const apiLogger = new StructuredLogger("mvphrm.api");
export const uiLogger = new StructuredLogger("mvphrm.ui");

export default StructuredLogger;
