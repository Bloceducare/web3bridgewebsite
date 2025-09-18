import { cn, utilityIndex } from "@/lib/utils"


export const Utility = () => {
    return (
        <section className="w-full flex flex-col justify-center items-center gap-12 lg:px-20 px-4 mb-28 md:mt-10 mt-0">
            <h1 className="font-semibold lg:text-5xl md:text-4xl text-foreground text-3xl text-center capitalize">Utility Index</h1>
            <main className="w-full grid lg:grid-cols-4 md:grid-cols-2 gap-6">
                {
                    utilityIndex.map((item, index) => (
                        <div key={index} className={cn("flex flex-col gap-4 px-6 py-12 border-2  rounded-3xl", {
                            "bg-gradient-to-t from-transparent via-teal-100/20 to-teal-100/70 border-teal-500/40  ": index === 0,
                            "bg-gradient-to-t from-transparent via-amber-100/20 to-amber-100/70 border-amber-500/40 ": index === 1,
                            "bg-gradient-to-t from-transparent via-violet-200/20 to-violet-200/70 border-violet-500/40": index === 2,
                            "bg-gradient-to-t from-transparent via-rose-200/20 to-rose-200/70 border-rose-500/40": index === 3
                        })}>
                            <h3 className={cn("font-semibold text-3xl", {
                                "text-teal-800": index === 0,
                                "text-amber-600": index === 1,
                                "text-violet-800": index === 2,
                                "text-rose-800": index === 3
                            })}>{item.percent}</h3>
                            <p className="text-foreground tracking-wider text-sm md:text-base">{item.text}</p>
                        </div>
                    ))

                }
            </main>
        </section>
    )
}
