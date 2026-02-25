"use client";

import EmployeeForm from "@/components/EmployeeForm";
import EmployeeList from "@/components/EmployeeList";

export default function EmployeesPage() {
  return (
    <section>
      <h1>Employee Management</h1>
      <EmployeeForm />
      <EmployeeList />
    </section>
  );
}
