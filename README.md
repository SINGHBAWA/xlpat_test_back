**Guide to run the code**

* Install all dependencies by running command:
```
pip install -r reuirements.txt
```

* Run command to parse data from url
```
pyhon manage.py parse_patents
```
--publication_number <publication_number> (optional parameter to specify the patent page to parse)
```
pyhon manage.py parse_patents --publication_number <publication_number>
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
