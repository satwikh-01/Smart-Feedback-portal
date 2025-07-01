"use client"

import { zodResolver } from "@hookform/resolvers/zod"
import { useForm } from "react-hook-form"
import * as z from "zod"
import Link from "next/link"
import React, { useState, useEffect } from "react"
import { toast } from "sonner"

import { Button } from "@/components/ui/button"
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form"
import {
    Select,
    SelectContent,
    SelectItem,
    SelectTrigger,
    SelectValue,
} from "@/components/ui/select"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useApi } from "@/hooks/use-api"
import { User } from "@/types"

const formSchema = z.object({
    employee_id: z.coerce.number(),
});

export default function AddEmployeePage() {
    const { apiFetch } = useApi();
    const [employees, setEmployees] = useState<User[]>([]);
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        const fetchEmployees = async () => {
            const fetchedEmployees = await apiFetch("/users/employees");
            setEmployees(fetchedEmployees);
        };
        fetchEmployees();
    }, [apiFetch]);


    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            employee_id: undefined,
        },
    })

    async function onSubmit(values: z.infer<typeof formSchema>) {
        setIsSubmitting(true);
        toast.info("Adding employee to your team...");
        try {
            await apiFetch(`/teams/me/members/${values.employee_id}`, {
                method: 'POST',
            });
            toast.success("Employee added successfully!");
            form.reset();
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || "Failed to add employee.");
        }
        setIsSubmitting(false);
    }

    return (
        <div className="flex items-center justify-center min-h-screen py-8 bg-gray-100 dark:bg-gray-900">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle>Add Employee</CardTitle>
                    <CardDescription>Select an employee to add to your team.</CardDescription>
                </CardHeader>
                <CardContent>
                    <Form {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                            <FormField
                                control={form.control}
                                name="employee_id"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Select Employee</FormLabel>
                                        <Select onValueChange={(value) => field.onChange(parseInt(value))} disabled={isSubmitting}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select an employee to add" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                {employees.map(employee => (
                                                    <SelectItem key={employee.id} value={String(employee.id)}>
                                                        {employee.full_name} ({employee.email})
                                                    </SelectItem>
                                                ))}
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            <Button type="submit" className="w-full" disabled={isSubmitting}>
                                {isSubmitting ? "Adding Employee..." : "Add Employee"}
                            </Button>
                        </form>
                    </Form>
                    <div className="mt-4 text-center text-sm">
                        <Link href="/" className="underline">
                            Back to Dashboard
                        </Link>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
