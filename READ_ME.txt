Description: This code is for a Qt-based Python application centered around the creation and assignment of recipes for the fabrication of planar solar cells. 

Current Capabilities: New structures (each layer of the solar cell stack) can be defined from the ground up and saved/assigned to devices. Each layer in the structure contains two 
    main pieces of information; parameters, and attributes. Parameters are used to define the general fabrication procedure of the layer, usually specified with a primary general 
    parameter, leading to more and more specific points. Each parameter is assigned a list of attributes, which constitutes of variable groups (for organization's sake), and 
    variables. Variables are typically given a descriptive name and a value,which can be changed to suit exact details of the deposition protocol being used. 
    
    Each layer must be fully assigned a parameter path to be considered defined (list of parameters clicked until no more are available). Accordingly, all attributes must be
    altered to match the exact details of the deposition. Once a single layer is defined, another can be added on top and so on until the entire device's architecture is entered.
    
    To assign these structures to devices, a list of raw input devices must be imported, selected, and the set with the current structure. These devices can afterwards be saved with
    the full information of their architecture.
