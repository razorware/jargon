Window {
  target: sample.Sample
  title: "Sample 3: Basic Quick Start"
  //  this creates a named value tuple
  size: width:500 height:300
  //  this creates a dictionary with 2 dictionary entries
  startup {
    left: 50
    top: 125
  }
  
  Resources {
    
  }
  
  Grid {
    Label {
      text: "Hello, World!"
    }
  }
}