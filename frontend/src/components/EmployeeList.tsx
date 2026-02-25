"use client";

import { useQuery } from "@tanstack/react-query";
import Table from "@/components/UI/Table";
import { listEmployees } from "@/lib/api";
import { Employee } from "@/types";

export default function EmployeeList() {
  const { data, isLoading, isError, error } = useQuery<Employee[]>({
    queryKey: ["employees"],
    queryFn: listEmployees,
  });

  if (isLoading) return <p>Loading employees...</p>;
  if (isError) return <p>Error: {(error as Error).message}</p>;

  const employees = data ?? [];

  return (
    <section>
      <h2 className="text-lg font-semibold mb-2">Employee List</h2>
      <Table
        headers={["ID", "Name", "Email", "Department"]}
        rows={employees.map((e) => [e.id, e.name, e.email, e.department])}
      />
    </section>
  );
}
