"use client";

import React, { useEffect, useState } from "react";
import { Users, CheckCircle, AlertCircle, TrendingUp } from "lucide-react";
import { motion } from "framer-motion";

interface HubSpace {
  id: number;
  name: string;
  total_capacity: number;
  current_occupancy: number;
  available_spaces: number;
  occupancy_percentage: number;
  is_active: boolean;
}

export default function AvailableSpacesSection() {
  const [spaces, setSpaces] = useState<HubSpace[]>([]);
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchSpaces = async () => {
      try {
        const [spacesRes, statsRes] = await Promise.all([
          fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/v2/hub/space/all/`),
          fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/v2/hub/space/stats/`),
        ]);

        const spacesData = await spacesRes.json();
        const statsData = await statsRes.json();

        if (spacesData.success) {
          setSpaces(spacesData.data || []);
        }
        if (statsData.success) {
          setStats(statsData.data);
        }
      } catch (error) {
        console.error("Error fetching spaces:", error);
      } finally {
        setLoading(false);
      }
    };

    fetchSpaces();
  }, []);

  const getOccupancyColor = (percentage: number) => {
    if (percentage >= 90) return "text-red-500";
    if (percentage >= 70) return "text-yellow-500";
    return "text-green-500";
  };

  const getOccupancyBgColor = (percentage: number) => {
    if (percentage >= 90) return "bg-red-500/10";
    if (percentage >= 70) return "bg-yellow-500/10";
    return "bg-green-500/10";
  };

  if (loading) {
    return (
      <section className="py-16 md:py-24 w-full bg-muted/20">
        <div className="max-w-7xl mx-auto px-4 md:px-6">
          <div className="text-center">Loading space availability...</div>
        </div>
      </section>
    );
  }

  return (
    <section className="py-24 md:py-32 w-full bg-background">
      <div className="max-w-7xl mx-auto px-4 md:px-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.6 }}
          className="text-center mb-12"
        >
          <h2 className="text-4xl md:text-5xl font-bold mb-4 tracking-tight">
            Hub Availability
          </h2>
          <p className="text-lg text-muted-foreground max-w-2xl mx-auto">
            Real-time information about available spaces in the hub
          </p>
        </motion.div>

        {/* Overall Stats */}
        {stats && (
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true }}
            transition={{ duration: 0.6, delay: 0.1 }}
            className="grid grid-cols-2 md:grid-cols-4 gap-4 md:gap-6 mb-12"
          >
            <div className="p-6 rounded-lg bg-background border border-border">
              <div className="flex items-center gap-3 mb-2">
                <Users className="w-5 h-5 text-bridgeRed" />
                <span className="text-sm text-muted-foreground font-medium">Total Capacity</span>
              </div>
              <div className="text-2xl md:text-3xl font-bold text-bridgeRed">
                {stats.total_capacity}
              </div>
            </div>

            <div className="p-6 rounded-xl bg-gradient-to-br from-blue-500/10 to-indigo-500/10 border border-blue-500/20">
              <div className="flex items-center gap-3 mb-2">
                <TrendingUp className="w-5 h-5 text-blue-500" />
                <span className="text-sm text-muted-foreground">Occupied</span>
              </div>
              <div className="text-2xl md:text-3xl font-bold text-blue-600 dark:text-blue-400">
                {stats.total_occupancy}
              </div>
            </div>

            <div className="p-6 rounded-xl bg-gradient-to-br from-green-500/10 to-emerald-500/10 border border-green-500/20">
              <div className="flex items-center gap-3 mb-2">
                <CheckCircle className="w-5 h-5 text-green-500" />
                <span className="text-sm text-muted-foreground">Available</span>
              </div>
              <div className="text-2xl md:text-3xl font-bold text-green-600 dark:text-green-400">
                {stats.total_available}
              </div>
            </div>

            <div className="p-6 rounded-xl bg-gradient-to-br from-violet-500/10 to-purple-500/10 border border-violet-500/20">
              <div className="flex items-center gap-3 mb-2">
                <AlertCircle className="w-5 h-5 text-violet-500" />
                <span className="text-sm text-muted-foreground">Occupancy</span>
              </div>
              <div className={`text-2xl md:text-3xl font-bold ${getOccupancyColor(stats.occupancy_percentage)}`}>
                {Math.round(stats.occupancy_percentage)}%
              </div>
            </div>
          </motion.div>
        )}

        {/* Individual Spaces */}
        {spaces.length > 0 && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {spaces.map((space, index) => (
              <motion.div
                key={space.id}
                initial={{ opacity: 0, y: 20 }}
                whileInView={{ opacity: 1, y: 0 }}
                viewport={{ once: true }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
                className={`p-6 rounded-lg border ${
                  space.available_spaces > 0
                    ? "bg-background border-border hover:border-bridgeRed/30"
                    : "bg-muted border-red-500/30"
                } transition-all`}
              >
                <div className="flex items-center justify-between mb-4">
                  <h3 className="text-xl font-semibold text-foreground">
                    {space.name}
                  </h3>
                  {space.is_active ? (
                    <span className="px-3 py-1 rounded-full bg-green-500/20 text-green-600 dark:text-green-400 text-xs font-medium">
                      Active
                    </span>
                  ) : (
                    <span className="px-3 py-1 rounded-full bg-gray-500/20 text-gray-600 dark:text-gray-400 text-xs font-medium">
                      Inactive
                    </span>
                  )}
                </div>

                <div className="space-y-3">
                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Capacity</span>
                    <span className="font-semibold">{space.total_capacity} people</span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Occupied</span>
                    <span className="font-semibold">{space.current_occupancy} people</span>
                  </div>

                  <div className="flex justify-between items-center">
                    <span className="text-sm text-muted-foreground">Available</span>
                    <span className={`font-bold ${space.available_spaces > 0 ? "text-green-600 dark:text-green-400" : "text-red-600 dark:text-red-400"}`}>
                      {space.available_spaces} spaces
                    </span>
                  </div>

                  {/* Progress Bar */}
                  <div className="mt-4">
                    <div className="flex justify-between items-center mb-2">
                      <span className="text-xs text-muted-foreground">Occupancy</span>
                      <span className={`text-xs font-semibold ${getOccupancyColor(space.occupancy_percentage)}`}>
                        {Math.round(space.occupancy_percentage)}%
                      </span>
                    </div>
                    <div className="w-full bg-muted rounded-full h-2 overflow-hidden">
                      <motion.div
                        initial={{ width: 0 }}
                        whileInView={{ width: `${space.occupancy_percentage}%` }}
                        viewport={{ once: true }}
                        transition={{ duration: 1, delay: index * 0.1 }}
                        className={`h-full rounded-full ${
                          space.occupancy_percentage >= 90
                            ? "bg-red-500"
                            : space.occupancy_percentage >= 70
                            ? "bg-yellow-500"
                            : "bg-green-500"
                        }`}
                      />
                    </div>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>
        )}

        {spaces.length === 0 && !loading && (
          <div className="text-center py-12 text-muted-foreground">
            No spaces available at the moment. Check back later!
          </div>
        )}
      </div>
    </section>
  );
}

