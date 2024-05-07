"use client";

import { useEffect, useState } from "react";

export const useFetchAllCourses = () => {
  const [data, setData] = useState<any>();
  const [isLoading, setIsLoading] = useState(true);

  const fetchData = async () => {
    try {
      const res = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/cohort/course/all`
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
