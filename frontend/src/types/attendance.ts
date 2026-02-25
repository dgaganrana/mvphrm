export type AttendanceStatus = "Present" | "Absent";

export interface AttendanceRecord {
  id: number;
  employee_id: number;
  date: string; // ISO date string (YYYY-MM-DD)
  status: AttendanceStatus;
}

export interface AttendanceFormData {
  employeeId: string;
  date: string;
  status: AttendanceStatus;
}

export interface AttendanceResponse {
  id?: number;
  employee_id: number;
  date: string;
  status: AttendanceStatus;
}


