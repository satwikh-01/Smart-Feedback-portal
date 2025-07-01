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
import { Sparkles } from "lucide-react";
import { User, Feedback } from "@/types";
import { useEffect } from "react";

const feedbackFormSchema = z.object({
    strengths: z.string().optional(),
    areas_for_improvement: z.string().optional(),
    feedback: z.string().min(1, { message: "Please enter or generate feedback before submitting." }),
    sentiment: z.enum(["positive", "neutral", "negative"]),
    tag_ids: z.array(z.number()).optional(),
});

interface GiveFeedbackFormProps {
    employee: User;
    onFeedbackSubmitted: () => void;
    setOpen: (open: boolean) => void;
    existingFeedback?: Feedback;
}

export default function GiveFeedbackForm({ employee, onFeedbackSubmitted, setOpen, existingFeedback }: GiveFeedbackFormProps) {
    const { apiFetch } = useApi();
    const [isSubmitting, setIsSubmitting] = useState(false);
    const [isAiLoading, setIsAiLoading] = useState(false);

    const form = useForm<z.infer<typeof feedbackFormSchema>>({
        resolver: zodResolver(feedbackFormSchema),
        defaultValues: {
            strengths: existingFeedback?.strengths || "",
            areas_for_improvement: existingFeedback?.areas_for_improvement || "",
            feedback: existingFeedback?.feedback || "",
            sentiment: existingFeedback?.sentiment,
            tag_ids: existingFeedback?.tags.map(t => t.id) || [],
        },
        mode: "onChange",
    });

    useEffect(() => {
        if (existingFeedback) {
            form.reset({
                strengths: existingFeedback.strengths || "",
                areas_for_improvement: existingFeedback.areas_for_improvement || "",
                feedback: existingFeedback.feedback || "",
                sentiment: existingFeedback.sentiment,
                tag_ids: existingFeedback.tags.map(t => t.id) || [],
            });
        }
    }, [existingFeedback, form]);

    const handleGenerateAiFeedback = async () => {
        const strengths = form.getValues("strengths");
        const areas = form.getValues("areas_for_improvement");

        if (!strengths && !areas) {
            toast.warning("Please provide strengths or areas for improvement to generate feedback.");
            return;
        }

        setIsAiLoading(true);
        toast.info("Generating AI feedback...");
        try {
            const result = await apiFetch('/ai/generate-feedback', {
                method: 'POST',
                body: JSON.stringify({ strengths, areas_for_improvement: areas }),
            });

            if (result) {
                form.setValue("feedback", result.feedback, { shouldValidate: true });
                form.setValue("sentiment", result.sentiment, { shouldValidate: true });
                form.setValue("tag_ids", result.tag_ids);
                toast.success("AI feedback generated successfully.");
            }
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || "Failed to generate AI feedback.");
        } finally {
            setIsAiLoading(false);
        }
    };

    async function onSubmit(values: z.infer<typeof feedbackFormSchema>) {
        setIsSubmitting(true);
        const { strengths, areas_for_improvement, feedback, sentiment, tag_ids } = values;
        const payload = {
            strengths,
            areas_for_improvement,
            feedback,
            sentiment,
            tag_ids,
            employee_id: employee.id,
        };

        const url = existingFeedback ? `/feedback/${existingFeedback.id}` : '/feedback/';
        const method = existingFeedback ? 'PUT' : 'POST';

        if (existingFeedback) {
            if (payload.strengths && payload.strengths.trim() === '') {
                payload.strengths = undefined;
            }
            if (payload.areas_for_improvement && payload.areas_for_improvement.trim() === '') {
                payload.areas_for_improvement = undefined;
            }
        }

        try {
            await apiFetch(url, {
                method: method,
                body: JSON.stringify(payload),
            });
            toast.success(`Feedback for ${employee.full_name} has been ${existingFeedback ? 'updated' : 'submitted'}.`);
            onFeedbackSubmitted();
            setOpen(false);
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || `Failed to ${existingFeedback ? 'update' : 'submit'} feedback.`);
        } finally {
            setIsSubmitting(false);
        }
    }

    return (
        <Form {...form}>
            <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-6">
                <div>
                    <h3 className="text-lg font-medium">
                        {existingFeedback ? "Edit Feedback for" : "Feedback for"} {employee.full_name}
                    </h3>
                    <p className="text-sm text-muted-foreground">
                        {existingFeedback ? "Update the feedback details below." : "Provide structured feedback for your team member."}
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

                {!existingFeedback && (
                    <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        disabled={isAiLoading}
                        onClick={handleGenerateAiFeedback}
                        className="w-full"
                    >
                        <Sparkles className="mr-2 h-4 w-4" />
                        {isAiLoading ? "Generating..." : "Generate with AI"}
                    </Button>
                )}

                {form.watch("feedback") && (
                    <FormField
                        control={form.control}
                        name="feedback"
                        render={({ field }) => (
                            <FormItem>
                                <FormLabel>Generated Feedback</FormLabel>
                                <FormControl>
                                    <Textarea
                                        placeholder="AI-generated feedback will appear here."
                                        className="resize-none h-32"
                                        {...field}
                                    />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                )}

                <Button type="submit" disabled={isSubmitting || !form.formState.isValid} className="w-full">
                    {isSubmitting ? (existingFeedback ? "Updating..." : "Submitting...") : (existingFeedback ? "Update Feedback" : "Submit Feedback")}
                </Button>
            </form>
        </Form>
    );
}
