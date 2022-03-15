This is written pretty cheaply. The base idea is simple. We use numbers 0-{SQLITE MAX/user added limit}.
We can split this service out at several levels, but as of right now it will simply run till it hits max.
There is a verbosity switch that you can invoke so that you get full output. Otherwise the output of the program
will either be the id that is to be used in the new shortened URL (host service should provide it's own domain)
or it will provide the fully qualified URL given the id. Since this app makes use of SQLITE it is extremely
lightweight and should be able to handle a decent amount of reads and writes

Usage:
python main.py -url [url]
    In this case it will return a number from 0 - {Max}
python main.py -id [id]
    In this case it will return a url