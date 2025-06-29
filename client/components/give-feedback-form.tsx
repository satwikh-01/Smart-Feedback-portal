"use client";

import { zodResolver } from "@hookform/resolvers/zod";
import { useForm } from "react-hook-form";
import * as z from "zod";
import { toast } from "sonner";
import { useState } from "react";
import { useApi } from "@/hooks/use-api";
import { Button } from "@/components/ui/button";
import {
    Form,
    FormControl,
    FormField,
    FormItem,
    FormLabel,
    FormMessage,
} from "@/components/ui/form";
import { Textarea } from "@/components/ui/textarea";
import { RadioGroup, RadioGroupItem } from "@/components/ui/radio-group";
import { Sparkles } from "lucide-react";
import { User } from "@/types";

const feedbackFormSchema = z.object({
    strengths: z.string().min(10, { message: "Please provide some detail on strengths." }),
    areas_for_improvement: z.string().min(10, { message: "Please provide some detail on areas for improvement." }),
    sentiment: z.enum(["positive", "neutral", "negative"], { required_error: "You must select a sentiment." }),
});

interface GiveFeedbackFormProps {
    employee: User;
    onFeedbackSubmitted: () => void;
    setOpen: (open: boolean) => void;
}

export default function GiveFeedbackForm({ employee, onFeedbackSubmitted, setOpen }: GiveFeedbackFormProps) {
    const { apiFetch } = useApi();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isAiLoading, setIsAiLoading] = useState(false);

    const form = useForm<z.infer<typeof feedbackFormSchema>>({
        resolver: zodResolver(feedbackFormSchema),
        defaultValues: {
            strengths: "",
            areas_for_improvement: "",
        }
    });

    const handleAiSuggest = async () => {
        setIsAiLoading(true);
        toast.info("Generating AI feedback suggestion...");
        try {
            const prompt = `Key points for feedback for ${employee.full_name}:`;
            const result = await apiFetch('/ai/suggest-feedback', {
                method: 'POST',
                body: JSON.stringify({ prompt }),
            });
            if (result) {
                form.setValue("strengths", result);
                toast.success("AI suggestion generated.");
            }
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || "Failed to get AI suggestion.");
        } finally {
            setIsAiLoading(false);
        }
    }

    async function onSubmit(values: z.infer<typeof feedbackFormSchema>) {
        setIsSubmitting(true);
        try {
            const feedbackData = {
                ...values,
                employee_id: employee.id,
            };
            await apiFetch('/feedback/', {
                method: 'POST',
                body: JSON.stringify(feedbackData),
            });
            toast.success(`Feedback for ${employee.full_name} has been submitted.`);
            onFeedbackSubmitted(); // This will trigger a data refresh on the dashboard
            setOpen(false); // Close the dialog
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || "Failed to submit feedback.");
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                <div>
                    <h3 className="text-lg font-medium">Feedback for {employee.full_name}</h3>
                    <p className="text-sm text-muted-foreground">
                        Provide structured feedback for your team member.
                    </p>
                </div>

                <FormField
                    control={form.control}
                    name="strengths"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Strengths</FormLabel>
                            <FormControl>
                                <Textarea
                                    placeholder="What are their key strengths and recent wins?"
                                    className="resize-none"
                                    {...field}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <FormField
                    control={form.control}
                    name="areas_for_improvement"
                    render={({ field }) => (
                        <FormItem>
                            <FormLabel>Areas for Improvement</FormLabel>
                            <FormControl>
                                <Textarea
                                    placeholder="What are some areas they can focus on developing?"
                                    className="resize-none"
                                    {...field}
                                />
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />
                <Button
                    type="button"
                    variant="outline"
                    size="sm"
                    disabled={isAiLoading}
                    onClick={handleAiSuggest}
                >
                    <Sparkles className="mr-2 h-4 w-4" />
                    {isAiLoading ? "Generating..." : "Suggest with AI"}
                </Button>

                <FormField
                    control={form.control}
                    name="sentiment"
                    render={({ field }) => (
                        <FormItem className="space-y-3">
                            <FormLabel>Overall Sentiment</FormLabel>
                            <FormControl>
                                <RadioGroup
                                    onValueChange={field.onChange}
                                    defaultValue={field.value}
                                    className="flex flex-col space-y-1"
                                >
                                    <FormItem className="flex items-center space-x-3 space-y-0">
                                        <FormControl>
                                            <RadioGroupItem value="positive" />
                                        </FormControl>
                                        <FormLabel className="font-normal">Positive</FormLabel>
                                    </FormItem>
                                    <FormItem className="flex items-center space-x-3 space-y-0">
                                        <FormControl>
                                            <RadioGroupItem value="neutral" />
                                        </FormControl>
                                        <FormLabel className="font-normal">Neutral</FormLabel>
                                    </FormItem>
                                    <FormItem className="flex items-center space-x-3 space-y-0">
                                        <FormControl>
                                            <RadioGroupItem value="negative" />
                                        </FormControl>
                                        <FormLabel className="font-normal">Negative</FormLabel>
                                    </FormItem>
                                </RadioGroup>
                            </FormControl>
                            <FormMessage />
                        </FormItem>
                    )}
                />

                <Button type="submit" disabled={isSubmitting} className="w-full">
                    {isSubmitting ? "Submitting..." : "Submit Feedback"}
                </Button>
            </form>
        </Form>
    );
}
