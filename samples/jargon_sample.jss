Window {
  target: sample.Sample
  title: "Sample 3: Basic Quick Start"
  //  packed parameters creates a dictionary
  size: width:500 height:300
  //  attribute list creates a node collection
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