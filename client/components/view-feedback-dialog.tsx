"use client";

import { useEffect, useState, useCallback } from "react";
import { useApi } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";
import { User, Feedback } from "@/types";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogTrigger } from "@/components/ui/dialog";
import GiveFeedbackForm from "./give-feedback-form";
import { Edit, Eye } from "lucide-react";

interface ViewFeedbackDialogProps {
    employee: User;
}

export default function ViewFeedbackDialog({ employee }: ViewFeedbackDialogProps) {
    const { apiFetch } = useApi();
    const [feedbackList, setFeedbackList] = useState<Feedback[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [editingFeedback, setEditingFeedback] = useState<Feedback | null>(null);
    const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);

    const fetchFeedbackData = useCallback(async () => {
        try {
            setIsLoading(true);
            const data = await apiFetch(`/feedback/`);
            if (data) {
                const employeeFeedback = data.filter((f: Feedback) => f.employee.id === employee.id);
                setFeedbackList(employeeFeedback);
            }
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || "Failed to fetch feedback.");
        } finally {
            setIsLoading(false);
        }
    }, [apiFetch, employee.id]);

    useEffect(() => {
        fetchFeedbackData();
    }, [fetchFeedbackData]);

    const handleEditFeedbackClick = (feedback: Feedback) => {
        setEditingFeedback(feedback);
        setIsEditDialogOpen(true);
    };

    if (isLoading) {
        return (
            <div className="space-y-4">
                <Skeleton className="h-8 w-1/3" />
                <Skeleton className="h-4 w-1/2" />
                <div className="space-y-4">
                    <Skeleton className="h-48 w-full" />
                    <Skeleton className="h-48 w-full" />
                </div>
            </div>
        );
    }

    return (
        <div className="space-y-6">
            <div>
                <h2 className="text-2xl font-bold">Feedback for {employee.full_name}</h2>
            </div>
            {feedbackList.length > 0 ? (
                <div className="space-y-4 max-h-[60vh] overflow-y-auto pr-4">
                    {feedbackList.map((feedback) => (
                        <Card key={feedback.id}>
                            <CardHeader>
                                <div className="flex justify-between items-start">
                                    <div>
                                        <CardTitle>Feedback from you</CardTitle>
                                        <p className="text-sm text-muted-foreground">
                                            {new Date(feedback.created_at).toLocaleDateString('en-US', {
                                                year: 'numeric', month: 'long', day: 'numeric'
                                            })}
                                        </p>
                                    </div>
                                    <Badge variant={feedback.sentiment === 'positive' ? 'default' : feedback.sentiment === 'negative' ? 'destructive' : 'secondary'}>
                                        {feedback.sentiment}
                                    </Badge>
                                </div>
                            </CardHeader>
                            <CardContent className="flex justify-end items-center gap-2">
                                <Dialog>
                                    <DialogTrigger asChild>
                                        <Button variant="outline" size="sm"><Eye className="mr-2 h-4 w-4" />View</Button>
                                    </DialogTrigger>
                                    <DialogContent className="sm:max-w-md">
                                        <div className="space-y-4">
                                            <div>
                                                <h4 className="font-semibold">Strengths</h4>
                                                <p className="text-muted-foreground">{feedback.strengths}</p>
                                            </div>
                                            <div>
                                                <h4 className="font-semibold">Areas for Improvement</h4>
                                                <p className="text-muted-foreground">{feedback.areas_for_improvement}</p>
                                            </div>
                                            <div>
                                                <h4 className="font-semibold">AI Generated Feedback</h4>
                                                <p className="text-muted-foreground">{feedback.feedback}</p>
                                            </div>
                                            <Separator />
                                        </div>
                                    </DialogContent>
                                </Dialog>
                                <Dialog open={isEditDialogOpen && editingFeedback?.id === feedback.id} onOpenChange={(open) => {
                                    if (!open) {
                                        setEditingFeedback(null);
                                    }
                                    setIsEditDialogOpen(open);
                                }}>
                                    <DialogTrigger asChild>
                                        <Button variant="outline" size="sm" onClick={() => handleEditFeedbackClick(feedback)}>
                                            <Edit className="mr-2 h-4 w-4" />
                                            Edit
                                        </Button>
                                    </DialogTrigger>
                                    <DialogContent className="sm:max-w-md">
                                        {editingFeedback && (
                                            <GiveFeedbackForm
                                                employee={editingFeedback.employee}
                                                onFeedbackSubmitted={fetchFeedbackData}
                                                setOpen={setIsEditDialogOpen}
                                                existingFeedback={editingFeedback}
                                            />
                                        )}
                                    </DialogContent>
                                </Dialog>
                            </CardContent>
                        </Card>
                    ))}
                </div>
            ) : (
                <div className="text-center py-16 border-dashed border-2 rounded-lg">
                    <h3 className="text-xl font-semibold">No feedback given yet</h3>
                    <p className="text-muted-foreground">Give feedback to this team member to see it here.</p>
                </div>
            )}
        </div>
    );
}
