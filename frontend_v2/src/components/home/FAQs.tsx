import faqs from "@/data/FAQs"
import { Accordion, AccordionContent, AccordionItem, AccordionTrigger } from "../ui/accordion"


const FAQs = () => {
    return (
        <section className="w-full lg:my-28 my-16 flex flex-col items-center md:gap-8 gap-8 justify-center radial-gradient lg:px-6 md:px-2">
            <div className="flex flex-col items-center gap-3">
                <h1 className="font-semibold leading-tight lg:text-5xl md:text-3xl text-[1.72rem] text-center">FAQs</h1>
                <p className="w-full text-muted-foreground text-center">Don’t worry, we are here to explain everything you might want to know</p>
            </div>
            <main className="w-full lg:w-[60%] md:w-[80%]">
                <Accordion type="single" collapsible className="w-full ring-2 ring-red-200 dark:ring-bridgeRed/50  rounded-lg">
                    {
                        faqs.map((faq, index) => (
                            <AccordionItem value={`item-${index}`} key={index} className="py-3 px-6 border-red-300 dark:border-bridgeRed/50">
                                <AccordionTrigger className="text-base text-start font-medium">{faq.question}</AccordionTrigger>
                                <AccordionContent>
                                    {faq.answer}
                                </AccordionContent>
                            </AccordionItem>
                        ))
                    }
                </Accordion>
            </main>
        </section>
    )
}

export default FAQs