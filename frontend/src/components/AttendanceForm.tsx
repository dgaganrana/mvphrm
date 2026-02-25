"use client";

import { useState, ChangeEvent, FormEvent } from "react";
import Button from "@/components/UI/Button";
import Input from "@/components/UI/Input";
import { AttendanceFormData, AttendanceResponse } from "@/types/attendance";
import { markAttendance } from "@/lib/api";

export default function AttendanceForm() {
  const [form, setForm] = useState<AttendanceFormData>({
    employeeId: "",
    date: "",
    status: "Present",
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const handleChange = (e: ChangeEvent<HTMLInputElement | HTMLSelectElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      const data = await markAttendance({
        employee_id: Number(form.employeeId),
        date: form.date,
        status: form.status,
      });

      // Log response for debugging
      console.log("Attendance response:", data);
      
      const empId = data.employee_id;
      setMessage(
        `Attendance marked successfully for employee ${empId} on ${data.date}`
      );
      setForm({ employeeId: "", date: "", status: "Present" });
    } catch (err: any) {
      setMessage(err.message);
    } finally {
      setLoading(false);
    }
  };


  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Employee ID"
        name="employeeId"
        value={form.employeeId}
        onChange={handleChange}
        required
      />
      <Input
        label="Date"
        type="date"
        name="date"
        value={form.date}
        onChange={handleChange}
        required
      />
      <label className="block">
        Status:
        <select
          name="status"
          value={form.status}
          onChange={handleChange}
          className="ml-2 border rounded px-2 py-1"
        >
          <option value="Present">Present</option>
          <option value="Absent">Absent</option>
        </select>
      </label>
      <Button type="submit" disabled={loading}>
        {loading ? "Submitting..." : "Mark Attendance"}
      </Button>
      {message && <p className="mt-2 text-sm">{message}</p>}
    </form>
  );
}
