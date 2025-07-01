"use client";

import { useEffect, useState, useCallback } from "react";
import { useApi } from "@/hooks/use-api";
import { Bell, BellRing } from "lucide-react";
import {
    DropdownMenu,
    DropdownMenuContent,
    DropdownMenuItem,
    DropdownMenuTrigger,
    DropdownMenuSeparator,
} from "@/components/ui/dropdown-menu";
import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { toast } from "sonner";
import { Notification } from "@/types";
import { formatDistanceToNow } from 'date-fns';

export default function NotificationBell() {
    const { apiFetch } = useApi();
    const [notifications, setNotifications] = useState<Notification[]>([]);
    const [unreadCount, setUnreadCount] = useState(0);

    const fetchNotifications = useCallback(async () => {
        try {
            const data = await apiFetch("/notifications");
            if (data) {
                setNotifications(data);
                setUnreadCount(data.filter((n: Notification) => !n.is_read).length);
            }
        } catch (error) {
            // Don't show toast for background fetches
            console.error("Failed to fetch notifications:", error);
        }
    }, [apiFetch]);

    useEffect(() => {
        fetchNotifications();
        const interval = setInterval(fetchNotifications, 30000); // Poll every 30 seconds
        return () => clearInterval(interval);
    }, [fetchNotifications]);

    const handleNotificationClick = async (notification: Notification) => {
        if (!notification.is_read) {
            try {
                await apiFetch(`/notifications/${notification.id}/read`, {
                    method: 'PATCH',
                });
                fetchNotifications(); // Re-fetch to update the list and count
            } catch (error) {
                const e = error as Error;
                toast.error(e.message || "Failed to mark notification as read.");
            }
        }
    };

    return (
        <DropdownMenu>
            <DropdownMenuTrigger asChild>
                <Button variant="ghost" size="icon" className="relative">
                    {unreadCount > 0 ? <BellRing className="h-5 w-5" /> : <Bell className="h-5 w-5" />}
                    {unreadCount > 0 && (
                        <Badge
                            variant="destructive"
                            className="absolute -top-1 -right-1 h-5 w-5 justify-center rounded-full p-0"
                        >
                            {unreadCount}
                        </Badge>
                    )}
                </Button>
            </DropdownMenuTrigger>
            <DropdownMenuContent align="end" className="w-80">
                <div className="p-2 font-bold">Notifications</div>
                <DropdownMenuSeparator />
                {notifications.length > 0 ? (
                    notifications.map((n) => (
                        <DropdownMenuItem
                            key={n.id}
                            onClick={() => handleNotificationClick(n)}
                            className={`cursor-pointer ${!n.is_read ? 'font-bold' : ''}`}
                        >
                            <div className="flex flex-col">
                                <p className="text-sm">{n.message}</p>
                                <p className="text-xs text-muted-foreground">
                                    {formatDistanceToNow(new Date(n.created_at), { addSuffix: true })}
                                </p>
                            </div>
                        </DropdownMenuItem>
                    ))
                ) : (
                    <div className="p-2 text-center text-sm text-muted-foreground">
                        No new notifications.
                    </div>
                )}
            </DropdownMenuContent>
        </DropdownMenu>
    );
}
