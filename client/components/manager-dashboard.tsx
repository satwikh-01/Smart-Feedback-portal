"use client";

import { useEffect, useState, useCallback } from "react";
import { useApi } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";
import { User } from "@/types";
import {
    Table,
    TableBody,
    TableCell,
    TableHead,
    TableHeader,
    TableRow,
} from "@/components/ui/table";
import {
    Dialog,
    DialogContent,
    DialogTrigger,
} from "@/components/ui/dialog";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import GiveFeedbackForm from "./give-feedback-form";
import { SentimentChart } from "./sentiment-chart";
import { Download, Users, MessageSquareText } from "lucide-react";
import { saveAs } from "file-saver";

interface TeamData {
    id: number;
    name: string;
    manager: User;
    members: User[];
}

interface Stat {
    sentiment: string;
    count: number;
}

export default function ManagerDashboard() {
    const { apiFetch } = useApi();
    const [team, setTeam] = useState<TeamData | null>(null);
    const [stats, setStats] = useState<Stat[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isDialogOpen, setIsDialogOpen] = useState(false);
    const [selectedEmployee, setSelectedEmployee] = useState<User | null>(null);

    const fetchData = useCallback(async () => {
        try {
            // Set loading to true only if it's the initial fetch
            if (!team) setIsLoading(true);

            const [teamData, statsData] = await Promise.all([
                apiFetch("/teams/me"),
                apiFetch("/teams/me/stats")
            ]);
            if (teamData) setTeam(teamData);
            if (statsData) setStats(statsData);
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || "Failed to fetch dashboard data.");
        } finally {
            setIsLoading(false);
        }
    }, [apiFetch, team]);

    useEffect(() => {
        fetchData();
    }, []);

    const handleGiveFeedbackClick = (employee: User) => {
        setSelectedEmployee(employee);
        setIsDialogOpen(true);
    };

    const handleExportPdf = async () => {
        toast.info("Generating your team's PDF report...");
        try {
            const blob = await apiFetch("/feedback/export/pdf", {}, 'blob');
            if (blob) {
                saveAs(blob, "team_feedback_report.pdf");
                toast.success("Report downloaded successfully.");
            }
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || "Failed to export PDF.");
        }
    }

    if (isLoading) {
        return (
            <div className="space-y-6">
                <Skeleton className="h-8 w-1/3 mb-2" />
                <Skeleton className="h-4 w-1/4 mb-8" />
                <div className="grid gap-4 md:grid-cols-2">
                    <Skeleton className="h-32 w-full" />
                    <Skeleton className="h-32 w-full" />
                </div>
                <div className="grid gap-4 md:grid-cols-7">
                    <Skeleton className="col-span-4 h-64 w-full" />
                    <Skeleton className="col-span-3 h-64 w-full" />
                </div>
            </div>
        );
    }

    if (!team) {
        return (
            <div>
                <h1 className="text-3xl font-bold">Manager Dashboard</h1>
                <p className="text-muted-foreground">You are not currently managing a team.</p>
            </div>
        );
    }

    const totalFeedback = stats.reduce((acc, curr) => acc + curr.count, 0);

    return (
        <div className="space-y-6">
            <div className="flex flex-col sm:flex-row justify-between sm:items-center gap-4">
                <div>
                    <h1 className="text-3xl font-bold">{team.name}</h1>
                    <p className="text-muted-foreground">Oversee your team&apos;s performance and feedback trends.</p>
                </div>
                <Button onClick={handleExportPdf} disabled={totalFeedback === 0}>
                    <Download className="mr-2 h-4 w-4" />
                    Export Report
                </Button>
            </div>

            <div className="grid gap-4 md:grid-cols-2">
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Team Size</CardTitle>
                        <Users className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{team.members.length} Members</div>
                    </CardContent>
                </Card>
                <Card>
                    <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
                        <CardTitle className="text-sm font-medium">Total Feedback</CardTitle>
                        <MessageSquareText className="h-4 w-4 text-muted-foreground" />
                    </CardHeader>
                    <CardContent>
                        <div className="text-2xl font-bold">{totalFeedback} Items Given</div>
                    </CardContent>
                </Card>
            </div>

            <div className="grid gap-4 lg:grid-cols-7">
                <Card className="lg:col-span-4">
                    <CardHeader>
                        <CardTitle>Team Members</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <Table>
                            <TableHeader>
                                <TableRow>
                                    <TableHead>Name</TableHead>
                                    <TableHead className="hidden sm:table-cell">Email</TableHead>
                                    <TableHead className="text-right">Actions</TableHead>
                                </TableRow>
                            </TableHeader>
                            <TableBody>
                                {team.members.length > 0 ? (
                                    team.members.map((member) => (
                                        <TableRow key={member.id}>
                                            <TableCell className="font-medium">{member.full_name}</TableCell>
                                            <TableCell className="hidden sm:table-cell">{member.email}</TableCell>
                                            <TableCell className="text-right">
                                                <Dialog open={isDialogOpen && selectedEmployee?.id === member.id} onOpenChange={(open) => {
                                                    if (!open) {
                                                        setSelectedEmployee(null);
                                                    }
                                                    setIsDialogOpen(open);
                                                }}>
                                                    <DialogTrigger asChild>
                                                        <Button variant="outline" size="sm" onClick={() => handleGiveFeedbackClick(member)}>
                                                            Give Feedback
                                                        </Button>
                                                    </DialogTrigger>
                                                    <DialogContent className="sm:max-w-md">
                                                        {selectedEmployee && (
                                                            <GiveFeedbackForm
                                                                employee={selectedEmployee}
                                                                onFeedbackSubmitted={fetchData}
                                                                setOpen={setIsDialogOpen}
                                                            />
                                                        )}
                                                    </DialogContent>
                                                </Dialog>
                                            </TableCell>
                                        </TableRow>
                                    ))
                                ) : (
                                    <TableRow>
                                        <TableCell colSpan={3} className="text-center">
                                            No members in this team yet.
                                        </TableCell>
                                    </TableRow>
                                )}
                            </TableBody>
                        </Table>
                    </CardContent>
                </Card>

                <Card className="lg:col-span-3">
                    <CardHeader>
                        <CardTitle>Sentiment Overview</CardTitle>
                    </CardHeader>
                    <CardContent>
                        {totalFeedback > 0 ? (
                            <SentimentChart data={stats} />
                        ) : (
                            <div className="flex items-center justify-center h-[350px]">
                                <p className="text-muted-foreground">No sentiment data yet.</p>
                            </div>
                        )}
                    </CardContent>
                </Card>
            </div>

        </div>
    );
}
