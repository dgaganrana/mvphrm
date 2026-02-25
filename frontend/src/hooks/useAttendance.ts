"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { AttendanceRecord, AttendanceResponse } from "@/types";
import { getAttendance, markAttendance as markAttendanceApi } from "@/lib/api";

export function useAttendance(employeeId: number) {
  const queryClient = useQueryClient();

  // Fetch attendance records
  const { data: attendance, isLoading, error } = useQuery<AttendanceRecord[]>({
    queryKey: ["attendance", employeeId],
    queryFn: () => getAttendance(employeeId),
    enabled: !!employeeId,
  });

  // Mark attendance
  const markAttendance = useMutation<
    AttendanceResponse,
    Error,
    { employee_id: number; date: string; status: string }
  >({
    mutationFn: markAttendanceApi,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["attendance", employeeId] }),
  });

  return { attendance, isLoading, error, markAttendance };
}
