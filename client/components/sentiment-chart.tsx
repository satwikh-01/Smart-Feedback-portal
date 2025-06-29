"use client"

import { Bar, BarChart, ResponsiveContainer, XAxis, YAxis, Tooltip, Legend } from "recharts"

interface SentimentChartProps {
    data: {
        sentiment: string;
        count: number;
    }[];
}

export function SentimentChart({ data }: SentimentChartProps) {
    const chartData = data.map(item => ({
        name: item.sentiment.charAt(0).toUpperCase() + item.sentiment.slice(1),
        count: item.count,
    }));

    return (
        <ResponsiveContainer width="100%" height={350}>
            <BarChart data={chartData}>
                <XAxis
                    dataKey="name"
                    stroke="#888888"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                />
                <YAxis
                    stroke="#888888"
                    fontSize={12}
                    tickLine={false}
                    axisLine={false}
                    allowDecimals={false}
                />
                <Tooltip
                    contentStyle={{
                        backgroundColor: 'hsl(var(--background))',
                        borderColor: 'hsl(var(--border))'
                    }}
                />
                <Legend />
                <Bar dataKey="count" fill="hsl(var(--primary))" radius={[4, 4, 0, 0]} />
            </BarChart>
        </ResponsiveContainer>
    )
}
