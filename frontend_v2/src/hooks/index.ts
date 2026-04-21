"use client";

import { useEffect, useState } from "react";

export const useFetchAllCoursesById = (token: string, ids: number[]) => {
  const [data, setData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    try {
      const results: any[] = [];

      for (const id of ids) {
        const res = await fetch(
          `${process.env.NEXT_PUBLIC_BASE_URL}/cohort/course/${id}`,
          {
            method: "GET",
            headers: {
              Authorization: `${token}`,
            },
          }
        );

        const response = await res.json();
        if (response.success && response.data) {
          results.push(response.data);
        }
      }

      setData(results);
    } catch (error) {
      console.error("Error fetching courses:", error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { data, isLoading };
};

export const useFetchAllCourses = () => {
  const [data, setData] = useState<any>();
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/cohort/course/all/`
      );
      const result = await res.json();
      setData(result.data);
    } catch (error) {
      console.log(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { isLoading, data };
};

export const useFetchAllRegistration = () => {
  const [data, setData] = useState<any>();
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/cohort/registration/all/`
      );
      const result = await res.json();

      setData(result.data);
    } catch (error) {
      console.log(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { isLoading, data };
};

export const useFetchTestimonials = () => {
  const [data, setData] = useState<any>();
  const [isLoading, setIsLoading] = useState(true);
  const fetchData = async () => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/cohort/testimonial/all/`
      );
      const result = await res.json();

      setData(result.data);
    } catch (error) {
      console.log(error);
    } finally {
      setIsLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
  }, []);

  return { isLoading, data };
};

export async function useFetchExistingParticipants() {
  const base = process.env.NEXT_PUBLIC_BASE_URL;
  if (!base) {
    throw new Error("NEXT_PUBLIC_BASE_URL is not set");
  }
  const response = await fetch(`${base}/cohort/participant/all/`);

  if (!response.ok) {
    console.log("Failed to fetch existing participants");
    throw new Error("Failed to fetch existing participants");
  }

  const { data } = await response.json();
  return data.results;
}
export async function getCohortStatus() {
  const base = process.env.NEXT_PUBLIC_BASE_URL;
  if (!base) {
    throw new Error("NEXT_PUBLIC_BASE_URL is not set");
  }
  const response = await fetch(`${base}/cohort/course/all_opened/`);

  if (!response.ok) {
    console.log("Failed to fetch cohort open courses");
    throw new Error("Failed to fetch cohort status");
  }

  const { data } = await response.json();
  return data;
}

export const useSubmitHubRegistration = () => {
  const submitRegistration = async (data: {
    name: string;
    email: string;
    phone_number: string;
    location: string;
    reason: string;
    role: string;
    contribution: string;
  }) => {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/v2/hub/registration/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(data),
      }
    );

    const result = await response.json();

    if (!response.ok) {
      throw new Error(result.message || "Failed to submit registration");
    }

    return result;
  };

  return { submitRegistration };
};
