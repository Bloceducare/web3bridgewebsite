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
  jobRequirements: string[];
}

export const dummyJobData: JobDescription[] = [
  {
    id: "1",
    title: "Smart Contract Writer",
    workplaceType: "Remote",
    employmentTYpe: "Full-Time",
    companyOverview:
      "Block3 is a pioneering organization in the blockchain and Web3 space, committed to developing innovative decentralized applications (dApps) and solutions. We are looking for a talented Smart Contract Writer to join our team and help shape the future of decentralized technologies.",
    jobDescription:
      "Block3 is a pioneering organization in the blockchain and Web3 space, committed to developing innovative decentralized applications (dApps) and solutions. We are looking for a talented Smart Contract Writer to join our team and help shape the future of decentralized technologies.",
    responsibilities: [
      "Design and Develop Smart Contracts",
      "Security and Testing",
      "Blockchain Integration",
      "Documentation and Code Maintenance",
    ],
    jobRequirements: [
      "Strong experience with Solidity and Ethereum. Familiarity with other languages like Rust or Vyper is a plus.",
      "2-3 years in blockchain development, focusing on smart contracts.",
      "Experience with dApps and smart contract security is essential.",
      "Bachelor’s degree in Computer Science or a related field, or equivalent experience.",
    ],
  },
];
