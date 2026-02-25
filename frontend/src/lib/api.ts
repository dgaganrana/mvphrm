import { AttendanceResponse } from "@/types";
import { Employee } from "@/types";
import { AttendanceRecord } from "@/types";
import { apiLogger } from "./logger";

// Get BASE_URL at function call time (runtime) instead of module load time
function getBaseUrl(): string {
  const url = process.env.NEXT_PUBLIC_BACKEND_URL || 
    (typeof window !== "undefined" ? window.location.origin : "");
  
  if (!url) {
    throw new Error(
      "Backend URL is not configured. Set NEXT_PUBLIC_BACKEND_URL environment variable."
    );
  }
  
  return url;
}

async function request<T>(endpoint: string, options: RequestInit = {}): Promise<T> {
  const BASE_URL = getBaseUrl();
  const correlationId = apiLogger.getCorrelationId();
  const startTime = performance.now();
  const url = `${BASE_URL}${endpoint}`;

  apiLogger.debug(`API request starting`, {
    method: options.method || "GET",
    endpoint,
    correlationId,
  });

  try {
    const res = await fetch(url, {
      headers: {
        "Content-Type": "application/json",
        "X-Correlation-ID": correlationId,
      },
      ...options,
    });

    const duration = performance.now() - startTime;

    if (!res.ok) {
      const error = await res.json().catch(() => ({}));
      const errorMessage = error.detail || `API request failed with status ${res.status}`;
      
      apiLogger.error(`API request failed`, {
        method: options.method || "GET",
        endpoint,
        statusCode: res.status,
        duration,
        error: errorMessage,
      });
      
      throw new Error(errorMessage);
    }

    const data = await res.json();

    apiLogger.debug(`API request completed`, {
      method: options.method || "GET",
      endpoint,
      statusCode: res.status,
      duration,
    });

    return data;
  } catch (error) {
    const duration = performance.now() - startTime;
    apiLogger.error(`API request error`, {
      method: options.method || "GET",
      endpoint,
      duration,
      error: error instanceof Error ? error.message : String(error),
    });
    throw error;
  }
}

// Attendance APIs
export async function markAttendance(
  data: { employee_id: number; date: string; status: string }
): Promise<AttendanceResponse> {
  return request<AttendanceResponse>("/attendance/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function getAttendance(employeeId: number): Promise<AttendanceRecord[]> {
  return request<AttendanceRecord[]>(`/attendance/${employeeId}`, {
    method: "GET",
  });
}

// Employee APIs
export async function createEmployee(data: Omit<Employee, "id">): Promise<Employee> {
  return request<Employee>("/employees/", {
    method: "POST",
    body: JSON.stringify(data),
  });
}

export async function listEmployees(): Promise<Employee[]> {
  return request<Employee[]>("/employees/", { method: "GET" });
}

export async function getEmployee(id: number): Promise<Employee> {
  return request<Employee>(`/employees/${id}`, { method: "GET" });
}

export async function updateEmployee(id: number, data: Omit<Employee, "id">): Promise<Employee> {
  return request<Employee>(`/employees/${id}`, {
    method: "PUT",
    body: JSON.stringify(data),
  });
}

export async function deleteEmployee(id: number): Promise<void> {
  await request<void>(`/employees/${id}`, { method: "DELETE" });
}
