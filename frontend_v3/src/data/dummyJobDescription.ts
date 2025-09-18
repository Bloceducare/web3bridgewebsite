export interface JobDescription {
  id: string;
  title: string;
  workplaceType: string;
  duration?: string;
  employmentTYpe: string;
  imageUrl?: string;
  companyOverview: string;
  jobDescription: string;
  responsibilities: string[];
  Qualifications: string[];
  jobRequirements?: string[];

}

export const dummyJobData: JobDescription[] = [
  {
    id: "1",
    title: "Video Editor",
    workplaceType: "Remote",
    employmentTYpe: "Full-Time",
    companyOverview:
      "Web3bridge is an organization dedicated to building a thriving community of blockchain developers, enthusiasts, and contributors across Africa. We offer training, mentorship, and support for individuals keen on learning about Web3 technologies, blockchain development, and decentralized applications (dApps). Our hands-on cohort-based learning programs, technical bootcamps, and community-driven initiatives equip participants with the skills needed to make meaningful contributions to the blockchain ecosystem. At Web3bridge, our media team plays a crucial role in capturing the essence of our journey. Through weekly video projects, cohort introduction videos, and engaging visual content that highlights our students’ and mentors’ experiences, we bring our community’s stories to life.",
    jobDescription:
      "We are seeking a talented and passionate Video Editor to join our dynamic media team. The ideal candidate will have a solid foundation in video editing techniques and a keen eye for storytelling. You will contribute to creating captivating content for our various platforms, ensuring our message reaches and resonates with our audience.",
    responsibilities: [
      "Edit video content, including cutting, trimming, and assembling footage",
      "Collaborate with the creative team to develop video concepts and storyboards",
      "Organize and manage video files and assets",
      "Utilize video editing software proficiently (Adobe Premiere Pro, Final Cut Pro)",
      "Assist with color correction, audio mixing, and special effects",
      "Stay updated on industry trends and best practices",
    ],
    Qualifications:[
     " Proficiency in video editing software (e.g., Adobe Premiere Pro, Final Cut Pro)",
   " Experience with YouTube content creation is a plus",
    "Strong attention to detail and organizational skills",
   " Knowledge of the production process",
    "Basic knowledge of audio editing and mixing",
   " Excellent organizational and time management skills",
    "Ability to work collaboratively in a fast-paced environment",
    "Passion for visual storytelling and media production",
    "Excellent communication skills",
    "Organized, goal-oriented, and result-driven"
    ],
  },
  {
    id: "2",
    title: "Secretary",
    workplaceType: "Remote",
    employmentTYpe: "Full-Time",
   companyOverview:
      "Web3bridge is an organization dedicated to building a thriving community of blockchain developers, enthusiasts, and contributors across Africa. We offer training, mentorship, and support for individuals keen on learning about Web3 technologies, blockchain development, and decentralized applications (dApps). Our hands-on cohort-based learning programs, technical bootcamps, and community-driven initiatives equip participants with the skills needed to make meaningful contributions to the blockchain ecosystem. At Web3bridge, our media team plays a crucial role in capturing the essence of our journey. Through weekly video projects, cohort introduction videos, and engaging visual content that highlights our students’ and mentors’ experiences, we bring our community’s stories to life.",
    jobDescription:
      "We are seeking a highly organized and detail-oriented Secretary to join our dynamic team. The Secretary will play a critical role in managing key administrative tasks for our cohort programs and maintaining smooth communication within the team and with external stakeholders. The ideal candidate will be responsible for managing important documents, coordinating schedules, and ensuring the timely execution of tasks.",
    responsibilities: [
      "Manage Registration and Cohort Data: Maintain and update the registration sheet for new cohort applicants. Arrange and organize cohort-related data, ensuring all information is accurate and up to date.",
      "Support Email Management: Monitor and manage the support email inbox, notifying relevant team members of emails requiring attention and responses. Respond to basic student inquiries and escalate more complex issues to the appropriate departments.",
      "Deferment and Assessment Coordination: Open and manage sheets to track students applying to defer their participation in the cohort. Aggregate scores and assessment sheets from mentors, ensuring all data is compiled and ready for analysis.",
      "File and Document Management: Manage and organize digital files, ensuring easy access and proper version control for all cohort-related documents. Maintain confidentiality and secure storage of student and cohort data.",
      "Cohort Calendar Management: Manage and coordinate calendar invites and scheduling for cohort activities before and during the cohort. Ensure that all relevant stakeholders are informed of key dates, deadlines, and events.",
      "Meeting and Communication Coordination: Prepare meeting agendas and take minutes during team meetings, ensuring all actions and discussions are properly documented and followed up on. Act as the central point of contact for internal communications between different departments and teams.",
      "Feedback and Report Preparation: Assist in organizing and collecting feedback from students and mentors to help improve the cohort experience. Prepare progress reports by compiling data from registration sheets, assessments, and feedback for management review.",
      "Event and Workshop Logistics Support: Assist in coordinating logistics for cohort events, workshops, and webinars, ensuring that everything runs smoothly and efficiently."
   ],

    Qualifications: [
      "Proven experience as a secretary, administrative assistant, or in a similar role.",
      "Strong organizational and time-management skills.",
     " Proficiency in Microsoft Office, Google Workspace, and other relevant office software.",
      "Excellent communication skills, both written and verbal.",
      "Attention to detail and ability to manage multiple tasks simultaneously.",
      "Ability to maintain confidentiality and handle sensitive information.",
    ],
    jobRequirements:[
      "Experience in an educational or cohort-based environment.",
      "Familiarity with online collaboration tools and project management software."
    ]
  },
];
