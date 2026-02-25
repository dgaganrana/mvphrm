"use client";

import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { Employee } from "@/types";
import {
  listEmployees,
  createEmployee,
  deleteEmployee as deleteEmployeeApi,
} from "@/lib/api";

export function useEmployees() {
  const queryClient = useQueryClient();

  // Fetch employees
  const { data: employees, isLoading, error } = useQuery<Employee[]>({
    queryKey: ["employees"],
    queryFn: listEmployees,
  });

  // Add employee
  const addEmployee = useMutation<Employee, Error, Omit<Employee, "id">>({
    mutationFn: createEmployee,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["employees"] }),
  });

  // Delete employee
  const deleteEmployee = useMutation<void, Error, number>({
    mutationFn: deleteEmployeeApi,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: ["employees"] }),
  });

  return { employees, isLoading, error, addEmployee, deleteEmployee };
}
