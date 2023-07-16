import React,{useEffect, useState} from 'react';

import ReactDOM from 'react-dom';

// For base64 decode/encode
import { Buffer } from 'buffer'

import { 
  FlexBox,
  Heading,
  SpectacleLogo,
  UnorderedList,
  CodeSpan,
  OrderedList,
  ListItem,
  Appear,
  Slide,
  Deck,
  Text,
  Grid,
  Box,
  Image,
  CodePane,
  MarkdownSlide,
  MarkdownSlideSet,
  Notes,
  DefaultTemplate,
  SlideLayout
 } from 'spectacle';

// Componnet Styling
import './style.scss'

export default function Presentation(lesson, {children}) {

  const theme = {
    colors: {
      primary: '#fff',
      secondary: '#fff'
    },
    shadows: {
      boxShadow: 'black'
    },
    backdropStyle: {
      position: 'relative',
      backgroundRepeat: 'repeat',
      backgroundColor: '#FFF',
      backgroundImage: 'url("data:image/svg+xml;base64,PHN2ZyB2ZXJzaW9uPSIxLjIiIHhtbG5zPSJodHRwOi8vd3d3LnczLm9yZy8yMDAwL3N2ZyIgdmlld0JveD0iMCAwIDYgNiIgd2lkdGg9IjYiIGhlaWdodD0iNiI+Cgk8dGl0bGU+aW1hZ2Utc3ZnPC90aXRsZT4KCTxkZWZzPgoJCTxpbWFnZSAgd2lkdGg9IjYiIGhlaWdodD0iNiIgaWQ9ImltZzEiIGhyZWY9ImRhdGE6aW1hZ2UvcG5nO2Jhc2U2NCxpVkJPUncwS0dnb0FBQUFOU1VoRVVnQUFBQVlBQUFBR0FnTUFBQUNkb2dmYkFBQUFBWE5TUjBJQjJja3Nmd0FBQUFsUVRGUkYrZm41Ky92NzlmWDFyakZYQ2dBQUFCUkpSRUZVZUp4allBeGdnS0FRQm9hd0JVQUVBQlNHQXpSem0wRk5BQUFBQUVsRlRrU3VRbUNDIi8+Cgk8L2RlZnM+Cgk8c3R5bGU+Cgk8L3N0eWxlPgoJPHVzZSBpZD0iTGF5ZXIiIGhyZWY9IiNpbWcxIiB4PSIwIiB5PSIwIi8+Cjwvc3ZnPg==")',
    }
  };

  let lessonData = JSON.parse(atob(lesson.lesson))

  const template = <DefaultTemplate />;

  const counter = 0

  return (
    <Deck className={"deck"} transition={['none']} theme={theme} template={template}>
      {
        Object.entries(lessonData).map(([slide, slideContent]) => {
          {
           {counter++}
           return ( 
            <MarkdownSlide key={`slide-${counter}`}>
            {slideContent}
            </MarkdownSlide>
            )
          }
        }
        )
      } 

{/*      <MarkdownSlide componentProps={{ color: 'yellow' }}>
        {`
          # This is a Markdown Slide

          - You can pass props down to all elements on the slide.
          - Just use the \`componentProps\` prop.
        `}
      </MarkdownSlide>*/}
{/*      <MarkdownSlide>
      {atob(lesson.lesson)}
      </MarkdownSlide>*/}
      
    </Deck>
  );
};