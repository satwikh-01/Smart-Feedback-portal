"use client";

import { useEffect, useState, useCallback } from "react";
import { useApi } from "@/hooks/use-api";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";
import { Feedback } from "@/types";
import { Card, CardContent, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Button } from "@/components/ui/button";
import { Separator } from "@/components/ui/separator";
import { saveAs } from 'file-saver';
import { Download, MessageSquarePlus } from "lucide-react";
import {
    Accordion,
    AccordionContent,
    AccordionItem,
    AccordionTrigger,
} from "@/components/ui/accordion";

export default function EmployeeDashboard() {
    const { apiFetch } = useApi();
    const [feedbackList, setFeedbackList] = useState<Feedback[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [isRequesting, setIsRequesting] = useState(false);

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

    const handleRequestFeedback = async () => {
        setIsRequesting(true);
        toast.info("Sending your request for feedback...");
        try {
            await apiFetch("/feedback/request", { method: 'POST' });
            toast.success("Your manager has been notified of your request.");
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || "Failed to request feedback.");
        } finally {
            setIsRequesting(false);
        }
    };

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
                <div className="flex items-center gap-2">
                    <Button onClick={handleRequestFeedback} disabled={isRequesting}>
                        <MessageSquarePlus className="mr-2 h-4 w-4" />
                        {isRequesting ? "Requesting..." : "Request Feedback"}
                    </Button>
                    <Button onClick={handleExportPdf} disabled={feedbackList.length === 0}>
                        <Download className="mr-2 h-4 w-4" />
                        Export as PDF
                    </Button>
                </div>
            </div>

            {feedbackList.length > 0 ? (
                <Accordion type="single" collapsible className="w-full">
                    {feedbackList.map((feedback) => (
                        <AccordionItem value={`item-${feedback.id}`} key={feedback.id}>
                            <AccordionTrigger>
                                <div className="flex justify-between items-center w-full pr-4">
                                    <div className="text-left">
                                        <p className="font-semibold">Feedback from {feedback.manager?.full_name || 'your manager'}</p>
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
                            </AccordionTrigger>
                            <AccordionContent>
                                <Card>
                                    <CardContent className="pt-6 space-y-4">
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
                            </AccordionContent>
                        </AccordionItem>
                    ))}
                </Accordion>
            ) : (
                <div className="text-center py-16 border-dashed border-2 rounded-lg">
                    <h3 className="text-xl font-semibold">No feedback yet</h3>
                    <p className="text-muted-foreground">Check back later for feedback from your manager.</p>
                </div>
            )}
        </div>
    );
}
