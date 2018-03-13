<p align="center">
    <img src="https://github.com/razorware/jargon/blob/master/images/razorware_jargon_logo.png"
         alt="razorware.jargon logo"
         title="RazorWare.Jargon" />
</p>

# Jargon: A robust, lightweight data structure

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

Jargon is more flexible than JSON. For instance, in the example of above, there are only a couple of elements encapsulated with '"'. Also, there is no root symbol
required as in JSON. A JSON document must start with `{` and close with `}`. Jargon does not require anything. The following is a valid jargon data structure:

```
Person {
    id:     1
    dob:    1/1/2000
    name:   "John Doe"
}

Address {
    1 {
        street: "123 Main St"
        city:   Dallas
        state:  TX
        zip:    75227
    }
    2 {
        street: "456 Southwest Blvd"
        city:   Arlington
        state:  TX
        zip:
    }
}
```

`Person` and `Address` are separate keys with their own child nodes. Apply double quotes to values with spaces. If quotes had not encapsulated
the (street, for example) values. Otherwise, `street: 123 Main St` result is problematic.  
_NOTE: this behavior has not yet been determined and would most likely throw an exception._

If a keyed value were expected to be a list, then the following format is required:

```
Grocery_List {
    produce:    apples, lettuce, carrots, potatoes
    dairy:      milk, cheese 
}
```

`produce` and `dairy` both have enumerated values, or lists.

There are no end of line symbols. The parser is friendly to both `\r` and `\n`. Whitespaces are generally ignored except when formatting a keyed value.

Formatting will have a lot of flexibility. I am purposefully intent on minimizing the variety of symbols. There are currently fewer symbols here than in JSON and presents a far
cleaner markup for a data structure than XML. Look for an implementation of Jargon to be used in PyLE at some point in the future.
 
Jargon recognizes several formats for data:

integers:       500
floats:         29.75
dictionary:
```
size:   w:500 h:500
```
results in: `{'w': 500, 'h': 500}`

lists: 
```
list:   100, "text information", 1/1/2000
```
results in: `[100, 'text information', '1/1/2000']`

In progress (_TODO's and other stuff_):
* add handling of unique node value collections, see Ex: 1 
* add validator (validation template)

Ex: 1
```
data: People {
    ...
}
data: Addresses {
    ...
}    
```