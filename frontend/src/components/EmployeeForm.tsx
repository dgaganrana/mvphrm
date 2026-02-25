"use client";

import { useState, ChangeEvent, FormEvent } from "react";
import Button from "@/components/UI/Button";
import Input from "@/components/UI/Input";
import { createEmployee } from "@/lib/api";
import { Employee } from "@/types";

export default function EmployeeForm() {
  const [form, setForm] = useState<Omit<Employee, "id">>({
    name: "",
    email: "",
    department: "",
  });
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState<string | null>(null);

  const handleChange = (e: ChangeEvent<HTMLInputElement>) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e: FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setMessage(null);

    try {
      const data = await createEmployee(form);
      setMessage(`Employee ${data.name} added successfully!`);
      setForm({ name: "", email: "", department: "" });
    } catch (err: any) {
      setMessage(err.message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <Input
        label="Full Name"
        name="name"
        value={form.name}
        onChange={handleChange}
        required
      />
      <Input
        label="Email"
        type="email"
        name="email"
        value={form.email}
        onChange={handleChange}
        required
      />
      <Input
        label="Department"
        name="department"
        value={form.department}
        onChange={handleChange}
      />
      <Button type="submit" disabled={loading}>
        {loading ? "Submitting..." : "Add Employee"}
      </Button>
      {message && <p className="mt-2 text-sm">{message}</p>}
    </form>
  );
}
