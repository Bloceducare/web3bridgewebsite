import faqs from "@/data/FAQs"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../ui/accordion"
import CustomSection from "./CustomSection"
import MaxWrapper from "../shared/MaxWrapper"


const FAQs = () => {
    return (
        <>
            <section className="w-full lg:my-28 my-16 flex flex-col items-center justify-center lg:px-6 md:px-2">


                <CustomSection heading="FAQS" description="See frequently asked questions">
                    <div className="h-[2px] w-full bg-[linear-gradient(to_right,hsla(223,5%,29%,0)_5%,hsla(223,5%,29%,1)_15%,hsla(223,5%,29%,1)_80%,hsla(223,5%,29%,0)_100%)]" />

                    <MaxWrapper>

                        <Accordion type="single" collapsible className="w-full border-s border-[hsla(223,5%,29%)]">
                            {
                                faqs.map((faq, index) => (
                                    <AccordionItem value={`item-${index}`} key={index} className="py-3 px-6">
                                        <AccordionTrigger className="text-2xl text-start font-medium">{faq.question}</AccordionTrigger>
                                        <AccordionContent className="text-[hsla(227,4%,52%,1)]">
                                            {faq.answer}
                                        </AccordionContent>
                                    </AccordionItem>
                                ))
                            }
                        </Accordion>
                    </MaxWrapper>
                </CustomSection>


            </section>
        </>

    )
}

export default FAQs
