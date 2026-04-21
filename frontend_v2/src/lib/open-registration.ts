/**
 * Latest **open** programme (registration) id that explicitly includes this course.
 * Does not fall back to unrelated open programmes.
 */
export function resolveOpenRegistrationIdForCourse(
  courseId: number,
  registrations: unknown[] | undefined
): number | undefined {
  if (!registrations?.length) return undefined;
  const open = registrations.filter(
    (r: any) => r && r.is_open === true
  ) as any[];
  const linked = open.filter((r: any) => {
    const ids = (Array.isArray(r.courses) ? r.courses : [])
      .map((c: any) => (typeof c === "number" ? c : c?.id))
      .filter((id: unknown) => id != null);
    return ids.includes(courseId);
  });
  if (!linked.length) return undefined;
  const best = linked.reduce((a: any, b: any) =>
    (Number(b.id) || 0) > (Number(a.id) || 0) ? b : a
  );
  return typeof best.id === "number" ? best.id : undefined;
}
