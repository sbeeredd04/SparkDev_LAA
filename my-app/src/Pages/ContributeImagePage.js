import React from 'react'
import Placeholder from './placeholder.png'

function ContributeImagePage() {
  return (
    <div>Contribute Image Page
        <p>Instructions</p>
        <ol>
            <li>Write the instructions UJJWAL!!</li>
            <li>Find me in ContributeImagePage.js</li>
        </ol>
        <div>
            <img src={Placeholder} />
            <input type="file" accept="image/*" />
            
        </div>
    </div>
    
  )
}

export default ContributeImagePage