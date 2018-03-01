<p align="center">
    <img src="https://github.com/razorware/pyxelbox/blob/master/images/razorware_jargon_logo.png"
         alt="razorware.jargon logo"
         title="RazorWare.Jargon" />
</p>

# Jargon: A robust, lightweight data structure with an extremely easy format to master.

As I have mentioned, JSON is good. Not great, though, because it feels like something is missing. XML and its associated markup languages are extremely bloated.
 
Jargon, however, allows for easy nesting like XML without all the extra typing. I borrowed from CSS to evolve the basic paradigm. The first parser is written in 
Python. With it, I am able to generate lists of nodes, encapsulate child nodes and, if I desire, force the parser to create a uniquely keyed dictionary. Additionally,
the standard structure has formats that cause the parser to create tuples, named tuples or lists.

Here is an example:

```
Window {
    target: sample.Sample
    title: "Working Title"
    size: w:500 h:300
    
    Resources {
        images: "..\..\images"
    }
    
    // supports single-line comments
    
    /*
        multi-line comments are also supported
    */
}
```