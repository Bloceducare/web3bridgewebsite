"use client";

import React from "react";

interface ResultType {
  success?: boolean;
  data?: any[];
  message?: string;
  errors?: string;
}

export const useFetchAllCourses = () => {
  const [courses, setCourses] = React.useState<any[]>();
  const [isLoading, setIsLoading] = React.useState(false);
  const [isError, setIsError] = React.useState("");

  const fetchAllCourses = async () => {
    try {
      setIsLoading(true);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/cohort/course/all`
      );
      const result: ResultType = await response.json();

      if (result.success === true) {
        setCourses(result.data);
      }
    } catch (error: any) {
      setIsError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  React.useEffect(() => {
    fetchAllCourses();
  }, []);

  return { isError, isLoading, courses };
};

export const useFetchSingleCourse = (id: number) => {
  const [course, setCourse] = React.useState<any>();
  const [isLoading, setIsLoading] = React.useState(false);
  const [isError, setIsError] = React.useState("");

  const fetchCourse = async () => {
    try {
      setIsLoading(true);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/cohort/course/${id}`
      );
      const result: ResultType = await response.json();

      if (result.success === true) {
        setCourse(result.data);
      }
    } catch (error: any) {
      setIsError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  React.useEffect(() => {
    fetchCourse();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [id]);

  return { isError, isLoading, course };
};

export const useFetchAllRegistration = () => {
  const [registrations, setRegistrations] = React.useState<any>();
  const [isLoading, setIsLoading] = React.useState(false);
  const [isError, setIsError] = React.useState("");

  const fetchCourse = async () => {
    try {
      setIsLoading(true);

      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/cohort/registration/all`
      );
      const result: ResultType = await response.json();

      if (result.success === true) {
        setRegistrations(result.data);
      }
    } catch (error: any) {
      setIsError(error.message);
    } finally {
      setIsLoading(false);
    }
  };

  React.useEffect(() => {
    fetchCourse();
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  return { isError, isLoading, registrations };
};
