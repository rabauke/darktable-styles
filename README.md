# darktable-styles

My styles for the [darktable](http://www.darktable.org/) raw developer. 

* **film emulation:** Various styles to emulate the look of analog film via the color look up module and the tone curve.  All these styles are based on [G'MIC film emulation](http://gmic.eu/film_emulation/index.shtml).  Note, that the color look up module can only approximate the effect of G'MIC film emulation.  The styles should be applied to processed JPEG files or to RAW files with a suitable active base curve.  The `tools` directory contains Python scrips that have been employed to generate these darktable styles.  To run these scrips darktable needs to be configured to write pfm files in LAB color space.

* **for Sony:** Various styles for processing RAW files of Sony cameras.
