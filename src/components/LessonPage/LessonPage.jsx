// React core
import React,{useEffect, useState} from 'react';

// For base64 decode/encode
import { Buffer } from 'buffer'

// Componnet Styling
import './style.scss'

// Auto-generated Table of Contents
import * as tocbot from 'tocbot';
@use 'tocbot/src/scss/tocbot';

// Input component
import Input from '../../partials/Input/Input'

import Footer from '../Footer/Footer'

// Clipboard Access - for copy on-select
import Clippy from '../../partials/Clippy/Clippy'

// For base64 decode/encode
import { Buffer } from 'buffer'

import Presentation from 'partials/Presentation'

import {
  useParams
} from "react-router";

import {
  useSearchParams
} from "react-router-dom";

export default function LessonPage({
}) {

  // Derive topic and lesson names from URL parameters
  let { topicName, lessonName } = useParams();
  const [searchParams] = useSearchParams();
  // For receiving the lesson data
  // from the python process
  const [lesson, loadLesson] = useState('')

  const lessonType = searchParams.get('type')

  const tocVisible = {
    visibility: "visible",
    height: 'calc(50% - 1em)'
  };

  const tocHidden = {
    visibility: "hidden",
  };

  useEffect(() => {
      console.log(`Calling Lesson URI at ${topicName}/${lessonName}`)
      fetch(process.env.REACT_APP_API_URI_LOAD_LESSON, {  
          method: 'POST',  
          headers: {
              Accept: 'application/json',
              'Content-Type': 'application/json',
          },  
           body: JSON.stringify({
            uri: encodeURIComponent(`${topicName}/${lessonName}`)
           })
      }).then(function (response) {  
        
        if(response.status!=200) {
          console.log("Failed to retrieve encoded lesson, HTTP error was: ", response.statusText);
        } else {
          response.json().then(function(data) {
            loadLesson(data.encodedLesson);
            console.log("Successfully retrieved encoded lesson");
          });
        }

      }).catch(function (error) {  
        console.log("Failed to retrieve encoded lesson, error was: ", error);
      });
  },[]);  

  useEffect(() => {
      tocbot.init({
          // Where to render the table of contents.
          tocSelector: '.js-toc',
          // Where to grab the headings to build the table of contents.
          contentSelector: 'main',
          // Which headings to grab inside of the contentSelector element.
          headingSelector: 'h1, h2, h3, h4, h5, h6',
          // For headings inside relative or absolute positioned containers within content.
          hasInnerContainers: true,
          // Main class to add to lists.
          linkClass: 'toc-link',
          // Class that gets added when a list should be collapsed.
          isCollapsedClass: 'is-collapsed',
          // Smooth scrolling enabled.
          scrollSmooth: true,
          // Smooth scroll duration.
          scrollSmoothDuration: 420,
          headingsOffset: 40,
          collapseDepth: 0,
      });  

  }, [lesson])
    
  return (

      <div className='lesson-container'>
        <div className='lesson-container-title'>
          <Clippy/>
        </div>
        { (lesson && lessonType == 'standard') ?
          [
            <nav key="js-toc-on" className="js-toc" style={tocVisible}></nav>,
            <main key="lesson-content" className='lesson-content-container' dangerouslySetInnerHTML={{ __html: Buffer.from(lesson, 'base64').toString('ascii'); }} />,
            // <Presentation />
            <Footer lesson={lesson} />
          ]
          :
          (lesson && lessonType == 'presentation') ?
          [
            <Presentation lesson={lesson} />,
            <Footer lesson={lesson} />
          ]
          :
          <nav key="js-toc-off" className="js-toc" style={tocHidden}></nav>
        }
      </div>

  );
}