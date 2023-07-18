import React, { useEffect, useState } from 'react';
import { hashString } from 'utils/Utils'

// Componnet Styling
import './style.scss'

export default function DashboardCard({ 
    cardData,
    cardTitle
  }
  ) {

  let counter = 0

  console.log('Rendering News Card')
  console.log(cardData)


  return (

    <div className="col-span-full xl:col-span-6 bg-white shadow-lg rounded-sm border border-slate-200">
      <header className="px-5 py-4 border-b border-slate-100">
        <h2 className="font-semibold text-slate-800">{cardTitle}</h2>
      </header>
      <div className="p-3">
      {        
        Object.keys(cardData).length > 0 && !cardData?.error
        ?
          Object.entries(cardData).map((newsGroupObj)=> {
            {let newsGroupObjGroupID = newsGroupObj[0]}
            {counter++}
            return (
                <div key={`div-${newsGroupObjGroupID}-${counter}`}>
                  <header className="text-xs uppercase text-slate-400 bg-slate-50 rounded-sm font-semibold p-2">
                  {newsGroupObjGroupID}
                  </header>
                  <ul key={`ul-${newsGroupObjGroupID}`} className="news-article my-1">
                  {
                    Object.entries(newsGroupObj[1]).map((newsObj)=> {
                        {let articleTitle = newsObj[1][1]}
                        {let articleURL = newsObj[1][2]}
                        {let articleTitleHash = hashString(articleTitle)}
                        {counter++}
                        return <li key={`li-${articleTitleHash}-${counter}`} className="flex px-2">
                        <a key={`div-${articleTitleHash}-${counter}`} href={articleURL}>{articleTitle}</a>
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
                  'RECEIVED NO ARTICLES'
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
