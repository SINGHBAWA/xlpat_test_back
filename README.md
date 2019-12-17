**Guide to run the code**

* Install all dependencies by running command:
```
pip install -r reuirement.txt
```
* Run command to parse data from url
```
pyhon manage.py parse_patents
```

* Run server for APIs
```
python manage.py runserver
```


**For developers**

In the file below, change the patent publication_number to parse the patents data from another page:
```
patent > management > commnands > parse_patents.py
```
