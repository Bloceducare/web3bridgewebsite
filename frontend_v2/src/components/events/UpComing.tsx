import React from 'react'
import EventImage1 from "../../../public/events/6.png";
import EventImage2 from "../../../public/events/7.png";
import EventImage3 from "../../../public/events/8.png";
import EventCard from './EventCard';


const UpComing = () => {
    return (
        <section className='w-full flex flex-col items-center lg:gap-16 gap-8 lg:my-44 md:my-20 my-28 radial-gradient lg:px-16 md:px-8 px-4'>
            <div className='w-full flex flex-col gap-2'>
                <h1 className='font-semibold lg:text-5xl  text-3xl text-center capitalize'>Upcoming Events</h1>
                <p className='text-center text-muted-foreground text-xl font-light'>A number of web3 events you may love to attend</p>
            </div>
            <main className='w-full grid lg:grid-cols-3 md:grid-cols-2 lg:gap-8 md:gap-10 gap-12'>
                {/* <EventCard image={EventImage1} text={'Practical hands-on exercises on using IPFS for file Storage and retrieval'} />
                <EventCard image={EventImage2} text={'Practical hands-on exercises on using IPFS for file Storage and retrieval'} />
                <EventCard image={EventImage3} text={'Practical hands-on exercises on using IPFS for file Storage and retrieval'} /> */}
            </main>
        </section>
    )
}

export default UpComing