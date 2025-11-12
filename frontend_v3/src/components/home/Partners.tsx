import Image from "next/image";
import CustomSection from "./CustomSection";
import eth from "/public/home/eth.png"
import polygon from "/public/home/polygon.png"
import lisk from "/public/home/lisk.png"
import hydro from "/public/home/hydro.png"
import push from "/public/home/push.png"
import starknet from "/public/home/starknet.png"
import kernel from "/public/home/kernel.png"
import orbit from "/public/home/orbit.png"
import stellar from "/public/home/stellar.png"

type IconsProps = {
  id:string;
  src: string;
  alt: string
}

const Icons: IconsProps[] = [
  {id: crypto.randomUUID(), src: eth.src, alt:"etherem logo"},
   {id: crypto.randomUUID(), src: polygon.src, alt:"polygon logo"},
  {id: crypto.randomUUID(), src: lisk.src, alt:"lisk logo"}, 
  {id: crypto.randomUUID(), src: hydro.src, alt:"hydro logo"}, 
  {id: crypto.randomUUID(), src: push.src, alt:"push logo"}, 
  {id: crypto.randomUUID(), src: starknet.src, alt:"starknet logo"}, 
  {id: crypto.randomUUID(), src: kernel.src, alt:"kernel logo"}, 
  {id: crypto.randomUUID(), src: orbit.src, alt:"orbit logo"}, 
  {id: crypto.randomUUID(), src: stellar.src, alt:"stellar logo"},


]


const Partners: React.FC = () => (
  <section className=" w-full flex flex-col py-24 items-center">
    <CustomSection
      heading="partners"
      description="These protocols and Networks have trusted and  partnered with us over years"
    > 
     
       <div className="rounded-2xl h-[328px] w-[621px] bg-gradient-to-r from-[hsla(0,0%,14%,1)] to-[hsla(40,0%,28%,0.67)] p-[2px] mt-14 relative">
        <div className="h-full w-full dark:bg-black rounded-2xl relative">
 
       <div className="rounded-2xl h-[328px] w-[699px] bg-gradient-to-r from-[hsla(0,0%,14%,1)] to-[hsla(40,0%,28%,0.67)] p-[2px] mt-6 absolute -right-10">
        <div className="h-full m-auto p-4 flex flex-col justify-center dark:bg-black rounded-2xl">

              <div className="grid grid-cols-3 grid-rows-3 items-center justify-center gap-8">
              {Icons.map(({src, id, alt}) => (
                  <div key={id} className="h-auto flex items-center justify-center">
                     <Image src={src} alt={alt} height={64} width={0} className="object-cover w-auto" />

               
                  </div>
                 ))}

              </div>

             

            
              
        </div>
            
        </div>

        </div>

      </div> 
    
    </CustomSection>
  </section>
);

export default Partners;
