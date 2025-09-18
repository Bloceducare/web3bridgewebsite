import MaxWrapper from "@/components/shared/MaxWrapper";
import SuccessForm from "@/components/shared/SuccessForm";

export default function Page() {
  return (
    <MaxWrapper className="flex-1 flex items-center justify-center flex-col gap-10 mt-16 md:mt-20">
      <SuccessForm />
    </MaxWrapper>
  );
}
