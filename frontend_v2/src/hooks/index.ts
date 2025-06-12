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
  const response = await fetch(
    "https://web3bridgewebsitebackend.onrender.com/api/v2/cohort/participant/all/"
  );

  if (!response.ok) {
    console.log("Failed to fetch existing participants");
    throw new Error("Failed to fetch existing participants");
  }

  const { data } = await response.json();
  return data.results;
}
export async function getCohortStatus() {
  const response = await fetch(
    "https://web3bridgewebsitebackend.onrender.com/api/v2/cohort/course/all_opened/"
  );

  if (!response.ok) {
    console.log("Failed to fetch existing participants");
    throw new Error("Failed to fetch existing participants");
  }

  const { data } = await response.json();
  // console.log(data);
  return data;
}
