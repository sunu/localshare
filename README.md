# `localshare`

Share files over the local network between computers from the commandline.

## How to install

Easiest way to install is to use pip. This project requires Python 3 for now.

    $ pip install localshare

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

## Development

Create a virtualenv, make sure you're using Python 3. For example on my machine I do
    
    $ virtualenv -p python3.4 env
    $ . env/bin/activate

Then install the dependencies

    $ pip install -r requirements.txt

Run the tests using pytest, add more if you want.

    $ py.test

Setup the app for tinkering

    $ pip install --editable .

Now try out the commands, add new features and enjoy.

Pull requests and bug reports are most welcome!

## License

This project is licensed under the MIT license.