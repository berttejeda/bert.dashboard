import React, { useEffect, useState } from 'react';
import { hashString } from 'utils/Utils'

export default function DashboardCard({ 
    cardData,
    cardTitle
  }
  ) {

  let counter = 0

  return (

    <div className="col-span-full xl:col-span-6 bg-white shadow-lg rounded-sm border border-slate-200">
      <header className="px-5 py-4 border-b border-slate-100">
        <h2 className="font-semibold text-slate-800">{cardTitle}</h2>
      </header>
      <div className="p-3">
      {        
        Object.keys(cardData).length > 0 && !cardData?.error
        ?
          Object.entries(cardData).map((messageGroupObj)=> {
            {let messageGroupID = messageGroupObj[0]}
            {counter++}
            return (
                <div key={`div-${messageGroupID}-${counter}`}>
                  <header className="text-xs uppercase text-slate-400 bg-slate-50 rounded-sm font-semibold p-2">
                  {messageGroupID}
                  </header>
                  <ul key={`ul-${messageGroupID}`} className="my-1">
                  {
                  Object.entries(messageGroupObj[1]).map((messageObj)=> {
                      {let message = messageObj[1]}
                      {let messageHash = hashString(message)}
                      {counter++}
                      return <li key={`li-${messageHash}-${counter}`} className="flex px-2">
                      <div className="self-center font-medium text-slate-800" key={`div-${messageHash}-${counter}`}>{message}</div>
                      </li>
                  })
                  }
                  </ul>
                </div>
              )
            }
            )
          :   <div>
              <header className="text-xs uppercase text-slate-400 bg-slate-50 rounded-sm font-semibold p-2">
              {
                !cardData?.error
                ?
                  'RECEIVED NO MESSAGES'
                : 'Error'
              }
              </header>
              <ul className="my-1">
              <li className="flex px-2">
              {cardData?.error}
              </li>
              </ul>
            </div>
      }
      </div>
    </div>
  );


}
