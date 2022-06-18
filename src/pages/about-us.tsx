import HeaderImg from '../../assests/about-us/about-header-image.svg'
import GroupImg from '../../assests/about-us/group-image.svg'
import Founder from '../../assests/about-us/Founder.svg'
import Cofounder from '../../assests/about-us/Cofounder.svg'
import Head from '../../assests/about-us/Head.svg'
import LeadDev from '../../assests/about-us/LeadDev.svg'
import Developer1 from '../../assests/about-us/Developer1.svg'
import Developer2 from '../../assests/about-us/Developer2.svg'
import Developer3 from '../../assests/about-us/Developer3.svg'
import Developer4 from '../../assests/about-us/Developer4.svg'
import Developer5 from '../../assests/about-us/Developer5.svg'
import Investor from '../../assests/about-us/Investor.svg'
import Image from 'next/image'
import Button from '../components/Button'
type Images = {
  name: string
  role: string
  image: any
}
const About = () => {
  const images: Images[] = [
    {
      name: 'Awosika Israel Ayodeji',
      role: 'Founder, Program Manger',
      image: Founder,
    },
    {
      name: 'Akinnusotu Temitayo Daniel',
      role: 'Co-founder, Lead Dev/Mentor',
      image: Cofounder,
    },
    {
      name: 'Katangole Allan',
      role: 'Head, Technical Training',
      image: Head,
    },
    {
      name: 'Jeremiah Noah',
      role: 'Lead dev/ Mentor',
      image: LeadDev,
    },
    {
      name: 'Oke Kehinde',
      role: 'Developer',
      image: Developer1,
    },
    {
      name: 'Fatolu Pelumi',
      role: 'Developer',
      image: Developer2,
    },
    {
      name: 'Abimbola Adebayo',
      role: 'Devloper/ Mentor',
      image: Developer3,
    },
    {
      name: 'Falilat Owolabi',
      role: 'Developer',
      image: Developer4,
    },
    {
      name: 'Ademola Kelvin',
      role: 'Developer',
      image: Developer5,
    },
    {
      name: 'Michael Jerry',
      role: 'Community/ Social Media Lead',
      image: Developer3,
    },
    {
      name: 'Billy Luedtke',
      role: 'Advisor & Angel investor',
      image: Investor,
    },
    {
      name: 'Ademola Kelvin',
      role: 'Developer',
      image: Developer5,
    },
  ]
  return (
    <>
      <header className="flex w-[80%] items-center justify-around  mt-12 mx-auto">
        <Image src={HeaderImg} height={326} width={326} />
        <div className="w-[50%]">
          <h1 className="text-[2rem] font-bold mb-6 text-[#151515] dark:text-[#D0D0D0]">
            Hey! I'm Ayodeji, business developer, Blockchain Educator and
            founder of Web 3 bridge.
          </h1>
          <p className="text-[#737373]">
            If you've got a couple of minutes I'd love to share the story of how
            web 3 bridge has grown as a bootstrapped startup. It's been an
            awesome journey and I couldn't have done it without the support of
            my team around me.
          </p>
        </div>
      </header>
      <section className="flex mt-24 mb-12 items-start justify-around  px-8 ">
        <div className="bg-[#F3F3F3] dark:bg-[#111111] px-14 py-12 dark:border dark:border-[#444444]">
          <h1 className="text-center dark:text-white border-b border-b-[#A0A0A0] pb-6 px-4">
            OUR STORY IN TO THE WEB 3
          </h1>
          <ul className="text-[#707070] dark:text-[#D0D0D0] text-sm">
            <li className="my-3">
              <p>Problem</p>
            </li>
            <li className="my-3">
              <p>Solution</p>
            </li>
            <li className="my-3">
              <p>Remote developers</p>
            </li>
            <li className="my-3">
              <p>Lagos</p>
            </li>
            <li className="my-3">
              <p>Physical</p>
            </li>
          </ul>
          <Button
            class="text-center block mx-auto w-full py-2 mt-4"
            type="background"
            content="View Cohorts"
          />
        </div>
        <div className="w-[50%]">
          <Image src={GroupImg} className={'w-full'} />
          <h1 className="mb-6 mt-4 font-bold text-2xl text-[#151515] dark:text-[#D0D0D0]">
            Developers dont have to pay so much to learn web 3
          </h1>
          <p className="mb-4 text-[#737373] dark:text-[#D0D0D0]">
            Web3bridge is a program created in 2019 to train Web3 developers in
            Africa. We are working on building sustainable Web3 economy in
            Africa through remote and onsite Web3 development training,
            supporting web3 developers and startups, and lowering barriers of
            entry into the Web3 ecosystem.
          </p>
          <p className="mt-6 text-[#737373] dark:text-[#D0D0D0]">
            And we take care of Accomodation Feeding and data expenses for all
            our onsite participants during the program to make it easier for
            them to learn
          </p>
        </div>
      </section>
      <section className="mt-[10rem] px-12">
        <h1 className="dark:text-[#D0D0D0] font-bold text-[2rem] ml-8 my-12">
          Pioneered By Awesome Team
        </h1>
        <div className=" flex flex-wrap w-full justify-between">
          {images.map((items, index) => {
            return (
              <div key={index} className="w-30% text-center mb-24 text-white">
                <Image src={items?.image} height={400} width={400} />
                <h1 className="text-xl text-[#151515] dark:text-white font-bold">
                  {items?.name}
                </h1>
                <p className="text-[#A1A1A1]">{items?.role}</p>
              </div>
            )
          })}
        </div>
      </section>
    </>
  )
}

export default About
