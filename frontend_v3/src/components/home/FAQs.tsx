import faqs from "@/data/FAQs"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../ui/accordion"
import CustomSection from "./CustomSection"


const FAQs = () => {
    return (
        <section className="w-full lg:my-28 my-16 flex flex-col items-center justify-center radial-gradient lg:px-6 md:px-2">
      <CustomSection heading="FAQS" description="See frequently asked questions">
            <main className="w-full lg:w-[60%] md:w-[80%]">
                <Accordion type="single" collapsible className="w-full ring-2 ring-red-200 dark:ring-bridgeRed/50  rounded-lg">
                    {
                        faqs.map((faq, index) => (
                            <AccordionItem value={`item-${index}`} key={index} className="py-3 px-6 border-red-300 dark:border-bridgeRed/50">
                                <AccordionTrigger className="text-base text-start font-medium">{faq.question}</AccordionTrigger>
                                <AccordionContent className="text-[hsla(227,4%,52%,1)]">
                                    {faq.answer}
                                </AccordionContent>
                            </AccordionItem>
                        ))
                    }
                </Accordion>
            </main>
                  </CustomSection>

        </section>
    )
}

export default FAQs
