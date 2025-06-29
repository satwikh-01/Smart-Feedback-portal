"use client";

import { useEffect, useState, useCallback } from "react";
import { useApi } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";
import { User, Comment } from "@/types";
import { Card, CardContent, CardDescription, CardFooter, CardHeader, CardTitle } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import CommentSection from "./comment-section";
import { saveAs } from 'file-saver';
import { Download } from "lucide-react";

interface Feedback {
    id: number;
    strengths: string;
    areas_for_improvement: string;
    sentiment: 'positive' | 'neutral' | 'negative';
    acknowledged: boolean;
    created_at: string;
    manager: User;
    comments: Comment[];
}

export default function EmployeeDashboard() {
    const { apiFetch } = useApi();
    const [feedbackList, setFeedbackList] = useState<Feedback[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    const fetchFeedbackData = useCallback(async () => {
        try {
            setIsLoading(true);
            const data = await apiFetch("/feedback/");
            if (data) {
                setFeedbackList(data);
            }
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || "Failed to fetch feedback.");
        } finally {
            setIsLoading(false);
        }
    }, [apiFetch]);

    useEffect(() => {
        fetchFeedbackData();
    }, [fetchFeedbackData]);

    const handleExportPdf = async () => {
        toast.info("Generating your PDF report...");
        try {
            const blob = await apiFetch("/feedback/export/pdf", {}, 'blob');
            if (blob) {
                saveAs(blob, "feedback_report.pdf");
                toast.success("Report downloaded successfully.");
            }
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || "Failed to export PDF.");
        }
    }

    const handleAcknowledge = async (feedbackId: number) => {
        toast.info("Acknowledging feedback...");
        try {
            await apiFetch(`/feedback/${feedbackId}/acknowledge`, {
                method: 'PATCH',
            });
            setFeedbackList(currentFeedback =>
                currentFeedback.map(item =>
                    item.id === feedbackId ? { ...item, acknowledged: true } : item
                )
            );
            toast.success("Feedback acknowledged!");
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || "Failed to acknowledge feedback.");
        }
    };

    const handleCommentAdded = (feedbackId: number, newComment: Comment) => {
        setFeedbackList(currentList =>
            currentList.map(item =>
                item.id === feedbackId
                    ? { ...item, comments: [...item.comments, newComment] }
                    : item
            )
        );
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
            <div className="flex justify-between items-center">
                <div>
                    <h1 className="text-3xl font-bold">Your Feedback</h1>
                    <p className="text-muted-foreground">Here is a timeline of all the feedback you have received.</p>
                </div>
                <Button onClick={handleExportPdf} disabled={feedbackList.length === 0}>
                    <Download className="mr-2 h-4 w-4" />
                    Export as PDF
                </Button>
            </div>

            {feedbackList.length > 0 ? (
                <div className="space-y-4">
                    {feedbackList.map((feedback) => (
                        <Card key={feedback.id}>
                            <CardHeader>
                                <div className="flex justify-between items-start">
                                    <div>
                                        <CardTitle>Feedback from {feedback.manager.full_name}</CardTitle>
                                        <CardDescription>
                                            {new Date(feedback.created_at).toLocaleDateString('en-US', {
                                                year: 'numeric', month: 'long', day: 'numeric'
                                            })}
                                        </CardDescription>
                                    </div>
                                    <Badge variant={feedback.sentiment === 'positive' ? 'default' : feedback.sentiment === 'negative' ? 'destructive' : 'secondary'}>
                                        {feedback.sentiment}
                                    </Badge>
                                </div>
                            </CardHeader>
                            <CardContent className="space-y-4">
                                <div>
                                    <h4 className="font-semibold">Strengths</h4>
                                    <p className="text-muted-foreground">{feedback.strengths}</p>
                                </div>
                                <div>
                                    <h4 className="font-semibold">Areas for Improvement</h4>
                                    <p className="text-muted-foreground">{feedback.areas_for_improvement}</p>
                                </div>
                                <Separator />
                                <CommentSection
                                    feedbackId={feedback.id}
                                    initialComments={feedback.comments}
                                    onCommentAdded={(newComment) => handleCommentAdded(feedback.id, newComment)}
                                />
                            </CardContent>
                            <CardFooter className="flex justify-end items-center">
                                {!feedback.acknowledged ? (
                                    <Button onClick={() => handleAcknowledge(feedback.id)}>
                                        Acknowledge
                                    </Button>
                                ) : (
                                    <span className="text-sm text-muted-foreground">Acknowledged ✓</span>
                                )}
                            </CardFooter>
                        </Card>
                    ))}
                </div>
            ) : (
                <div className="text-center py-16 border-dashed border-2 rounded-lg">
                    <h3 className="text-xl font-semibold">No feedback yet</h3>
                    <p className="text-muted-foreground">Check back later for feedback from your manager.</p>
                </div>
            )}
        </div>
    );
}
