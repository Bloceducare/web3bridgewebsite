import Image from 'next/image'
import HeaderImg from '../../assests/alumni/headerImg.svg'
import GroupImg from '../../assests/alumni/group-image.svg'
import AbdurImg from '../../assests/alumni/abdur.svg'
import AyoImg from '../../assests/alumni/ayodeji.svg'
import OlaImg from '../../assests/alumni/olayinka.svg'
import Button from '../components/Button'

const Alumni = () => {
  return (
    <>
      <header className="flex pt-10 px-16 items-center">
        <div className="w-[50%] px-16">
          <h2 className="text-[#FA0101] ">JOIN OUR ALUMNI COMMUNITY</h2>
          <h1 className=" dark:text-[#D0D0D0] text-3xl font-bold py-8">
            Welcome to Web 3 Bridge Alumni Community Hub
          </h1>
          <p className="text-[#737373]">
            The community is home to hundreds of thousands of developers,
            technologists, and enthusiasts. People who have graduated our
            cohort, feel free to mingle please.
          </p>
        </div>
        <Image src={HeaderImg} />
      </header>
      <section className="text-center mt-[6rem] px-40">
        <h1 className="dark:text-[#D0D0D0] text-3xl mb-6 font-bold">
          Cohort VI officially end, the bumpy ride begins
        </h1>
        <p className="mb-20 mx-auto text-[#737373] w-[50%]">
          Participants of our Web3Bridge program will be participating in Catch
          the flag; where they will be hacking a smart contract with rewards
        </p>
        <Image src={GroupImg} />
        <div className="w-full flex justify-center mt-4">
          <button className="bg-[#FA0101] mx-1  h-4 w-4 rounded-full cursor-pointer"></button>
          <button className="bg-[#FEE0E0] mx-1 h-4 w-4 rounded-full cursor-pointer"></button>
          <button className="bg-[#FEE0E0] mx-1 h-4 w-4 rounded-full cursor-pointer"></button>
          <button className="bg-[#FEE0E0] mx-1 h-4 w-4 rounded-full cursor-pointer"></button>
        </div>
      </section>
      <section className="mt-32 text-center">
        <h1 className="dark:text-[#D0D0D0] mb-4 text-3xl text-bold">
          Past Mentees of our cohorts
        </h1>
        <h2 className="text-[#737373] mb-24">
          Aliquam et in sit libero nisl ultrices morbi. Curabitur ipsum maecenas
          aliquam commodo.
        </h2>
        <div className="flex items-center justify-around px-12">
          <div className="text-center">
            <Image src={AbdurImg} />
            <h1 className="font-bold mb-2 dark:text-[#D0D0D0]">
              Abdur-rasheed Idris
            </h1>
            <p className="text-[#A1A1A1] text-sm">
              Cohort II, Web 2 dark:text-[#D0D0D0] Mentee{' '}
            </p>
            <p className="text-[#A1A1A1] text-sm">(2019)</p>
          </div>
          <div className="text-center">
            <Image src={AyoImg} />
            <h1 className="font-bold mb-2 dark:text-[#D0D0D0]">
              Ayodeji Ayomide
            </h1>
            <p className="text-[#A1A1A1] text-sm">Cohort III, Web 3</p>
            <p className="text-[#A1A1A1] text-sm"> Mentee (2020)</p>
          </div>
          <div className="text-center">
            <Image src={OlaImg} />
            <h1 className="font-bold mb-2 dark:text-[#D0D0D0]">
              Olayinka Ademola
            </h1>
            <p className="text-[#A1A1A1] text-sm">Cohort IV, Web 2</p>
            <p className="text-[#A1A1A1] text-sm"> Mentee (2021)</p>
          </div>
        </div>
        <Button
          class=" px-10 py-1 mt-12 dark:text-[#D0D0D0] border-[#151515] dark:border-[#D0D0D0]"
          type="transparent"
          content="View More"
        />
      </section>
      <section className="bg-[#F3F3F3] dark:bg-[#151515] text-center py-14 mt-24">
        <h1 className="text-3xl font-bold mb-8 dark:text-[#D0D0D0]">
          Join our Alumni Club
        </h1>
        <p className="w-[50%] mx-auto mb-12 text-[#737373]">
          Tellus id nunc vitae pellentesque ornare. Facilisis dignissim nisl hac
          nascetur facilisis in nisi. Nullam maecenas risus adipiscing nulla
          integer eget viverra.
        </p>
        <Button
          class="text-white bg-[#151515] dark:bg-[#FA0101] dark:border-[#FA0101] px-6 py-2"
          type="transparent"
          content="Become a member"
        />
      </section>
    </>
  )
}

export default Alumni
