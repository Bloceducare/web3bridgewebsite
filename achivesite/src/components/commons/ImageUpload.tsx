import { useState } from 'react';
import React from 'react';
import {useDropzone} from 'react-dropzone';
import Button from './Button';

function Basic({label,name, disabled=false, setValues,  errors, validateName, }) {
  const [selectedFile, setSelectedFile] = useState<any>({})  
  
  const { getRootProps, getInputProps} = useDropzone({
    onDrop: acceptedFiles => {
      const reader = new FileReader();
      reader.readAsDataURL(acceptedFiles[0]);
      reader.onloadend = () => {
        setSelectedFile(
          {         
          preview: URL.createObjectURL(acceptedFiles[0]),
          fileBase64: reader.result,
          formatted:{
            name: acceptedFiles[0].name,
            size: acceptedFiles[0].size,
            type:acceptedFiles[0].type,
          }   
        }
        ) 
        setValues(name,reader.result)
        setValues(validateName, {
          name: acceptedFiles[0].name.split(" ").join("_").split("-").join("_"),
          size: acceptedFiles[0].size,
          type: acceptedFiles[0].type,
        })
    
      };
      
    },
    maxFiles: 1,
    accept:{
      "image/jpeg": [".jpg", ".jpeg"],
      "image/png": [".png"],
    },
    maxSize: 800000,
    
    
  });
  


  
  const files = (
    
    <div className='flex'>   
      <img src={selectedFile?.preview} className="w-20 h-20" /> 
    </div>
  );


  return (
    <section className="container">      
    {
      !!selectedFile?.formatted && (
        <div className='dark:text-white10'>     
        {selectedFile?.formatted?.name}          
  </div>
      )
    }
      <div {...getRootProps({className: 'dropzone'})}>
        <input 
        className='hidden'
        {...getRootProps()}
        />
        {
          !(!!selectedFile?.formatted) && <StyledDropImage label={label} />
        }
       
      {
        (!!selectedFile?.formatted)  &&
        <>
         <div className='flex items-center justify-between p-3 border'>
         <div>
        {files}
          </div> 
          <div>
            <Button>
            Change Picture
            </Button>
            </div>
        </div>
        </>
      }
      </div>
     
    </section>
  );
}


export default Basic;

function StyledDropImage({label}) {
  return (
    <div >
    
<div 
className="my-2 capitalize dark:text-white10">{label}</div>
<div className="flex items-center justify-center w-full">
<label htmlFor="dropzone-file" className="flex flex-col items-center justify-center w-full h-32 border-2 border-gray-300 border-dashed rounded-lg cursor-pointer bg-gray-50 dark:hover:bg-bray-800 dark:bg-gray-700 hover:bg-gray-100 dark:border-gray-600 dark:hover:border-gray-500 dark:hover:bg-gray-600">
<div className="flex flex-col items-center justify-center pt-5 pb-6">
  <svg aria-hidden="true" className="w-10 h-10 mb-3 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12" /></svg>
  <p className="mb-2 text-sm text-gray-500 dark:text-gray-400"><span className="font-semibold">Click to upload</span> or drag and drop</p>
  <p className="text-xs text-gray-500 dark:text-gray-400">JPG or PNG (MAX. 800x400px)</p>
</div>
</label>
</div>

    </div>
  )
}