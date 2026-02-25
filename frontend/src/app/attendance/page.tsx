"use client";

import AttendanceForm from "@/components/AttendanceForm";
import AttendanceTable from "@/components/AttendanceTable";

export default function AttendancePage() {
  return (
    <section>
      <h1>Attendance Records</h1>
      <AttendanceForm />
      <AttendanceTable />
    </section>
  );
}
