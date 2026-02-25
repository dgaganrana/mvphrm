"use client";

import { useQuery } from "@tanstack/react-query";
import Table from "@/components/UI/Table";
import { getAttendance } from "@/lib/api";
import { AttendanceRecord } from "@/types";

export default function AttendanceTable({ employeeId = 1 }: { employeeId?: number }) {
  const { data, isLoading, isError, error } = useQuery<AttendanceRecord[]>({
    queryKey: ["attendance", employeeId],
    queryFn: () => getAttendance(employeeId),
  });

  if (isLoading) return <p>Loading attendance records...</p>;
  if (isError) return <p>Error: {(error as Error).message}</p>;

  const records = data ?? [];

  return (
    <section>
      <h2 className="text-lg font-semibold mb-2">Attendance Records</h2>
      <Table
        headers={["ID", "Employee ID", "Date", "Status"]}
        rows={records.map((r) => [r.id, r.employeeId, r.date, r.status])}
      />
    </section>
  );
}
