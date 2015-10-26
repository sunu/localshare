# `localshare`

Share files over the local network between computers from the commandline.

## How to use

To share a file, cd into the folder and run
    
    $ localshare share myfile.txt

On the receiver end
    
    $ localshare download myfile.txt

To see a list of all available files

    $ localshare download

Then you can choose a file to download or press `ctrl + c` to quit.

By default the sharing server will close after any peer downloads your file. To
keep it running indefinitely

    $ localshare share myfile.txt --forever

Again, `ctrl + c` to close the server.

## License

This project is licensed under the MIT license.