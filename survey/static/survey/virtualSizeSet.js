// This function is to check effective vitual height and width of screen.
// This is implemented for mobile scaling as vh changes depending on onscreen keyboard etc.

let vh = window.innerHeight * 0.01;

document.documentElement.style.setProperty("--vh", `${vh}px`);

let vw = window.innerWidth * 0.01;

document.documentElement.style.setProperty("--vw", `${vw}px`);
