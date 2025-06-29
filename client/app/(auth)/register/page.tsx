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
    FormDescription,
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
import { Input } from "@/components/ui/input"
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card"
import { useAuth } from "@/context/auth-context"
import { useApi } from "@/hooks/use-api"

const formSchema = z.object({
    email: z.string().email(),
    full_name: z.string().min(2, { message: "Full name must be at least 2 characters." }),
    password: z.string().min(8, { message: "Password must be at least 8 characters." }),
    role: z.enum(["manager", "employee"]),
    team_name: z.string().optional(),
    team_id: z.coerce.number().optional(),
}).refine(data => {
    if (data.role === "manager") {
        return !!data.team_name && data.team_name.length > 0;
    }
    return true;
}, {
    message: "Team name is required for managers.",
    path: ["team_name"],
})
    .refine(data => {
        if (data.role === "employee") {
            return data.team_id !== undefined;
        }
        return true;
    }, {
        message: "Team selection is required for employees.",
        path: ["team_id"],
    });

export default function RegisterPage() {
    const { register } = useAuth();
    const { getTeams } = useApi();
    const [teams, setTeams] = useState<{ id: number; name: string }[]>([]);
    const [isSubmitting, setIsSubmitting] = useState(false);

    useEffect(() => {
        const fetchTeams = async () => {
            const fetchedTeams = await getTeams();
            setTeams(fetchedTeams);
        };
        fetchTeams();
    }, [getTeams]);


    const form = useForm<z.infer<typeof formSchema>>({
        resolver: zodResolver(formSchema),
        defaultValues: {
            email: "",
            full_name: "",
            password: "",
            role: "employee",
            team_name: "",
            team_id: undefined,
        },
    })

    const selectedRole = form.watch("role");

    async function onSubmit(values: z.infer<typeof formSchema>) {
        setIsSubmitting(true);
        toast.info("Attempting to create account...");
        await register(values);
        setIsSubmitting(false);
    }

    return (
        <div className="flex items-center justify-center min-h-screen py-8 bg-gray-100 dark:bg-gray-900">
            <Card className="w-full max-w-md">
                <CardHeader>
                    <CardTitle>Register</CardTitle>
                    <CardDescription>Create a new account to join the team.</CardDescription>
                </CardHeader>
                <CardContent>
                    <Form {...form}>
                        <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
                            <FormField
                                control={form.control}
                                name="full_name"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Full Name</FormLabel>
                                        <FormControl>
                                            <Input placeholder="John Doe" {...field} disabled={isSubmitting} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={form.control}
                                name="email"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Email</FormLabel>
                                        <FormControl>
                                            <Input placeholder="name@example.com" {...field} disabled={isSubmitting} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={form.control}
                                name="password"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Password</FormLabel>
                                        <FormControl>
                                            <Input type="password" placeholder="••••••••" {...field} disabled={isSubmitting} />
                                        </FormControl>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />
                            <FormField
                                control={form.control}
                                name="role"
                                render={({ field }) => (
                                    <FormItem>
                                        <FormLabel>Role</FormLabel>
                                        <Select onValueChange={field.onChange} defaultValue={field.value} disabled={isSubmitting}>
                                            <FormControl>
                                                <SelectTrigger>
                                                    <SelectValue placeholder="Select your role" />
                                                </SelectTrigger>
                                            </FormControl>
                                            <SelectContent>
                                                <SelectItem value="employee">Employee</SelectItem>
                                                <SelectItem value="manager">Manager</SelectItem>
                                            </SelectContent>
                                        </Select>
                                        <FormMessage />
                                    </FormItem>
                                )}
                            />

                            {selectedRole === 'manager' && (
                                <FormField
                                    control={form.control}
                                    name="team_name"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>New Team Name</FormLabel>
                                            <FormControl>
                                                <Input placeholder="e.g., Marketing Team" {...field} disabled={isSubmitting} />
                                            </FormControl>
                                            <FormDescription>As a manager, you will create and lead a new team.</FormDescription>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            )}

                            {selectedRole === 'employee' && (
                                <FormField
                                    control={form.control}
                                    name="team_id"
                                    render={({ field }) => (
                                        <FormItem>
                                            <FormLabel>Join a Team</FormLabel>
                                            <Select onValueChange={(value) => field.onChange(parseInt(value))} disabled={isSubmitting}>
                                                <FormControl>
                                                    <SelectTrigger>
                                                        <SelectValue placeholder="Select a team to join" />
                                                    </SelectTrigger>
                                                </FormControl>
                                                <SelectContent>
                                                    {teams.map(team => (
                                                        <SelectItem key={team.id} value={String(team.id)}>
                                                            {team.name}
                                                        </SelectItem>
                                                    ))}
                                                </SelectContent>
                                            </Select>
                                            <FormMessage />
                                        </FormItem>
                                    )}
                                />
                            )}

                            <Button type="submit" className="w-full" disabled={isSubmitting}>
                                {isSubmitting ? "Creating Account..." : "Create Account"}
                            </Button>
                        </form>
                    </Form>
                    <div className="mt-4 text-center text-sm">
                        Already have an account?{" "}
                        <Link href="/login" className="underline">
                            Login
                        </Link>
                    </div>
                </CardContent>
            </Card>
        </div>
    )
}
