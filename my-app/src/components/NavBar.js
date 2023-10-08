import React from 'react'
import Placeholder from './placeholder.png'

function NavBar() {
  return (
    <div className='Nav-Bar'>
        
        <h1>Susie Q's</h1>
        <a href="#" class="logo">
        <img src={Placeholder} width="10%"/>
        </a>
        <nav class="navbar">
            <a href="index.html" class="active">Home</a>
            <a href="intro.html" class="active">Fundraising</a>
            <a href="project.html" class="active">About us</a>
            <a href="experiments.html" class="active">Donate</a>
        </nav>
    </div>
  )
}

export default NavBar