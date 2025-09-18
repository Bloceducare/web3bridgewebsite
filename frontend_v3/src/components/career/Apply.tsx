import { ApplicationModal } from "./ApplicationModal";

export default function ApplicationCTA() {
  return (
    <section className="bg-[#FB88880F] dark:bg-gray-900 text-black dark:text-white py-16 px-4 sm:px-6 lg:px-8">
      <div className="sm:max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between">
        <div className="mb-8 md:mb-0 md:mr-8">
          <h2 className="text-3xl font-[600] max-w-[24rem] mb-4 text-black dark:text-white">
            Ready to apply for an open position?
          </h2>
          <p className="text-base max-w-2xl text-gray-700 dark:text-gray-300">
            There must be a reason you are here. Find a role that matches your
            skills and passion, and apply today. We&apos;re excited to see what
            you&apos;ll bring to the table.
          </p>
        </div>
        <ApplicationModal />
      </div>
    </section>
  );
}
