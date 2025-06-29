"use client";

import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import * as z from "zod";
import { useApi } from "@/hooks/use-api";
import { Comment } from "@/types";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { Form, FormControl, FormField, FormItem, FormMessage } from "@/components/ui/form";
import { toast } from "sonner";
import { Sparkles } from "lucide-react";

const commentFormSchema = z.object({
    content: z.string().min(1, "Comment cannot be empty."),
});

interface CommentSectionProps {
    feedbackId: number;
    initialComments: Comment[];
    onCommentAdded: (newComment: Comment) => void;
}

export default function CommentSection({ feedbackId, initialComments, onCommentAdded }: CommentSectionProps) {
    const { apiFetch } = useApi();
    const [comments, setComments] = useState<Comment[]>(initialComments);
    const [isAiLoading, setIsAiLoading] = useState(false);

    const form = useForm<z.infer<typeof commentFormSchema>>({
        resolver: zodResolver(commentFormSchema),
        defaultValues: { content: "" },
    });

    const handleRephrase = async () => {
        const content = form.getValues("content");
        if (!content) {
            toast.error("Please write a comment to rephrase.");
            return;
        }
        setIsAiLoading(true);
        toast.info("Rephrasing your comment with AI...");
        try {
            const result = await apiFetch('/ai/rephrase', {
                method: 'POST',
                body: JSON.stringify({ text: content }),
            });
            if (result) {
                form.setValue("content", result);
                toast.success("Comment rephrased!");
            }
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || "Failed to rephrase comment.");
        } finally {
            setIsAiLoading(false);
        }
    };

    async function onSubmit(values: z.infer<typeof commentFormSchema>) {
        try {
            const newComment = await apiFetch(`/feedback/${feedbackId}/comments`, {
                method: 'POST',
                body: JSON.stringify(values),
            });
            if (newComment) {
                setComments(prev => [...prev, newComment]);
                onCommentAdded(newComment);
                form.reset();
                toast.success("Comment posted.");
            }
        } catch (error) {
            const e = error as Error;
            toast.error(e.message || "Failed to post comment.");
        }
    }

    return (
        <div className="pt-4 space-y-4">
            <h4 className="font-semibold text-lg">Discussion</h4>
            <div className="space-y-4">
                {comments.map((comment) => (
                    <div key={comment.id} className="flex items-start space-x-3">
                        <Avatar className="h-8 w-8">
                            <AvatarFallback>{comment.user.full_name?.charAt(0).toUpperCase()}</AvatarFallback>
                        </Avatar>
                        <div className="flex-1">
                            <p className="text-sm font-semibold">{comment.user.full_name}</p>
                            <p className="text-sm text-muted-foreground">{comment.content}</p>
                            <p className="text-xs text-muted-foreground/70">
                                {new Date(comment.created_at).toLocaleDateString()}
                            </p>
                        </div>
                    </div>
                ))}
            </div>
            <Form {...form}>
                <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-2">
                    <FormField
                        control={form.control}
                        name="content"
                        render={({ field }) => (
                            <FormItem>
                                <FormControl>
                                    <Textarea placeholder="Write a comment..." {...field} />
                                </FormControl>
                                <FormMessage />
                            </FormItem>
                        )}
                    />
                    <div className="flex justify-between items-center">
                        <Button
                            type="button"
                            variant="ghost"
                            size="sm"
                            onClick={handleRephrase}
                            disabled={isAiLoading}>
                            <Sparkles className="mr-2 h-4 w-4" />
                            {isAiLoading ? "Rephrasing..." : "Rephrase"}
                        </Button>
                        <Button type="submit" disabled={form.formState.isSubmitting}>Post Comment</Button>
                    </div>
                </form>
            </Form>
        </div>
    );
}
