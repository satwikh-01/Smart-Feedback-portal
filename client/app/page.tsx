"use client";

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import { useAuth } from "@/context/auth-context";
import MainLayout from "@/components/main-layout";
import ManagerDashboard from "@/components/manager-dashboard";
import EmployeeDashboard from "@/components/employee-dashboard";
import { Skeleton } from "@/components/ui/skeleton";

export default function HomePage() {
  const { user, isLoading, token } = useAuth();
  const router = useRouter();

  useEffect(() => {
    // If loading is finished and there's no token, redirect to login
    if (!isLoading && !token) {
      router.push("/login");
    }
  }, [isLoading, token, router]);

  // Display a loading skeleton while checking auth status
  if (isLoading || !user) {
    return (
      <div className="flex flex-col min-h-screen">
        <header className="sticky top-0 z-50 w-full border-b bg-background/95">
          <div className="container flex h-14 items-center justify-end">
            <Skeleton className="h-8 w-8 rounded-full" />
          </div>
        </header>
        <main className="flex-1 container py-8">
          <Skeleton className="h-8 w-1/4 mb-4" />
          <Skeleton className="h-4 w-1/3" />
        </main>
      </div>
    );
  }

  // Once loaded, display the correct dashboard based on the user's role
  return (
    <MainLayout>
      {user.role === "manager" ? <ManagerDashboard /> : <EmployeeDashboard />}
    </MainLayout>
  );
}
